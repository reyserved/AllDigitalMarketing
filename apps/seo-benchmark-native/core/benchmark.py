from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd

from .classify import classify_urls, parse_custom_rules
from .io import ensure_output_dir, load_input_frames, normalize_columns, read_csv_strict, write_csv
from .prompt_template import build_prompt_template
from .recommend import build_action_plan, build_why_recommendation, compute_tags
from .reporting import analysis_dataframe, build_blank_bucket_row, build_qa_summary, qa_dataframe
from .schemas import (
    DEFAULT_BUCKETS,
    FILE_KEY_TO_BUCKET,
    L3M_METRIC_MAP,
    MOM_METRIC_MAP,
    OUTPUT_COLUMNS,
    QA_COLUMNS,
    WINDOW_TO_FILE_KEYS,
    YOY_METRIC_MAP,
    RunConfig,
    RunResult,
)
from .validate import (
    has_blocking_issues,
    make_issue,
    validate_duplicate_urls,
    validate_metadata_union,
    validate_required_columns,
    validate_url_parity,
    validation_message,
)


def _to_num(value: object) -> Optional[float]:
    if value is None:
        return None
    txt = str(value).strip()
    if not txt or txt.upper() in {"N/A", "#N/A", "NAN"}:
        return None
    txt = txt.replace(",", "").replace("%", "")
    try:
        return float(txt)
    except ValueError:
        return None


def _sum_col(df: pd.DataFrame, col: str) -> Optional[float]:
    if col not in df.columns:
        return None
    vals = [_to_num(v) for v in df[col].tolist()]
    nums = [v for v in vals if v is not None]
    if not nums:
        return None
    return float(sum(nums))


def _count_non_null(df: pd.DataFrame, col: str) -> int:
    if col not in df.columns:
        return 0
    return sum(1 for v in df[col].tolist() if _to_num(v) is not None)


def _pct(cur: Optional[float], prev: Optional[float]) -> Optional[float]:
    if cur is None or prev is None or prev == 0:
        return None
    return (cur - prev) / prev * 100


def _ctr(clicks: Optional[float], impr: Optional[float]) -> Optional[float]:
    if clicks is None or impr is None or impr == 0:
        return None
    return clicks / impr * 100


def _fmt_num(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}"


