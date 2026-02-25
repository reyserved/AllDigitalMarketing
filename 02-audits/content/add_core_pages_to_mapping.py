#!/usr/bin/env python3
"""Add 17 Omnipress core URLs to pages keyword mapping with exact-match rows."""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


BASE_DIR = Path(__file__).resolve().parent

MAPPING_PATH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Keyword Mapping - pages.csv"
METADATA_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - core-pages-metadata.csv"
L3M_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - Core Pages - L3M.csv"
YOY_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - core-pages-YoY.csv"
SOURCE_KEYWORDS_PATH = BASE_DIR.parent.parent / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research.csv"

MAPPING_FIELDS = [
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
    "i",
    "in",
    "is",
    "it",
    "its",
    "my",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "us",
    "we",
    "what",
    "should",
    "with",
    "you",
    "your",
}

BRAND_TERMS = {
    "omnipress",
    "omnipress madison",
    "omni print",
    "omni printing",
    "omni printer",
}

GENERIC_SINGLETONS = {
    "about",
    "conference",
    "conferences",
    "training",
    "event",
    "service",
    "services",
    "request",
    "quote",
    "form",
    "product",
    "pricing",
    "newsletter",
    "application",
    "bags",
    "features",
    "videos",
    "quick",
    "tips",
}

REJECT_PHRASES = {
    "application for employment omnipress",
    "request for quote omnipress",
    "newsletter signup omnipress",
    "bags request for quote",
    "conferences event",
    "training product",
}


@dataclass(frozen=True)
class UrlSpec:
    url: str
    intent: str
    cluster: str
    rows_needed: int


TARGET_SPECS = [
    UrlSpec("https://omnipress.com/training/fulfillment/5-easy-steps-to-a-successful-print-fulfillment-transition/", "Informational", "Training", 1),
    UrlSpec("https://omnipress.com/training/pricing/", "Transactional", "Training", 3),
    UrlSpec("https://omnipress.com/training/training-manual-printing/", "Commercial", "Training", 3),
    UrlSpec("https://omnipress.com/support/", "Navigational", "Support", 1),
    UrlSpec("https://omnipress.com/newsletter-signup/", "Transactional", "Support", 3),
    UrlSpec("https://omnipress.com/contact/", "Navigational", "Support", 1),
    UrlSpec("https://omnipress.com/printer-quiz/", "Informational", "Support", 1),
    UrlSpec("https://omnipress.com/conferences/pricing/", "Transactional", "Conferences", 3),
    UrlSpec("https://omnipress.com/conferences/event-services/event-services-contact-form/", "Transactional", "Conferences", 3),
    UrlSpec("https://omnipress.com/conferences/event-services/", "Commercial", "Conferences", 3),
    UrlSpec("https://omnipress.com/conferences/event-swag-bags/request-for-quote/", "Transactional", "Conferences", 3),
    UrlSpec("https://omnipress.com/conferences/event-swag-bags/", "Commercial", "Conferences", 3),
    UrlSpec("https://omnipress.com/careers/omnipress-application-form/", "Transactional", "Careers", 3),
    UrlSpec("https://omnipress.com/conferences/abstract-management/catalyst-quick-tips/", "Informational", "Conferences", 1),
    UrlSpec("https://omnipress.com/careers/", "Navigational", "Careers", 1),
    UrlSpec("https://omnipress.com/conferences/abstract-management/catalyst-features-videos/", "Informational", "Conferences", 1),
    UrlSpec("https://omnipress.com/about-us/", "Navigational", "Brand", 1),
]


