#!/usr/bin/env python3
"""Remap Omnipress *_none keyword rows using source keyword data (Expansion-aware)."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


BASE_DIR = Path("/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis")
SOURCE_PATH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research.csv"

INPUT_FILES = [
    Path("/Users/reymartjansarigumba/Downloads/Omnipress _ Keyword Research 2.2026 - Page_none.csv"),
    Path("/Users/reymartjansarigumba/Downloads/Omnipress _ Keyword Research 2.2026 - blogs_none.csv"),
]

QA_PATH = BASE_DIR / "Omnipress_None_Remap_QA.csv"

EXPECTED_COLUMNS = [
    "Keyword",
    "Search Volume",
    "Search Intent",
    "Topic Cluster",
    "Current URL",
    "Meta Title",
    "Meta Description",
    "H1",
    "Match Type",
    "Suggested Action",
    "Notes",
]

PLACEHOLDER_FLAG = "[map based on existing keyword data"

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
    "your",
    "you",
    "our",
    "we",
}

ACTION_WORDS = ("add ", "include ", "update ", "expand ", "align ", "cover ", "strengthen ")

INTENT_PRIORITY = {
    "Transactional": 4,
    "Commercial": 3,
    "Informational": 2,
    "Navigational": 1,
}


def normalize_url(raw: str) -> str:
    value = (raw or "").strip()
    if not value:
        return ""
    value = value.replace("http://", "https://")
    if value.startswith("//"):
        value = f"https:{value}"
    if "://" not in value:
        value = f"https://{value.lstrip('/')}"
    parsed = urlsplit(value)
    if not parsed.netloc:
        return ""
    host = parsed.netloc.lower()
    path = re.sub(r"/+", "/", parsed.path or "/")
    if not path.startswith("/"):
        path = f"/{path}"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"https://{host}{path}"


def output_url(normalized: str) -> str:
    norm = normalize_url(normalized)
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


def normalize_text_for_phrase(text: str) -> str:
    lowered = (text or "").lower()
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return normalize_space(lowered)


def tokenize(text: str) -> set[str]:
    cleaned = normalize_text_for_phrase(text)
    tokens = []
    for token in cleaned.split(" "):
        if len(token) <= 1:
            continue
        if token in STOPWORDS:
            continue
        tokens.append(token)
    return set(tokens)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def safe_float(value: str) -> float:
    raw = (value or "").strip().replace(",", "")
    if not raw:
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return 0.0


def format_sv(value: float) -> str:
    if value <= 0:
        return ""
    rounded = round(value)
    if abs(value - rounded) < 1e-9:
        return str(int(rounded))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def parse_source_flags(source_value: str) -> tuple[bool, bool, bool]:
    parts = [p.strip() for p in (source_value or "").split(";") if p.strip()]
    has_expansion = "Expansion" in parts
    has_semrush = "SEMrush" in parts
    has_semrush_gsc = has_semrush and "GSC Query" in parts
    return has_semrush_gsc, has_semrush and not has_expansion, has_expansion


def source_rank(has_semrush_gsc: bool, has_semrush_nonexp: bool) -> int:
    if has_semrush_gsc:
        return 1
    if has_semrush_nonexp:
        return 2
    return 3


def normalize_intent(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    parts = [p.strip().lower() for p in re.split(r"[;|/,]+", text) if p.strip()]
    mapped: list[str] = []
    for part in parts:
        if "transaction" in part or "purchase" in part or "buy" in part or part == "do":
            mapped.append("Transactional")
        elif "commercial" in part or "investigat" in part:
            mapped.append("Commercial")
        elif "inform" in part or "know" in part:
            mapped.append("Informational")
        elif "navigat" in part or "brand" in part or part == "go":
            mapped.append("Navigational")
    if not mapped:
        title = text.title()
        return title if title in INTENT_PRIORITY else ""
    mapped = sorted(set(mapped), key=lambda x: (-INTENT_PRIORITY[x], x))
    return mapped[0]


def dominant_counter(counter: Counter[str]) -> str:
    if not counter:
        return ""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        rows = [{k: (v or "") for k, v in row.items()} for row in reader]
    return header, rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_source_data(rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, dict[str, object]]]]:
    url_meta: dict[str, dict[str, str]] = {}
    url_candidates: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)

    for row in rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue

        meta_slot = url_meta.setdefault(
            url,
            {
                "meta_title": "",
                "meta_description": "",
                "h1": "",
            },
        )
        title = normalize_space(row.get("Title 1", ""))
        desc = normalize_space(row.get("Meta Description 1", ""))
        h1 = normalize_space(row.get("H1-1", ""))
        if title and not meta_slot["meta_title"]:
            meta_slot["meta_title"] = title
        if desc and not meta_slot["meta_description"]:
            meta_slot["meta_description"] = desc
        if h1 and not meta_slot["h1"]:
            meta_slot["h1"] = h1

        keyword_raw = normalize_space(row.get("Keyword", ""))
        keyword_norm = normalize_keyword(keyword_raw)
        if not keyword_norm:
            continue
        if PLACEHOLDER_FLAG in keyword_norm:
            continue

        slot = url_candidates[url].setdefault(
            keyword_norm,
            {
                "keyword_raw": keyword_raw,
                "search_volume": 0.0,
                "intent_counter": Counter(),
                "has_semrush_gsc": False,
                "has_semrush_nonexp": False,
                "has_expansion": False,
                "best_source_rank": 3,
                "best_position_semrush_gsc": None,
                "max_impressions": 0.0,
                "title": title,
                "h1": h1,
            },
        )

        sv = safe_float(row.get("Search Volume", ""))
        if sv > float(slot["search_volume"]):
            slot["search_volume"] = sv
            if keyword_raw:
                slot["keyword_raw"] = keyword_raw

        intent = normalize_intent(row.get("Intent", ""))
        if intent:
            slot["intent_counter"][intent] += 1  # type: ignore[index]

        semrush_gsc, semrush_nonexp, expansion = parse_source_flags(row.get("Source", ""))
        if semrush_gsc:
            slot["has_semrush_gsc"] = True
        if semrush_nonexp:
            slot["has_semrush_nonexp"] = True
        if expansion:
            slot["has_expansion"] = True
        rank = source_rank(bool(slot["has_semrush_gsc"]), bool(slot["has_semrush_nonexp"]))
        slot["best_source_rank"] = min(int(slot["best_source_rank"]), rank)

        if semrush_gsc:
            position = safe_float(row.get("Current Position", ""))
            if position > 0:
                best_pos = slot["best_position_semrush_gsc"]
                if best_pos is None or position < best_pos:
                    slot["best_position_semrush_gsc"] = position

        impressions = safe_float(row.get("GSC Impressions", ""))
        if impressions > float(slot["max_impressions"]):
            slot["max_impressions"] = impressions

        if title and not slot["title"]:
            slot["title"] = title
        if h1 and not slot["h1"]:
            slot["h1"] = h1

    return url_meta, url_candidates


def compute_candidate_score(
    keyword_norm: str,
    candidate: dict[str, object],
    url: str,
    row_intent: str,
) -> dict[str, object]:
    slug = urlsplit(url).path.strip("/")
    slug_text = normalize_text_for_phrase(slug.replace("/", " ").replace("-", " ").replace("_", " "))
    title_text = normalize_text_for_phrase(str(candidate.get("title", "")))
    h1_text = normalize_text_for_phrase(str(candidate.get("h1", "")))

    keyword_tokens = tokenize(keyword_norm)
    slug_tokens = tokenize(slug_text)
    title_tokens = tokenize(title_text)
    h1_tokens = tokenize(h1_text)

    slug_overlap = jaccard(keyword_tokens, slug_tokens)
    h1_overlap = jaccard(keyword_tokens, h1_tokens)
    title_overlap = jaccard(keyword_tokens, title_tokens)

    phrase_hits = 0
    if keyword_norm and keyword_norm in slug_text:
        phrase_hits += 1
    if keyword_norm and keyword_norm in title_text:
        phrase_hits += 1
    if keyword_norm and keyword_norm in h1_text:
        phrase_hits += 1

    has_semrush_gsc = bool(candidate.get("has_semrush_gsc"))
    has_semrush_nonexp = bool(candidate.get("has_semrush_nonexp"))
    if has_semrush_gsc:
        source_bonus = 0.20
    elif has_semrush_nonexp:
        source_bonus = 0.10
    else:
        source_bonus = 0.00

    source_intent = dominant_counter(candidate.get("intent_counter", Counter()))  # type: ignore[arg-type]
    if source_intent and row_intent:
        intent_bonus = 0.15 if source_intent == row_intent else -0.10
    elif not source_intent:
        intent_bonus = 0.05
    else:
        intent_bonus = 0.0

    sv = float(candidate.get("search_volume", 0.0))
    volume_bonus = min(math.log10(1 + sv) / 4, 0.10) if sv > 0 else 0.0

    score = (
        0.45 * max(slug_overlap, h1_overlap)
        + 0.20 * title_overlap
        + 0.15 * (phrase_hits / 3.0)
        + source_bonus
        + intent_bonus
        + volume_bonus
    )

    lexical_relevance = phrase_hits >= 1 or max(slug_overlap, h1_overlap, title_overlap) >= 0.20
    quality_ok = score >= 0.35
    accepted = lexical_relevance and quality_ok

    return {
        "keyword_norm": keyword_norm,
        "keyword_raw": str(candidate.get("keyword_raw", keyword_norm)),
        "source_intent": source_intent,
        "row_intent": row_intent,
        "search_volume": sv,
        "phrase_hits": phrase_hits,
        "slug_overlap": slug_overlap,
        "h1_overlap": h1_overlap,
        "title_overlap": title_overlap,
        "score": score,
        "accepted": accepted,
        "source_rank": int(candidate.get("best_source_rank", 3)),
        "has_semrush_gsc": has_semrush_gsc,
        "best_position_semrush_gsc": candidate.get("best_position_semrush_gsc"),
        "max_impressions": float(candidate.get("max_impressions", 0.0)),
    }


def select_winner(candidates: list[dict[str, object]]) -> dict[str, object] | None:
    valid = [c for c in candidates if c["accepted"]]
    if not valid:
        return None
    valid.sort(
        key=lambda c: (
            -float(c["score"]),
            -int(c["phrase_hits"]),
            -float(c["search_volume"]),
            int(c["source_rank"]),
            str(c["keyword_raw"]).lower(),
        )
    )
    return valid[0]


def exact_note(winner: dict[str, object]) -> str:
    components = []
    if int(winner["phrase_hits"]) >= 2:
        components.append("keyword phrase appears across slug/H1/title")
    else:
        components.append("strong keyword overlap with slug/H1/title")
    row_intent = str(winner.get("row_intent", ""))
    src_intent = str(winner.get("source_intent", ""))
    if row_intent and src_intent and row_intent == src_intent:
        components.append("intent is aligned")
    if winner.get("has_semrush_gsc") and winner.get("best_position_semrush_gsc"):
        pos = float(winner["best_position_semrush_gsc"])
        components.append(f"GSC-supported ranking signal (position {int(pos) if pos.is_integer() else pos})")
    return "Fully aligned: " + "; ".join(components) + "."


def partial_note(winner: dict[str, object]) -> str:
    actions: list[str] = []
    if int(winner["phrase_hits"]) == 0:
        actions.append("add the exact keyword in Meta Title and H1")
    elif int(winner["phrase_hits"]) == 1:
        actions.append("reinforce the exact keyword across Meta Title and H1")
    else:
        actions.append("tighten keyword prominence in key headings")
    if str(winner.get("row_intent", "")):
        actions.append("expand body copy to fully satisfy search intent")
    return "Optimize: " + "; ".join(actions) + "."


def no_match_note() -> str:
    return "No reliable same-URL keyword fit from source after relevance scoring."


def remap_rows(
    rows: list[dict[str, str]],
    url_meta: dict[str, dict[str, str]],
    url_candidates: dict[str, dict[str, dict[str, object]]],
) -> tuple[list[dict[str, str]], dict[str, int], dict[str, int], int]:
    out_rows: list[dict[str, str]] = []
    match_counts = Counter()
    source_mix_counts = Counter()
    intent_counts = Counter()
    traced_keywords = 0

    for row in rows:
        current = {field: row.get(field, "") for field in EXPECTED_COLUMNS}
        url = normalize_url(current.get("Current URL", ""))
        row_intent = normalize_intent(current.get("Search Intent", ""))
        if row_intent:
            current["Search Intent"] = row_intent

        candidates_for_url = url_candidates.get(url, {})
        scored = [
            compute_candidate_score(keyword_norm, candidate, url, row_intent)
            for keyword_norm, candidate in candidates_for_url.items()
        ] if url else []

        winner = select_winner(scored)

        if winner is None:
            current["Keyword"] = ""
            current["Search Volume"] = ""
            current["Match Type"] = "None"
            current["Suggested Action"] = "None"
            current["Notes"] = no_match_note()
            match_counts["None"] += 1
        else:
            traced_keywords += 1
            current["Keyword"] = str(winner["keyword_raw"])
            current["Search Volume"] = format_sv(float(winner["search_volume"]))

            source_intent = str(winner.get("source_intent", ""))
            if source_intent:
                current["Search Intent"] = source_intent

            if float(winner["score"]) >= 0.75 or (
                int(winner["phrase_hits"]) >= 2
                and max(float(winner["slug_overlap"]), float(winner["h1_overlap"])) >= 0.35
            ):
                match_type = "Exact"
            else:
                match_type = "Partial"
            current["Match Type"] = match_type

            rank_proof = (
                bool(winner.get("has_semrush_gsc"))
                and winner.get("best_position_semrush_gsc") is not None
                and float(winner["best_position_semrush_gsc"]) <= 10
            )
            if match_type == "Exact" and rank_proof:
                current["Suggested Action"] = "None"
            else:
                current["Suggested Action"] = "Optimize"

            if match_type == "Exact":
                current["Notes"] = exact_note(winner)
            else:
                current["Notes"] = partial_note(winner)

            src_rank = int(winner["source_rank"])
            if src_rank == 1:
                source_mix_counts["SEMrush;GSC Query"] += 1
            elif src_rank == 2:
                source_mix_counts["SEMrush"] += 1
            else:
                source_mix_counts["Expansion"] += 1

            row_int = normalize_intent(row.get("Search Intent", ""))
            final_int = normalize_intent(current.get("Search Intent", ""))
            if row_int and final_int:
                if row_int == final_int:
                    intent_counts["match"] += 1
                else:
                    intent_counts["mismatch"] += 1
            else:
                intent_counts["unknown"] += 1

            match_counts[match_type] += 1

        meta = url_meta.get(url, {})
        if winner is not None:
            if not current.get("Meta Title", "") and meta.get("meta_title", ""):
                current["Meta Title"] = meta["meta_title"]
            if not current.get("Meta Description", "") and meta.get("meta_description", ""):
                current["Meta Description"] = meta["meta_description"]
            if not current.get("H1", "") and meta.get("h1", ""):
                current["H1"] = meta["h1"]

        current["Current URL"] = output_url(url) if url else current.get("Current URL", "")
        out_rows.append(current)

    return out_rows, dict(match_counts), dict(source_mix_counts), dict(intent_counts), traced_keywords


def note_check_exact(note: str) -> bool:
    note_lower = (note or "").strip().lower()
    return all(word not in note_lower for word in ACTION_WORDS)


def note_check_partial(note: str) -> bool:
    note_lower = (note or "").strip().lower()
    return note_lower.startswith("optimize:") and any(word in note_lower for word in ACTION_WORDS)


def try_write_output(path: Path, rows: list[dict[str, str]]) -> Path:
    try:
        write_csv(path, rows, EXPECTED_COLUMNS)
        return path
    except PermissionError:
        fallback = BASE_DIR / f"{path.stem}_UPDATED{path.suffix}"
        write_csv(fallback, rows, EXPECTED_COLUMNS)
        return fallback
    except OSError:
        fallback = BASE_DIR / f"{path.stem}_UPDATED{path.suffix}"
        write_csv(fallback, rows, EXPECTED_COLUMNS)
        return fallback


def run() -> None:
    source_header, source_rows = read_csv(SOURCE_PATH)
    if not source_header:
        raise RuntimeError(f"Source file is empty: {SOURCE_PATH}")

    url_meta, url_candidates = build_source_data(source_rows)

    qa_rows: list[dict[str, str]] = []
    total_summary = Counter()
    output_paths: dict[str, Path] = {}

    def qa(check: str, result: str, details: str) -> None:
        qa_rows.append({"Check": check, "Result": result, "Details": details})

    for input_path in INPUT_FILES:
        header, rows = read_csv(input_path)
        file_tag = input_path.name

        schema_ok = header == EXPECTED_COLUMNS
        qa(f"{file_tag} schema unchanged", "PASS" if schema_ok else "FAIL", "; ".join(header))

        remapped_rows, match_counts, source_mix, intent_counts, traced_keywords = remap_rows(
            rows, url_meta, url_candidates
        )

        out_path = try_write_output(input_path, remapped_rows)
        output_paths[file_tag] = out_path

        row_count_ok = len(remapped_rows) == len(rows)
        qa(
            f"{file_tag} row count preserved",
            "PASS" if row_count_ok else "FAIL",
            f"before={len(rows)}; after={len(remapped_rows)}",
        )

        placeholder_remaining = sum(
            1
            for row in remapped_rows
            if PLACEHOLDER_FLAG in normalize_keyword(row.get("Keyword", ""))
        )
        qa(
            f"{file_tag} placeholder keyword removed",
            "PASS" if placeholder_remaining == 0 else "FAIL",
            f"remaining={placeholder_remaining}",
        )

        trace_fail = 0
        for row in remapped_rows:
            keyword_norm = normalize_keyword(row.get("Keyword", ""))
            url = normalize_url(row.get("Current URL", ""))
            if not keyword_norm:
                continue
            if keyword_norm not in url_candidates.get(url, {}):
                trace_fail += 1
        qa(
            f"{file_tag} chosen keywords trace to same URL source rows",
            "PASS" if trace_fail == 0 else "FAIL",
            f"trace_fail={trace_fail}; traced={traced_keywords}",
        )

        exact_rows = [row for row in remapped_rows if row.get("Match Type", "") == "Exact"]
        partial_rows = [row for row in remapped_rows if row.get("Match Type", "") == "Partial"]
        none_rows = [row for row in remapped_rows if row.get("Match Type", "") == "None"]

        exact_note_fail = sum(1 for row in exact_rows if not note_check_exact(row.get("Notes", "")))
        partial_note_fail = sum(1 for row in partial_rows if not note_check_partial(row.get("Notes", "")))
        none_consistency_fail = sum(
            1
            for row in none_rows
            if row.get("Suggested Action", "") != "None" or normalize_keyword(row.get("Keyword", "")) != ""
        )

        qa(
            f"{file_tag} exact notes are rationale-only",
            "PASS" if exact_note_fail == 0 else "FAIL",
            f"violations={exact_note_fail}; exact_rows={len(exact_rows)}",
        )
        qa(
            f"{file_tag} partial notes are actionable",
            "PASS" if partial_note_fail == 0 else "FAIL",
            f"violations={partial_note_fail}; partial_rows={len(partial_rows)}",
        )
        qa(
            f"{file_tag} none rows action consistency",
            "PASS" if none_consistency_fail == 0 else "FAIL",
            f"violations={none_consistency_fail}; none_rows={len(none_rows)}",
        )

        qa(
            f"{file_tag} summary",
            "INFO",
            " | ".join(
                [
                    f"output={out_path}",
                    f"Exact={match_counts.get('Exact', 0)}",
                    f"Partial={match_counts.get('Partial', 0)}",
                    f"None={match_counts.get('None', 0)}",
                    f"SEMrush;GSC Query={source_mix.get('SEMrush;GSC Query', 0)}",
                    f"SEMrush={source_mix.get('SEMrush', 0)}",
                    f"Expansion={source_mix.get('Expansion', 0)}",
                    f"intent_match={intent_counts.get('match', 0)}",
                    f"intent_mismatch={intent_counts.get('mismatch', 0)}",
                    f"intent_unknown={intent_counts.get('unknown', 0)}",
                ]
            ),
        )

        total_summary["Exact"] += match_counts.get("Exact", 0)
        total_summary["Partial"] += match_counts.get("Partial", 0)
        total_summary["None"] += match_counts.get("None", 0)
        total_summary["SEMrush;GSC Query"] += source_mix.get("SEMrush;GSC Query", 0)
        total_summary["SEMrush"] += source_mix.get("SEMrush", 0)
        total_summary["Expansion"] += source_mix.get("Expansion", 0)

    qa(
        "Overall summary",
        "INFO",
        " | ".join(
            [
                f"Exact={total_summary['Exact']}",
                f"Partial={total_summary['Partial']}",
                f"None={total_summary['None']}",
                f"SEMrush;GSC Query={total_summary['SEMrush;GSC Query']}",
                f"SEMrush={total_summary['SEMrush']}",
                f"Expansion={total_summary['Expansion']}",
            ]
        ),
    )

    write_csv(QA_PATH, qa_rows, ["Check", "Result", "Details"])


if __name__ == "__main__":
    run()