def _fmt_pct(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def _fmt_pp(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f} pp"


def _url_path(url: str) -> str:
    return str(url).replace("https://", "").replace("http://", "").split("/", 1)[-1].rstrip("/")


def _rollup(df: pd.DataFrame, metric_map: Dict[str, str]) -> Dict[str, Optional[float]]:
    out: Dict[str, Optional[float]] = {}
    for key, col in metric_map.items():
        out[key] = _sum_col(df, col)

    out["click_delta_pct"] = _pct(out["cur_clicks"], out["prev_clicks"])
    out["impr_delta_pct"] = _pct(out["cur_impr"], out["prev_impr"])
    out["users_delta_pct"] = _pct(out["cur_users"], out["prev_users"])
    out["events_delta_pct"] = _pct(out["cur_events"], out["prev_events"])
    out["cur_ctr"] = _ctr(out["cur_clicks"], out["cur_impr"])
    out["prev_ctr"] = _ctr(out["prev_clicks"], out["prev_impr"])
    out["ctr_pp"] = (
        out["cur_ctr"] - out["prev_ctr"]
        if out["cur_ctr"] is not None and out["prev_ctr"] is not None
        else None
    )
    return out


def _breadth(df: pd.DataFrame, cur_col: str, prev_col: str) -> Dict[str, int]:
    out = {"up": 0, "down": 0, "flat": 0, "na": 0}
    if cur_col not in df.columns or prev_col not in df.columns:
        out["na"] = int(df.shape[0])
        return out

    for _, row in df.iterrows():
        cur = _to_num(row[cur_col])
        prev = _to_num(row[prev_col])
        if cur is None or prev is None:
            out["na"] += 1
        elif cur > prev:
            out["up"] += 1
        elif cur < prev:
            out["down"] += 1
        else:
            out["flat"] += 1
    return out


def _coverage_counts(df: pd.DataFrame, metric_map: Dict[str, str]) -> Dict[str, int]:
    return {
        "users_cur": _count_non_null(df, metric_map["cur_users"]),
        "events_cur": _count_non_null(df, metric_map["cur_events"]),
    }


def _combine_window(
    window: str,
    performance_frames: Dict[str, pd.DataFrame],
    qa_rows: List[Dict[str, str]],
) -> pd.DataFrame:
    parts: List[pd.DataFrame] = []
    for key in WINDOW_TO_FILE_KEYS[window]:
        df = performance_frames[key].copy()
        df["__source_file"] = key
        df["__source_bucket"] = FILE_KEY_TO_BUCKET[key]
        parts.append(df)

    combined = pd.concat(parts, axis=0, ignore_index=True)

    if "URL" not in combined.columns:
        return combined

    combined["URL"] = combined["URL"].astype(str).str.strip()
    combined = combined[combined["URL"] != ""].copy()

    dupes = combined[combined["URL"].duplicated(keep=False)]
    if not dupes.empty:
        for url in dupes["URL"].unique().tolist()[:100]:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="cross_bucket_duplicate_url",
                    bucket="",
                    url=url,
                    source_file=f"{window}_all",
                    field="URL",
                    detected_value="duplicate across source files",
                    expected_rule="Each URL should map to one source file per window",
                    message="URL appears multiple times in the same window across source files.",
                    suggested_fix="Remove duplicate URL rows or reconcile source bucket assignments.",
                )
            )

    deduped = combined.drop_duplicates(subset=["URL"], keep="first").reset_index(drop=True)
    return deduped


def _build_movements(df: pd.DataFrame, metric_map: Dict[str, str]) -> List[Dict[str, float]]:
    if df.empty:
        return []

    out: List[Dict[str, float]] = []
    for _, row in df.iterrows():
        url = str(row.get("URL", "")).strip()
        if not url:
            continue

        cur_click = _to_num(row.get(metric_map["cur_clicks"]))
        prev_click = _to_num(row.get(metric_map["prev_clicks"]))
        cur_impr = _to_num(row.get(metric_map["cur_impr"]))
        prev_impr = _to_num(row.get(metric_map["prev_impr"]))

        c1 = cur_click if cur_click is not None else 0.0
        c0 = prev_click if prev_click is not None else 0.0
        i1 = cur_impr if cur_impr is not None else 0.0
        i0 = prev_impr if prev_impr is not None else 0.0

        if max(c1, c0) < 3 and max(i1, i0) < 20:
            continue

        out.append(
            {
                "url": url,
                "click_change": c1 - c0,
                "impr_change": i1 - i0,
            }
        )
    return out


def _select_driver_urls(
    movement_by_window: Dict[str, List[Dict[str, float]]],
) -> Tuple[List[str], List[str]]:
    window_order = ["l3m", "mom", "yoy"]

    def pick(direction: str) -> List[str]:
        selected: List[str] = []
        seen = set()
        for window in window_order:
            moves = movement_by_window.get(window, [])
            candidates = []
            for move in moves:
                change = move["click_change"]
                if direction == "positive" and change > 0:
                    candidates.append(move)
                if direction == "negative" and change < 0:
                    candidates.append(move)

            candidates.sort(
                key=lambda x: (abs(x["click_change"]), abs(x["impr_change"])),
                reverse=True,
            )

            for move in candidates:
                url = move["url"]
                if url in seen:
                    continue
                selected.append(url)
                seen.add(url)
                if len(selected) == 3:
                    return selected
        return selected

    return pick("positive"), pick("negative")


