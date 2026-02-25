#!/usr/bin/env python3
"""Rebuild keyword rows for 17 Omnipress core URLs in keyword research sheet."""

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

TARGET_CSV = BASE_DIR / "Omnipress _ Keyword Research 2.2026 - Omnipress _ Keyword Research (1).csv"
PAGES_MAPPING = (
    BASE_DIR.parent.parent
    / "02-audits/content/Omnipress _ Keyword Research 2.2026 - Keyword Mapping - pages.csv"
)
METADATA_CSV = (
    BASE_DIR.parent.parent
    / "02-audits/content/Benchmark Performance _ Omnipress - core-pages-metadata.csv"
)
QA_CSV = BASE_DIR / "Omnipress_Core17_Rebuild_QA.csv"

TARGET_ORDER = [
    "https://omnipress.com/training/fulfillment/5-easy-steps-to-a-successful-print-fulfillment-transition/",
    "https://omnipress.com/training/pricing/",
    "https://omnipress.com/training/training-manual-printing/",
    "https://omnipress.com/support/",
    "https://omnipress.com/newsletter-signup/",
    "https://omnipress.com/contact/",
    "https://omnipress.com/printer-quiz/",
    "https://omnipress.com/conferences/pricing/",
    "https://omnipress.com/conferences/event-services/event-services-contact-form/",
    "https://omnipress.com/conferences/event-services/",
    "https://omnipress.com/conferences/event-swag-bags/request-for-quote/",
    "https://omnipress.com/conferences/event-swag-bags/",
    "https://omnipress.com/careers/omnipress-application-form/",
    "https://omnipress.com/conferences/abstract-management/catalyst-quick-tips/",
    "https://omnipress.com/careers/",
    "https://omnipress.com/conferences/abstract-management/catalyst-features-videos/",
    "https://omnipress.com/about-us/",
]

TARGET_RULES = {
    "https://omnipress.com/training/fulfillment/5-easy-steps-to-a-successful-print-fulfillment-transition": {
        "page_type": "RESOURCE",
        "cluster": "Training Solutions",
        "subcluster": "Training Fulfillment",
        "intent": "informational",
    },
    "https://omnipress.com/training/pricing": {
        "page_type": "CONVERSION",
        "cluster": "Training Solutions",
        "subcluster": "General Product/Service",
        "intent": "",
    },
    "https://omnipress.com/training/training-manual-printing": {
        "page_type": "SERVICE",
        "cluster": "Training Solutions",
        "subcluster": "Training Manual Printing",
        "intent": "commercial",
    },
    "https://omnipress.com/support": {
        "page_type": "UTILITY",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/newsletter-signup": {
        "page_type": "UTILITY",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/contact": {
        "page_type": "UTILITY",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/printer-quiz": {
        "page_type": "UTILITY",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/conferences/pricing": {
        "page_type": "CONVERSION",
        "cluster": "Conference Solutions",
        "subcluster": "General Product/Service",
        "intent": "",
    },
    "https://omnipress.com/conferences/event-services/event-services-contact-form": {
        "page_type": "CONVERSION",
        "cluster": "Conference Solutions",
        "subcluster": "General Product/Service",
        "intent": "",
    },
    "https://omnipress.com/conferences/event-services": {
        "page_type": "SERVICE",
        "cluster": "Conference Solutions",
        "subcluster": "General Product/Service",
        "intent": "commercial",
    },
    "https://omnipress.com/conferences/event-swag-bags/request-for-quote": {
        "page_type": "CONVERSION",
        "cluster": "Conference Solutions",
        "subcluster": "General Product/Service",
        "intent": "",
    },
    "https://omnipress.com/conferences/event-swag-bags": {
        "page_type": "SERVICE",
        "cluster": "Conference Solutions",
        "subcluster": "Conference Printing",
        "intent": "commercial",
    },
    "https://omnipress.com/careers/omnipress-application-form": {
        "page_type": "CAREER",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/conferences/abstract-management/catalyst-quick-tips": {
        "page_type": "PRODUCT",
        "cluster": "Conference Solutions",
        "subcluster": "Abstract Management Education",
        "intent": "informational",
    },
    "https://omnipress.com/careers": {
        "page_type": "CAREER-HUB",
        "cluster": "Brand/Navigational",
        "subcluster": "Unmapped",
        "intent": "navigational",
    },
    "https://omnipress.com/conferences/abstract-management/catalyst-features-videos": {
        "page_type": "PRODUCT",
        "cluster": "Conference Solutions",
        "subcluster": "Abstract Management Education",
        "intent": "informational",
    },
    "https://omnipress.com/about-us": {
        "page_type": "BRAND",
        "cluster": "Brand/Navigational",
        "subcluster": "Brand Pages",
        "intent": "navigational",
    },
}