INTENT_CUES = {
    "Transactional": {
        "pricing",
        "quote",
        "request",
        "contact form",
        "signup",
        "application",
        "apply",
        "request for quote",
        "newsletter signup",
        "application for employment",
        "form",
        "contact",
    },
    "Commercial": {
        "service",
        "services",
        "event services",
        "swag",
        "swag bags",
        "event swag bag",
        "training manual",
        "manual printing",
        "print fulfillment",
        "printing",
        "product",
    },
    "Informational": {
        "tips",
        "quick tips",
        "videos",
        "features videos",
        "quiz",
        "steps",
        "guide",
        "transition",
        "print partner",
        "training materials",
        "print fulfillment transition",
    },
    "Navigational": {
        "support",
        "contact",
        "careers",
        "about",
        "newsletter",
        "knowledge base",
        "omnipress",
    },
}


def normalize_url(raw_url: str) -> str:
    raw = (raw_url or "").strip()
    if not raw:
        return ""
    raw = raw.replace("http://", "https://")
    if "://" not in raw:
        raw = f"https://{raw.lstrip('/')}"
    parsed = urlsplit(raw)
    if not parsed.netloc:
        return ""
    host = parsed.netloc.lower()
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


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", (text or "").lower())
    return normalize_space(cleaned)


def normalize_keyword(text: str) -> str:
    return normalize_space((text or "").lower())


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [tok for tok in normalized.split(" ") if tok]


def safe_float(raw: str) -> float:
    value = (raw or "").strip().replace(",", "")
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def read_csv_dict(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{k: (v or "") for k, v in row.items()} for row in csv.DictReader(handle)]


def read_l3m_urls(path: Path) -> set[str]:
    urls = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if len(row) >= 1:
                url = normalize_url(row[0])
                if url:
                    urls.add(url)
    return urls


def read_yoy_urls(path: Path) -> set[str]:
    urls = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if len(row) >= 1:
                url = normalize_url(row[0])
                if url:
                    urls.add(url)
    return urls


def generate_ngrams(tokens: list[str], max_n: int = 5) -> set[str]:
    phrases = set()
    n_tokens = len(tokens)
    for n in range(1, max_n + 1):
        if n > n_tokens:
            continue
        for i in range(0, n_tokens - n + 1):
            phrase = " ".join(tokens[i : i + n]).strip()
            if phrase:
                phrases.add(phrase)
    return phrases


def keyword_is_brand_dominated(keyword: str) -> bool:
    phrase = normalize_keyword(keyword)
    if not phrase:
        return True
    if phrase in BRAND_TERMS:
        return True
    if "omnipress" in phrase and len(phrase.split(" ")) <= 3:
        return True
    if "omni print" in phrase:
        return True
    return False


def phrase_presence(phrase: str, slug_text: str, title_text: str, h1_text: str) -> tuple[int, list[str]]:
    hits = []
    if phrase and phrase in slug_text:
        hits.append("URL")
    if phrase and phrase in title_text:
        hits.append("Title")
    if phrase and phrase in h1_text:
        hits.append("H1")
    return len(hits), hits


def intent_fit_score(phrase: str, intent: str) -> int:
    phrase_l = normalize_keyword(phrase)
    cues = INTENT_CUES.get(intent, set())
    score = 0
    for cue in cues:
        if cue in phrase_l:
            score += 2 if " " in cue else 1
    return score


def lexical_score(phrase: str) -> int:
    tokens = [tok for tok in phrase.split(" ") if tok]
    if not tokens:
        return -10
    if len(tokens) == 1:
        return 2
    if 2 <= len(tokens) <= 4:
        return 4
    return 0


def infer_candidate_phrases(slug_text: str, title_text: str, h1_text: str) -> set[str]:
    candidates = set()
    for text in (slug_text, title_text, h1_text):
        tokens = [tok for tok in text.split(" ") if tok]
        candidates.update(generate_ngrams(tokens, max_n=4))
    # Add a few normalized phrase variants likely to be strong exact candidates.
    candidates = {normalize_space(c) for c in candidates if c and not all(tok in STOPWORDS for tok in c.split(" "))}
    return {c for c in candidates if c}


