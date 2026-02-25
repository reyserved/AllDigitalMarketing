#!/usr/bin/env python3
"""Top up 7 Omnipress core URLs to at least 5 mapped keywords each."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


BASE_DIR = Path(__file__).resolve().parent

MAPPING_PATH = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Keyword Mapping - pages.csv"
METADATA_PATH = BASE_DIR / "Benchmark Performance _ Omnipress - core-pages-metadata.csv"
SOURCE_PATH = BASE_DIR.parent.parent / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research.csv"
OUT_QA_PATH = BASE_DIR / "Omnipress_Target7_Expansion_QA.csv"

TARGET_URLS = [
    "https://omnipress.com/training/pricing/",
    "https://omnipress.com/training/training-manual-printing/",
    "https://omnipress.com/support/",
    "https://omnipress.com/printer-quiz/",
    "https://omnipress.com/conferences/pricing/",
    "https://omnipress.com/conferences/event-services/",
    "https://omnipress.com/conferences/abstract-management/catalyst-quick-tips/",
]

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

MIN_VARIANTS = 5

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
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}

INTENT_QUALIFIERS: dict[str, list[str]] = {
    "Transactional": ["pricing", "cost", "quote", "request", "buy", "order", "rfq"],
    "Commercial": ["professional", "custom", "managed", "enterprise", "solutions", "services", "best"],
    "Informational": ["guide", "tips", "how to", "overview", "checklist", "best practices", "quick"],
    "Navigational": ["official", "customer", "help", "support", "contact", "portal", "team"],
}

SOURCE_PRIORITY = {
    "SEMrush;GSC Query": 0,
    "SEMrush": 1,
    "Expansion": 2,
    "Inferred": 3,
}


@dataclass
class Candidate:
    keyword: str
    qualifier: str
    seed_keyword: str
    source_type: str
    source_raw: str
    source_intent: str
    search_volume: str
    search_volume_num: float
    current_position: float | None
    score: float
    slug_overlap: float
    h1_overlap: float
    title_overlap: float
    phrase_hits: list[str]
    accepted: bool
    reason: str
    fallback: bool


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_text(text: str) -> str:
    return normalize_space(re.sub(r"[^a-z0-9]+", " ", (text or "").lower()))


def normalize_keyword(text: str) -> str:
    return normalize_space((text or "").lower())


def normalize_intent(text: str) -> str:
    base = normalize_keyword(text)
    if not base:
        return ""
    if "transaction" in base:
        return "Transactional"
    if "commercial" in base:
        return "Commercial"
    if "inform" in base:
        return "Informational"
    if "navig" in base:
        return "Navigational"
    return text.strip().title()


def normalize_url(raw_url: str) -> str:
    raw = (raw_url or "").strip()
    if not raw:
        return ""
    raw = raw.replace("http://", "https://")
    if "://" not in raw:
        raw = "https://" + raw.lstrip("/")
    parsed = urlsplit(raw)
    if not parsed.netloc:
        return ""
    host = parsed.netloc.lower()
    path = re.sub(r"/+", "/", parsed.path or "/")
    if not path.startswith("/"):
        path = "/" + path
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
        path = path + "/"
    return f"https://{parsed.netloc}{path}"


def tokenize(text: str) -> list[str]:
    return [tok for tok in normalize_text(text).split(" ") if tok]


def filter_tokens(tokens: list[str]) -> list[str]:
    return [tok for tok in tokens if tok and tok not in STOPWORDS]


def safe_float(raw_value: str) -> float:
    value = normalize_space(raw_value).replace(",", "")
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def maybe_float(raw_value: str) -> float | None:
    value = normalize_space(raw_value).replace(",", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_csv_dict(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{k: (v or "") for k, v in row.items()} for row in csv.DictReader(handle)]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a.intersection(b))
    union = len(a.union(b))
    if union == 0:
        return 0.0
    return inter / union


def phrase_hits(keyword_norm: str, slug_text: str, title_text: str, h1_text: str) -> list[str]:
    hits: list[str] = []
    if keyword_norm and keyword_norm in slug_text:
        hits.append("URL")
    if keyword_norm and keyword_norm in title_text:
        hits.append("Title")
    if keyword_norm and keyword_norm in h1_text:
        hits.append("H1")
    return hits


def source_bucket(source_raw: str) -> tuple[str, int]:
    src = normalize_space(source_raw)
    src_norm = normalize_keyword(src)
    if "expansion" in src_norm:
        return "Expansion", 0
    if src:
        return "Source", 1
    return "Inferred", 2


def derive_seed_from_keyword(keyword: str) -> str:
    tokens = filter_tokens(tokenize(keyword))
    if not tokens:
        return ""
    return normalize_space(" ".join(tokens[: min(3, len(tokens))]))


def derive_qualifier(raw_qualifier: str, keyword: str, seed_keyword: str, intent: str) -> str:
    q = normalize_space(raw_qualifier)
    if q:
        return q
    keyword_norm = normalize_text(keyword)
    seed_norm = normalize_text(seed_keyword)
    if keyword_norm and seed_norm and seed_norm in keyword_norm:
        prefix = normalize_space(keyword_norm.split(seed_norm, 1)[0])
        if prefix:
            return prefix
    keyword_tokens = filter_tokens(tokenize(keyword))
    seed_tokens = set(filter_tokens(tokenize(seed_keyword)))
    for token in keyword_tokens:
        if token not in seed_tokens:
            return token
    pool = INTENT_QUALIFIERS.get(intent, [])
    return pool[0] if pool else "core"


def generate_ngrams(tokens: list[str], min_n: int = 1, max_n: int = 4) -> list[str]:
    ngrams: list[str] = []
    for n in range(min_n, max_n + 1):
        if n > len(tokens):
            continue
        for idx in range(0, len(tokens) - n + 1):
            ngrams.append(" ".join(tokens[idx : idx + n]))
    return ngrams


def build_seed_candidates(url: str, title: str, h1: str) -> list[str]:
    parsed = urlsplit(url)
    slug_tokens = filter_tokens(tokenize(parsed.path.replace("/", " ").replace("-", " ")))
    title_tokens = filter_tokens(tokenize(title))
    h1_tokens = filter_tokens(tokenize(h1))

    slug_text = normalize_space(" ".join(slug_tokens))
    title_text = normalize_space(" ".join(title_tokens))
    h1_text = normalize_space(" ".join(h1_tokens))

    all_phrases = generate_ngrams(slug_tokens, 1, 4)
    all_phrases += generate_ngrams(title_tokens, 1, 4)
    all_phrases += generate_ngrams(h1_tokens, 1, 4)

    scored: dict[str, tuple[int, int]] = {}
    for phrase in all_phrases:
        phrase_norm = normalize_space(phrase)
        if not phrase_norm:
            continue
        phrase_tokens = phrase_norm.split(" ")
        if all(tok in STOPWORDS for tok in phrase_tokens):
            continue
        presence = 0
        if phrase_norm in slug_text:
            presence += 1
        if phrase_norm in title_text:
            presence += 1
        if phrase_norm in h1_text:
            presence += 1
        if presence == 0:
            continue
        if len(phrase_tokens) == 1 and phrase_tokens[0] in {"omnipress", "training", "conferences"}:
            continue
        prior = scored.get(phrase_norm)
        score = (presence, len(phrase_tokens))
        if prior is None or score > prior:
            scored[phrase_norm] = score

    sorted_phrases = sorted(scored.keys(), key=lambda p: (-scored[p][0], -scored[p][1], p))
    return sorted_phrases


def compute_candidate_score(
    keyword: str,
    intent_target: str,
    intent_source: str,
    source_type: str,
    search_volume: float,
    slug_tokens: set[str],
    title_tokens: set[str],
    h1_tokens: set[str],
    slug_text: str,
    title_text: str,
    h1_text: str,
) -> tuple[float, float, float, float, list[str], bool, str]:
    kw_norm = normalize_text(keyword)
    kw_tokens = set(filter_tokens(kw_norm.split(" ")))
    slug_overlap = jaccard(kw_tokens, slug_tokens)
    h1_overlap = jaccard(kw_tokens, h1_tokens)
    title_overlap = jaccard(kw_tokens, title_tokens)
    hits = phrase_hits(kw_norm, slug_text, title_text, h1_text)
    phrase_bonus = len(hits) / 3.0

    src_bonus = 0.0
    if source_type == "Expansion":
        src_bonus = 0.20
    elif source_type == "Source":
        src_bonus = 0.10

    src_intent_norm = normalize_intent(intent_source)
    intent_bonus = 0.05
    if src_intent_norm:
        intent_bonus = 0.15 if src_intent_norm == intent_target else -0.10

    vol_bonus = min(math.log10(1.0 + max(search_volume, 0.0)) / 4.0, 0.10)
    score = (
        0.45 * max(slug_overlap, h1_overlap)
        + 0.20 * title_overlap
        + 0.15 * phrase_bonus
        + src_bonus
        + intent_bonus
        + vol_bonus
    )

    max_overlap = max(slug_overlap, h1_overlap, title_overlap)
    lexical_gate = len(hits) >= 1 or max_overlap >= 0.20
    quality_gate = score >= 0.35
    accepted = lexical_gate and quality_gate
    reason = "accepted" if accepted else f"gates_failed(lexical={lexical_gate},quality={quality_gate})"
    return score, slug_overlap, h1_overlap, title_overlap, hits, accepted, reason


def source_priority_value(source_type: str, source_raw: str) -> int:
    if source_type == "Inferred":
        return SOURCE_PRIORITY["Inferred"]
    raw = normalize_space(source_raw)
    if raw in SOURCE_PRIORITY:
        return SOURCE_PRIORITY[raw]
    if source_type == "Expansion":
        return SOURCE_PRIORITY["Expansion"]
    return SOURCE_PRIORITY["SEMrush"]


def build_source_candidates(
    source_rows: list[dict[str, str]],
    *,
    intent_target: str,
    slug_tokens: set[str],
    title_tokens: set[str],
    h1_tokens: set[str],
    slug_text: str,
    title_text: str,
    h1_text: str,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in source_rows:
        keyword = normalize_space(row.get("Keyword", ""))
        if not keyword:
            continue
        seed_keyword = normalize_space(row.get("Seed Keyword", ""))
        if not seed_keyword:
            seed_keyword = derive_seed_from_keyword(keyword)
        src_type, _bucket = source_bucket(row.get("Source", ""))
        qualifier = derive_qualifier(
            row.get("Qualifier", ""),
            keyword,
            seed_keyword,
            intent_target,
        )
        sv_raw = normalize_space(row.get("Search Volume", ""))
        sv_num = safe_float(sv_raw)
        score, slug_overlap, h1_overlap, title_overlap, hits, accepted, reason = compute_candidate_score(
            keyword=keyword,
            intent_target=intent_target,
            intent_source=row.get("Intent", ""),
            source_type=src_type,
            search_volume=sv_num,
            slug_tokens=slug_tokens,
            title_tokens=title_tokens,
            h1_tokens=h1_tokens,
            slug_text=slug_text,
            title_text=title_text,
            h1_text=h1_text,
        )
        candidates.append(
            Candidate(
                keyword=keyword,
                qualifier=qualifier,
                seed_keyword=seed_keyword,
                source_type=src_type,
                source_raw=normalize_space(row.get("Source", "")) or src_type,
                source_intent=normalize_space(row.get("Intent", "")),
                search_volume=sv_raw,
                search_volume_num=sv_num,
                current_position=maybe_float(row.get("Current Position", "")),
                score=score,
                slug_overlap=slug_overlap,
                h1_overlap=h1_overlap,
                title_overlap=title_overlap,
                phrase_hits=hits,
                accepted=accepted,
                reason=reason,
                fallback=False,
            )
        )
    return candidates


def build_inferred_candidates(
    *,
    url: str,
    title: str,
    h1: str,
    intent_target: str,
    slug_tokens: set[str],
    title_tokens: set[str],
    h1_tokens: set[str],
    slug_text: str,
    title_text: str,
    h1_text: str,
) -> list[Candidate]:
    pool = INTENT_QUALIFIERS.get(intent_target, ["core", "guide", "services", "overview", "help"])
    seeds = build_seed_candidates(url, title, h1)
    if not seeds:
        path_tokens = filter_tokens(tokenize(urlsplit(url).path.replace("/", " ").replace("-", " ")))
        if path_tokens:
            seeds = [normalize_space(" ".join(path_tokens[: min(3, len(path_tokens))]))]

    candidates: list[Candidate] = []
    seen_keywords: set[str] = set()
    for qualifier in pool:
        for seed in seeds[:12]:
            if not seed:
                continue
            seed_tokens = seed.split(" ")
            if qualifier in seed_tokens:
                keyword = seed
            else:
                keyword = normalize_space(f"{qualifier} {seed}")
            keyword_norm = normalize_keyword(keyword)
            if not keyword_norm or keyword_norm in seen_keywords:
                continue
            seen_keywords.add(keyword_norm)
            score, slug_overlap, h1_overlap, title_overlap, hits, accepted, reason = compute_candidate_score(
                keyword=keyword,
                intent_target=intent_target,
                intent_source=intent_target,
                source_type="Inferred",
                search_volume=0.0,
                slug_tokens=slug_tokens,
                title_tokens=title_tokens,
                h1_tokens=h1_tokens,
                slug_text=slug_text,
                title_text=title_text,
                h1_text=h1_text,
            )
            candidates.append(
                Candidate(
                    keyword=keyword,
                    qualifier=qualifier,
                    seed_keyword=seed,
                    source_type="Inferred",
                    source_raw="Inferred",
                    source_intent=intent_target,
                    search_volume="",
                    search_volume_num=0.0,
                    current_position=None,
                    score=score,
                    slug_overlap=slug_overlap,
                    h1_overlap=h1_overlap,
                    title_overlap=title_overlap,
                    phrase_hits=hits,
                    accepted=accepted,
                    reason=reason,
                    fallback=False,
                )
            )
    return candidates


def fallback_candidates(
    *,
    url: str,
    title: str,
    h1: str,
    intent_target: str,
    slug_tokens: set[str],
    title_tokens: set[str],
    h1_tokens: set[str],
    slug_text: str,
    title_text: str,
    h1_text: str,
) -> list[Candidate]:
    pool = INTENT_QUALIFIERS.get(intent_target, ["core", "guide", "services", "overview", "help"])
    phrases = build_seed_candidates(url, title, h1)
    fallback: list[Candidate] = []
    for idx, phrase in enumerate(phrases):
        qualifier = pool[idx % len(pool)]
        keyword = normalize_space(f"{qualifier} {phrase}") if qualifier not in phrase.split(" ") else phrase
        score, slug_overlap, h1_overlap, title_overlap, hits, _accepted, _reason = compute_candidate_score(
            keyword=keyword,
            intent_target=intent_target,
            intent_source=intent_target,
            source_type="Inferred",
            search_volume=0.0,
            slug_tokens=slug_tokens,
            title_tokens=title_tokens,
            h1_tokens=h1_tokens,
            slug_text=slug_text,
            title_text=title_text,
            h1_text=h1_text,
        )
        fallback.append(
            Candidate(
                keyword=keyword,
                qualifier=qualifier,
                seed_keyword=phrase,
                source_type="Inferred",
                source_raw="Inferred",
                source_intent=intent_target,
                search_volume="",
                search_volume_num=0.0,
                current_position=None,
                score=score,
                slug_overlap=slug_overlap,
                h1_overlap=h1_overlap,
                title_overlap=title_overlap,
                phrase_hits=hits,
                accepted=True,
                reason="fallback_topup",
                fallback=True,
            )
        )
    return fallback


def dominant_value(values: list[str], fallback: str = "") -> str:
    clean = [normalize_space(v) for v in values if normalize_space(v)]
    if not clean:
        return fallback
    counts = Counter(clean)
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[0][0]


def choose_match_type(candidate: Candidate) -> str:
    max_overlap = max(candidate.slug_overlap, candidate.h1_overlap)
    if (len(candidate.phrase_hits) >= 2 and max_overlap >= 0.35) or candidate.score >= 0.75:
        return "Exact"
    return "Partial"


def choose_action(candidate: Candidate, match_type: str) -> str:
    if match_type != "Exact":
        return "Optimize"
    if candidate.current_position is not None and candidate.current_position <= 10:
        source_norm = normalize_keyword(candidate.source_raw)
        if "gsc query" in source_norm:
            return "None"
    return "Optimize"


def build_note(candidate: Candidate, match_type: str) -> str:
    lineage = f"Lineage={candidate.qualifier}+{candidate.seed_keyword}; Source={candidate.source_type}"
    if match_type == "Exact":
        hit_txt = "/".join(candidate.phrase_hits) if candidate.phrase_hits else "URL-Title-H1 signals"
        return f"Fully aligned to page signals ({hit_txt}). {lineage}."
    return (
        f"Add '{candidate.keyword}' in Title/H1 and expand intent-matched section copy. "
        f"{lineage}."
    )


def main() -> None:
    mapping_rows = read_csv_dict(MAPPING_PATH)
    metadata_rows = read_csv_dict(METADATA_PATH)
    source_rows = read_csv_dict(SOURCE_PATH)

    target_norm_urls = [normalize_url(url) for url in TARGET_URLS]
    target_set = set(target_norm_urls)

    metadata_by_url: dict[str, dict[str, str]] = {}
    for row in metadata_rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue
        data = metadata_by_url.setdefault(
            url,
            {"title": "", "meta_desc": "", "h1": ""},
        )
        if not data["title"] and normalize_space(row.get("Title 1", "")):
            data["title"] = normalize_space(row.get("Title 1", ""))
        if not data["meta_desc"] and normalize_space(row.get("Meta Description 1", "")):
            data["meta_desc"] = normalize_space(row.get("Meta Description 1", ""))
        if not data["h1"] and normalize_space(row.get("H1-1", "")):
            data["h1"] = normalize_space(row.get("H1-1", ""))

    source_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        url = normalize_url(row.get("Address", ""))
        if not url:
            continue
        source_by_url[url].append(row)

    mapping_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in mapping_rows:
        url = normalize_url(row.get("Current URL", ""))
        if url:
            mapping_by_url[url].append(row)

    added_rows: list[dict[str, str]] = []
    qa_rows: list[dict[str, str]] = []

    for url in target_norm_urls:
        current_rows = mapping_by_url.get(url, [])
        if not current_rows:
            raise SystemExit(f"Target URL missing in mapping file: {url}")

        existing_keywords = {
            normalize_keyword(row.get("Keyword", ""))
            for row in current_rows
            if normalize_keyword(row.get("Keyword", ""))
        }
        deficit = max(0, MIN_VARIANTS - len(existing_keywords))
        if deficit == 0:
            continue

        dominant_intent = normalize_intent(
            dominant_value([row.get("Search Intent", "") for row in current_rows], fallback="Commercial")
        )
        if not dominant_intent:
            dominant_intent = "Commercial"
        dominant_cluster = dominant_value([row.get("Topic Cluster", "") for row in current_rows], fallback="Unclustered")

        meta = metadata_by_url.get(url, {"title": "", "meta_desc": "", "h1": ""})
        meta_title = meta.get("title", "")
        meta_desc = meta.get("meta_desc", "")
        h1 = meta.get("h1", "")

        slug_tokens = set(filter_tokens(tokenize(urlsplit(url).path.replace("/", " ").replace("-", " "))))
        title_tokens = set(filter_tokens(tokenize(meta_title)))
        h1_tokens = set(filter_tokens(tokenize(h1)))

        slug_text = normalize_space(" ".join(slug_tokens))
        title_text = normalize_text(meta_title)
        h1_text = normalize_text(h1)

        source_candidates = build_source_candidates(
            source_by_url.get(url, []),
            intent_target=dominant_intent,
            slug_tokens=slug_tokens,
            title_tokens=title_tokens,
            h1_tokens=h1_tokens,
            slug_text=slug_text,
            title_text=title_text,
            h1_text=h1_text,
        )
        inferred_candidates = build_inferred_candidates(
            url=url,
            title=meta_title,
            h1=h1,
            intent_target=dominant_intent,
            slug_tokens=slug_tokens,
            title_tokens=title_tokens,
            h1_tokens=h1_tokens,
            slug_text=slug_text,
            title_text=title_text,
            h1_text=h1_text,
        )
        fallback = fallback_candidates(
            url=url,
            title=meta_title,
            h1=h1,
            intent_target=dominant_intent,
            slug_tokens=slug_tokens,
            title_tokens=title_tokens,
            h1_tokens=h1_tokens,
            slug_text=slug_text,
            title_text=title_text,
            h1_text=h1_text,
        )

        all_candidates = source_candidates + inferred_candidates + fallback
        all_candidates.sort(
            key=lambda cand: (
                source_priority_value(cand.source_type, cand.source_raw),
                0 if cand.accepted else 1,
                0 if not cand.fallback else 1,
                -cand.score,
                -len(cand.phrase_hits),
                -cand.search_volume_num,
                normalize_keyword(cand.keyword),
            )
        )

        selected: list[Candidate] = []
        used_qualifiers: set[str] = set()
        seen_keywords = set(existing_keywords)

        for cand in all_candidates:
            cand_key = normalize_keyword(cand.keyword)
            if not cand_key or cand_key in seen_keywords:
                continue
            qualifier_norm = normalize_keyword(cand.qualifier)
            if not qualifier_norm:
                qualifier_norm = f"q{len(used_qualifiers) + 1}"
                cand.qualifier = qualifier_norm
            if qualifier_norm in used_qualifiers:
                continue
            if not cand.accepted and not cand.fallback:
                continue
            selected.append(cand)
            seen_keywords.add(cand_key)
            used_qualifiers.add(qualifier_norm)
            if len(selected) == deficit:
                break

        if len(selected) < deficit:
            raise SystemExit(f"Could not satisfy {deficit} new variants for {url}. Got {len(selected)}.")

        for cand in selected:
            match_type = choose_match_type(cand)
            action = choose_action(cand, match_type)
            note = build_note(cand, match_type)
            new_row = {
                "Keyword": cand.keyword,
                "Search Volume": cand.search_volume,
                "Search Intent": dominant_intent,
                "Topic Cluster": dominant_cluster,
                "Current URL": display_url(url),
                "Meta Title": meta_title,
                "Meta Description": meta_desc,
                "H1": h1,
                "Match Type": match_type,
                "Suggested Action": action,
                "Notes": note,
            }
            added_rows.append(new_row)
            qa_rows.append(
                {
                    "URL": display_url(url),
                    "Qualifier": cand.qualifier,
                    "Seed Keyword": cand.seed_keyword,
                    "Keyword": cand.keyword,
                    "Source Type": cand.source_type,
                    "Score": f"{cand.score:.4f}",
                    "Match Type": match_type,
                    "Suggested Action": action,
                    "Hit Signals": "|".join(cand.phrase_hits) if cand.phrase_hits else "",
                    "Reason": cand.reason,
                }
            )

    if not added_rows:
        print("No rows needed. All target URLs already have >=5 keyword variants.")
    else:
        with MAPPING_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=MAPPING_FIELDS)
            writer.writeheader()
            for row in mapping_rows:
                writer.writerow({field: row.get(field, "") for field in MAPPING_FIELDS})
            for row in added_rows:
                writer.writerow({field: row.get(field, "") for field in MAPPING_FIELDS})

    qa_fields = [
        "URL",
        "Qualifier",
        "Seed Keyword",
        "Keyword",
        "Source Type",
        "Score",
        "Match Type",
        "Suggested Action",
        "Hit Signals",
        "Reason",
    ]
    with OUT_QA_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=qa_fields)
        writer.writeheader()
        writer.writerows(qa_rows)

    final_rows = read_csv_dict(MAPPING_PATH)
    final_by_url: dict[str, set[str]] = defaultdict(set)
    for row in final_rows:
        url = normalize_url(row.get("Current URL", ""))
        kw = normalize_keyword(row.get("Keyword", ""))
        if url in target_set and kw:
            final_by_url[url].add(kw)

    print(f"Added rows: {len(added_rows)}")
    for url in target_norm_urls:
        print(f"{display_url(url)} -> {len(final_by_url[url])} variants")
    print(f"Wrote QA: {OUT_QA_PATH}")


if __name__ == "__main__":
    main()