HEADER = [
    "Address",
    "Page Type",
    "Crawl Depth",
    "Title 1",
    "Meta Description 1",
    "Meta Description 1 Length",
    "Meta Description 1 Pixel Width",
    "H1-1",
    "Cluster",
    "Subcluster",
    "Qualifier",
    "Seed Keyword",
    "Keyword",
    "Intent",
    "Funnel Stage",
    "Search Volume",
    "Keyword Difficulty",
    "CPC",
    "SERP Features",
    "Source",
    "Current Position",
    "GSC Impressions",
    "GSC Clicks",
    "GSC Position",
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
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "your",
    "our",
    "you",
}

INTENT_QUALIFIERS = {
    "informational": ["guide", "tips", "how to", "checklist", "overview", "best practices", "quick", "videos"],
    "navigational": ["official", "support", "contact", "newsletter", "careers", "about", "application", "form"],
    "commercial": ["custom", "professional", "managed", "services", "solutions", "enterprise", "best"],
    "conversion": ["pricing", "quote", "request", "request for quote", "contact form", "demo", "application"],
}

INTENT_CUES = {
    "informational": {"guide", "tips", "how", "checklist", "overview", "video", "videos", "quick"},
    "navigational": {"official", "support", "contact", "newsletter", "career", "careers", "about", "application", "form"},
    "commercial": {"services", "solutions", "professional", "custom", "managed", "enterprise", "printing"},
    "conversion": {"pricing", "quote", "request", "demo", "contact form", "application", "rfq"},
}


@dataclass
class Candidate:
    keyword: str
    qualifier: str
    seed_keyword: str
    source_hint: str
    source_intent: str
    semantic_score: float
    intent_fit: int
    sv_proxy: float
    site_popularity: float
    demand_score: float
    exact_presence: int
    clarity_score: int
    origin_rank: int
    reason: str


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_text(text: str) -> str:
    return normalize_space(re.sub(r"[^a-z0-9]+", " ", (text or "").lower()))


def normalize_keyword(text: str) -> str:
    return normalize_space((text or "").lower())


def normalize_url(raw_url: str) -> str:
    raw = (raw_url or "").strip().replace("http://", "https://")
    if not raw:
        return ""
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


def display_url(norm_url: str) -> str:
    norm = normalize_url(norm_url)
    if not norm:
        return ""
    parsed = urlsplit(norm)
    path = parsed.path
    if path != "/" and not path.endswith("/"):
        path += "/"
    return f"https://{parsed.netloc}{path}"


def tokenize(text: str) -> list[str]:
    return [tok for tok in normalize_text(text).split(" ") if tok]


def filtered_tokens(text: str) -> list[str]:
    return [tok for tok in tokenize(text) if tok not in STOPWORDS]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = len(a.union(b))
    if union == 0:
        return 0.0
    return len(a.intersection(b)) / union


def safe_float(value: str) -> float:
    raw = normalize_space(value).replace(",", "")
    if not raw:
        return 0.0
    try:
        return float(raw)
    except ValueError:
        return 0.0


def derive_crawl_depth(url_norm: str) -> str:
    path = urlsplit(url_norm).path
    segments = [s for s in path.split("/") if s]
    return str(len(segments))


def infer_intent_class(target_intent: str) -> str:
    t = normalize_keyword(target_intent)
    if t:
        return t
    return "conversion"


def detect_keyword_intent(keyword: str) -> str:
    kw = normalize_text(keyword)
    if not kw:
        return "conversion"
    for intent_class, cues in INTENT_CUES.items():
        for cue in cues:
            if cue in kw:
                return intent_class
    return "commercial"


