#!/usr/bin/env python3
"""Fix page clusters and complete sitemap URL coverage for Omnipress split mapping files."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


BASE_DIR = Path(__file__).resolve().parent

SOURCE_FILE = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research.csv"
PAGE_SITEMAP_FILE = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - page-sitemap.csv"
POST_SITEMAP_FILE = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - post-sitemap.csv"

PAGES_FILE = BASE_DIR / "Omnipress_Keyword_Mapping_FINAL_PAGES.csv"
BLOGS_FILE = BASE_DIR / "Omnipress_Keyword_Mapping_FINAL_BLOGS.csv"
QA_FILE = BASE_DIR / "Omnipress_Keyword_Mapping_FINAL_SPLIT_QA.csv"

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

ALLOWED_PAGE_TYPES = {"SERVICE", "MAIN-SERVICE", "PRODUCT", "PRODUCT-HUB", "CONVERSION"}
ALLOWED_BLOG_TYPES = {"BLOG", "BLOG-HUB"}

INTENT_PRIORITY = {
    "Transactional": 4,
    "Commercial": 3,
    "Informational": 2,
    "Navigational": 1,
}

COVERAGE_NOTE = "Optimize: coverage row seeded from URL slug; refine title/H1/content to target this term."


def normalize_url(raw_url: str) -> str:
    raw = (raw_url or "").strip()
    if not raw:
        return ""
    if raw.startswith("//"):
        raw = f"https:{raw}"
    if "://" not in raw:
        raw = f"https://{raw.lstrip('/')}"
    parsed = urlsplit(raw)
    if not parsed.netloc:
        return ""
    netloc = parsed.netloc.lower().strip()
    if netloc.endswith(":443"):
        netloc = netloc[:-4]
    path = re.sub(r"/+", "/", parsed.path or "/")
    if not path.startswith("/"):
        path = f"/{path}"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"https://{netloc}{path}"


def output_url(url_key: str) -> str:
    key = normalize_url(url_key)
    if not key:
        return ""
    parsed = urlsplit(key)
    path = parsed.path or "/"
    if path != "/" and not path.endswith("/"):
        path = f"{path}/"
    return f"https://{parsed.netloc}{path}"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        rows: list[dict[str, str]] = []
        for row in reader:
            rows.append({k: (v or "") for k, v in row.items()})
    return header, rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: (row.get(field, "") or "") for field in fieldnames})


def normalize_intent(raw_intent: str) -> str:
    raw = (raw_intent or "").strip()
    if not raw:
        return ""
    parts = [p.strip().lower() for p in re.split(r"[;|/,]+", raw) if p.strip()]
    if not parts:
        parts = [raw.lower()]

    mapped: list[str] = []
    for part in parts:
        if (
            "transaction" in part
            or "purchase" in part
            or "buy" in part
            or part == "do"
        ):
            mapped.append("Transactional")
        elif "commercial" in part or "investigat" in part:
            mapped.append("Commercial")
        elif "inform" in part or "know" in part:
            mapped.append("Informational")
        elif "navigat" in part or part == "go" or "brand" in part:
            mapped.append("Navigational")
        else:
            candidate = part.title()
            if candidate in INTENT_PRIORITY:
                mapped.append(candidate)

    if not mapped:
        return ""
    unique = sorted(set(mapped), key=lambda x: (-INTENT_PRIORITY[x], x))
    return unique[0]


def dominant_from_counter(counter: Counter[str]) -> str:
    if not counter:
        return ""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def safe_number(value: str) -> float:
    raw = (value or "").strip()
    if not raw:
        return 0.0
    raw = raw.replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def top_level_slug(url_key: str) -> str:
    key = normalize_url(url_key)
    if not key:
        return ""
    path = urlsplit(key).path.strip("/")
    if not path:
        return ""
    return path.split("/", 1)[0]


def top_level_cluster_label(url_key: str) -> str:
    slug = top_level_slug(url_key)
    if not slug:
        return "Unclustered"
    text = slug.replace("-", " ").replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "Unclustered"
    label = text.title()
    label = re.sub(r"\bAnd\b", "&", label)
    return label or "Unclustered"


def seeded_keyword_from_path(url_key: str) -> str:
    key = normalize_url(url_key)
    if not key:
        return "coverage keyword"
    path = urlsplit(key).path.strip("/")
    if not path:
        return "homepage"
    seeded = path.replace("-", " ").replace("_", " ").replace("/", " ")
    seeded = re.sub(r"\s+", " ", seeded).strip().lower()
    return seeded or "coverage keyword"


def ensure_unique_keyword(seed: str, used_lower: set[str]) -> str:
    base = (seed or "").strip() or "coverage keyword"
    if base.lower() not in used_lower:
        used_lower.add(base.lower())
        return base
    idx = 2
    while True:
        candidate = f"{base} (coverage {idx})"
        if candidate.lower() not in used_lower:
            used_lower.add(candidate.lower())
            return candidate
        idx += 1


def read_sitemap_urls(path: Path) -> list[str]:
    header, rows = read_csv(path)
    if not header:
        return []
    preferred_fields = ["URL", "Address", "loc"]
    field = ""
    for candidate in preferred_fields:
        if candidate in header:
            field = candidate
            break
    if not field:
        field = header[0]

    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        key = normalize_url(row.get(field, ""))
        if key and key not in seen:
            seen.add(key)
            ordered.append(key)
    return ordered


def build_url_metadata(source_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    aggregate: dict[str, dict[str, object]] = {}
    for row in source_rows:
        key = normalize_url(row.get("Address", ""))
        if not key:
            continue
        slot = aggregate.setdefault(
            key,
            {
                "page_types": Counter(),
                "clusters": Counter(),
                "intents": Counter(),
                "meta_title": "",
                "meta_description": "",
                "h1": "",
            },
        )

        page_type = (row.get("Page Type", "") or "").strip().upper()
        if page_type:
            slot["page_types"][page_type] += 1  # type: ignore[index]

        cluster = (row.get("Cluster", "") or "").strip()
        if cluster:
            slot["clusters"][cluster] += 1  # type: ignore[index]

        intent_raw = row.get("Intent", "") or row.get("Intents", "")
        intent = normalize_intent(intent_raw)
        if intent:
            slot["intents"][intent] += 1  # type: ignore[index]

        title = (row.get("Title 1", "") or "").strip()
        desc = (row.get("Meta Description 1", "") or "").strip()
        h1 = (row.get("H1-1", "") or "").strip()
        if title and not slot["meta_title"]:
            slot["meta_title"] = title
        if desc and not slot["meta_description"]:
            slot["meta_description"] = desc
        if h1 and not slot["h1"]:
            slot["h1"] = h1

    result: dict[str, dict[str, str]] = {}
    for key, slot in aggregate.items():
        page_types: Counter[str] = slot["page_types"]  # type: ignore[assignment]
        clusters: Counter[str] = slot["clusters"]  # type: ignore[assignment]
        intents: Counter[str] = slot["intents"]  # type: ignore[assignment]
        blog_clusters = Counter(
            {name: count for name, count in clusters.items() if name.upper().startswith("BLOG-")}
        )
        result[key] = {
            "dominant_page_type": dominant_from_counter(page_types),
            "dominant_cluster": dominant_from_counter(clusters),
            "dominant_blog_cluster": dominant_from_counter(blog_clusters),
            "dominant_intent": dominant_from_counter(intents),
            "meta_title": str(slot["meta_title"]),
            "meta_description": str(slot["meta_description"]),
            "h1": str(slot["h1"]),
        }
    return result


def coerce_to_expected_schema(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    coerced: list[dict[str, str]] = []
    for row in rows:
        coerced.append({field: (row.get(field, "") or "").strip() for field in EXPECTED_COLUMNS})
    return coerced


def fill_blank_meta(row: dict[str, str], url_meta: dict[str, dict[str, str]]) -> None:
    key = normalize_url(row.get("Current URL", ""))
    if not key:
        return
    meta = url_meta.get(key, {})
    if not row.get("Meta Title", "") and meta.get("meta_title", ""):
        row["Meta Title"] = meta["meta_title"]
    if not row.get("Meta Description", "") and meta.get("meta_description", ""):
        row["Meta Description"] = meta["meta_description"]
    if not row.get("H1", "") and meta.get("h1", ""):
        row["H1"] = meta["h1"]


def row_sort_key(row: dict[str, str]) -> tuple[str, float, str]:
    cluster = (row.get("Topic Cluster", "") or "").strip().lower()
    volume = safe_number(row.get("Search Volume", ""))
    keyword = (row.get("Keyword", "") or "").strip().lower()
    return (cluster, -volume, keyword)


def verify_sorted(rows: list[dict[str, str]]) -> tuple[bool, int]:
    for idx in range(1, len(rows)):
        if row_sort_key(rows[idx - 1]) > row_sort_key(rows[idx]):
            return False, idx + 1
    return True, -1


def is_blog_url(url_key: str) -> bool:
    key = normalize_url(url_key)
    if not key:
        return False
    path = urlsplit(key).path.lower()
    return path == "/blog" or path.startswith("/blog/")


def duplicate_keywords(rows: list[dict[str, str]]) -> list[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        keyword = (row.get("Keyword", "") or "").strip().lower()
        if keyword:
            counter[keyword] += 1
    return sorted([k for k, count in counter.items() if count > 1])


def format_preview(values: list[str], limit: int = 5) -> str:
    if not values:
        return "-"
    if len(values) <= limit:
        return "; ".join(values)
    return f"{'; '.join(values[:limit])}; ... (+{len(values) - limit} more)"


def run() -> None:
    source_header, source_rows = read_csv(SOURCE_FILE)
    if not source_header:
        raise RuntimeError(f"Source file appears empty: {SOURCE_FILE}")

    _, pages_rows_raw = read_csv(PAGES_FILE)
    _, blogs_rows_raw = read_csv(BLOGS_FILE)
    pages_rows = coerce_to_expected_schema(pages_rows_raw)
    blogs_rows = coerce_to_expected_schema(blogs_rows_raw)
    pages_before = len(pages_rows)
    blogs_before = len(blogs_rows)

    url_meta = build_url_metadata(source_rows)
    page_sitemap_urls = read_sitemap_urls(PAGE_SITEMAP_FILE)
    post_sitemap_urls = read_sitemap_urls(POST_SITEMAP_FILE)

    eligible_page_urls = [
        url
        for url in page_sitemap_urls
        if url_meta.get(url, {}).get("dominant_page_type", "") in ALLOWED_PAGE_TYPES
    ]

    # Re-cluster all existing page rows from slug top-level and normalize URL formatting.
    for row in pages_rows:
        key = normalize_url(row.get("Current URL", ""))
        if key:
            row["Current URL"] = output_url(key)
            row["Topic Cluster"] = top_level_cluster_label(key)
            fill_blank_meta(row, url_meta)
        else:
            row["Topic Cluster"] = "Unclustered"

    # Preserve blog clusters; only normalize blank clusters to Unclustered.
    for row in blogs_rows:
        key = normalize_url(row.get("Current URL", ""))
        if key:
            row["Current URL"] = output_url(key)
            fill_blank_meta(row, url_meta)
        if not (row.get("Topic Cluster", "") or "").strip():
            row["Topic Cluster"] = "Unclustered"

    existing_page_urls = {
        normalize_url(row.get("Current URL", "")) for row in pages_rows if row.get("Current URL", "").strip()
    }
    existing_blog_urls = {
        normalize_url(row.get("Current URL", "")) for row in blogs_rows if row.get("Current URL", "").strip()
    }

    missing_page_urls = [url for url in eligible_page_urls if url not in existing_page_urls]
    missing_post_urls = [url for url in post_sitemap_urls if url not in existing_blog_urls]

    page_keyword_used = {
        (row.get("Keyword", "") or "").strip().lower()
        for row in pages_rows
        if (row.get("Keyword", "") or "").strip()
    }
    blog_keyword_used = {
        (row.get("Keyword", "") or "").strip().lower()
        for row in blogs_rows
        if (row.get("Keyword", "") or "").strip()
    }

    added_page_rows: list[dict[str, str]] = []
    added_blog_rows: list[dict[str, str]] = []

    for url in missing_page_urls:
        meta = url_meta.get(url, {})
        dominant_page_type = meta.get("dominant_page_type", "")
        seed = seeded_keyword_from_path(url)
        keyword = ensure_unique_keyword(seed, page_keyword_used)
        row = {field: "" for field in EXPECTED_COLUMNS}
        row["Keyword"] = keyword
        row["Search Volume"] = ""
        row["Search Intent"] = "Transactional" if dominant_page_type == "CONVERSION" else "Commercial"
        row["Topic Cluster"] = top_level_cluster_label(url)
        row["Current URL"] = output_url(url)
        row["Meta Title"] = meta.get("meta_title", "")
        row["Meta Description"] = meta.get("meta_description", "")
        row["H1"] = meta.get("h1", "")
        row["Match Type"] = "Partial"
        row["Suggested Action"] = "Optimize"
        row["Notes"] = COVERAGE_NOTE
        pages_rows.append(row)
        added_page_rows.append(row)

    for url in missing_post_urls:
        meta = url_meta.get(url, {})
        seed = seeded_keyword_from_path(url)
        keyword = ensure_unique_keyword(seed, blog_keyword_used)
        intent = meta.get("dominant_intent", "") or "Informational"
        cluster = meta.get("dominant_blog_cluster", "") or "Unclustered"
        row = {field: "" for field in EXPECTED_COLUMNS}
        row["Keyword"] = keyword
        row["Search Volume"] = ""
        row["Search Intent"] = intent
        row["Topic Cluster"] = cluster
        row["Current URL"] = output_url(url)
        row["Meta Title"] = meta.get("meta_title", "")
        row["Meta Description"] = meta.get("meta_description", "")
        row["H1"] = meta.get("h1", "")
        row["Match Type"] = "Partial"
        row["Suggested Action"] = "Optimize"
        row["Notes"] = COVERAGE_NOTE
        blogs_rows.append(row)
        added_blog_rows.append(row)

    pages_rows.sort(key=row_sort_key)
    blogs_rows.sort(key=row_sort_key)

    write_csv(PAGES_FILE, pages_rows, EXPECTED_COLUMNS)
    write_csv(BLOGS_FILE, blogs_rows, EXPECTED_COLUMNS)

    # QA
    qa_rows: list[dict[str, str]] = []

    def add_check(check: str, result: str, details: str) -> None:
        qa_rows.append({"Check": check, "Result": result, "Details": details})

    schema_ok = True
    for path in (PAGES_FILE, BLOGS_FILE):
        header, _ = read_csv(path)
        if header != EXPECTED_COLUMNS:
            schema_ok = False
    add_check(
        "Output schema matches expected 11-column order",
        "PASS" if schema_ok else "FAIL",
        "; ".join(EXPECTED_COLUMNS),
    )

    page_urls_out = {
        normalize_url(row.get("Current URL", "")) for row in pages_rows if row.get("Current URL", "").strip()
    }
    blog_urls_out = {
        normalize_url(row.get("Current URL", "")) for row in blogs_rows if row.get("Current URL", "").strip()
    }

    pages_missing_after = sorted([url for url in eligible_page_urls if url not in page_urls_out])
    blogs_missing_after = sorted([url for url in post_sitemap_urls if url not in blog_urls_out])

    pages_coverage_ok = len(pages_missing_after) == 0
    blogs_coverage_ok = len(blogs_missing_after) == 0

    add_check(
        "Pages eligible URL coverage (service/product/conversion)",
        "PASS" if pages_coverage_ok else "FAIL",
        f"{len(eligible_page_urls) - len(pages_missing_after)}/{len(eligible_page_urls)}; missing={format_preview([output_url(u) for u in pages_missing_after])}",
    )
    add_check(
        "Blogs post URL coverage",
        "PASS" if blogs_coverage_ok else "FAIL",
        f"{len(post_sitemap_urls) - len(blogs_missing_after)}/{len(post_sitemap_urls)}; missing={format_preview([output_url(u) for u in blogs_missing_after])}",
    )

    page_cluster_violations: list[str] = []
    for row in pages_rows:
        key = normalize_url(row.get("Current URL", ""))
        if not key:
            continue
        expected_cluster = top_level_cluster_label(key)
        actual_cluster = (row.get("Topic Cluster", "") or "").strip()
        if expected_cluster != actual_cluster:
            page_cluster_violations.append(
                f"{row.get('Keyword','')}|{output_url(key)}|expected={expected_cluster}|actual={actual_cluster}"
            )
    add_check(
        "Page cluster label follows top-level slug rule",
        "PASS" if not page_cluster_violations else "FAIL",
        f"violations={len(page_cluster_violations)}; sample={format_preview(page_cluster_violations)}",
    )

    page_added_type_violations: list[str] = []
    for row in added_page_rows:
        key = normalize_url(row.get("Current URL", ""))
        dominant_pt = url_meta.get(key, {}).get("dominant_page_type", "")
        if dominant_pt not in ALLOWED_PAGE_TYPES:
            page_added_type_violations.append(f"{output_url(key)}|{dominant_pt or 'UNKNOWN'}")
    add_check(
        "No utility/brand in page coverage additions",
        "PASS" if not page_added_type_violations else "FAIL",
        f"violations={len(page_added_type_violations)}; sample={format_preview(page_added_type_violations)}",
    )

    page_dupes = duplicate_keywords(pages_rows)
    blog_dupes = duplicate_keywords(blogs_rows)
    add_check(
        "Keyword uniqueness in PAGES (case-insensitive)",
        "PASS" if not page_dupes else "FAIL",
        f"duplicates={len(page_dupes)}; sample={format_preview(page_dupes)}",
    )
    add_check(
        "Keyword uniqueness in BLOGS (case-insensitive)",
        "PASS" if not blog_dupes else "FAIL",
        f"duplicates={len(blog_dupes)}; sample={format_preview(blog_dupes)}",
    )

    added_pages_ok = len(added_page_rows) == 19
    added_blogs_ok = len(added_blog_rows) == 22
    add_check(
        "Added coverage rows count - PAGES",
        "PASS" if added_pages_ok else "FAIL",
        f"expected=19; actual={len(added_page_rows)}",
    )
    add_check(
        "Added coverage rows count - BLOGS",
        "PASS" if added_blogs_ok else "FAIL",
        f"expected=22; actual={len(added_blog_rows)}",
    )

    note_violations: list[str] = []
    for row in added_page_rows + added_blog_rows:
        if (row.get("Notes", "") or "").strip() != COVERAGE_NOTE:
            note_violations.append(
                f"{row.get('Keyword','')}|{row.get('Current URL','')}|{row.get('Notes','')}"
            )
    add_check(
        "Coverage-row note format compliance",
        "PASS" if not note_violations else "FAIL",
        f"violations={len(note_violations)}; sample={format_preview(note_violations)}",
    )

    blogs_url_purity = [row.get("Current URL", "") for row in blogs_rows if not is_blog_url(row.get("Current URL", ""))]
    pages_url_purity = [row.get("Current URL", "") for row in pages_rows if is_blog_url(row.get("Current URL", ""))]
    add_check(
        "BLOGS URL purity (/blog/ only)",
        "PASS" if not blogs_url_purity else "FAIL",
        f"violations={len(blogs_url_purity)}; sample={format_preview(blogs_url_purity)}",
    )
    add_check(
        "PAGES URL purity (no /blog/ URLs)",
        "PASS" if not pages_url_purity else "FAIL",
        f"violations={len(pages_url_purity)}; sample={format_preview(pages_url_purity)}",
    )

    page_type_violations = []
    for row in pages_rows:
        key = normalize_url(row.get("Current URL", ""))
        if not key:
            continue
        page_type = url_meta.get(key, {}).get("dominant_page_type", "")
        if page_type and page_type not in ALLOWED_PAGE_TYPES:
            page_type_violations.append(f"{output_url(key)}|{page_type}")
    blog_type_violations = []
    for row in blogs_rows:
        key = normalize_url(row.get("Current URL", ""))
        if not key:
            continue
        page_type = url_meta.get(key, {}).get("dominant_page_type", "")
        if page_type and page_type not in ALLOWED_BLOG_TYPES:
            blog_type_violations.append(f"{output_url(key)}|{page_type}")
    add_check(
        "PAGES dominant page-type purity",
        "PASS" if not page_type_violations else "FAIL",
        f"violations={len(page_type_violations)}; sample={format_preview(page_type_violations)}",
    )
    add_check(
        "BLOGS dominant page-type purity",
        "PASS" if not blog_type_violations else "FAIL",
        f"violations={len(blog_type_violations)}; sample={format_preview(blog_type_violations)}",
    )

    pages_sorted_ok, pages_sorted_line = verify_sorted(pages_rows)
    blogs_sorted_ok, blogs_sorted_line = verify_sorted(blogs_rows)
    add_check(
        "Sort verification PAGES (cluster asc, volume desc, keyword asc)",
        "PASS" if pages_sorted_ok else "FAIL",
        f"rows={len(pages_rows)}; failure_row={pages_sorted_line if pages_sorted_line > 0 else '-'}",
    )
    add_check(
        "Sort verification BLOGS (cluster asc, volume desc, keyword asc)",
        "PASS" if blogs_sorted_ok else "FAIL",
        f"rows={len(blogs_rows)}; failure_row={blogs_sorted_line if blogs_sorted_line > 0 else '-'}",
    )

    # Explicit examples requested by user.
    sample_urls = [
        "https://omnipress.com/abstract-and-application-management/",
        "https://omnipress.com/bindings-tabs-finishes/",
    ]
    for sample_url in sample_urls:
        cluster_values = sorted(
            {
                row.get("Topic Cluster", "")
                for row in pages_rows
                if normalize_url(row.get("Current URL", "")) == normalize_url(sample_url)
            }
        )
        add_check(
            "Sample URL cluster check",
            "INFO",
            f"url={output_url(sample_url)}; clusters={format_preview(cluster_values)}",
        )

    add_check("Rows before split update", "INFO", f"pages={pages_before}; blogs={blogs_before}")
    add_check(
        "Rows after split update",
        "INFO",
        f"pages={len(pages_rows)}; blogs={len(blogs_rows)}; total={len(pages_rows)+len(blogs_rows)}",
    )

    write_csv(QA_FILE, qa_rows, ["Check", "Result", "Details"])


if __name__ == "__main__":
    run()
