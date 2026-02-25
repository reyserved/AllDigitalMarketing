from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

DEFAULT_BUCKETS = ["Service", "Location", "Supporting"]
ALLOWED_TAGS = [
    "Fundamentals",
    "Content Refresh",
    "Technical Assessment",
    "Internal Linking",
]

OUTPUT_COLUMNS = [
    "Bucket",
    "URLs In Bucket",
    "Data Coverage Notes",
    "L3M Benchmark",
    "MoM Benchmark",
    "YoY Benchmark",
    "Top Positive Drivers",
    "Top Negative Drivers",
    "Metadata/H1 Opportunities",
    "Why_Recommendation",
    "Next Steps Tags",
    "Action Plan",
]

QA_COLUMNS = [
    "severity",
    "issue_type",
    "bucket",
    "url",
    "source_file",
    "field",
    "detected_value",
    "expected_rule",
    "message",
    "suggested_fix",
]

WINDOW_TO_FILE_KEYS = {
    "l3m": ["l3m_service", "l3m_location", "l3m_supporting"],
    "mom": ["mom_service", "mom_location", "mom_supporting"],
    "yoy": ["yoy_service", "yoy_location", "yoy_supporting"],
}

FILE_KEY_TO_BUCKET = {
    "l3m_service": "Service",
    "l3m_location": "Location",
    "l3m_supporting": "Supporting",
    "mom_service": "Service",
    "mom_location": "Location",
    "mom_supporting": "Supporting",
    "yoy_service": "Service",
    "yoy_location": "Location",
    "yoy_supporting": "Supporting",
}

REQUIRED_PERFORMANCE_COLUMNS = {
    "l3m": [
        "URL",
        "L3M Clicks",
        "Prev 3M Clicks",
        "L3M Impressions",
        "Prev 3M Impressions",
        "L3M New Users",
        "Prev 3M New Users",
        "L3M Key Events",
        "Prev 3M Key Events",
    ],
    "mom": [
        "URL",
        "L1M Clicks",
        "P1M  Clicks",
        "L1M Impressions",
        "P1M Impressions",
        "L1M New Users",
        "Prev 1M New Users",
        "L1M Key Events",
        "P1M Key Events",
    ],
    "yoy": [
        "URL",
        "L3M Clicks",
        "L3M LY Clicks",
        "L3M Impressions",
        "L3M LY Impressions",
        "L3M New Users",
        "L3M_LY New Users",
        "L3M Key Events",
        "L3M_LY Key Events",
    ],
}

REQUIRED_METADATA_COLUMNS = [
    "URL",
    "Type",
    "Title 1",
    "Meta Description 1",
    "H1-1",
]

L3M_METRIC_MAP = {
    "cur_clicks": "L3M Clicks",
    "prev_clicks": "Prev 3M Clicks",
    "cur_impr": "L3M Impressions",
    "prev_impr": "Prev 3M Impressions",
    "cur_users": "L3M New Users",
    "prev_users": "Prev 3M New Users",
    "cur_events": "L3M Key Events",
    "prev_events": "Prev 3M Key Events",
}

MOM_METRIC_MAP = {
    "cur_clicks": "L1M Clicks",
    "prev_clicks": "P1M  Clicks",
    "cur_impr": "L1M Impressions",
    "prev_impr": "P1M Impressions",
    "cur_users": "L1M New Users",
    "prev_users": "Prev 1M New Users",
    "cur_events": "L1M Key Events",
    "prev_events": "P1M Key Events",
}

YOY_METRIC_MAP = {
    "cur_clicks": "L3M Clicks",
    "prev_clicks": "L3M LY Clicks",
    "cur_impr": "L3M Impressions",
    "prev_impr": "L3M LY Impressions",
    "cur_users": "L3M New Users",
    "prev_users": "L3M_LY New Users",
    "cur_events": "L3M Key Events",
    "prev_events": "L3M_LY Key Events",
}


@dataclass
class CustomBucketRule:
    name: str
    url_contains: List[str] = field(default_factory=list)
    title_contains: List[str] = field(default_factory=list)
    meta_contains: List[str] = field(default_factory=list)
    h1_contains: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)


@dataclass
class RunConfig:
    input_paths: Dict[str, Path]
    metadata_path: Path
    custom_rules_text: str
    output_root: Path


@dataclass
class RunResult:
    success: bool
    output_dir: Path
    analysis_csv: Path
    qa_csv: Path
    qa_summary_txt: Path
    prompt_text: str
    qa_issue_count: int
    qa_error_count: int
    validation_blocked: bool
    bucket_order: List[str]