def _format_driver_text(
    urls: Sequence[str],
    movement_by_window: Dict[str, List[Dict[str, float]]],
) -> str:
    lookup = defaultdict(dict)
    for window, rows in movement_by_window.items():
        for item in rows:
            lookup[item["url"]][window] = item

    labels = {"l3m": "L3M", "mom": "MoM", "yoy": "YoY"}
    chunks: List[str] = []

    for url in urls:
        parts = [f"/{_url_path(url)}"]
        for window in ["l3m", "mom", "yoy"]:
            item = lookup.get(url, {}).get(window)
            if item is None:
                continue
            c = int(round(item["click_change"]))
            i = int(round(item["impr_change"]))
            c_sign = "+" if c > 0 else ""
            i_sign = "+" if i > 0 else ""
            parts.append(f"{labels[window]}: {c_sign}{c} clicks, {i_sign}{i} impr")
        chunks.append(" | ".join(parts))

    return "; ".join(chunks) if chunks else "N/A"


def _title_h1_mismatch(title: str, h1: str) -> bool:
    title_core = str(title).split("|", 1)[0].strip().lower()
    h1_text = str(h1).strip().lower()
    if not title_core or not h1_text:
        return False

    tokens = [tok for tok in title_core.replace("/", " ").replace("-", " ").split() if len(tok) > 2]
    if not tokens:
        return False

    probe = tokens[:2]
    return all(tok not in h1_text for tok in probe)


def _metadata_opportunities(
    bucket_urls: Sequence[str],
    metadata_df: pd.DataFrame,
    negative_driver_urls: Sequence[str],
) -> str:
    meta_lookup = {}
    if "URL" in metadata_df.columns:
        for _, row in metadata_df.iterrows():
            url = str(row.get("URL", "")).strip()
            if url and url not in meta_lookup:
                meta_lookup[url] = row

    titles_over = []
    metas_over = []
    mismatches = []

    for url in bucket_urls:
        row = meta_lookup.get(url)
        if row is None:
            continue
        title = str(row.get("Title 1", "")).strip()
        meta = str(row.get("Meta Description 1", "")).strip()
        if len(title) > 60:
            titles_over.append(url)
        if len(meta) > 160:
            metas_over.append(url)

    for url in negative_driver_urls:
        row = meta_lookup.get(url)
        if row is None:
            continue
        if _title_h1_mismatch(str(row.get("Title 1", "")), str(row.get("H1-1", ""))):
            mismatches.append(url)

    text = (
        f"Title >60 chars: {len(titles_over)} pages; "
        f"Meta >160 chars: {len(metas_over)} pages; "
        f"Title/H1 mismatch among top decliners: {len(mismatches)} pages"
    )

    if titles_over:
        text += "; Sample title length issues: " + ", ".join(f"/{_url_path(u)}" for u in titles_over[:2])
    if metas_over:
        text += "; Sample meta length issues: " + ", ".join(f"/{_url_path(u)}" for u in metas_over[:2])
    if mismatches:
        text += "; Priority mismatch pages: " + ", ".join(f"/{_url_path(u)}" for u in mismatches[:2])

    return text


def _weak_high_impr_pages(l3m_df: pd.DataFrame, l3m_rollup: Dict[str, Optional[float]]) -> int:
    bucket_ctr = l3m_rollup.get("cur_ctr")
    if bucket_ctr is None or bucket_ctr <= 0:
        return 0

    weak_threshold = bucket_ctr * 0.8
    weak = 0
    for _, row in l3m_df.iterrows():
        clicks = _to_num(row.get(L3M_METRIC_MAP["cur_clicks"]))
        impr = _to_num(row.get(L3M_METRIC_MAP["cur_impr"]))
        if clicks is None or impr is None or impr < 1000 or impr == 0:
            continue
        page_ctr = clicks / impr * 100
        if page_ctr < weak_threshold:
            weak += 1
    return weak


