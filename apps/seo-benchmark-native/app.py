from __future__ import annotations

import html
from pathlib import Path
from typing import Dict

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from core.benchmark import run_benchmark
from core.schemas import RunConfig

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = WORKSPACE_ROOT / "output" / "spreadsheet" / "seo-benchmark"

DEFAULT_INPUTS = {
    "l3m_service": "01-clients/l3m/L3M-services.csv",
    "l3m_location": "01-clients/l3m/L3M-location.csv",
    "l3m_supporting": "01-clients/l3m/L3M-supporting.csv",
    "mom_service": "01-clients/mom/mom-services.csv",
    "mom_location": "01-clients/mom/mom-location.csv",
    "mom_supporting": "01-clients/mom/mom-supporting.csv",
    "yoy_service": "01-clients/yoy/yoy-services.csv",
    "yoy_location": "01-clients/yoy/yoy-location.csv",
    "yoy_supporting": "01-clients/yoy/yoy-supporting.csv",
}
DEFAULT_METADATA = "metadata-h1.csv"


def _resolve_path(path_str: str) -> Path:
    p = Path(path_str.strip())
    if p.is_absolute():
        return p
    return (WORKSPACE_ROOT / p).resolve()


def _render_copy_prompt(prompt_text: str) -> None:
    escaped = html.escape(prompt_text)
    snippet = f"""
    <div style='margin-top:8px;'>
      <textarea id='seoPromptBox' style='width:100%;height:280px;font-family:monospace;'>{escaped}</textarea>
      <button
        style='margin-top:8px;padding:6px 12px;cursor:pointer;'
        onclick="navigator.clipboard.writeText(document.getElementById('seoPromptBox').value)">
        Copy Prompt
      </button>
    </div>
    """
    components.html(snippet, height=360)


def _input_block(label: str, key: str, default: str) -> str:
    return st.text_input(label=label, value=default, key=key)


st.set_page_config(page_title="SEO Benchmark Native", page_icon="📊", layout="wide")
st.title("SEO Benchmark Native App")
st.caption("Deterministic bucket benchmarking for L3M, MoM, and YoY with QA safeguards.")

with st.form("seo_benchmark_form"):
    st.subheader("Required Performance Inputs")

    c1, c2, c3 = st.columns(3)
    with c1:
        l3m_service = _input_block("L3M Service CSV", "l3m_service", DEFAULT_INPUTS["l3m_service"])
        mom_service = _input_block("MoM Service CSV", "mom_service", DEFAULT_INPUTS["mom_service"])
        yoy_service = _input_block("YoY Service CSV", "yoy_service", DEFAULT_INPUTS["yoy_service"])

    with c2:
        l3m_location = _input_block("L3M Location CSV", "l3m_location", DEFAULT_INPUTS["l3m_location"])
        mom_location = _input_block("MoM Location CSV", "mom_location", DEFAULT_INPUTS["mom_location"])
        yoy_location = _input_block("YoY Location CSV", "yoy_location", DEFAULT_INPUTS["yoy_location"])

    with c3:
        l3m_supporting = _input_block("L3M Supporting CSV", "l3m_supporting", DEFAULT_INPUTS["l3m_supporting"])
        mom_supporting = _input_block("MoM Supporting CSV", "mom_supporting", DEFAULT_INPUTS["mom_supporting"])
        yoy_supporting = _input_block("YoY Supporting CSV", "yoy_supporting", DEFAULT_INPUTS["yoy_supporting"])

    st.subheader("Metadata/H1 Input (Required)")
    metadata_path_str = st.text_input("Metadata CSV", value=DEFAULT_METADATA, key="metadata")

    st.subheader("Custom Bucket Rules (Optional)")
    st.caption(
        "Format: BucketName: url_contains=a,b; title_contains=c; meta_contains=d; h1_contains=e; exclude=x,y"
    )
    custom_rules_text = st.text_area(
        "Custom Rules",
        value="",
        placeholder="Blog: url_contains=/blog/,/insights/; title_contains=blog,guide\n"
        "Service Area: url_contains=/service-area/,/locations/; h1_contains=service area",
        height=120,
    )

    submitted = st.form_submit_button("Run Benchmark")

if submitted:
    input_paths = {
        "l3m_service": _resolve_path(l3m_service),
        "l3m_location": _resolve_path(l3m_location),
        "l3m_supporting": _resolve_path(l3m_supporting),
        "mom_service": _resolve_path(mom_service),
        "mom_location": _resolve_path(mom_location),
        "mom_supporting": _resolve_path(mom_supporting),
        "yoy_service": _resolve_path(yoy_service),
        "yoy_location": _resolve_path(yoy_location),
        "yoy_supporting": _resolve_path(yoy_supporting),
    }
    metadata_path = _resolve_path(metadata_path_str)

    missing = [str(path) for path in list(input_paths.values()) + [metadata_path] if not path.exists()]
    if missing:
        st.error("Run blocked: one or more files do not exist.")
        for item in missing:
            st.write(f"- {item}")
        st.stop()

    config = RunConfig(
        input_paths=input_paths,
        metadata_path=metadata_path,
        custom_rules_text=custom_rules_text,
        output_root=OUTPUT_ROOT,
    )

    try:
        result = run_benchmark(config)
    except Exception as exc:  # noqa: BLE001
        st.exception(exc)
        st.stop()

    if result.validation_blocked:
        st.warning("Validation errors detected. Main CSV written with blank metric fields and explanatory notes.")
    else:
        st.success("Benchmark completed successfully.")

    st.markdown("### Output Files")
    st.write(f"Output folder: `{result.output_dir}`")
    st.write(f"Analysis CSV: `{result.analysis_csv}`")
    st.write(f"QA CSV: `{result.qa_csv}`")
    st.write(f"QA Summary: `{result.qa_summary_txt}`")

    st.markdown("### Run Health")
    st.write(f"Total QA issues: **{result.qa_issue_count}**")
    st.write(f"QA errors: **{result.qa_error_count}**")
    st.write(f"Buckets in output: **{', '.join(result.bucket_order)}**")

    analysis_df = pd.read_csv(result.analysis_csv, dtype=str, keep_default_na=False)
    qa_df = pd.read_csv(result.qa_csv, dtype=str, keep_default_na=False)

    st.markdown("### Analysis Preview")
    st.dataframe(analysis_df, use_container_width=True)

    st.markdown("### QA Preview")
    st.dataframe(qa_df, use_container_width=True)

    st.markdown("### Prompt Template")
    st.caption("Use this prompt template for repeatable benchmark requests.")
    _render_copy_prompt(result.prompt_text)
