from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Set, Tuple

import pandas as pd

from .schemas import (
    FILE_KEY_TO_BUCKET,
    REQUIRED_METADATA_COLUMNS,
    REQUIRED_PERFORMANCE_COLUMNS,
)


BLOCKING_ISSUE_TYPES = {
    "missing_required_column",
    "url_set_mismatch",
    "metadata_url_mismatch",
}


def make_issue(
    severity: str,
    issue_type: str,
    bucket: str,
    url: str,
    source_file: str,
    field: str,
    detected_value: str,
    expected_rule: str,
    message: str,
    suggested_fix: str,
) -> Dict[str, str]:
    return {
        "severity": severity,
        "issue_type": issue_type,
        "bucket": bucket,
        "url": url,
        "source_file": source_file,
        "field": field,
        "detected_value": detected_value,
        "expected_rule": expected_rule,
        "message": message,
        "suggested_fix": suggested_fix,
    }


def validate_required_columns(
    performance_frames: Dict[str, pd.DataFrame],
    metadata_df: pd.DataFrame,
    qa_rows: List[Dict[str, str]],
) -> None:
    for file_key, df in performance_frames.items():
        window = file_key.split("_", 1)[0]
        required = REQUIRED_PERFORMANCE_COLUMNS[window]
        missing = [col for col in required if col not in df.columns]
        for col in missing:
            qa_rows.append(
                make_issue(
                    severity="error",
                    issue_type="missing_required_column",
                    bucket=FILE_KEY_TO_BUCKET.get(file_key, ""),
                    url="",
                    source_file=file_key,
                    field=col,
                    detected_value="missing",
                    expected_rule="Column must exist",
                    message=f"Required column '{col}' is missing from {file_key}.",
                    suggested_fix="Add the missing column with expected naming before rerunning.",
                )
            )

    missing_meta = [col for col in REQUIRED_METADATA_COLUMNS if col not in metadata_df.columns]
    for col in missing_meta:
        qa_rows.append(
            make_issue(
                severity="error",
                issue_type="missing_required_column",
                bucket="",
                url="",
                source_file="metadata",
                field=col,
                detected_value="missing",
                expected_rule="Column must exist",
                message=f"Required metadata column '{col}' is missing.",
                suggested_fix="Ensure metadata CSV includes URL, Type, Title 1, Meta Description 1, and H1-1.",
            )
        )


def validate_duplicate_urls(
    frames: Dict[str, pd.DataFrame],
    metadata_df: pd.DataFrame,
    qa_rows: List[Dict[str, str]],
) -> None:
    for key, df in frames.items():
        if "URL" not in df.columns:
            continue
        dupes = df[df["URL"].duplicated(keep=False)]["URL"].dropna().astype(str).unique().tolist()
        for url in dupes:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="duplicate_url",
                    bucket=FILE_KEY_TO_BUCKET.get(key, ""),
                    url=url,
                    source_file=key,
                    field="URL",
                    detected_value="duplicate",
                    expected_rule="Each URL should appear once per file",
                    message=f"Duplicate URL found in {key}: {url}",
                    suggested_fix="Deduplicate URL rows before rerunning.",
                )
            )

    if "URL" in metadata_df.columns:
        dupes = (
            metadata_df[metadata_df["URL"].duplicated(keep=False)]["URL"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        for url in dupes:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="duplicate_url",
                    bucket="",
                    url=url,
                    source_file="metadata",
                    field="URL",
                    detected_value="duplicate",
                    expected_rule="Each URL should appear once in metadata",
                    message=f"Duplicate URL found in metadata: {url}",
                    suggested_fix="Deduplicate metadata URL rows before rerunning.",
                )
            )


def _url_set(df: pd.DataFrame) -> Set[str]:
    if "URL" not in df.columns:
        return set()
    return {str(u).strip() for u in df["URL"].astype(str).tolist() if str(u).strip()}