def _coverage_note(
    bucket_size: int,
    l3m_cov: Dict[str, int],
    mom_cov: Dict[str, int],
    yoy_cov: Dict[str, int],
    custom_bucket_with_no_urls: bool,
    validation_note: Optional[str] = None,
) -> str:
    base = (
        f"Data coverage (rows={bucket_size}): "
        f"L3M users {l3m_cov['users_cur']}/{bucket_size}, events {l3m_cov['events_cur']}/{bucket_size}; "
        f"MoM users {mom_cov['users_cur']}/{bucket_size}, events {mom_cov['events_cur']}/{bucket_size}; "
        f"YoY users {yoy_cov['users_cur']}/{bucket_size}, events {yoy_cov['events_cur']}/{bucket_size}."
    )
    if custom_bucket_with_no_urls:
        base += " Requested custom bucket has zero matched URLs for this run."
    if validation_note:
        base += f" {validation_note}"
    return base


def _build_benchmark_text(
    label: str,
    rollup: Dict[str, Optional[float]],
    breadth_click: Dict[str, int],
    breadth_impr: Dict[str, int],
) -> str:
    return (
        f"{label}: clicks {_fmt_num(rollup['cur_clicks'])} vs {_fmt_num(rollup['prev_clicks'])} "
        f"({_fmt_pct(rollup['click_delta_pct'])}), impressions {_fmt_num(rollup['cur_impr'])} vs {_fmt_num(rollup['prev_impr'])} "
        f"({_fmt_pct(rollup['impr_delta_pct'])}), CTR {_fmt_pct(rollup['cur_ctr'])} vs {_fmt_pct(rollup['prev_ctr'])} "
        f"({_fmt_pp(rollup['ctr_pp'])}). Users {_fmt_num(rollup['cur_users'])} vs {_fmt_num(rollup['prev_users'])} "
        f"({_fmt_pct(rollup['users_delta_pct'])}); key events {_fmt_num(rollup['cur_events'])} vs {_fmt_num(rollup['prev_events'])} "
        f"({_fmt_pct(rollup['events_delta_pct'])}). Breadth: click winners/decliners {breadth_click['up']}/{breadth_click['down']}, "
        f"impression winners/decliners {breadth_impr['up']}/{breadth_impr['down']}."
    )


def _empty_metrics_row(bucket: str, url_count: int, note: str) -> Dict[str, str]:
    return build_blank_bucket_row(bucket=bucket, url_count=url_count, note=note)


