from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from core.benchmark import run_benchmark
from core.classify import classify_urls, parse_custom_rules
from core.schemas import RunConfig


def _write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def _l3m_headers() -> list[str]:
    return [
        "URL",
        "L3M Clicks",
        "Prev 3M Clicks",
        "L3M Impressions",
        "Prev 3M Impressions",
        "L3M New Users",
        "Prev 3M New Users",
        "L3M Key Events",
        "Prev 3M Key Events",
    ]


def _mom_headers() -> list[str]:
    return [
        "URL",
        "L1M Clicks",
        "P1M  Clicks",
        "L1M Impressions",
        "P1M Impressions",
        "L1M New Users",
        "Prev 1M New Users",
        "L1M Key Events",
        "P1M Key Events",
    ]


def _yoy_headers() -> list[str]:
    return [
        "URL",
        "L3M Clicks",
        "L3M LY Clicks",
        "L3M Impressions",
        "L3M LY Impressions",
        "L3M New Users",
        "L3M_LY New Users",
        "L3M Key Events",
        "L3M_LY Key Events",
    ]


def test_parse_custom_rules() -> None:
    rules = parse_custom_rules(
        "Blog: url_contains=/blog/,/insights/; title_contains=blog,guide; exclude=/tag/"
    )
    assert len(rules) == 1
    assert rules[0].name == "Blog"
    assert rules[0].url_contains == ["/blog/", "/insights/"]
    assert rules[0].title_contains == ["blog", "guide"]
    assert rules[0].exclude == ["/tag/"]


def test_classify_keeps_provided_type_on_conflict() -> None:
    metadata = pd.DataFrame(
        [
            {
                "URL": "https://example.com/locations/chicago/",
                "Type": "Supporting",
                "Title 1": "Chicago Office | Example",
                "Meta Description 1": "Find our Chicago office",
                "H1-1": "Chicago Office",
            }
        ]
    )
    qa_rows = []
    final_map, inferred_map, _ = classify_urls(
        all_urls=["https://example.com/locations/chicago/"],
        metadata_df=metadata,
        custom_rules=[],
        qa_rows=qa_rows,
    )

    assert inferred_map["https://example.com/locations/chicago/"] == "Location"
    assert final_map["https://example.com/locations/chicago/"] == "Supporting"
    assert any(row["issue_type"] == "type_conflict" for row in qa_rows)


def test_validation_blocked_outputs_blank_metrics(tmp_path: Path) -> None:
    input_root = tmp_path / "in"

    # Service files intentionally mismatch URL sets between windows.
    _write_csv(
        input_root / "l3m-service.csv",
        _l3m_headers(),
        [
            ["https://example.com/service/a", "10", "8", "1000", "900", "20", "18", "2", "1"],
            ["https://example.com/service/b", "6", "5", "500", "450", "10", "8", "1", "1"],
        ],
    )
    _write_csv(
        input_root / "mom-service.csv",
        _mom_headers(),
        [["https://example.com/service/a", "4", "3", "300", "250", "8", "7", "1", "1"]],
    )
    _write_csv(
        input_root / "yoy-service.csv",
        _yoy_headers(),
        [
            ["https://example.com/service/a", "10", "9", "1000", "800", "20", "17", "2", "1"],
            ["https://example.com/service/b", "6", "5", "500", "420", "10", "9", "1", "1"],
        ],
    )

    # Location/supporting files are present with valid headers but no rows.
    _write_csv(input_root / "l3m-location.csv", _l3m_headers(), [])
    _write_csv(input_root / "mom-location.csv", _mom_headers(), [])
    _write_csv(input_root / "yoy-location.csv", _yoy_headers(), [])
    _write_csv(input_root / "l3m-supporting.csv", _l3m_headers(), [])
    _write_csv(input_root / "mom-supporting.csv", _mom_headers(), [])
    _write_csv(input_root / "yoy-supporting.csv", _yoy_headers(), [])

    metadata_headers = ["URL", "Type", "Title 1", "Meta Description 1", "H1-1"]
    _write_csv(
        input_root / "metadata.csv",
        metadata_headers,
        [
            ["https://example.com/service/a", "Service", "A", "A", "A"],
            ["https://example.com/service/b", "Service", "B", "B", "B"],
        ],
    )

    config = RunConfig(
        input_paths={
            "l3m_service": input_root / "l3m-service.csv",
            "l3m_location": input_root / "l3m-location.csv",
            "l3m_supporting": input_root / "l3m-supporting.csv",
            "mom_service": input_root / "mom-service.csv",
            "mom_location": input_root / "mom-location.csv",
            "mom_supporting": input_root / "mom-supporting.csv",
            "yoy_service": input_root / "yoy-service.csv",
            "yoy_location": input_root / "yoy-location.csv",
            "yoy_supporting": input_root / "yoy-supporting.csv",
        },
        metadata_path=input_root / "metadata.csv",
        custom_rules_text="",
        output_root=tmp_path / "out",
    )

    result = run_benchmark(config)
    analysis = pd.read_csv(result.analysis_csv, dtype=str, keep_default_na=False)

    assert result.validation_blocked is True
    assert analysis.shape[0] >= 3
    assert analysis["L3M Benchmark"].eq("").all()
    assert analysis["Data Coverage Notes"].str.contains("Validation failed", na=False).any()
