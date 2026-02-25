#!/usr/bin/env python3
"""Generate Omnipress page-level on-page opportunities (weighted + rule-based + QA trace)."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


BASE_DIR = Path(__file__).resolve().parent

MAPPING_PATH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Keyword Mapping - pages.csv"
METADATA_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - core-pages-metadata.csv"
L3M_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - Core Pages - L3M.csv"
YOY_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - core-pages-YoY.csv"

OUT_WEIGHTED = BASE_DIR / "Omnipress_OnPage_Opportunities_Pages_Weighted.csv"
OUT_RULE = BASE_DIR / "Omnipress_OnPage_Opportunities_Pages_RuleBased.csv"
OUT_QA = BASE_DIR / "Omnipress_OnPage_Opportunities_Pages_QA_Trace.csv"

# Performance-heavy weights, summing to 1.00.
PERF_WEIGHTS = {
    "l3m_clicks_pct": 0.14,
    "l3m_impr_pct": 0.10,
    "l3m_engaged_pct": 0.08,
    "l3m_users_pct": 0.08,
    "l3m_conv_pct": 0.10,
    "yoy_clicks_pct": 0.14,
    "yoy_impr_pct": 0.10,
    "yoy_engaged_pct": 0.08,
    "yoy_users_pct": 0.08,
    "yoy_conv_pct": 0.10,
}

METRIC_ORDER = [
    "l3m_clicks_pct",
    "l3m_impr_pct",
    "l3m_engaged_pct",
    "l3m_users_pct",
    "l3m_conv_pct",
    "yoy_clicks_pct",
    "yoy_impr_pct",
    "yoy_engaged_pct",
    "yoy_users_pct",
    "yoy_conv_pct",
]

METRIC_LABELS = {
    "l3m_clicks_pct": "L3M Clicks",
    "l3m_impr_pct": "L3M Impr",
    "l3m_engaged_pct": "L3M Engaged",
    "l3m_users_pct": "L3M Users",
    "l3m_conv_pct": "L3M Conv",
    "yoy_clicks_pct": "YoY Clicks",
    "yoy_impr_pct": "YoY Impr",
    "yoy_engaged_pct": "YoY Engaged",
    "yoy_users_pct": "YoY Users",
    "yoy_conv_pct": "YoY Conv",
}


def normalize_url(raw_url: str) -> str:
    raw = (raw_url or "").strip()
    if not raw:
        return ""
    raw = raw.replace("http://", "https://")
    if raw.startswith("//"):
        raw = f"https:{raw}"
    if "://" not in raw:
        raw = f"https://{raw.lstrip('/')}"
    parsed = urlsplit(raw)
    if not parsed.netloc:
        return ""
    host = parsed.netloc.lower().strip()
    path = re.sub(r"/+", "/", parsed.path or "/")
    if not path.startswith("/"):
        path = f"/{path}"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"https://{host}{path}"


def display_url(normalized_url: str) -> str:
    norm = normalize_url(normalized_url)
    if not norm:
        return ""
    parsed = urlsplit(norm)
    path = parsed.path
    if path != "/" and not path.endswith("/"):
        path = f"{path}/"
    return f"https://{parsed.netloc}{path}"


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_keyword(text: str) -> str:
    return normalize_space((text or "").lower())


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", (text or "").lower())
    return normalize_space(cleaned)


def safe_float(raw: str) -> float:
    value = (raw or "").strip().replace(",", "")
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def parse_percent(raw: str) -> float | None:
    text = (raw or "").strip()
    if not text or text in {"#N/A", "N/A", "-"}:
        return None
    text = text.replace(",", "")
    if text.endswith("%"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        return None


def format_decimal(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def format_ratio(value: float) -> str:
    return f"{value:.4f}"


def format_score(value: float) -> str:
    return f"{value:.2f}"


def severity_from_delta(delta_pct: float | None) -> float | None:
    if delta_pct is None:
        return None
    return max(0.0, min(1.0, (-delta_pct) / 40.0))


def category_rank(match_type: str, suggested_action: str) -> int:
    mt = (match_type or "").strip()
    sa = (suggested_action or "").strip()
    if mt == "Partial" and sa == "Optimize":
        return 0
    if mt == "Exact" and sa == "Optimize":
        return 1
    if mt == "Exact" and sa == "None":
        return 2
    return 3


def confidence_label(metrics_available: int) -> str:
    if metrics_available >= 8:
        return "High"
    if metrics_available >= 5:
        return "Medium"
    return "Low"


def weighted_tier(score: float) -> str:
    if score >= 75:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def build_other_keywords_summary(other_keywords: list[str]) -> str:
    if not other_keywords:
        return "0 remaining"
    unique = []
    seen = set()
    for keyword in other_keywords:
        nk = normalize_keyword(keyword)
        if nk in seen:
            continue
        seen.add(nk)
        unique.append(keyword)
    shown = unique[:8]
    remainder = len(unique) - len(shown)
    base = f"{len(unique)} remaining: " + " | ".join(shown)
    if remainder > 0:
        base += f" ...(+{remainder} more)"
    return base


def metric_out(raw_value: str, parsed_value: float | None) -> str:
    # Keep raw benchmark text in outputs for strict source parity (e.g., N/A, #N/A, -).
    if parsed_value is None:
        return (raw_value or "").strip()
    return (raw_value or "").strip()


def choose_topic_cluster(rows: list[dict[str, Any]]) -> str:
    counts = Counter((row.get("Topic Cluster", "") or "").strip() for row in rows if (row.get("Topic Cluster", "") or "").strip())
    if not counts:
        return "Unclustered"
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def build_themes(
    *,
    title_h1_issue: bool,
    content_issue: bool,
    ctr_issue: bool,
    demand_issue: bool,
    conversion_issue: bool,
) -> tuple[str, str]:
    candidates = []
    if conversion_issue:
        candidates.append((5, "Conversion Path Optimization"))
    if demand_issue:
        candidates.append((4, "Demand Recovery"))
    if ctr_issue:
        candidates.append((3, "Snippet/CTR Refinement"))
    if content_issue:
        candidates.append((2, "Content Depth & Intent Coverage"))
    if title_h1_issue:
        candidates.append((1, "Title/H1 Keyword Alignment"))

    if not candidates:
        return "No Critical On-Page Gap", ""
    candidates.sort(key=lambda item: (-item[0], item[1]))
    primary = candidates[0][1]
    secondary = candidates[1][1] if len(candidates) > 1 else ""
    return primary, secondary


def build_action(
    *,
    primary_keyword: str,
    title_h1_issue: bool,
    content_issue: bool,
    ctr_issue: bool,
    demand_issue: bool,
    conversion_issue: bool,
) -> str:
    steps: list[str] = []

    if primary_keyword:
        if title_h1_issue:
            steps.append(f"Add '{primary_keyword}' to title and H1.")
        else:
            steps.append(f"Reinforce '{primary_keyword}' prominence in title/H1.")

    if content_issue:
        steps.append("Expand sections to satisfy partial-intent keyword coverage.")
    if ctr_issue:
        steps.append("Test CTR-focused title/meta variants aligned to intent.")
    if demand_issue:
        steps.append("Refresh topical depth and internal links to recover demand.")
    if conversion_issue:
        steps.append("Strengthen CTA messaging and conversion path copy.")

    if not steps:
        return "Maintain current on-page targeting; monitor performance."

    # Keep concise but actionable.
    return " ".join(steps[:4])


def build_notes(
    *,
    partial_count: int,
    exact_count: int,
    optimize_count: int,
    metric_raw: dict[str, str],
    metric_parsed: dict[str, float | None],
    primary_theme: str,
) -> str:
    evidence = f"Mapping mix: partial={partial_count}, exact={exact_count}, optimize={optimize_count}."

    negatives = [
        (name, metric_parsed[name], metric_raw[name])
        for name in METRIC_ORDER
        if metric_parsed[name] is not None and metric_parsed[name] < 0
    ]
    negatives.sort(key=lambda item: item[1])  # most negative first
    snippets: list[str] = []
    for name, _parsed, raw in negatives[:3]:
        snippets.append(f"{METRIC_LABELS[name]} {raw.strip()}")

    if not snippets:
        positives = [
            (name, metric_parsed[name], metric_raw[name])
            for name in METRIC_ORDER
            if metric_parsed[name] is not None and metric_parsed[name] >= 0
        ]
        positives.sort(key=lambda item: item[1], reverse=True)
        for name, _parsed, raw in positives[:2]:
            snippets.append(f"{METRIC_LABELS[name]} {raw.strip()}")

    perf = "Performance signals: " + "; ".join(snippets) + "." if snippets else "Performance signals: limited benchmark data."
    return f"{evidence} {perf} Focus: {primary_theme}."


def parse_l3m(path: Path) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)  # header
        for row_idx, row in enumerate(reader, start=2):
            if len(row) < 17:
                continue
            norm_url = normalize_url(row[0])
            if not norm_url:
                continue
            data[norm_url] = {
                "row_index": row_idx,
                "raw_url": row[0],
                "raw_clicks": row[4],
                "raw_impr": row[7],
                "raw_engaged": row[10],
                "raw_users": row[13],
                "raw_conv": row[16],
                "l3m_clicks_pct": parse_percent(row[4]),
                "l3m_impr_pct": parse_percent(row[7]),
                "l3m_engaged_pct": parse_percent(row[10]),
                "l3m_users_pct": parse_percent(row[13]),
                "l3m_conv_pct": parse_percent(row[16]),
            }
    return data


def parse_yoy(path: Path) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)  # header
        for row_idx, row in enumerate(reader, start=2):
            if len(row) < 17:
                continue
            norm_url = normalize_url(row[0])
            if not norm_url:
                continue
            data[norm_url] = {
                "row_index": row_idx,
                "raw_url": row[0],
                "raw_clicks": row[4],
                "raw_impr": row[7],
                "raw_engaged": row[10],
                "raw_users": row[13],
                "raw_conv": row[16],
                "yoy_clicks_pct": parse_percent(row[4]),
                "yoy_impr_pct": parse_percent(row[7]),
                "yoy_engaged_pct": parse_percent(row[10]),
                "yoy_users_pct": parse_percent(row[13]),
                "yoy_conv_pct": parse_percent(row[16]),
            }
    return data


def parse_metadata(path: Path) -> dict[str, dict[str, Any]]:
    by_url: dict[str, dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row_idx, row in enumerate(reader, start=2):
            norm_url = normalize_url(row.get("Address", ""))
            if not norm_url:
                continue
            by_url[norm_url] = {
                "row_index": row_idx,
                "raw_url": row.get("Address", "") or "",
                "title": normalize_space(row.get("Title 1", "")),
                "meta_desc": normalize_space(row.get("Meta Description 1", "")),
                "h1": normalize_space(row.get("H1-1", "")),
            }
    return by_url


def parse_mapping(path: Path) -> dict[str, list[dict[str, Any]]]:
    by_url: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row_idx, row in enumerate(reader, start=2):
            norm_url = normalize_url(row.get("Current URL", ""))
            if not norm_url:
                continue
            by_url[norm_url].append(
                {
                    "row_index": row_idx,
                    "raw_url": row.get("Current URL", "") or "",
                    "Keyword": normalize_space(row.get("Keyword", "")),
                    "Search Volume": row.get("Search Volume", "") or "",
                    "Search Intent": normalize_space(row.get("Search Intent", "")),
                    "Topic Cluster": normalize_space(row.get("Topic Cluster", "")),
                    "Match Type": normalize_space(row.get("Match Type", "")),
                    "Suggested Action": normalize_space(row.get("Suggested Action", "")),
                    "Notes": normalize_space(row.get("Notes", "")),
                }
            )
    return by_url


def dedupe_mapping_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dedup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (
            normalize_keyword(row.get("Keyword", "")),
            row.get("Match Type", ""),
            row.get("Suggested Action", ""),
        )
        if not key[0]:
            continue
        current = dedup.get(key)
        if current is None:
            dedup[key] = row
            continue
        current_sv = safe_float(current.get("Search Volume", ""))
        row_sv = safe_float(row.get("Search Volume", ""))
        if row_sv > current_sv:
            dedup[key] = row
        elif row_sv == current_sv and int(row["row_index"]) < int(current["row_index"]):
            dedup[key] = row
    return list(dedup.values())


def build_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    mapping_by_url = parse_mapping(MAPPING_PATH)
    metadata_by_url = parse_metadata(METADATA_PATH)
    l3m_by_url = parse_l3m(L3M_PATH)
    yoy_by_url = parse_yoy(YOY_PATH)

    weighted_rows: list[dict[str, str]] = []
    rule_rows: list[dict[str, str]] = []
    qa_rows: list[dict[str, str]] = []

    for norm_url in sorted(mapping_by_url.keys()):
        raw_mapping_rows = mapping_by_url[norm_url]
        dedup_rows = dedupe_mapping_rows(raw_mapping_rows)
        dedup_rows.sort(
            key=lambda row: (
                category_rank(row.get("Match Type", ""), row.get("Suggested Action", "")),
                -safe_float(row.get("Search Volume", "")),
                normalize_keyword(row.get("Keyword", "")),
            )
        )

        keyword_rows_count = len(dedup_rows)
        exact_count = sum(1 for row in dedup_rows if row.get("Match Type", "") == "Exact")
        partial_count = sum(1 for row in dedup_rows if row.get("Match Type", "") == "Partial")
        optimize_count = sum(1 for row in dedup_rows if row.get("Suggested Action", "") == "Optimize")
        none_action_count = sum(1 for row in dedup_rows if row.get("Suggested Action", "") == "None")
        partial_ratio = (partial_count / keyword_rows_count) if keyword_rows_count else 0.0

        top_rows = dedup_rows[:3]
        top_keywords = [row.get("Keyword", "") for row in top_rows]
        while len(top_keywords) < 3:
            top_keywords.append("")
        other_keywords = [row.get("Keyword", "") for row in dedup_rows[3:]]
        other_summary = build_other_keywords_summary(other_keywords)

        topic_cluster = choose_topic_cluster(dedup_rows)

        primary_keyword = top_keywords[0]
        primary_keyword_norm = normalize_text(primary_keyword)

        metadata = metadata_by_url.get(norm_url, {})
        meta_title = metadata.get("title", "")
        meta_desc = metadata.get("meta_desc", "")
        h1 = metadata.get("h1", "")

        title_norm = normalize_text(meta_title)
        h1_norm = normalize_text(h1)

        missing_meta_desc = not bool(meta_desc)
        missing_h1 = not bool(h1)
        primary_absent_title = bool(primary_keyword_norm) and primary_keyword_norm not in title_norm
        primary_absent_h1 = bool(primary_keyword_norm) and primary_keyword_norm not in h1_norm

        gap_flags = []
        if missing_meta_desc:
            gap_flags.append("Missing Meta Description")
        if missing_h1:
            gap_flags.append("Missing H1")
        if primary_absent_title:
            gap_flags.append("Primary Keyword Missing in Title")
        if primary_absent_h1:
            gap_flags.append("Primary Keyword Missing in H1")
        metadata_gaps = "; ".join(gap_flags) if gap_flags else "None"

        metadata_risk_score = 100.0 * (len(gap_flags) / 4.0)

        l3 = l3m_by_url.get(norm_url, {})
        yy = yoy_by_url.get(norm_url, {})

        metric_raw = {
            "l3m_clicks_pct": l3.get("raw_clicks", ""),
            "l3m_impr_pct": l3.get("raw_impr", ""),
            "l3m_engaged_pct": l3.get("raw_engaged", ""),
            "l3m_users_pct": l3.get("raw_users", ""),
            "l3m_conv_pct": l3.get("raw_conv", ""),
            "yoy_clicks_pct": yy.get("raw_clicks", ""),
            "yoy_impr_pct": yy.get("raw_impr", ""),
            "yoy_engaged_pct": yy.get("raw_engaged", ""),
            "yoy_users_pct": yy.get("raw_users", ""),
            "yoy_conv_pct": yy.get("raw_conv", ""),
        }
        metric_parsed: dict[str, float | None] = {
            "l3m_clicks_pct": l3.get("l3m_clicks_pct", None),
            "l3m_impr_pct": l3.get("l3m_impr_pct", None),
            "l3m_engaged_pct": l3.get("l3m_engaged_pct", None),
            "l3m_users_pct": l3.get("l3m_users_pct", None),
            "l3m_conv_pct": l3.get("l3m_conv_pct", None),
            "yoy_clicks_pct": yy.get("yoy_clicks_pct", None),
            "yoy_impr_pct": yy.get("yoy_impr_pct", None),
            "yoy_engaged_pct": yy.get("yoy_engaged_pct", None),
            "yoy_users_pct": yy.get("yoy_users_pct", None),
            "yoy_conv_pct": yy.get("yoy_conv_pct", None),
        }

        metrics_available = sum(1 for key in METRIC_ORDER if metric_parsed[key] is not None)
        data_confidence = confidence_label(metrics_available)

        weighted_sum = 0.0
        available_weight = 0.0
        for key in METRIC_ORDER:
            metric_value = metric_parsed[key]
            severity = severity_from_delta(metric_value)
            if severity is None:
                continue
            weight = PERF_WEIGHTS[key]
            weighted_sum += severity * weight
            available_weight += weight
        performance_risk_score = (100.0 * weighted_sum / available_weight) if available_weight > 0 else 0.0

        exact_ratio = (exact_count / keyword_rows_count) if keyword_rows_count else 0.0
        optimize_ratio = (optimize_count / keyword_rows_count) if keyword_rows_count else 0.0
        mapping_risk_score = 100.0 * (
            0.65 * partial_ratio + 0.25 * optimize_ratio + 0.10 * (1.0 - exact_ratio)
        )

        weighted_priority_score = (
            0.70 * performance_risk_score
            + 0.20 * mapping_risk_score
            + 0.10 * metadata_risk_score
        )
        weighted_priority = weighted_tier(weighted_priority_score)

        major_decline_count = sum(
            1 for key in METRIC_ORDER if metric_parsed[key] is not None and metric_parsed[key] <= -20
        )
        moderate_decline_count = sum(
            1 for key in METRIC_ORDER if metric_parsed[key] is not None and metric_parsed[key] <= -10
        )

        mapping_friction = partial_ratio >= 0.60 or exact_count == 0
        metadata_friction = bool(gap_flags)
        conv_shock = (
            (metric_parsed["l3m_conv_pct"] is not None and metric_parsed["l3m_conv_pct"] <= -20)
            or (metric_parsed["yoy_conv_pct"] is not None and metric_parsed["yoy_conv_pct"] <= -20)
        )

        high_conditions = []
        if conv_shock and mapping_friction:
            high_conditions.append("Conv shock + mapping friction")
        if major_decline_count >= 2:
            high_conditions.append(">=2 major metric declines")
        if major_decline_count >= 1 and mapping_friction:
            high_conditions.append("Major decline + mapping friction")

        medium_conditions = []
        if moderate_decline_count >= 2:
            medium_conditions.append(">=2 moderate metric declines")
        if mapping_friction:
            medium_conditions.append("Mapping friction")
        if metadata_friction:
            medium_conditions.append("Metadata friction")

        if high_conditions:
            rule_priority = "High"
            trigger_reason = "; ".join(high_conditions)
        elif medium_conditions:
            rule_priority = "Medium"
            trigger_reason = "; ".join(medium_conditions)
        else:
            rule_priority = "Low"
            trigger_reason = "No aggressive trigger"

        title_h1_issue = primary_absent_title or primary_absent_h1
        content_issue = partial_ratio >= 0.60
        ctr_issue = (
            (metric_parsed["l3m_clicks_pct"] is not None and metric_parsed["l3m_clicks_pct"] < 0 and metric_parsed["l3m_impr_pct"] is not None and metric_parsed["l3m_impr_pct"] >= 0)
            or (metric_parsed["yoy_clicks_pct"] is not None and metric_parsed["yoy_clicks_pct"] < 0 and metric_parsed["yoy_impr_pct"] is not None and metric_parsed["yoy_impr_pct"] >= 0)
        )
        demand_issue = (
            metric_parsed["l3m_impr_pct"] is not None
            and metric_parsed["yoy_impr_pct"] is not None
            and metric_parsed["l3m_impr_pct"] < 0
            and metric_parsed["yoy_impr_pct"] < 0
        )
        conversion_issue = any(
            metric_parsed[key] is not None and metric_parsed[key] < 0
            for key in ("l3m_conv_pct", "yoy_conv_pct")
        )

        primary_theme, secondary_theme = build_themes(
            title_h1_issue=title_h1_issue,
            content_issue=content_issue,
            ctr_issue=ctr_issue,
            demand_issue=demand_issue,
            conversion_issue=conversion_issue,
        )
        suggested_action = build_action(
            primary_keyword=primary_keyword,
            title_h1_issue=title_h1_issue,
            content_issue=content_issue,
            ctr_issue=ctr_issue,
            demand_issue=demand_issue,
            conversion_issue=conversion_issue,
        )
        notes = build_notes(
            partial_count=partial_count,
            exact_count=exact_count,
            optimize_count=optimize_count,
            metric_raw=metric_raw,
            metric_parsed=metric_parsed,
            primary_theme=primary_theme,
        )

        output_url_value = display_url(norm_url)
        base_row = {
            "URL": output_url_value,
            "Topic Cluster": topic_cluster,
            "Top Keyword 1": top_keywords[0],
            "Top Keyword 2": top_keywords[1],
            "Top Keyword 3": top_keywords[2],
            "Other Keywords Summary": other_summary,
            "Keyword Rows (Count)": str(keyword_rows_count),
            "Exact Count": str(exact_count),
            "Partial Count": str(partial_count),
            "Optimize Count": str(optimize_count),
            "None Action Count": str(none_action_count),
            "Partial Ratio": format_ratio(partial_ratio),
            "Meta Title": meta_title,
            "Meta Description": meta_desc,
            "H1": h1,
            "Metadata Gaps": metadata_gaps,
            "L3M Δ Clicks %": metric_out(metric_raw["l3m_clicks_pct"], metric_parsed["l3m_clicks_pct"]),
            "L3M Δ Impr %": metric_out(metric_raw["l3m_impr_pct"], metric_parsed["l3m_impr_pct"]),
            "L3M Δ Engaged Sessions %": metric_out(metric_raw["l3m_engaged_pct"], metric_parsed["l3m_engaged_pct"]),
            "L3M Δ Users %": metric_out(metric_raw["l3m_users_pct"], metric_parsed["l3m_users_pct"]),
            "L3M Δ Conv %": metric_out(metric_raw["l3m_conv_pct"], metric_parsed["l3m_conv_pct"]),
            "YoY Δ Clicks %": metric_out(metric_raw["yoy_clicks_pct"], metric_parsed["yoy_clicks_pct"]),
            "YoY Δ Impr %": metric_out(metric_raw["yoy_impr_pct"], metric_parsed["yoy_impr_pct"]),
            "YoY Δ Engaged Sessions %": metric_out(metric_raw["yoy_engaged_pct"], metric_parsed["yoy_engaged_pct"]),
            "YoY Δ Users %": metric_out(metric_raw["yoy_users_pct"], metric_parsed["yoy_users_pct"]),
            "YoY Δ Conv %": metric_out(metric_raw["yoy_conv_pct"], metric_parsed["yoy_conv_pct"]),
            "Metrics Available (out of 10)": str(metrics_available),
            "Data Confidence": data_confidence,
            "Primary Opportunity Theme": primary_theme,
            "Secondary Opportunity Theme": secondary_theme,
            "Suggested Action": suggested_action,
            "Notes": notes,
        }

        weighted_rows.append(
            {
                **base_row,
                "Performance Risk Score": format_score(performance_risk_score),
                "Mapping Risk Score": format_score(mapping_risk_score),
                "Metadata Risk Score": format_score(metadata_risk_score),
                "Weighted Priority Score": format_score(weighted_priority_score),
                "Weighted Priority Tier": weighted_priority,
            }
        )

        rule_rows.append(
            {
                **base_row,
                "Major Decline Count (<=-20%)": str(major_decline_count),
                "Moderate Decline Count (<=-10%)": str(moderate_decline_count),
                "Rule Priority Tier": rule_priority,
                "Rule Trigger Reason": trigger_reason,
            }
        )

        parse_warnings = []
        if norm_url not in metadata_by_url:
            parse_warnings.append("Missing metadata row")
        if norm_url not in l3m_by_url:
            parse_warnings.append("Missing L3M row")
        if norm_url not in yoy_by_url:
            parse_warnings.append("Missing YoY row")
        for key in METRIC_ORDER:
            raw_value = metric_raw[key]
            parsed_value = metric_parsed[key]
            if (raw_value or "").strip() and parsed_value is None:
                parse_warnings.append(f"Unparsed metric: {METRIC_LABELS[key]} raw='{raw_value.strip()}'")

        raw_mapping_urls = sorted(set(row.get("raw_url", "") for row in raw_mapping_rows if row.get("raw_url", "")))
        top_source_rows = [str(row.get("row_index", "")) for row in top_rows]
        while len(top_source_rows) < 3:
            top_source_rows.append("")

        qa_rows.append(
            {
                "URL": output_url_value,
                "Normalized URL": norm_url,
                "Mapping Raw URLs": " | ".join(raw_mapping_urls),
                "Mapping Row Count (Raw)": str(len(raw_mapping_rows)),
                "Mapping Row Count (Dedup)": str(keyword_rows_count),
                "Top Keyword 1": top_keywords[0],
                "Top Keyword 1 Source Row": top_source_rows[0],
                "Top Keyword 2": top_keywords[1],
                "Top Keyword 2 Source Row": top_source_rows[1],
                "Top Keyword 3": top_keywords[2],
                "Top Keyword 3 Source Row": top_source_rows[2],
                "Exact Count": str(exact_count),
                "Partial Count": str(partial_count),
                "Optimize Count": str(optimize_count),
                "None Action Count": str(none_action_count),
                "Topic Cluster": topic_cluster,
                "Metadata Raw URL": metadata.get("raw_url", ""),
                "Metadata Title Raw": meta_title,
                "Metadata Description Raw": meta_desc,
                "Metadata H1 Raw": h1,
                "L3M Raw URL": l3.get("raw_url", ""),
                "L3M Raw Δ Clicks % (col5)": metric_raw["l3m_clicks_pct"],
                "L3M Raw Δ Impr % (col8)": metric_raw["l3m_impr_pct"],
                "L3M Raw Δ Engaged Sessions % (col11)": metric_raw["l3m_engaged_pct"],
                "L3M Raw Δ Users % (col14)": metric_raw["l3m_users_pct"],
                "L3M Raw Δ Conv % (col17)": metric_raw["l3m_conv_pct"],
                "L3M Parsed Δ Clicks %": "" if metric_parsed["l3m_clicks_pct"] is None else format_decimal(metric_parsed["l3m_clicks_pct"]),
                "L3M Parsed Δ Impr %": "" if metric_parsed["l3m_impr_pct"] is None else format_decimal(metric_parsed["l3m_impr_pct"]),
                "L3M Parsed Δ Engaged Sessions %": "" if metric_parsed["l3m_engaged_pct"] is None else format_decimal(metric_parsed["l3m_engaged_pct"]),
                "L3M Parsed Δ Users %": "" if metric_parsed["l3m_users_pct"] is None else format_decimal(metric_parsed["l3m_users_pct"]),
                "L3M Parsed Δ Conv %": "" if metric_parsed["l3m_conv_pct"] is None else format_decimal(metric_parsed["l3m_conv_pct"]),
                "YoY Raw URL": yy.get("raw_url", ""),
                "YoY Raw Δ Clicks % (col5)": metric_raw["yoy_clicks_pct"],
                "YoY Raw Δ Impr % (col8)": metric_raw["yoy_impr_pct"],
                "YoY Raw Δ Engaged Sessions % (col11)": metric_raw["yoy_engaged_pct"],
                "YoY Raw Δ Users % (col14)": metric_raw["yoy_users_pct"],
                "YoY Raw Δ Conv % (col17)": metric_raw["yoy_conv_pct"],
                "YoY Parsed Δ Clicks %": "" if metric_parsed["yoy_clicks_pct"] is None else format_decimal(metric_parsed["yoy_clicks_pct"]),
                "YoY Parsed Δ Impr %": "" if metric_parsed["yoy_impr_pct"] is None else format_decimal(metric_parsed["yoy_impr_pct"]),
                "YoY Parsed Δ Engaged Sessions %": "" if metric_parsed["yoy_engaged_pct"] is None else format_decimal(metric_parsed["yoy_engaged_pct"]),
                "YoY Parsed Δ Users %": "" if metric_parsed["yoy_users_pct"] is None else format_decimal(metric_parsed["yoy_users_pct"]),
                "YoY Parsed Δ Conv %": "" if metric_parsed["yoy_conv_pct"] is None else format_decimal(metric_parsed["yoy_conv_pct"]),
                "Metrics Available (out of 10)": str(metrics_available),
                "Data Confidence": data_confidence,
                "Parse Warnings": " | ".join(parse_warnings),
            }
        )

    weighted_rows.sort(key=lambda row: (-safe_float(row["Weighted Priority Score"]), row["URL"].lower()))
    rule_rank = {"High": 0, "Medium": 1, "Low": 2}
    rule_rows.sort(
        key=lambda row: (
            rule_rank.get(row["Rule Priority Tier"], 9),
            -safe_float(row["Major Decline Count (<=-20%)"]),
            -safe_float(row["Moderate Decline Count (<=-10%)"]),
            row["URL"].lower(),
        )
    )
    qa_rows.sort(key=lambda row: row["URL"].lower())

    return weighted_rows, rule_rows, qa_rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    weighted_rows, rule_rows, qa_rows = build_rows()

    weighted_fields = [
        "URL",
        "Topic Cluster",
        "Top Keyword 1",
        "Top Keyword 2",
        "Top Keyword 3",
        "Other Keywords Summary",
        "Keyword Rows (Count)",
        "Exact Count",
        "Partial Count",
        "Optimize Count",
        "None Action Count",
        "Partial Ratio",
        "Meta Title",
        "Meta Description",
        "H1",
        "Metadata Gaps",
        "L3M Δ Clicks %",
        "L3M Δ Impr %",
        "L3M Δ Engaged Sessions %",
        "L3M Δ Users %",
        "L3M Δ Conv %",
        "YoY Δ Clicks %",
        "YoY Δ Impr %",
        "YoY Δ Engaged Sessions %",
        "YoY Δ Users %",
        "YoY Δ Conv %",
        "Metrics Available (out of 10)",
        "Data Confidence",
        "Primary Opportunity Theme",
        "Secondary Opportunity Theme",
        "Suggested Action",
        "Notes",
        "Performance Risk Score",
        "Mapping Risk Score",
        "Metadata Risk Score",
        "Weighted Priority Score",
        "Weighted Priority Tier",
    ]

    rule_fields = [
        "URL",
        "Topic Cluster",
        "Top Keyword 1",
        "Top Keyword 2",
        "Top Keyword 3",
        "Other Keywords Summary",
        "Keyword Rows (Count)",
        "Exact Count",
        "Partial Count",
        "Optimize Count",
        "None Action Count",
        "Partial Ratio",
        "Meta Title",
        "Meta Description",
        "H1",
        "Metadata Gaps",
        "L3M Δ Clicks %",
        "L3M Δ Impr %",
        "L3M Δ Engaged Sessions %",
        "L3M Δ Users %",
        "L3M Δ Conv %",
        "YoY Δ Clicks %",
        "YoY Δ Impr %",
        "YoY Δ Engaged Sessions %",
        "YoY Δ Users %",
        "YoY Δ Conv %",
        "Metrics Available (out of 10)",
        "Data Confidence",
        "Primary Opportunity Theme",
        "Secondary Opportunity Theme",
        "Suggested Action",
        "Notes",
        "Major Decline Count (<=-20%)",
        "Moderate Decline Count (<=-10%)",
        "Rule Priority Tier",
        "Rule Trigger Reason",
    ]

    qa_fields = [
        "URL",
        "Normalized URL",
        "Mapping Raw URLs",
        "Mapping Row Count (Raw)",
        "Mapping Row Count (Dedup)",
        "Top Keyword 1",
        "Top Keyword 1 Source Row",
        "Top Keyword 2",
        "Top Keyword 2 Source Row",
        "Top Keyword 3",
        "Top Keyword 3 Source Row",
        "Exact Count",
        "Partial Count",
        "Optimize Count",
        "None Action Count",
        "Topic Cluster",
        "Metadata Raw URL",
        "Metadata Title Raw",
        "Metadata Description Raw",
        "Metadata H1 Raw",
        "L3M Raw URL",
        "L3M Raw Δ Clicks % (col5)",
        "L3M Raw Δ Impr % (col8)",
        "L3M Raw Δ Engaged Sessions % (col11)",
        "L3M Raw Δ Users % (col14)",
        "L3M Raw Δ Conv % (col17)",
        "L3M Parsed Δ Clicks %",
        "L3M Parsed Δ Impr %",
        "L3M Parsed Δ Engaged Sessions %",
        "L3M Parsed Δ Users %",
        "L3M Parsed Δ Conv %",
        "YoY Raw URL",
        "YoY Raw Δ Clicks % (col5)",
        "YoY Raw Δ Impr % (col8)",
        "YoY Raw Δ Engaged Sessions % (col11)",
        "YoY Raw Δ Users % (col14)",
        "YoY Raw Δ Conv % (col17)",
        "YoY Parsed Δ Clicks %",
        "YoY Parsed Δ Impr %",
        "YoY Parsed Δ Engaged Sessions %",
        "YoY Parsed Δ Users %",
        "YoY Parsed Δ Conv %",
        "Metrics Available (out of 10)",
        "Data Confidence",
        "Parse Warnings",
    ]

    write_csv(OUT_WEIGHTED, weighted_rows, weighted_fields)
    write_csv(OUT_RULE, rule_rows, rule_fields)
    write_csv(OUT_QA, qa_rows, qa_fields)

    print(f"Wrote {len(weighted_rows)} rows -> {OUT_WEIGHTED}")
    print(f"Wrote {len(rule_rows)} rows -> {OUT_RULE}")
    print(f"Wrote {len(qa_rows)} rows -> {OUT_QA}")


if __name__ == "__main__":
    main()