def _bucket_row(
    bucket: str,
    urls: Sequence[str],
    l3m_df: pd.DataFrame,
    mom_df: pd.DataFrame,
    yoy_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
    custom_bucket_requested: bool,
) -> Dict[str, str]:
    l3m_rollup = _rollup(l3m_df, L3M_METRIC_MAP)
    mom_rollup = _rollup(mom_df, MOM_METRIC_MAP)
    yoy_rollup = _rollup(yoy_df, YOY_METRIC_MAP)

    l3m_breadth_click = _breadth(l3m_df, L3M_METRIC_MAP["cur_clicks"], L3M_METRIC_MAP["prev_clicks"])
    l3m_breadth_impr = _breadth(l3m_df, L3M_METRIC_MAP["cur_impr"], L3M_METRIC_MAP["prev_impr"])
    mom_breadth_click = _breadth(mom_df, MOM_METRIC_MAP["cur_clicks"], MOM_METRIC_MAP["prev_clicks"])
    mom_breadth_impr = _breadth(mom_df, MOM_METRIC_MAP["cur_impr"], MOM_METRIC_MAP["prev_impr"])
    yoy_breadth_click = _breadth(yoy_df, YOY_METRIC_MAP["cur_clicks"], YOY_METRIC_MAP["prev_clicks"])
    yoy_breadth_impr = _breadth(yoy_df, YOY_METRIC_MAP["cur_impr"], YOY_METRIC_MAP["prev_impr"])

    l3m_cov = _coverage_counts(l3m_df, L3M_METRIC_MAP)
    mom_cov = _coverage_counts(mom_df, MOM_METRIC_MAP)
    yoy_cov = _coverage_counts(yoy_df, YOY_METRIC_MAP)

    movement_by_window = {
        "l3m": _build_movements(l3m_df, L3M_METRIC_MAP),
        "mom": _build_movements(mom_df, MOM_METRIC_MAP),
        "yoy": _build_movements(yoy_df, YOY_METRIC_MAP),
    }

    pos_urls, neg_urls = _select_driver_urls(movement_by_window)
    top_positive = _format_driver_text(pos_urls, movement_by_window)
    top_negative = _format_driver_text(neg_urls, movement_by_window)

    metadata_ops = _metadata_opportunities(urls, metadata_df, neg_urls)

    weak_pages = _weak_high_impr_pages(l3m_df, l3m_rollup)
    n = max(1, len(urls))
    users_ratio = min(l3m_cov["users_cur"], mom_cov["users_cur"], yoy_cov["users_cur"]) / n
    events_ratio = min(l3m_cov["events_cur"], mom_cov["events_cur"], yoy_cov["events_cur"]) / n
    tags = compute_tags(
        l3m=l3m_rollup,
        mom=mom_rollup,
        yoy=yoy_rollup,
        weak_high_impr_pages=weak_pages,
        coverage_ratio_users=users_ratio,
        coverage_ratio_events=events_ratio,
    )

    row = {
        "Bucket": bucket,
        "URLs In Bucket": str(len(urls)),
        "Data Coverage Notes": _coverage_note(
            bucket_size=len(urls),
            l3m_cov=l3m_cov,
            mom_cov=mom_cov,
            yoy_cov=yoy_cov,
            custom_bucket_with_no_urls=custom_bucket_requested and len(urls) == 0,
        ),
        "L3M Benchmark": _build_benchmark_text(
            "L3M vs Prev 3M",
            l3m_rollup,
            l3m_breadth_click,
            l3m_breadth_impr,
        ),
        "MoM Benchmark": _build_benchmark_text(
            "MoM (last month vs prior month)",
            mom_rollup,
            mom_breadth_click,
            mom_breadth_impr,
        ),
        "YoY Benchmark": _build_benchmark_text(
            "YoY (L3M vs L3M LY)",
            yoy_rollup,
            yoy_breadth_click,
            yoy_breadth_impr,
        ),
        "Top Positive Drivers": top_positive,
        "Top Negative Drivers": top_negative,
        "Metadata/H1 Opportunities": metadata_ops,
        "Why_Recommendation": build_why_recommendation(
            l3m=l3m_rollup,
            mom=mom_rollup,
            yoy=yoy_rollup,
            weak_high_impr_pages=weak_pages,
        ),
        "Next Steps Tags": ", ".join(tags),
        "Action Plan": build_action_plan(bucket),
    }
    return row