def validate_url_parity(
    performance_frames: Dict[str, pd.DataFrame],
    qa_rows: List[Dict[str, str]],
) -> Tuple[Set[str], Set[str], Set[str]]:
    service_keys = ["l3m_service", "mom_service", "yoy_service"]
    location_keys = ["l3m_location", "mom_location", "yoy_location"]
    supporting_keys = ["l3m_supporting", "mom_supporting", "yoy_supporting"]

    for bucket_name, keys in (
        ("Service", service_keys),
        ("Location", location_keys),
        ("Supporting", supporting_keys),
    ):
        sets = [_url_set(performance_frames[k]) for k in keys if k in performance_frames]
        if len(sets) == 3 and not (sets[0] == sets[1] == sets[2]):
            qa_rows.append(
                make_issue(
                    severity="error",
                    issue_type="url_set_mismatch",
                    bucket=bucket_name,
                    url="",
                    source_file=",".join(keys),
                    field="URL",
                    detected_value="URL sets differ across L3M/MoM/YoY",
                    expected_rule="All three windows must contain the same URL set per bucket",
                    message=f"{bucket_name} URL sets are not aligned across windows.",
                    suggested_fix="Reconcile URL lists across the three files for this bucket.",
                )
            )

    l3m_union = set()
    mom_union = set()
    yoy_union = set()

    for key, df in performance_frames.items():
        if key.startswith("l3m_"):
            l3m_union |= _url_set(df)
        elif key.startswith("mom_"):
            mom_union |= _url_set(df)
        elif key.startswith("yoy_"):
            yoy_union |= _url_set(df)

    if not (l3m_union == mom_union == yoy_union):
        qa_rows.append(
            make_issue(
                severity="error",
                issue_type="url_set_mismatch",
                bucket="",
                url="",
                source_file="all_performance_files",
                field="URL",
                detected_value=f"L3M={len(l3m_union)}, MoM={len(mom_union)}, YoY={len(yoy_union)}",
                expected_rule="Window URL unions must match",
                message="URL union mismatch across L3M/MoM/YoY windows.",
                suggested_fix="Ensure all windows include the same page universe.",
            )
        )

    return l3m_union, mom_union, yoy_union


def validate_metadata_union(
    window_union: Set[str],
    metadata_df: pd.DataFrame,
    qa_rows: List[Dict[str, str]],
) -> None:
    metadata_urls = _url_set(metadata_df)
    only_window = sorted(window_union - metadata_urls)
    only_meta = sorted(metadata_urls - window_union)

    if only_window or only_meta:
        qa_rows.append(
            make_issue(
                severity="error",
                issue_type="metadata_url_mismatch",
                bucket="",
                url="",
                source_file="metadata",
                field="URL",
                detected_value=f"window_only={len(only_window)}, metadata_only={len(only_meta)}",
                expected_rule="Metadata URL set must match benchmark URL set",
                message="Metadata URL set does not fully match performance URL set.",
                suggested_fix="Add missing URLs to metadata or remove non-matching URLs from source datasets.",
            )
        )

        for url in only_window[:25]:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="metadata_missing_url",
                    bucket="",
                    url=url,
                    source_file="metadata",
                    field="URL",
                    detected_value="missing_in_metadata",
                    expected_rule="URL exists in metadata",
                    message="URL exists in performance data but not in metadata.",
                    suggested_fix="Add URL row to metadata export.",
                )
            )

        for url in only_meta[:25]:
            qa_rows.append(
                make_issue(
                    severity="warning",
                    issue_type="orphan_metadata_url",
                    bucket="",
                    url=url,
                    source_file="metadata",
                    field="URL",
                    detected_value="missing_in_performance",
                    expected_rule="URL exists in performance data",
                    message="URL exists in metadata but not in performance windows.",
                    suggested_fix="Verify whether URL should be in benchmark source files.",
                )
            )


def has_blocking_issues(qa_rows: List[Dict[str, str]]) -> bool:
    return any(row["issue_type"] in BLOCKING_ISSUE_TYPES for row in qa_rows)


def validation_message(qa_rows: List[Dict[str, str]]) -> str:
    blockers = [row for row in qa_rows if row["issue_type"] in BLOCKING_ISSUE_TYPES]
    if not blockers:
        return "Validation passed."
    unique = sorted({f"{row['issue_type']}: {row['message']}" for row in blockers})
    return "Validation failed; metrics intentionally blank. " + " | ".join(unique)