def derive_seed_keyword(keyword: str, fallback: str) -> str:
    tokens = filtered_tokens(keyword)
    if not tokens:
        return fallback
    return normalize_space(" ".join(tokens[: min(4, len(tokens))]))


def derive_qualifier(keyword: str, seed_keyword: str, default_pool: list[str]) -> str:
    kw_tokens = filtered_tokens(keyword)
    seed_tokens = set(filtered_tokens(seed_keyword))
    for token in kw_tokens:
        if token not in seed_tokens:
            return token
    if default_pool:
        return default_pool[0]
    return "core"


def exact_presence_count(keyword_norm: str, slug_text: str, title_text: str, h1_text: str) -> int:
    hits = 0
    if keyword_norm and keyword_norm in slug_text:
        hits += 1
    if keyword_norm and keyword_norm in title_text:
        hits += 1
    if keyword_norm and keyword_norm in h1_text:
        hits += 1
    return hits


def clarity_score(keyword: str) -> int:
    n = len(filtered_tokens(keyword))
    if 2 <= n <= 5:
        return 2
    if n == 1:
        return 1
    return 0


def demand_to_expansion_count(page_demand: float) -> int:
    if page_demand >= 0.75:
        return 9
    if page_demand >= 0.60:
        return 8
    if page_demand >= 0.50:
        return 7
    if page_demand >= 0.40:
        return 6
    return 4


def read_csv_dict(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{k: (v or "") for k, v in row.items()} for row in csv.DictReader(handle)]


def build_global_stats(rows: list[dict[str, str]]) -> tuple[dict[str, float], dict[str, float], float, float]:
    sv_by_kw: dict[str, float] = {}
    token_freq: Counter[str] = Counter()
    for row in rows:
        keyword = normalize_space(row.get("Keyword", ""))
        nk = normalize_keyword(keyword)
        if nk:
            sv = safe_float(row.get("Search Volume", ""))
            if sv > sv_by_kw.get(nk, 0.0):
                sv_by_kw[nk] = sv
            for token in filtered_tokens(keyword):
                token_freq[token] += 1
    max_sv = max(sv_by_kw.values()) if sv_by_kw else 1.0
    max_tf = max(token_freq.values()) if token_freq else 1.0
    tf_norm = {token: freq / max_tf for token, freq in token_freq.items()}
    return sv_by_kw, tf_norm, max_sv, max_tf


def collect_existing_source_index(rows: list[dict[str, str]]) -> dict[str, dict[str, list[str]]]:
    idx: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        u = normalize_url(row.get("Address", ""))
        k = normalize_keyword(row.get("Keyword", ""))
        if u and k:
            src = normalize_space(row.get("Source", ""))
            if src:
                idx[u][k].append(src)
    return idx


def metadata_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        u = normalize_url(row.get("Address", ""))
        if not u:
            continue
        cur = out.setdefault(u, {"title": "", "meta": "", "h1": ""})
        if not cur["title"] and normalize_space(row.get("Title 1", "")):
            cur["title"] = normalize_space(row.get("Title 1", ""))
        if not cur["meta"] and normalize_space(row.get("Meta Description 1", "")):
            cur["meta"] = normalize_space(row.get("Meta Description 1", ""))
        if not cur["h1"] and normalize_space(row.get("H1-1", "")):
            cur["h1"] = normalize_space(row.get("H1-1", ""))
    return out