def topic_bonus(phrase: str, cluster: str) -> int:
    p = normalize_keyword(phrase)
    if cluster == "Training" and any(tok in p for tok in ("training", "manual", "fulfillment", "print", "course")):
        return 2
    if cluster == "Conferences" and any(tok in p for tok in ("conference", "event", "swag", "abstract", "catalyst")):
        return 2
    if cluster == "Support" and any(tok in p for tok in ("support", "contact", "newsletter", "quiz", "help")):
        return 2
    if cluster == "Careers" and any(tok in p for tok in ("career", "employment", "application")):
        return 2
    if cluster == "Brand" and any(tok in p for tok in ("about", "omnipress")):
        return 2
    return 0


def stopword_ratio_penalty(phrase: str) -> int:
    tokens = [tok for tok in phrase.split(" ") if tok]
    if not tokens:
        return -5
    stop_count = sum(1 for tok in tokens if tok in STOPWORDS)
    ratio = stop_count / len(tokens)
    if ratio > 0.5:
        return -5
    if ratio > 0.3:
        return -3
    if ratio > 0.2:
        return -1
    return 0


def is_noisy_phrase(phrase: str, *, allow_brand_like: bool) -> bool:
    p = normalize_keyword(phrase)
    tokens = [tok for tok in p.split(" ") if tok]
    if not tokens:
        return True
    if p in REJECT_PHRASES:
        return True
    if tokens[0] in {"bag", "bags"}:
        return True
    if any(len(tok) <= 1 for tok in tokens):
        return True
    if tokens[0] in STOPWORDS or tokens[-1] in STOPWORDS:
        return True
    if len(tokens) == 1 and tokens[0] in GENERIC_SINGLETONS:
        return True
    stop_ratio = sum(1 for tok in tokens if tok in STOPWORDS) / len(tokens)
    if stop_ratio > 0.5:
        return True
    if p.startswith("omnipress ") and p.endswith(" omnipress"):
        return True
    if p.endswith("omnipress") and p != "about omnipress":
        return True
    if any(tokens.count(tok) > 1 for tok in {"omnipress", "training", "event", "conference", "services"}):
        return True
    if not allow_brand_like and keyword_is_brand_dominated(p):
        return True
    if len(tokens) > 5:
        return True
    return False


def rank_candidates(
    *,
    candidates: list[dict[str, object]],
) -> list[dict[str, object]]:
    return sorted(
        candidates,
        key=lambda item: (
            -float(item["score"]),
            -int(item["presence_count"]),
            -int(item["intent_score"]),
            -int(bool(item["source_backed"])),
            -float(item["search_volume"]),
            -int(item["lexical_score"]),
            str(item["phrase"]),
        ),
    )


