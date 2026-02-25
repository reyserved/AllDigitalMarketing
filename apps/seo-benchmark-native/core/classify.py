from __future__ import annotations

import re
from dataclasses import asdict
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd

from .schemas import CustomBucketRule, DEFAULT_BUCKETS
from .validate import make_issue

LOCATION_TERMS = {
    "location",
    "locations",
    "branch",
    "office",
    "near me",
    "city",
    "county",
    "wi",
    "il",
    "ca",
    "fl",
    "ny",
    "tx",
    "loan office",
}

SUPPORTING_TERMS = {
    "about",
    "resource",
    "resources",
    "careers",
    "history",
    "community",
    "charitable",
    "calculator",
    "calculators",
    "contact",
    "learn",
    "demo",
    "faq",
    "guides",
}

SERVICE_TERMS = {
    "service",
    "services",
    "banking",
    "lending",
    "loan",
    "checking",
    "savings",
    "credit card",
    "mortgage",
    "cash management",
    "commercial",
    "business",
    "personal",
    "practice area",
}


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _split_terms(raw: str) -> List[str]:
    if not raw:
        return []
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


def parse_custom_rules(rules_text: str, qa_rows: Optional[List[Dict[str, str]]] = None) -> List[CustomBucketRule]:
    rules: List[CustomBucketRule] = []
    for idx, line in enumerate((rules_text or "").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if ":" not in stripped:
            if qa_rows is not None:
                qa_rows.append(
                    make_issue(
                        severity="warning",
                        issue_type="invalid_custom_rule",
                        bucket="",
                        url="",
                        source_file="custom_rules",
                        field=f"line_{idx}",
                        detected_value=stripped,
                        expected_rule="BucketName: key=value; key=value",
                        message="Skipping malformed custom rule (missing ':').",
                        suggested_fix="Use format: BucketName: url_contains=a,b; title_contains=c",
                    )
                )
            continue

        bucket, body = stripped.split(":", 1)
        bucket = bucket.strip()
        params = {
            "url_contains": [],
            "title_contains": [],
            "meta_contains": [],
            "h1_contains": [],
            "exclude": [],
        }

        for chunk in [c.strip() for c in body.split(";") if c.strip()]:
            if "=" not in chunk:
                continue
            key, value = chunk.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key in params:
                params[key] = _split_terms(value)

        if not bucket:
            continue

        rules.append(
            CustomBucketRule(
                name=bucket,
                url_contains=params["url_contains"],
                title_contains=params["title_contains"],
                meta_contains=params["meta_contains"],
                h1_contains=params["h1_contains"],
                exclude=params["exclude"],
            )
        )

    return rules


def _hits_any(text: str, terms: Sequence[str]) -> int:
    txt = _clean_text(text)
    return sum(1 for term in terms if term in txt)


def _custom_match(
    url: str,
    title: str,
    meta: str,
    h1: str,
    rule: CustomBucketRule,
) -> bool:
    combined = " | ".join([url, title, meta, h1]).lower()
    if any(ex in combined for ex in rule.exclude):
        return False

    checks = []
    if rule.url_contains:
        checks.append(_hits_any(url, rule.url_contains) > 0)
    if rule.title_contains:
        checks.append(_hits_any(title, rule.title_contains) > 0)
    if rule.meta_contains:
        checks.append(_hits_any(meta, rule.meta_contains) > 0)
    if rule.h1_contains:
        checks.append(_hits_any(h1, rule.h1_contains) > 0)

    if not checks:
        return False

    return all(checks)


def infer_bucket(
    url: str,
    title: str,
    meta: str,
    h1: str,
    custom_rules: Sequence[CustomBucketRule],
) -> str:
    # Custom rules outrank built-in inference.
    for rule in custom_rules:
        if _custom_match(url, title, meta, h1, rule):
            return rule.name

    url_txt = _clean_text(url)
    title_txt = _clean_text(title)
    meta_txt = _clean_text(meta)
    h1_txt = _clean_text(h1)
    combined = " | ".join([url_txt, title_txt, meta_txt, h1_txt])

    location_score = _hits_any(combined, LOCATION_TERMS)
    supporting_score = _hits_any(combined, SUPPORTING_TERMS)
    service_score = _hits_any(combined, SERVICE_TERMS)

    if "/locations/" in url_txt or "/branch/" in url_txt:
        location_score += 4
    if "/about-us/" in url_txt or "/resources/" in url_txt or "calculator" in url_txt:
        supporting_score += 3

    if location_score == 0 and supporting_score == 0 and service_score == 0:
        return "Unclassified"

    max_score = max(location_score, supporting_score, service_score)
    candidates = []
    if location_score == max_score:
        candidates.append("Location")
    if supporting_score == max_score:
        candidates.append("Supporting")
    if service_score == max_score:
        candidates.append("Service")

    # Deterministic tie-break order
    for bucket in ["Location", "Service", "Supporting"]:
        if bucket in candidates:
            return bucket

    return "Unclassified"


def classify_urls(
    all_urls: Sequence[str],
    metadata_df: pd.DataFrame,
    custom_rules: Sequence[CustomBucketRule],
    qa_rows: List[Dict[str, str]],
) -> Tuple[Dict[str, str], Dict[str, str], List[str]]:
    meta_lookup = {}
    if "URL" in metadata_df.columns:
        for _, row in metadata_df.iterrows():
            url = str(row.get("URL", "")).strip()
            if url and url not in meta_lookup:
                meta_lookup[url] = row

    final_map: Dict[str, str] = {}
    inferred_map: Dict[str, str] = {}

    dynamic_buckets: List[str] = []

    for url in sorted(set(all_urls)):
        row = meta_lookup.get(url)
        title = str(row.get("Title 1", "")) if row is not None else ""
        meta = str(row.get("Meta Description 1", "")) if row is not None else ""
        h1 = str(row.get("H1-1", "")) if row is not None else ""
        provided = str(row.get("Type", "")).strip() if row is not None else ""

        inferred = infer_bucket(url=url, title=title, meta=meta, h1=h1, custom_rules=custom_rules)
        inferred_map[url] = inferred

        if provided:
            final_type = provided
            if provided != inferred:
                qa_rows.append(
                    make_issue(
                        severity="warning",
                        issue_type="type_conflict",
                        bucket=provided,
                        url=url,
                        source_file="metadata",
                        field="Type",
                        detected_value=provided,
                        expected_rule=f"Inferred type is '{inferred}'",
                        message="Provided Type kept; inferred type differs.",
                        suggested_fix="Review URL intent and update Type if desired.",
                    )
                )
        else:
            final_type = inferred
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="missing_type_filled",
                    bucket=final_type,
                    url=url,
                    source_file="metadata",
                    field="Type",
                    detected_value="blank",
                    expected_rule=f"Filled from inference as '{final_type}'",
                    message="Type was blank and has been inferred deterministically.",
                    suggested_fix="Populate Type explicitly in metadata if needed.",
                )
            )

        if not final_type:
            final_type = "Unclassified"

        if final_type == "Unclassified":
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="unclassified_url",
                    bucket="Unclassified",
                    url=url,
                    source_file="metadata",
                    field="Type",
                    detected_value="No strong rule match",
                    expected_rule="URL maps to known bucket",
                    message="URL fell through all custom and built-in rules.",
                    suggested_fix="Add a custom bucket rule or adjust metadata Type.",
                )
            )

        if final_type not in DEFAULT_BUCKETS and final_type not in dynamic_buckets and final_type != "Unclassified":
            dynamic_buckets.append(final_type)

        final_map[url] = final_type

    return final_map, inferred_map, dynamic_buckets
