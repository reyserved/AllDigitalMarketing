from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


def _join_paths(paths: Iterable[Path]) -> str:
    return ", ".join(str(p) for p in paths)


def build_prompt_template(
    l3m_files: List[Path],
    mom_files: List[Path],
    yoy_files: List[Path],
    metadata_file: Path,
    custom_bucket_names: List[str],
    output_dir: Path,
) -> str:
    custom = ", ".join(custom_bucket_names) if custom_bucket_names else "None"

    return f"""TASK: Benchmark SEO page performance by bucket.

INPUT FILES
- L3M: {_join_paths(l3m_files)}
- MoM: {_join_paths(mom_files)}
- YoY: {_join_paths(yoy_files)}
- Metadata/H1: {metadata_file}

BUCKETS
- Default: Service, Location, Supporting
- Custom: {custom}
- Unclassified handling: include and flag QA issues

OUTPUT DIRECTORY
- {output_dir}

REQUIREMENTS
- Use weighted rollups for clicks, impressions, users, and key events.
- Report L3M, MoM, YoY insights per bucket.
- Include top positive/negative drivers with URL-level evidence.
- Include metadata/H1 opportunities and deterministic next-step tags.
- Do not fabricate missing values; if validation fails, leave metrics blank and explain in notes.
- Output CSV columns exactly:
  Bucket, URLs In Bucket, Data Coverage Notes, L3M Benchmark, MoM Benchmark, YoY Benchmark, Top Positive Drivers, Top Negative Drivers, Metadata/H1 Opportunities, Why_Recommendation, Next Steps Tags, Action Plan
"""