def build_candidates_for_url(
    *,
    spec: UrlSpec,
    title: str,
    h1: str,
    source_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    url = normalize_url(spec.url)
    path_tokens = tokenize(urlsplit(url).path.replace("/", " "))
    slug_text = normalize_space(" ".join(path_tokens))
    title_text = normalize_text(title)
    h1_text = normalize_text(h1)

    allow_brand_like = spec.cluster in {"Brand", "Careers", "Support"}

    merged: dict[str, dict[str, object]] = {}

    # Source-backed candidates.
    for row in source_rows:
        keyword_raw = normalize_space(row.get("Keyword", ""))
        keyword = normalize_keyword(keyword_raw)
        if not keyword:
            continue
        if is_noisy_phrase(keyword, allow_brand_like=allow_brand_like):
            continue
        presence_count, hit_fields = phrase_presence(keyword, slug_text, title_text, h1_text)
        if presence_count == 0:
            continue
        source_sv = safe_float(row.get("Search Volume", ""))
        intent_score = intent_fit_score(keyword, spec.intent)
        lex_score = lexical_score(keyword)
        t_bonus = topic_bonus(keyword, spec.cluster)
        penalty = stopword_ratio_penalty(keyword)
        score = (
            12 * presence_count
            + 8 * intent_score
            + 3
            + min(math.log10(1 + max(source_sv, 0.0)), 3.0)
            + lex_score
            + t_bonus
            + penalty
        )
        existing = merged.get(keyword)
        payload = {
            "phrase": keyword,
            "search_volume": source_sv,
            "source_backed": True,
            "presence_count": presence_count,
            "hit_fields": hit_fields,
            "intent_score": intent_score,
            "lexical_score": lex_score,
            "score": score,
        }
        if existing is None or float(payload["score"]) > float(existing["score"]):
            merged[keyword] = payload

    # Inferred candidates from slug/title/h1.
    inferred = infer_candidate_phrases(slug_text, title_text, h1_text)
    for phrase in inferred:
        keyword = normalize_keyword(phrase)
        if not keyword:
            continue
        if is_noisy_phrase(keyword, allow_brand_like=allow_brand_like):
            continue
        presence_count, hit_fields = phrase_presence(keyword, slug_text, title_text, h1_text)
        if presence_count == 0:
            continue
        intent_score = intent_fit_score(keyword, spec.intent)
        lex_score = lexical_score(keyword)
        t_bonus = topic_bonus(keyword, spec.cluster)
        penalty = stopword_ratio_penalty(keyword)
        score = (
            12 * presence_count
            + 8 * intent_score
            + 0
            + 0
            + lex_score
            + t_bonus
            + penalty
        )
        existing = merged.get(keyword)
        payload = {
            "phrase": keyword,
            "search_volume": 0.0,
            "source_backed": False,
            "presence_count": presence_count,
            "hit_fields": hit_fields,
            "intent_score": intent_score,
            "lexical_score": lex_score,
            "score": score,
        }
        if existing is None or float(payload["score"]) > float(existing["score"]):
            merged[keyword] = payload

    ranked = rank_candidates(candidates=list(merged.values()))
    return ranked


def exact_note(hit_fields: list[str]) -> str:
    fields = ", ".join(hit_fields) if hit_fields else "URL/title/H1"
    return f"Fully aligned: exact keyword appears in {fields}; mapped via intent/page-type rule."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-keywords-csv",
        default=str(SOURCE_KEYWORDS_PATH),
        help="Path to source keyword CSV (Address/Page Type/.../Keyword/... schema).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_keywords_path = Path(args.source_keywords_csv).expanduser().resolve()
    if not source_keywords_path.exists():
        print(f"Source keyword file not found: {source_keywords_path}")
        raise SystemExit(1)

    mapping_rows = read_csv_dict(MAPPING_PATH)
    metadata_rows = read_csv_dict(METADATA_PATH)
    source_rows = read_csv_dict(source_keywords_path)
    l3m_urls = read_l3m_urls(L3M_PATH)
    yoy_urls = read_yoy_urls(YOY_PATH)

    metadata_by_url = {}
    for row in metadata_rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue
        metadata_by_url[url] = {
            "title": normalize_space(row.get("Title 1", "")),
            "meta_desc": normalize_space(row.get("Meta Description 1", "")),
            "h1": normalize_space(row.get("H1-1", "")),
        }

    source_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue
        source_by_url[url].append(row)

    target_urls = [normalize_url(spec.url) for spec in TARGET_SPECS]

    missing = []
    for url in target_urls:
        if url not in metadata_by_url:
            missing.append((url, "metadata"))
        if url not in l3m_urls:
            missing.append((url, "l3m"))
        if url not in yoy_urls:
            missing.append((url, "yoy"))
    if missing:
        print("Validation failed. Missing required URL coverage:")
        for url, source_name in missing:
            print(f" - {url} missing in {source_name}")
        raise SystemExit(1)

    target_set = {normalize_url(spec.url) for spec in TARGET_SPECS}

    # Remove prior generated rows for these 17 URLs to keep reruns deterministic.
    base_mapping_rows = []
    removed_prior_generated = 0
    for row in mapping_rows:
        row_url = normalize_url(row.get("Current URL", ""))
        note = normalize_space(row.get("Notes", ""))
        if row_url in target_set and "mapped via intent/page-type rule" in note:
            removed_prior_generated += 1
            continue
        base_mapping_rows.append(row)

    existing_keys = set()
    existing_urls = set()
    for row in base_mapping_rows:
        url = normalize_url(row.get("Current URL", ""))
        keyword = normalize_keyword(row.get("Keyword", ""))
        match_type = normalize_space(row.get("Match Type", ""))
        action = normalize_space(row.get("Suggested Action", ""))
        if url:
            existing_urls.add(url)
        if url and keyword:
            existing_keys.add((url, keyword, match_type, action))

    new_rows: list[dict[str, str]] = []
    per_url_added = defaultdict(int)

    for spec in TARGET_SPECS:
        norm_url = normalize_url(spec.url)
        metadata = metadata_by_url[norm_url]
        title = metadata["title"]
        meta_desc = metadata["meta_desc"]
        h1 = metadata["h1"]

        candidates = build_candidates_for_url(
            spec=spec,
            title=title,
            h1=h1,
            source_rows=source_by_url.get(norm_url, []),
        )
        if not candidates:
            print(f"No exact-match candidates available for {norm_url}")
            raise SystemExit(1)

        selected: list[dict[str, object]] = []
        seen_keywords = set()
        for cand in candidates:
            keyword = normalize_keyword(str(cand["phrase"]))
            key = (norm_url, keyword, "Exact", "Optimize")
            if key in existing_keys or keyword in seen_keywords:
                continue
            selected.append(cand)
            seen_keywords.add(keyword)
            if len(selected) == spec.rows_needed:
                break

        if len(selected) < spec.rows_needed:
            print(f"Insufficient candidates for {norm_url}: needed {spec.rows_needed}, got {len(selected)}")
            raise SystemExit(1)

        for cand in selected:
            keyword = str(cand["phrase"])
            sv = float(cand["search_volume"])
            hit_fields = list(cand["hit_fields"])  # type: ignore[arg-type]
            row = {
                "Keyword": keyword,
                "Search Volume": str(int(sv)) if sv > 0 and abs(sv - int(sv)) < 1e-9 else (f"{sv:.2f}".rstrip("0").rstrip(".") if sv > 0 else ""),
                "Search Intent": spec.intent,
                "Topic Cluster": spec.cluster,
                "Current URL": display_url(norm_url),
                "Meta Title": title,
                "Meta Description": meta_desc,
                "H1": h1,
                "Match Type": "Exact",
                "Suggested Action": "Optimize",
                "Notes": exact_note(hit_fields),
            }
            new_rows.append(row)
            per_url_added[norm_url] += 1
            existing_keys.add((norm_url, normalize_keyword(keyword), "Exact", "Optimize"))

    # Hard expectation from plan.
    if len(new_rows) != 35:
        print(f"Unexpected new-row count: expected 35, got {len(new_rows)}")
        raise SystemExit(1)

    combined_rows = base_mapping_rows + new_rows

    with MAPPING_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=MAPPING_FIELDS)
        writer.writeheader()
        for row in combined_rows:
            writer.writerow({field: row.get(field, "") for field in MAPPING_FIELDS})

    updated_urls = set(existing_urls) | set(target_urls)
    print(f"Source keyword file: {source_keywords_path}")
    print(f"Removed prior generated rows for target URLs: {removed_prior_generated}")
    print(f"Added rows: {len(new_rows)}")
    print(f"Updated mapping rows: {len(combined_rows)}")
    print(f"Updated unique URLs: {len(updated_urls)}")
    for spec in TARGET_SPECS:
        norm_url = normalize_url(spec.url)
        print(f" - {display_url(norm_url)} -> added {per_url_added[norm_url]} rows")


if __name__ == "__main__":
    main()
