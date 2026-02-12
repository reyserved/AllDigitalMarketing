#!/usr/bin/env python3
"""
Builds final Omnipress keyword mapping outputs:
1) Omnipress_Keyword_Mapping_FINAL.csv
2) Omnipress_Keyword_Mapping_FINAL_QA.csv

Implements locked rules from the agreed plan with one update:
- Include zero-volume keywords and flag them as cluster-completeness terms in Notes.
"""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


BASE_DIR = Path("/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis")

INPUT_KEYWORD_RESEARCH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research.csv"
INPUT_PAGE_SITEMAP = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - page-sitemap.csv"
INPUT_POST_SITEMAP = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - post-sitemap.csv"
INPUT_CRAWL_DEPTH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - crawl_depth_l5.csv"
INPUT_DIRECTORY_GRAPH = BASE_DIR / "Directory Tree Graph_omnipress.html"

OUTPUT_MAPPING = BASE_DIR / "Omnipress_Keyword_Mapping_FINAL.csv"
OUTPUT_QA = BASE_DIR / "Omnipress_Keyword_Mapping_FINAL_QA.csv"


CORE_PAGE_TYPES = {
    "SERVICE",
    "MAIN-SERVICE",
    "PRODUCT",
    "PRODUCT-HUB",
    "BLOG",
    "BLOG-HUB",
    "CONVERSION",
}

SOURCE_PRIORITY = {
    "SEMrush;GSC Query": 0,
    "SEMrush": 1,
    "Seed": 2,
    "Expansion": 3,
}

OUTPUT_COLUMNS = [
    "Keyword",
    "Search Volume",
    "Search Intent",
    "Topic Cluster",
    "Current URL",
    "Match Type",
    "Suggested Action",
    "Notes",
]

STOP_WORDS = {
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
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "what",
    "when",
    "where",
    "why",
    "with",
    "you",
    "your",
}


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def normalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    if value.startswith("http://"):
        value = "https://" + value[len("http://") :]
    if value.endswith("/") and len(value) > len("https://"):
        value = value.rstrip("/") + "/"
    return value


def parse_float(value: str, default: float = 0.0) -> float:
    text = (value or "").strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def parse_int_or_float_string(value: str) -> str:
    num = parse_float(value, default=0.0)
    if math.isclose(num, int(num)):
        return str(int(num))
    return f"{num:.2f}".rstrip("0").rstrip(".")


def normalize_keyword(keyword: str) -> str:
    return re.sub(r"\s+", " ", (keyword or "").strip().lower())


def tokenize(text: str) -> List[str]:
    cleaned = re.sub(r"https?://", " ", (text or "").lower())
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned)
    tokens = [t for t in cleaned.split() if t and t not in STOP_WORDS]
    return tokens


def normalized_text_for_phrase(text: str) -> str:
    return " ".join(tokenize(text))