def run_benchmark(config: RunConfig) -> RunResult:
    qa_rows: List[Dict[str, str]] = []

    performance_frames = load_input_frames(config.input_paths)
    metadata_df = normalize_columns(read_csv_strict(config.metadata_path))

    validate_required_columns(performance_frames, metadata_df, qa_rows)
    validate_duplicate_urls(performance_frames, metadata_df, qa_rows)
    l3m_union, mom_union, yoy_union = validate_url_parity(performance_frames, qa_rows)

    window_union = l3m_union | mom_union | yoy_union
    validate_metadata_union(window_union, metadata_df, qa_rows)

    custom_rules = parse_custom_rules(config.custom_rules_text, qa_rows=qa_rows)
    custom_names = [rule.name for rule in custom_rules]

    final_type_by_url, inferred_by_url, dynamic_types = classify_urls(
        all_urls=sorted(window_union),
        metadata_df=metadata_df,
        custom_rules=custom_rules,
        qa_rows=qa_rows,
    )

    # Prepare combined window frames for bucket reaggregation.
    l3m_all = _combine_window("l3m", performance_frames, qa_rows)
    mom_all = _combine_window("mom", performance_frames, qa_rows)
    yoy_all = _combine_window("yoy", performance_frames, qa_rows)

    bucket_order: List[str] = []
    for bucket in custom_names + DEFAULT_BUCKETS + dynamic_types:
        if bucket not in bucket_order and bucket != "Unclassified":
            bucket_order.append(bucket)

    if any(v == "Unclassified" for v in final_type_by_url.values()):
        bucket_order.append("Unclassified")

    blocked = has_blocking_issues(qa_rows)
    blocked_note = validation_message(qa_rows) if blocked else None

    rows: List[Dict[str, str]] = []

    for bucket in bucket_order:
        bucket_urls = [url for url, b in final_type_by_url.items() if b == bucket]

        if bucket in custom_names and not bucket_urls:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="custom_bucket_no_match",
                    bucket=bucket,
                    url="",
                    source_file="custom_rules",
                    field="bucket",
                    detected_value="0 matched URLs",
                    expected_rule="At least one URL match",
                    message="Custom bucket has zero matched URLs for this run.",
                    suggested_fix="Adjust custom rule terms or verify URL/title/meta/H1 inputs.",
                )
            )

        if blocked:
            rows.append(
                _empty_metrics_row(
                    bucket=bucket,
                    url_count=len(bucket_urls),
                    note=(
                        f"{blocked_note}"
                        + (
                            " Requested custom bucket has zero matched URLs for this run."
                            if (bucket in custom_names and not bucket_urls)
                            else ""
                        )
                    ),
                )
            )
            continue

        l3m_bucket = l3m_all[l3m_all["URL"].isin(bucket_urls)].copy()
        mom_bucket = mom_all[mom_all["URL"].isin(bucket_urls)].copy()
        yoy_bucket = yoy_all[yoy_all["URL"].isin(bucket_urls)].copy()

        if not bucket_urls:
            rows.append(
                _empty_metrics_row(
                    bucket=bucket,
                    url_count=0,
                    note="No URLs assigned to this bucket for this run.",
                )
            )
            continue

        rows.append(
            _bucket_row(
                bucket=bucket,
                urls=bucket_urls,
                l3m_df=l3m_bucket,
                mom_df=mom_bucket,
                yoy_df=yoy_bucket,
                metadata_df=metadata_df,
                custom_bucket_requested=bucket in custom_names,
            )
        )

    analysis_df = analysis_dataframe(rows)
    qa_df = qa_dataframe(qa_rows)

    output_dir = ensure_output_dir(config.output_root)
    analysis_csv = output_dir / "benchmark-analysis.csv"
    qa_csv = output_dir / "benchmark-qa.csv"
    qa_summary_txt = output_dir / "benchmark-qa-summary.txt"

    write_csv(analysis_df, analysis_csv)
    write_csv(qa_df, qa_csv)

    qa_summary_txt.write_text(
        build_qa_summary(qa_df=qa_df, validation_blocked=blocked, output_dir=output_dir),
        encoding="utf-8",
    )

    prompt_text = build_prompt_template(
        l3m_files=[config.input_paths[k] for k in WINDOW_TO_FILE_KEYS["l3m"]],
        mom_files=[config.input_paths[k] for k in WINDOW_TO_FILE_KEYS["mom"]],
        yoy_files=[config.input_paths[k] for k in WINDOW_TO_FILE_KEYS["yoy"]],
        metadata_file=config.metadata_path,
        custom_bucket_names=custom_names,
        output_dir=output_dir,
    )

    return RunResult(
        success=True,
        output_dir=output_dir,
        analysis_csv=analysis_csv,
        qa_csv=qa_csv,
        qa_summary_txt=qa_summary_txt,
        prompt_text=prompt_text,
        qa_issue_count=int(qa_df.shape[0]),
        qa_error_count=int((qa_df["severity"] == "error").sum()) if not qa_df.empty else 0,
        validation_blocked=blocked,
        bucket_order=bucket_order,
    )
