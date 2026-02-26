#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, Tuple
from urllib.parse import urlsplit, urlunsplit

import pandas as pd


def _is_nan_like(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    s = str(value).strip().lower()
    return s in {"", "nan", "none", "null"}


def clean_url(value: Any) -> str:
    if _is_nan_like(value):
        return ""
    s = str(value).strip().strip('"').strip("'")
    s = re.sub(r"\s+", "", s)
    if s.startswith("//"):
        s = "https:" + s
    return s


def normalize_url(value: Any, *, add_trailing_slash: bool = True) -> str:
    url = clean_url(value)
    if not url:
        return ""
    if url.startswith("/"):
        url = "https://www.sterlinglawyers.com" + url

    parts = urlsplit(url)
    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    path = parts.path or "/"

    if add_trailing_slash:
        last_segment = path.rsplit("/", 1)[-1]
        has_extension = "." in last_segment and not last_segment.startswith(".")
        if path != "/" and not path.endswith("/") and not has_extension:
            path = path + "/"

    return urlunsplit((scheme, netloc, path, parts.query, ""))


def url_path(url: str) -> str:
    u = normalize_url(url, add_trailing_slash=False)
    if not u:
        return ""
    return urlsplit(u).path or "/"


def load_curl_map(path: Path) -> Dict[str, Tuple[int, str]]:
    df = pd.read_csv(path, sep="\t", header=None, names=["URL", "Status", "Effective"], dtype=str, keep_default_na=False)
    df["URL"] = df["URL"].map(normalize_url)
    df["Effective"] = df["Effective"].map(normalize_url)
    df["Status"] = df["Status"].astype(str).str.strip()

    mapping: Dict[str, Tuple[int, str]] = {}
    for _, r in df.iterrows():
        u = r["URL"]
        if not u:
            continue
        try:
            code = int(r["Status"]) if r["Status"] else 0
        except Exception:
            code = 0
        eff = r["Effective"] or ""
        mapping[u] = (code, eff)
        # Also allow direct lookups of the effective URL for convenience.
        if code == 200 and eff:
            mapping.setdefault(eff, (200, eff))
    return mapping


def suggest_replacement_for_redirect(current_target: str, mapping: Dict[str, Tuple[int, str]]) -> str:
    current_norm = normalize_url(current_target)
    if not current_norm:
        return ""
    info = mapping.get(current_norm)
    if not info:
        return ""
    code, eff = info
    if code != 200 or not eff:
        return ""

    # If an attorney profile redirects to the WI homepage, treat as retired and route to directory.
    current_path = url_path(current_norm).lower()
    eff_path = url_path(eff).lower()
    if "/wisconsin/attorneys/" in current_path and eff_path in {"/wisconsin/", "/"}:
        return "https://www.sterlinglawyers.com/wisconsin/attorneys/"

    return eff


def suggest_replacement_for_404(current_target: str) -> str:
    current_norm = normalize_url(current_target)
    if not current_norm:
        return ""
    # Common malformed pattern: blog URL concatenated with /wisconsin/attorneys/...
    idx = current_norm.lower().find("/wisconsin/attorneys/")
    if idx != -1:
        return "https://www.sterlinglawyers.com" + current_norm[idx:]
    return ""


def apply_updates_to_implementation(df: pd.DataFrame, mapping: Dict[str, Tuple[int, str]]) -> pd.DataFrame:
    out = df.copy()
    for col in ["Action", "Source URL", "Current Target URL", "Suggested Target URL"]:
        if col not in out.columns:
            out[col] = ""
        out[col] = out[col].astype(str).fillna("")
    if "Notes" not in out.columns:
        out["Notes"] = ""
    out["Notes"] = out["Notes"].astype(str).fillna("")

    # Remove ADD_CONTEXTUAL rows where the source blog is confirmed 404 in the curl map.
    def _source_is_404(row: pd.Series) -> bool:
        if row["Action"] != "ADD_CONTEXTUAL":
            return False
        src = normalize_url(row["Source URL"])
        info = mapping.get(src)
        return bool(info and info[0] == 404)

    out = out[~out.apply(_source_is_404, axis=1)].reset_index(drop=True)

    # Fill missing Suggested Target URL where it can be derived from curl effective URL.
    def _fill_suggested(row: pd.Series) -> str:
        suggested = normalize_url(row.get("Suggested Target URL", ""))
        if suggested:
            return suggested
        current = normalize_url(row.get("Current Target URL", ""))
        if not current:
            return ""

        # Prefer redirect-derived replacement when we have a 200 effective destination.
        repl = suggest_replacement_for_redirect(current, mapping)
        if repl:
            return repl

        # Fallback: fix known malformed 404 patterns.
        return suggest_replacement_for_404(current)

    out["Suggested Target URL"] = out.apply(_fill_suggested, axis=1)

    # Populate curl QA columns (prefer Suggested Target URL; fallback to Current Target URL).
    if "Curl Final Status" not in out.columns:
        out["Curl Final Status"] = ""
    if "Curl Effective URL" not in out.columns:
        out["Curl Effective URL"] = ""

    def _curl_lookup(row: pd.Series) -> Tuple[str, str]:
        suggested = normalize_url(row.get("Suggested Target URL", ""))
        current = normalize_url(row.get("Current Target URL", ""))

        lookup = suggested or current
        if not lookup:
            return ("", "")

        info = mapping.get(lookup)
        if info:
            code, eff = info
            return (str(code) if code else "", eff or "")

        # If Suggested is an effective URL from a known current target, inherit it.
        if current and current in mapping:
            code, eff = mapping[current]
            if suggested and eff and normalize_url(suggested) == normalize_url(eff):
                return (str(code) if code else "", eff or "")

        return ("", "")

    curl_vals = out.apply(_curl_lookup, axis=1, result_type="expand")
    out["Curl Final Status"] = curl_vals[0]
    out["Curl Effective URL"] = curl_vals[1]

    # Reclassify “redirect fixes” that actually end in 404 (common placeholder/malformed URLs).
    # These should be handled as remove/replace rather than URL normalization.
    redirect_to_404 = (out["Action"].eq("FIX_REDIRECT")) & (out["Curl Final Status"].astype(str).str.strip() == "404")
    if redirect_to_404.any():
        out.loc[redirect_to_404, "Action"] = "REMOVE_OR_REPLACE"
        out.loc[redirect_to_404, "Notes"] = out.loc[redirect_to_404, "Notes"].astype(str) + " [QA: final destination is 404]"

    # Replace Suggested Target URL with effective URL when curl confirms a different final destination.
    # (This is the “301 -> final 200” normalization rule.)
    def _normalize_to_effective(row: pd.Series) -> str:
        suggested = normalize_url(row.get("Suggested Target URL", ""))
        if not suggested:
            return ""
        info = mapping.get(suggested)
        if not info:
            return suggested
        code, eff = info
        if code == 200 and eff and normalize_url(eff) != suggested:
            return normalize_url(eff)
        return suggested

    out["Suggested Target URL"] = out.apply(_normalize_to_effective, axis=1)
    return out


def update_workbook(xlsx_in: Path, xlsx_out: Path, impl_df: pd.DataFrame, mapping: Dict[str, Tuple[int, str]]) -> None:
    sheets = pd.read_excel(xlsx_in, sheet_name=None, dtype=str, keep_default_na=False)

    # Terminology alignment: use "Core Page" instead of "Hub" in the outputs.
    # Target Universe: convert Source Hubs (IDs) -> Source Core Pages (URLs) using Tier-1 rows.
    tu_key = "Target Universe"
    tier1_id_to_url: Dict[str, str] = {}
    if tu_key in sheets:
        tu_df = sheets[tu_key].copy()
        if set(["Tier", "Parent Cluster ID", "URL"]).issubset(set(tu_df.columns)):
            tier1_rows = tu_df[tu_df["Tier"].astype(str).str.strip().eq("Tier-1")].copy()
            for _, r in tier1_rows.iterrows():
                cid = str(r.get("Parent Cluster ID", "")).strip()
                url = normalize_url(r.get("URL", ""))
                if cid and url:
                    tier1_id_to_url[cid] = url

        if "Source Hubs" in tu_df.columns and "Source Core Pages" not in tu_df.columns:
            def _ids_to_urls(value: Any) -> str:
                s = str(value).strip()
                if not s or s.lower() == "nan":
                    return ""
                parts = [p.strip() for p in s.split(",") if p.strip()]
                urls = [tier1_id_to_url.get(p, p) for p in parts]
                return ", ".join(urls)

            tu_df["Source Core Pages"] = tu_df["Source Hubs"].map(_ids_to_urls)
            tu_df = tu_df.drop(columns=["Source Hubs"])

        sheets[tu_key] = tu_df

    # Core Outlinks Audit: rename Hub columns for clarity.
    coa_key = "Core Outlinks Audit"
    if coa_key in sheets:
        coa_df = sheets[coa_key].copy()
        rename_map = {}
        if "Hub" in coa_df.columns:
            rename_map["Hub"] = "Core Page ID"
        if "Hub URL" in coa_df.columns:
            rename_map["Hub URL"] = "Core Page URL"
        if rename_map:
            coa_df = coa_df.rename(columns=rename_map)
        sheets[coa_key] = coa_df

    # Update Recommendations (Add Links) by removing 404 sources (same rule as implementation CSV).
    add_key = "Recommendations (Add Links)"
    if add_key in sheets:
        add_df = sheets[add_key].copy()
        if "Source URL" in add_df.columns:
            add_df = add_df[~add_df["Source URL"].map(lambda u: mapping.get(normalize_url(u), (0, ""))[0] == 404)].reset_index(drop=True)
        sheets[add_key] = add_df

    # Update Recommendations (Fix Existing): fill Suggested Target URL where missing using curl map.
    fix_key = "Recommendations (Fix Existing)"
    if fix_key in sheets:
        fix_df = sheets[fix_key].copy()
        for col in ["Current Target URL", "Suggested Target URL"]:
            if col not in fix_df.columns:
                fix_df[col] = ""
            fix_df[col] = fix_df[col].astype(str).fillna("")
        if "Notes" not in fix_df.columns:
            fix_df["Notes"] = ""
        fix_df["Notes"] = fix_df["Notes"].astype(str).fillna("")

        def _fill_fix_suggested(row: pd.Series) -> str:
            suggested = normalize_url(row.get("Suggested Target URL", ""))
            if suggested:
                return suggested
            current = normalize_url(row.get("Current Target URL", ""))
            if not current:
                return ""
            repl = suggest_replacement_for_redirect(current, mapping)
            if repl:
                return repl
            return suggest_replacement_for_404(current)

        fix_df["Suggested Target URL"] = fix_df.apply(_fill_fix_suggested, axis=1)

        if "Action" in fix_df.columns:
            fix_df["Action"] = fix_df["Action"].astype(str).fillna("")
            curr_norm = fix_df["Current Target URL"].map(normalize_url)
            is_404 = curr_norm.map(lambda u: mapping.get(u, (0, ""))[0] == 404)
            redirect_404 = fix_df["Action"].eq("FIX_REDIRECT") & is_404
            if redirect_404.any():
                fix_df.loc[redirect_404, "Action"] = "REMOVE_OR_REPLACE"
                fix_df.loc[redirect_404, "Notes"] = fix_df.loc[redirect_404, "Notes"].astype(str) + " [QA: final destination is 404]"
        sheets[fix_key] = fix_df

    # Update QA Issues: fill Suggested Target URL for NON_200_TARGET where possible + add BLOG_SOURCE_404.
    qa_key = "QA Issues"
    if qa_key in sheets:
        qa_df = sheets[qa_key].copy()
        for col in ["Issue Type", "Source URL", "Target URL (Normalized)", "Suggested Target URL"]:
            if col not in qa_df.columns:
                qa_df[col] = ""
            qa_df[col] = qa_df[col].astype(str).fillna("")

        def _fill_qa_suggested(row: pd.Series) -> str:
            suggested = normalize_url(row.get("Suggested Target URL", ""))
            if suggested:
                return suggested
            target = normalize_url(row.get("Target URL (Normalized)", ""))
            if not target:
                return ""
            repl = suggest_replacement_for_redirect(target, mapping)
            if repl:
                return repl
            return suggest_replacement_for_404(target)

        qa_df["Suggested Target URL"] = qa_df.apply(_fill_qa_suggested, axis=1)

        # If a blog is confirmed 404, drop the weaker “missing from export” signal for that same URL.
        confirmed_404_sources = set()
        for src, (code, _) in mapping.items():
            if code == 404 and src.endswith("/clients-journey-racine-child-support-lawyer/"):
                confirmed_404_sources.add(src)
        if confirmed_404_sources:
            qa_df = qa_df[~(qa_df["Issue Type"].eq("BLOG_SOURCE_MISSING_FROM_EXPORT") & qa_df["Source URL"].isin(confirmed_404_sources))].reset_index(drop=True)

        # Add BLOG_SOURCE_404 rows for any ADD_CONTEXTUAL source URLs removed.
        removed_sources = set(
            sheets.get("Recommendations (Add Links)", pd.DataFrame()).get("Source URL", pd.Series(dtype=str)).tolist()
        )
        # We removed rows already; detect via curl map for the known 404 blog.
        blog_404 = [u for u, (c, _) in mapping.items() if c == 404 and "/wisconsin/blog/" in url_path(u).lower()]
        extra_rows = []
        for src in blog_404:
            if src.endswith("/clients-journey-racine-child-support-lawyer/"):
                extra_rows.append(
                    {
                        "Issue Type": "BLOG_SOURCE_404",
                        "Source Type": "Blog",
                        "Source URL": src,
                        "Target URL (Raw)": "",
                        "Target URL (Normalized)": "",
                        "Anchor Text": "",
                        "Link Position": "",
                        "Status Code (Export)": "404",
                        "Suggested Target URL": "",
                        "Notes": "Source blog URL returns 404; remove from implementation list or 301 it to the best replacement.",
                    }
                )
        if extra_rows:
            qa_df = pd.concat([qa_df, pd.DataFrame(extra_rows)], ignore_index=True, sort=False)
            qa_df = qa_df.drop_duplicates(subset=["Issue Type", "Source URL"]).reset_index(drop=True)

        sheets[qa_key] = qa_df

    # Update Target Universe curl columns for Tier-3.
    if tu_key in sheets:
        tu_df = sheets[tu_key].copy()
        if "Curl Final Status" not in tu_df.columns:
            tu_df["Curl Final Status"] = ""
        if "Curl Effective URL" not in tu_df.columns:
            tu_df["Curl Effective URL"] = ""

        def _fill_tu(row: pd.Series) -> Tuple[str, str]:
            url = normalize_url(row.get("URL", ""))
            info = mapping.get(url)
            if not info:
                return ("", "")
            code, eff = info
            return (str(code) if code else "", eff or "")

        vals = tu_df.apply(_fill_tu, axis=1, result_type="expand")
        tu_df["Curl Final Status"] = vals[0]
        tu_df["Curl Effective URL"] = vals[1]
        sheets[tu_key] = tu_df

    # Update Overview KPIs using the updated sheets.
    overview_key = "Overview"
    if overview_key in sheets:
        overview_df = sheets[overview_key].copy()
        if set(["Metric", "Value"]).issubset(set(overview_df.columns)):
            # Recompute the two metrics we changed.
            add_count = int(len(sheets.get("Recommendations (Add Links)", pd.DataFrame())))
            fix_count = int(len(sheets.get("Recommendations (Fix Existing)", pd.DataFrame())))
            overview_df.loc[overview_df["Metric"].eq("Add-link recommendations (1 per blog)"), "Value"] = str(add_count)
            overview_df.loc[overview_df["Metric"].eq("Fix-existing recommendations"), "Value"] = str(fix_count)
        sheets[overview_key] = overview_df

    xlsx_out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(xlsx_out, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=name[:31])

    # Re-apply light usability formatting.
    from openpyxl import load_workbook

    wb = load_workbook(xlsx_out)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for col_cells in ws.columns:
            max_len = 0
            col_letter = col_cells[0].column_letter
            for c in col_cells[:2000]:
                v = "" if c.value is None else str(c.value)
                max_len = max(max_len, len(v))
            ws.column_dimensions[col_letter].width = min(max(12, max_len + 2), 70)
    wb.save(xlsx_out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply curl QA map to Sterling WI internal linking audit outputs.")
    parser.add_argument("--xlsx_in", required=True)
    parser.add_argument("--csv_in", required=True)
    parser.add_argument("--curl_map_tsv", required=True)
    parser.add_argument("--xlsx_out", required=True)
    parser.add_argument("--csv_out", required=True)
    args = parser.parse_args()

    mapping = load_curl_map(Path(args.curl_map_tsv))

    impl = pd.read_csv(args.csv_in, dtype=str, keep_default_na=False)
    impl_updated = apply_updates_to_implementation(impl, mapping)
    Path(args.csv_out).parent.mkdir(parents=True, exist_ok=True)
    impl_updated.to_csv(args.csv_out, index=False)

    update_workbook(Path(args.xlsx_in), Path(args.xlsx_out), impl_updated, mapping)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