def jaccard(tokens_a: Sequence[str], tokens_b: Sequence[str]) -> float:
    set_a, set_b = set(tokens_a), set(tokens_b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def parse_intent(raw_intent: str, fallback_page_type: str) -> str:
    raw = (raw_intent or "").strip().lower()
    if raw:
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        tags = set(parts)
        if "transactional" in tags:
            return "Transactional"
        if "commercial" in tags:
            return "Commercial"
        if "informational" in tags:
            return "Informational"
        if "navigational" in tags:
            return "Navigational"
    if fallback_page_type == "BLOG" or fallback_page_type == "BLOG-HUB":
        return "Informational"
    return "Commercial"


def extract_directory_graph_metadata(path: Path) -> Dict[str, Dict[str, str]]:
    html = path.read_text(encoding="utf-8")
    match = re.search(r"chart\.run\((\{.*?\})\);", html, re.S)
    if not match:
        return {}
    root = json.loads(match.group(1))
    meta: Dict[str, Dict[str, str]] = {}

    def walk(node: Dict[str, object]) -> None:
        display_url = str(node.get("display_url", "")).strip()
        if display_url:
            meta[normalize_url(display_url)] = {
                "response_code": str(node.get("response_code", "")).strip(),
                "non_indexable_reason": str(node.get("nonIndexableReason", "")).strip(),
            }
        for child in node.get("children") or []:
            walk(child)

    walk(root)
    return meta


def winner_rank(row: Dict[str, str]) -> Tuple[int, float, float]:
    source = (row.get("Source") or "").strip()
    source_rank = SOURCE_PRIORITY.get(source, 99)
    search_volume = parse_float(row.get("Search Volume"), default=0.0)
    crawl_depth = parse_float(row.get("Crawl Depth"), default=99.0)
    return (source_rank, -search_volume, crawl_depth)


def get_url_slug(url: str) -> str:
    u = normalize_url(url)
    if "://" in u:
        path = u.split("://", 1)[1]
        path = path.split("/", 1)[1] if "/" in path else ""
    else:
        path = u
    return path.strip("/")


def compute_score(
    keyword: str,
    url: str,
    h1: str,
    title: str,
    cluster_alignment: int,
) -> Tuple[float, float, float, float, int]:
    keyword_tokens = tokenize(keyword)
    slug_tokens = tokenize(get_url_slug(url))
    h1_tokens = tokenize(h1)
    title_tokens = tokenize(title)

    slug_overlap = jaccard(keyword_tokens, slug_tokens)
    h1_overlap = jaccard(keyword_tokens, h1_tokens)
    title_overlap = jaccard(keyword_tokens, title_tokens)

    phrase_text = " ".join(
        [
            normalized_text_for_phrase(get_url_slug(url)),
            normalized_text_for_phrase(h1),
            normalized_text_for_phrase(title),
        ]
    ).strip()
    phrase_candidate = " ".join(tokenize(keyword))
    phrase_bonus = 1 if phrase_candidate and phrase_candidate in phrase_text else 0

    score = (
        0.45 * max(slug_overlap, h1_overlap)
        + 0.25 * title_overlap
        + 0.20 * phrase_bonus
        + 0.10 * cluster_alignment
    )
    return score, slug_overlap, h1_overlap, title_overlap, phrase_bonus


def select_best_url_for_keyword(
    keyword: str,
    keyword_cluster: str,
    eligible_url_meta: Dict[str, Dict[str, str]],
) -> Tuple[str, Dict[str, float]]:
    best_url = ""
    best_payload = {
        "score": -1.0,
        "slug_overlap": 0.0,
        "h1_overlap": 0.0,
        "title_overlap": 0.0,
        "phrase_bonus": 0.0,
        "cluster_alignment": 0.0,
    }
    for url, meta in eligible_url_meta.items():
        url_cluster = (meta.get("dominant_cluster") or "").strip()
        cluster_alignment = 1 if keyword_cluster and keyword_cluster == url_cluster else 0
        score, slug_o, h1_o, title_o, phrase_bonus = compute_score(
            keyword=keyword,
            url=url,
            h1=meta.get("h1", ""),
            title=meta.get("title", ""),
            cluster_alignment=cluster_alignment,
        )
        payload = {
            "score": score,
            "slug_overlap": slug_o,
            "h1_overlap": h1_o,
            "title_overlap": title_o,
            "phrase_bonus": float(phrase_bonus),
            "cluster_alignment": float(cluster_alignment),
        }

        if score > best_payload["score"]:
            best_url, best_payload = url, payload
            continue

        if math.isclose(score, best_payload["score"], rel_tol=1e-9):
            # tie-breaker: prefer same-cluster URL, then shallower crawl depth, then lexical URL sort
            best_cluster_alignment = int(best_payload["cluster_alignment"])
            if cluster_alignment > best_cluster_alignment:
                best_url, best_payload = url, payload
                continue
            if cluster_alignment == best_cluster_alignment:
                best_depth = parse_float(eligible_url_meta.get(best_url, {}).get("crawl_depth", ""), 99.0)
                curr_depth = parse_float(meta.get("crawl_depth", ""), 99.0)
                if curr_depth < best_depth:
                    best_url, best_payload = url, payload
                    continue
                if math.isclose(curr_depth, best_depth) and url < best_url:
                    best_url, best_payload = url, payload

    return best_url, best_payload


def build() -> None:
    # Keep crawl depth file in workflow context (structural reference only).
    _crawl_depth_rows = read_csv(INPUT_CRAWL_DEPTH)

    keyword_rows = read_csv(INPUT_KEYWORD_RESEARCH)
    page_sitemap_rows = read_csv(INPUT_PAGE_SITEMAP)
    post_sitemap_rows = read_csv(INPUT_POST_SITEMAP)
    graph_meta = extract_directory_graph_metadata(INPUT_DIRECTORY_GRAPH)

    sitemap_urls = {
        normalize_url(row.get("URL", ""))
        for row in [*page_sitemap_rows, *post_sitemap_rows]
        if normalize_url(row.get("URL", ""))
    }

    # Build page-type lookup + URL metadata from keyword research.
    url_page_types: Dict[str, Counter] = defaultdict(Counter)
    url_cluster_counts: Dict[str, Counter] = defaultdict(Counter)
    url_h1: Dict[str, str] = {}
    url_title: Dict[str, str] = {}
    url_crawl_depth: Dict[str, str] = {}

    for row in keyword_rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue
        page_type = (row.get("Page Type") or "").strip()
        cluster = (row.get("Cluster") or "").strip()
        if page_type:
            url_page_types[url][page_type] += 1
        if cluster:
            url_cluster_counts[url][cluster] += 1
        if (row.get("H1-1") or "").strip() and url not in url_h1:
            url_h1[url] = row.get("H1-1", "").strip()
        if (row.get("Title 1") or "").strip() and url not in url_title:
            url_title[url] = row.get("Title 1", "").strip()
        depth = (row.get("Crawl Depth") or "").strip()
        if depth and url not in url_crawl_depth:
            url_crawl_depth[url] = depth

    # Determine eligible URLs by:
    # - in sitemap
    # - dominant page type in core scope
    # - graph says HTTP 200 + not nonindex
    eligible_url_meta: Dict[str, Dict[str, str]] = {}
    for url in sitemap_urls:
        dominant_page_type = ""
        if url_page_types.get(url):
            dominant_page_type = url_page_types[url].most_common(1)[0][0]
        if dominant_page_type not in CORE_PAGE_TYPES:
            continue

        gm = graph_meta.get(url, {})
        response_code = (gm.get("response_code") or "").strip()
        non_indexable_reason = (gm.get("non_indexable_reason") or "").strip().lower()
        if response_code and response_code != "200":
            continue
        if non_indexable_reason == "noindex":
            continue
        if non_indexable_reason in {"redirected", "canonicalised", "client error"}:
            continue

        dominant_cluster = ""
        if url_cluster_counts.get(url):
            dominant_cluster = url_cluster_counts[url].most_common(1)[0][0]

        eligible_url_meta[url] = {
            "page_type": dominant_page_type,
            "dominant_cluster": dominant_cluster,
            "h1": url_h1.get(url, ""),
            "title": url_title.get(url, ""),
            "crawl_depth": url_crawl_depth.get(url, ""),
        }

    # Candidate rows:
    # - keyword non-empty
    # - URL is eligible
    # - core page type
    # - include zero search volume rows
    candidate_rows_by_keyword: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in keyword_rows:
        keyword_raw = (row.get("Keyword") or "").strip()
        if not keyword_raw:
            continue
        keyword_norm = normalize_keyword(keyword_raw)
        if not keyword_norm:
            continue

        url = normalize_url(row.get("Address", ""))
        if not url or url not in eligible_url_meta:
            continue

        page_type = (row.get("Page Type") or "").strip()
        if page_type not in CORE_PAGE_TYPES:
            continue

        candidate_rows_by_keyword[keyword_norm].append(row)

    output_rows: List[Dict[str, str]] = []
    manual_review_rows: List[Dict[str, str]] = []

    for keyword_norm, rows in candidate_rows_by_keyword.items():
        winner = min(rows, key=winner_rank)
        winner_cluster = (winner.get("Cluster") or "").strip()
        winner_source = (winner.get("Source") or "").strip() or "Unknown"

        best_url, score_payload = select_best_url_for_keyword(
            keyword=winner.get("Keyword", ""),
            keyword_cluster=winner_cluster,
            eligible_url_meta=eligible_url_meta,
        )
        best_url_meta = eligible_url_meta.get(best_url, {})

        # cluster normalization
        topic_cluster = winner_cluster or (best_url_meta.get("dominant_cluster") or "").strip()
        if not topic_cluster:
            topic_cluster = "Unmapped/Noise"

        # intent normalization
        search_intent = parse_intent(
            raw_intent=winner.get("Intent", ""),
            fallback_page_type=best_url_meta.get("page_type", ""),
        )

        # match + action rules
        score = score_payload["score"]
        phrase_bonus = int(score_payload["phrase_bonus"])
        has_valid_url = bool(best_url)

        if not has_valid_url:
            match_type = "None"
            suggested_action = "Create New"
        else:
            if phrase_bonus == 1 or score >= 0.70:
                match_type = "Exact"
            elif score >= 0.30:
                match_type = "Partial"
            else:
                # Conservative gap policy: existing valid core URL => optimize.
                match_type = "Partial"

            current_position = parse_float(winner.get("Current Position"), default=999.0)
            if (
                match_type == "Exact"
                and winner_source == "SEMrush;GSC Query"
                and current_position <= 10
            ):
                suggested_action = "None"
            else:
                suggested_action = "Optimize"

        # include zero search volume keywords explicitly
        search_volume_num = parse_float(winner.get("Search Volume"), default=0.0)
        search_volume_text = parse_int_or_float_string(winner.get("Search Volume"))
        if search_volume_text == "":
            search_volume_text = "0"

        impressions = parse_int_or_float_string(winner.get("GSC Impressions"))
        current_pos_txt = parse_int_or_float_string(winner.get("Current Position"))

        if winner_source == "SEMrush;GSC Query":
            signals = f"position={current_pos_txt};impressions={impressions}"
        elif winner_source == "SEMrush":
            signals = f"position={current_pos_txt}"
        else:
            signals = "no-ranking-data"

        rationale = f"{match_type.lower()}(score={score:.2f})"
        action_reason = (
            "create-new"
            if suggested_action == "Create New"
            else ("none-strong-ranked" if suggested_action == "None" else "optimize-existing")
        )
        notes_parts = [
            f"Source={winner_source}",
            f"Rationale={rationale}",
            f"ActionReason={action_reason}",
            f"Signals={signals}",
        ]
        if search_volume_num <= 0:
            notes_parts.append("ZeroVolume=Essential cluster-completeness term")

        output_rows.append(
            {
                "Keyword": (winner.get("Keyword") or "").strip(),
                "Search Volume": search_volume_text,
                "Search Intent": search_intent,
                "Topic Cluster": topic_cluster,
                "Current URL": best_url if has_valid_url else "",
                "Match Type": match_type,
                "Suggested Action": suggested_action,
                "Notes": "; ".join(notes_parts),
            }
        )

        manual_review_rows.append(
            {
                "keyword": (winner.get("Keyword") or "").strip(),
                "search_volume": search_volume_text,
                "url": best_url,
                "cluster": topic_cluster,
                "score": f"{score:.2f}",
                "match_type": match_type,
                "action": suggested_action,
            }
        )

    # Stable sort for deterministic outputs: Search Volume desc, Keyword asc
    output_rows.sort(
        key=lambda row: (
            -parse_float(row.get("Search Volume"), default=0.0),
            normalize_keyword(row.get("Keyword", "")),
        )
    )
    manual_review_rows.sort(
        key=lambda row: (
            -parse_float(row.get("search_volume"), default=0.0),
            normalize_keyword(row.get("keyword", "")),
        )
    )

    with OUTPUT_MAPPING.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)

    # QA diagnostics
    qa_rows: List[Dict[str, str]] = []
    def add_check(check: str, result: str, details: str) -> None:
        qa_rows.append({"Check": check, "Result": result, "Details": details})

    # Check 1: exact schema order
    schema_ok = False
    with OUTPUT_MAPPING.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        schema_ok = header == OUTPUT_COLUMNS
    add_check(
        "Schema is exact 8-column target order",
        "PASS" if schema_ok else "FAIL",
        "; ".join(OUTPUT_COLUMNS),
    )

    # Check 2: uniqueness
    keywords = [normalize_keyword(r["Keyword"]) for r in output_rows]
    unique_ok = len(keywords) == len(set(keywords))
    add_check(
        "One row per unique keyword",
        "PASS" if unique_ok else "FAIL",
        f"rows={len(keywords)}; unique={len(set(keywords))}",
    )

    # Check 3: scope compliance for current URLs
    url_scope_violations = []
    for row in output_rows:
        url = normalize_url(row["Current URL"])
        if not url:
            continue
        if url not in eligible_url_meta:
            url_scope_violations.append(url)
    add_check(
        "Current URL is in allowed core scope",
        "PASS" if not url_scope_violations else "FAIL",
        f"violations={len(url_scope_violations)}",
    )

    # Check 4: create-new policy
    create_new_bad = []
    for row in output_rows:
        if row["Suggested Action"] == "Create New":
            if row["Current URL"] or row["Match Type"] != "None":
                create_new_bad.append(row["Keyword"])
    add_check(
        "Create New rows have blank URL and Match Type=None",
        "PASS" if not create_new_bad else "FAIL",
        f"violations={len(create_new_bad)}",
    )

    # Check 5: no blank intent
    blank_intent = sum(1 for r in output_rows if not (r["Search Intent"] or "").strip())
    add_check(
        "No blank Search Intent",
        "PASS" if blank_intent == 0 else "FAIL",
        f"blank_intent_rows={blank_intent}",
    )

    # Check 6: no blank cluster
    blank_cluster = sum(1 for r in output_rows if not (r["Topic Cluster"] or "").strip())
    add_check(
        "No blank Topic Cluster",
        "PASS" if blank_cluster == 0 else "FAIL",
        f"blank_cluster_rows={blank_cluster}",
    )

    # Check 7: action/match consistency
    invalid_action_match = []
    for row in output_rows:
        if row["Match Type"] == "Exact" and row["Suggested Action"] == "Create New":
            invalid_action_match.append(row["Keyword"])
    add_check(
        "Exact does not pair with Create New",
        "PASS" if not invalid_action_match else "FAIL",
        f"violations={len(invalid_action_match)}",
    )

    # Check 8: zero-volume keywords retained and noted
    zero_volume_rows = [r for r in output_rows if parse_float(r["Search Volume"], 0.0) <= 0]
    zero_volume_noted = [
        r
        for r in zero_volume_rows
        if "ZeroVolume=Essential cluster-completeness term" in (r["Notes"] or "")
    ]
    add_check(
        "Zero-volume keywords retained with essential-cluster note",
        "PASS" if len(zero_volume_rows) == len(zero_volume_noted) else "FAIL",
        f"zero_volume_rows={len(zero_volume_rows)}; noted={len(zero_volume_noted)}",
    )

    # Snapshot distributions
    add_check(
        "Distribution | Match Type",
        "INFO",
        str(dict(Counter(r["Match Type"] for r in output_rows))),
    )
    add_check(
        "Distribution | Suggested Action",
        "INFO",
        str(dict(Counter(r["Suggested Action"] for r in output_rows))),
    )
    add_check(
        "Distribution | Search Intent",
        "INFO",
        str(dict(Counter(r["Search Intent"] for r in output_rows))),
    )

    # Manual top-20 review section
    qa_rows.append({"Check": "Top 20 manual review sample", "Result": "INFO", "Details": "keyword|sv|cluster|url|score|match|action"})
    for item in manual_review_rows[:20]:
        qa_rows.append(
            {
                "Check": "Top20",
                "Result": "INFO",
                "Details": (
                    f"{item['keyword']}|{item['search_volume']}|{item['cluster']}|"
                    f"{item['url']}|{item['score']}|{item['match_type']}|{item['action']}"
                ),
            }
        )

    with OUTPUT_QA.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Check", "Result", "Details"])
        writer.writeheader()
        writer.writerows(qa_rows)

    print(f"Wrote: {OUTPUT_MAPPING}")
    print(f"Wrote: {OUTPUT_QA}")
    print(f"Rows in mapping: {len(output_rows)}")


if __name__ == "__main__":
    build()