def mapping_lookup(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        u = normalize_url(row.get("Current URL", ""))
        if u:
            out[u].append(row)
    return out


def source_lookup(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        u = normalize_url(row.get("Address", ""))
        if u:
            out[u].append(row)
    return out


def create_inferred_keywords(url_norm: str, title: str, h1: str, pool: list[str]) -> list[tuple[str, str, str]]:
    path = urlsplit(url_norm).path.replace("/", " ").replace("-", " ")
    seed_candidates: list[str] = []
    for text in [path, title, h1]:
        tokens = filtered_tokens(text)
        if not tokens:
            continue
        for n in [2, 3, 4]:
            if len(tokens) >= n:
                seed = normalize_space(" ".join(tokens[:n]))
                if seed and seed not in seed_candidates:
                    seed_candidates.append(seed)
    if not seed_candidates:
        fallback_tokens = filtered_tokens(path)
        if fallback_tokens:
            seed_candidates.append(normalize_space(" ".join(fallback_tokens[: min(3, len(fallback_tokens))])))

    inferred: list[tuple[str, str, str]] = []
    for seed in seed_candidates[:4]:
        for qualifier in pool:
            kw = seed if qualifier in seed.split(" ") else normalize_space(f"{qualifier} {seed}")
            inferred.append((qualifier, seed, kw))
    return inferred


def make_candidate(
    *,
    keyword: str,
    qualifier: str,
    seed_keyword: str,
    source_hint: str,
    source_intent: str,
    target_intent_class: str,
    slug_tokens: set[str],
    title_tokens: set[str],
    h1_tokens: set[str],
    slug_text: str,
    title_text: str,
    h1_text: str,
    sv_by_kw: dict[str, float],
    tf_norm: dict[str, float],
    max_sv: float,
    origin_rank: int,
    reason: str,
) -> Candidate:
    nk = normalize_keyword(keyword)
    kw_tokens = set(filtered_tokens(keyword))
    semantic_score = max(
        jaccard(kw_tokens, slug_tokens),
        jaccard(kw_tokens, title_tokens),
        jaccard(kw_tokens, h1_tokens),
    )

    cand_intent = normalize_keyword(source_intent)
    if not cand_intent:
        cand_intent = detect_keyword_intent(keyword)
    intent_fit = 1 if cand_intent == target_intent_class else 0
    if target_intent_class == "conversion":
        if normalize_keyword(source_intent) == "":
            intent_fit = 1
        elif detect_keyword_intent(keyword) == "conversion":
            intent_fit = 1

    sv_raw = sv_by_kw.get(nk, 0.0)
    sv_proxy = (sv_raw / max_sv) if max_sv > 0 else 0.0

    token_scores = [tf_norm.get(tok, 0.0) for tok in filtered_tokens(keyword)]
    site_popularity = (sum(token_scores) / len(token_scores)) if token_scores else 0.0

    demand_score = 0.45 * semantic_score + 0.25 * intent_fit + 0.20 * sv_proxy + 0.10 * site_popularity

    exact_presence = exact_presence_count(normalize_text(keyword), slug_text, title_text, h1_text)

    return Candidate(
        keyword=normalize_space(keyword),
        qualifier=normalize_space(qualifier),
        seed_keyword=normalize_space(seed_keyword),
        source_hint=source_hint,
        source_intent=normalize_space(source_intent),
        semantic_score=semantic_score,
        intent_fit=intent_fit,
        sv_proxy=sv_proxy,
        site_popularity=site_popularity,
        demand_score=demand_score,
        exact_presence=exact_presence,
        clarity_score=clarity_score(keyword),
        origin_rank=origin_rank,
        reason=reason,
    )


def resolve_primary_source(
    url_norm: str,
    primary_keyword: str,
    existing_source_index: dict[str, dict[str, list[str]]],
) -> str:
    nk = normalize_keyword(primary_keyword)
    for src in existing_source_index.get(url_norm, {}).get(nk, []):
        if "SEMrush;GSC Query" in src:
            return "SEMrush;GSC Query"
    return "SEMrush"


def non_empty_unique_qualifier(
    qualifier: str,
    used: set[str],
    pool: list[str],
    keyword: str,
) -> str:
    q = normalize_keyword(qualifier)
    if not q:
        q = derive_qualifier(keyword, keyword, pool)
    if q not in used:
        used.add(q)
        return q
    for alt in pool:
        a = normalize_keyword(alt)
        if a not in used:
            used.add(a)
            return a
    idx = 2
    while True:
        cand = f"{q}-{idx}"
        if cand not in used:
            used.add(cand)
            return cand
        idx += 1


def main() -> None:
    all_rows = read_csv_dict(TARGET_CSV)
    mapping_rows = read_csv_dict(PAGES_MAPPING)
    metadata_rows = read_csv_dict(METADATA_CSV)

    sv_by_kw, tf_norm, max_sv, _max_tf = build_global_stats(all_rows)
    existing_source_index = collect_existing_source_index(all_rows)
    source_by_url = source_lookup(all_rows)
    map_by_url = mapping_lookup(mapping_rows)
    meta_by_url = metadata_lookup(metadata_rows)

    target_norms = [normalize_url(u) for u in TARGET_ORDER]
    target_set = set(target_norms)

    for u in target_norms:
        if u not in meta_by_url:
            raise SystemExit(f"Missing metadata for target URL: {u}")

    # Preserve non-target rows as-is; replace target URLs entirely.
    preserved_rows = [row for row in all_rows if normalize_url(row.get("Address", "")) not in target_set]

    rebuilt_rows: list[dict[str, str]] = []
    qa_rows: list[dict[str, str]] = []

    for target_url in target_norms:
        rule = TARGET_RULES[target_url]
        target_intent = rule["intent"]
        target_intent_class = infer_intent_class(target_intent)
        qualifier_pool = INTENT_QUALIFIERS[target_intent_class]

        meta = meta_by_url[target_url]
        title = meta["title"]
        meta_desc = meta["meta"]
        h1 = meta["h1"]

        path_text = urlsplit(target_url).path.replace("/", " ").replace("-", " ")
        slug_tokens = set(filtered_tokens(path_text))
        title_tokens = set(filtered_tokens(title))
        h1_tokens = set(filtered_tokens(h1))
        slug_text = normalize_text(path_text)
        title_text = normalize_text(title)
        h1_text = normalize_text(h1)

        crawl_depth = ""
        existing_url_rows = source_by_url.get(target_url, [])
        depth_vals = [
            normalize_space(r.get("Crawl Depth", ""))
            for r in existing_url_rows
            if normalize_space(r.get("Crawl Depth", ""))
        ]
        if depth_vals:
            crawl_depth = Counter(depth_vals).most_common(1)[0][0]
        else:
            crawl_depth = derive_crawl_depth(target_url)

        candidate_map: dict[str, Candidate] = {}

        def register(candidate: Candidate) -> None:
            key = normalize_keyword(candidate.keyword)
            if not key:
                return
            prev = candidate_map.get(key)
            if prev is None:
                candidate_map[key] = candidate
                return
            prev_rank = (
                prev.origin_rank,
                -prev.exact_presence,
                -prev.intent_fit,
                -prev.demand_score,
                -prev.clarity_score,
                normalize_keyword(prev.keyword),
            )
            new_rank = (
                candidate.origin_rank,
                -candidate.exact_presence,
                -candidate.intent_fit,
                -candidate.demand_score,
                -candidate.clarity_score,
                normalize_keyword(candidate.keyword),
            )
            if new_rank < prev_rank:
                candidate_map[key] = candidate

        # Pool 1: existing source rows for URL.
        for row in existing_url_rows:
            keyword = normalize_space(row.get("Keyword", ""))
            if not keyword:
                continue
            seed = normalize_space(row.get("Seed Keyword", "")) or derive_seed_keyword(keyword, "")
            qual = normalize_space(row.get("Qualifier", ""))
            src = normalize_space(row.get("Source", "")) or "SEMrush"
            cand = make_candidate(
                keyword=keyword,
                qualifier=qual,
                seed_keyword=seed,
                source_hint=src,
                source_intent=row.get("Intent", ""),
                target_intent_class=target_intent_class,
                slug_tokens=slug_tokens,
                title_tokens=title_tokens,
                h1_tokens=h1_tokens,
                slug_text=slug_text,
                title_text=title_text,
                h1_text=h1_text,
                sv_by_kw=sv_by_kw,
                tf_norm=tf_norm,
                max_sv=max_sv,
                origin_rank=0,
                reason="pool1_existing",
            )
            register(cand)

        # Pool 2: pages mapping rows for URL.
        for row in map_by_url.get(target_url, []):
            keyword = normalize_space(row.get("Keyword", ""))
            if not keyword:
                continue
            seed = derive_seed_keyword(keyword, "")
            qual = derive_qualifier(keyword, seed, qualifier_pool)
            src_hint = "Expansion" if normalize_keyword(row.get("Match Type", "")) == "partial" else "SEMrush"
            cand = make_candidate(
                keyword=keyword,
                qualifier=qual,
                seed_keyword=seed,
                source_hint=src_hint,
                source_intent=row.get("Search Intent", ""),
                target_intent_class=target_intent_class,
                slug_tokens=slug_tokens,
                title_tokens=title_tokens,
                h1_tokens=h1_tokens,
                slug_text=slug_text,
                title_text=title_text,
                h1_text=h1_text,
                sv_by_kw=sv_by_kw,
                tf_norm=tf_norm,
                max_sv=max_sv,
                origin_rank=1,
                reason="pool2_pages_mapping",
            )
            register(cand)

        # Pool 3: inferred phrases from slug/title/h1.
        inferred = create_inferred_keywords(target_url, title, h1, qualifier_pool)
        for qual, seed, keyword in inferred:
            cand = make_candidate(
                keyword=keyword,
                qualifier=qual,
                seed_keyword=seed,
                source_hint="Expansion",
                source_intent=target_intent,
                target_intent_class=target_intent_class,
                slug_tokens=slug_tokens,
                title_tokens=title_tokens,
                h1_tokens=h1_tokens,
                slug_text=slug_text,
                title_text=title_text,
                h1_text=h1_text,
                sv_by_kw=sv_by_kw,
                tf_norm=tf_norm,
                max_sv=max_sv,
                origin_rank=2,
                reason="pool3_inferred",
            )
            register(cand)

        candidates = list(candidate_map.values())
        if not candidates:
            raise SystemExit(f"No candidates built for {target_url}")

        # Primary keyword selection.
        candidates.sort(
            key=lambda c: (
                -c.exact_presence,
                -c.intent_fit,
                -c.demand_score,
                -c.clarity_score,
                normalize_keyword(c.keyword),
            )
        )
        primary = candidates[0]
        page_demand = max(c.demand_score for c in candidates)
        expansion_count = demand_to_expansion_count(page_demand)

        used_keywords = {normalize_keyword(primary.keyword)}
        used_qualifiers: set[str] = set()
        expansions: list[Candidate] = []

        # Select expansion candidates from ranked list.
        exp_candidates = [c for c in candidates if normalize_keyword(c.keyword) != normalize_keyword(primary.keyword)]
        exp_candidates.sort(
            key=lambda c: (
                -c.demand_score,
                normalize_keyword(c.qualifier),
                normalize_keyword(c.keyword),
            )
        )
        for cand in exp_candidates:
            nk = normalize_keyword(cand.keyword)
            if not nk or nk in used_keywords:
                continue
            q = non_empty_unique_qualifier(cand.qualifier, used_qualifiers, qualifier_pool, cand.keyword)
            cand.qualifier = q
            expansions.append(cand)
            used_keywords.add(nk)
            if len(expansions) == expansion_count:
                break

        # If still short, generate deterministic fallback expansions.
        if len(expansions) < expansion_count:
            seed_fallback = primary.seed_keyword or derive_seed_keyword(primary.keyword, normalize_space(" ".join(filtered_tokens(path_text)[:3])))
            for qual in qualifier_pool:
                if len(expansions) >= expansion_count:
                    break
                q = non_empty_unique_qualifier(qual, used_qualifiers, qualifier_pool, primary.keyword)
                kw = seed_fallback if q in seed_fallback.split(" ") else normalize_space(f"{q} {seed_fallback}")
                nk = normalize_keyword(kw)
                if not nk or nk in used_keywords:
                    continue
                cand = make_candidate(
                    keyword=kw,
                    qualifier=q,
                    seed_keyword=seed_fallback,
                    source_hint="Expansion",
                    source_intent=target_intent,
                    target_intent_class=target_intent_class,
                    slug_tokens=slug_tokens,
                    title_tokens=title_tokens,
                    h1_tokens=h1_tokens,
                    slug_text=slug_text,
                    title_text=title_text,
                    h1_text=h1_text,
                    sv_by_kw=sv_by_kw,
                    tf_norm=tf_norm,
                    max_sv=max_sv,
                    origin_rank=3,
                    reason="fallback_generated",
                )
                expansions.append(cand)
                used_keywords.add(nk)

        if len(expansions) < expansion_count:
            raise SystemExit(f"Could not build required expansion rows for {target_url}: need {expansion_count}, got {len(expansions)}")

        primary_source = resolve_primary_source(target_url, primary.keyword, existing_source_index)

        def make_row(
            *,
            row_type: str,
            candidate: Candidate,
            source_value: str,
            qualifier_value: str,
        ) -> dict[str, str]:
            return {
                "Address": display_url(target_url),
                "Page Type": rule["page_type"],
                "Crawl Depth": crawl_depth,
                "Title 1": title,
                "Meta Description 1": meta_desc,
                "Meta Description 1 Length": "",
                "Meta Description 1 Pixel Width": "",
                "H1-1": h1,
                "Cluster": rule["cluster"],
                "Subcluster": rule["subcluster"],
                "Qualifier": qualifier_value,
                "Seed Keyword": candidate.seed_keyword,
                "Keyword": candidate.keyword,
                "Intent": rule["intent"],
                "Funnel Stage": "",
                "Search Volume": "",
                "Keyword Difficulty": "",
                "CPC": "",
                "SERP Features": "",
                "Source": source_value,
                "Current Position": "",
                "GSC Impressions": "",
                "GSC Clicks": "",
                "GSC Position": "",
                "Notes": "",
            }

        # Primary row (qualifier blank by default in this sheet style).
        primary_row = make_row(
            row_type="Primary",
            candidate=primary,
            source_value=primary_source,
            qualifier_value="",
        )
        rebuilt_rows.append(primary_row)
        qa_rows.append(
            {
                "URL": display_url(target_url),
                "Row Type": "Primary",
                "Qualifier": "",
                "Seed Keyword": primary.seed_keyword,
                "Keyword": primary.keyword,
                "Source": primary_source,
                "Demand Score": f"{primary.demand_score:.4f}",
                "Semantic Score": f"{primary.semantic_score:.4f}",
                "Intent Fit": str(primary.intent_fit),
                "SV Proxy": f"{primary.sv_proxy:.4f}",
                "Category Tuple": f"{rule['page_type']}|{rule['cluster']}|{rule['subcluster']}|{rule['intent']}",
                "Reason": primary.reason,
            }
        )

        # Expansion rows.
        for cand in expansions:
            row = make_row(
                row_type="Expansion",
                candidate=cand,
                source_value="Expansion",
                qualifier_value=cand.qualifier,
            )
            rebuilt_rows.append(row)
            qa_rows.append(
                {
                    "URL": display_url(target_url),
                    "Row Type": "Expansion",
                    "Qualifier": cand.qualifier,
                    "Seed Keyword": cand.seed_keyword,
                    "Keyword": cand.keyword,
                    "Source": "Expansion",
                    "Demand Score": f"{cand.demand_score:.4f}",
                    "Semantic Score": f"{cand.semantic_score:.4f}",
                    "Intent Fit": str(cand.intent_fit),
                    "SV Proxy": f"{cand.sv_proxy:.4f}",
                    "Category Tuple": f"{rule['page_type']}|{rule['cluster']}|{rule['subcluster']}|{rule['intent']}",
                    "Reason": cand.reason,
                }
            )

    output_rows = preserved_rows + rebuilt_rows

    with TARGET_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({field: row.get(field, "") for field in HEADER})

    qa_fields = [
        "URL",
        "Row Type",
        "Qualifier",
        "Seed Keyword",
        "Keyword",
        "Source",
        "Demand Score",
        "Semantic Score",
        "Intent Fit",
        "SV Proxy",
        "Category Tuple",
        "Reason",
    ]
    with QA_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=qa_fields)
        writer.writeheader()
        writer.writerows(qa_rows)

    # Summary output for quick validation in terminal.
    counts = Counter()
    for row in rebuilt_rows:
        counts[normalize_url(row["Address"])] += 1
    print(f"Preserved rows: {len(preserved_rows)}")
    print(f"Rebuilt rows: {len(rebuilt_rows)}")
    print(f"Final rows: {len(output_rows)}")
    for url in target_norms:
        print(f"{display_url(url)} -> {counts[url]} rows")
    print(f"QA rows: {len(qa_rows)} -> {QA_CSV}")


if __name__ == "__main__":
    main()
