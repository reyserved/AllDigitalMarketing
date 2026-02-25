from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .schemas import OUTPUT_COLUMNS, QA_COLUMNS


def build_blank_bucket_row(bucket: str, url_count: int, note: str) -> Dict[str, str]:
    row = {col: "" for col in OUTPUT_COLUMNS}
    row["Bucket"] = bucket
    row["URLs In Bucket"] = str(url_count)
    row["Data Coverage Notes"] = note
    return row


def analysis_dataframe(rows: List[Dict[str, str]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    df = pd.DataFrame(rows)
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[OUTPUT_COLUMNS]


def qa_dataframe(rows: List[Dict[str, str]]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=QA_COLUMNS)
    df = pd.DataFrame(rows)
    for col in QA_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[QA_COLUMNS]


def build_qa_summary(qa_df: pd.DataFrame, validation_blocked: bool, output_dir: Path) -> str:
    severity_counts = Counter(qa_df["severity"].tolist()) if not qa_df.empty else Counter()
    issue_counts = Counter(qa_df["issue_type"].tolist()) if not qa_df.empty else Counter()

    lines = []
    lines.append("SEO Benchmark QA Summary")
    lines.append(f"Output directory: {output_dir}")
    lines.append(f"Validation blocked metrics: {'yes' if validation_blocked else 'no'}")
    lines.append(f"Total QA issues: {int(qa_df.shape[0])}")
    lines.append(f"Errors: {severity_counts.get('error', 0)}")
    lines.append(f"Warnings: {severity_counts.get('warning', 0)}")

    if issue_counts:
        lines.append("Issue type counts:")
        for issue, count in sorted(issue_counts.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {issue}: {count}")

    if qa_df.empty:
        lines.append("No QA issues detected.")

    return "\n".join(lines) + "\n"
