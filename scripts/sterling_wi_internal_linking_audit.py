#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

import pandas as pd


SF_EXPECTED_COLUMNS = [
    "Type",
    "From",
    "To",
    "Anchor Text",
    "Alt Text",
    "Follow",
    "Target",
    "Rel",
    "Status Code",
    "Status",
    "Path Type",
    "Link Path",
    "Link Position",
    "Link Origin",
    "Size",
    "Transferred",
]


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


def url_path(value: Any) -> str:
    u = normalize_url(value, add_trailing_slash=False)
    if not u:
        return ""
    return urlsplit(u).path or "/"


def is_internal(url_norm: str) -> bool:
    if not url_norm:
        return False
    try:
        parts = urlsplit(url_norm)
    except Exception:
        return False
    return parts.netloc.lower() in {"www.sterlinglawyers.com", "sterlinglawyers.com"}


def is_wisconsin(url_norm: str) -> bool:
    return "/wisconsin/" in url_path(url_norm).lower()


def is_wi_blog(url_norm: str) -> bool:
    return "/wisconsin/blog/" in url_path(url_norm).lower()


def bucket_link_position(value: Any) -> str:
    s = str(value).strip()
    if s.lower() == "content":
        return "Content"
    if not s:
        return "Unknown"
    return "Template"


def stable_pick(options: List[str], key: str) -> str:
    if not options:
        return ""
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    idx = int(h[:8], 16) % len(options)
    return options[idx]


@dataclass(frozen=True)
class CurlResult:
    final_status: int
    effective_url: str


class CurlResolver:
    def __init__(self, *, timeout_seconds: int = 25) -> None:
        self._timeout_seconds = timeout_seconds
        self._cache: Dict[str, CurlResult] = {}

    def resolve(self, url: str) -> CurlResult:
        url_norm = normalize_url(url)
        if not url_norm:
            return CurlResult(final_status=0, effective_url="")
        if url_norm in self._cache:
            return self._cache[url_norm]

        # Curl can intermittently fail DNS/handshake in some environments (exit code != 0).
        # We still capture `-w` output and retry a few times; treat http_code=000 as unknown.
        cmd = [
            "curl",
            "-s",
            "-L",
            "-I",
            "--max-time",
            str(self._timeout_seconds),
            "--retry",
            "2",
            "--retry-delay",
            "0",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code} %{url_effective}",
            url_norm,
        ]

        code = 0
        eff = ""
        for _ in range(3):
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True)
                out = (proc.stdout or "").strip()
                m = re.match(r"^(\d{3})\s+(.*)$", out)
                if m:
                    http_code = int(m.group(1))
                    eff_val = m.group(2).strip()
                    if http_code >= 100:
                        code = http_code
                        eff = eff_val
                        break
                    # http_code=000 means unknown; keep best-effort effective URL and retry.
                    code = 0
                    eff = eff_val
                else:
                    code = 0
                    eff = ""
            except Exception:
                code = 0
                eff = ""

        result = CurlResult(final_status=code, effective_url=normalize_url(eff) if eff else "")
        self._cache[url_norm] = result
        return result


def read_csv_str(path: str | Path, *, usecols: Optional[List[str]] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, usecols=usecols, nrows=nrows)


def read_sf_links(path: str | Path) -> pd.DataFrame:
    df = read_csv_str(path)
    for col in SF_EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[SF_EXPECTED_COLUMNS]
    return df


def normalize_sf_links(df: pd.DataFrame, *, keep_raw: bool = True) -> pd.DataFrame:
    out = df.copy()
    if keep_raw:
        out["From (Raw)"] = out["From"]
        out["To (Raw)"] = out["To"]
        out["Anchor Text (Raw)"] = out["Anchor Text"]

    out["From"] = out["From"].map(normalize_url)
    out["To"] = out["To"].map(normalize_url)
    out["Anchor Text"] = out["Anchor Text"].astype(str).str.strip()
    out["Link Position"] = out["Link Position"].astype(str).str.strip()
    out["Type"] = out["Type"].astype(str).str.strip()
    out["Status Code"] = out["Status Code"].astype(str).str.strip()
    out["Is Internal"] = out["To"].map(is_internal)
    out["Is Wisconsin"] = out["To"].map(is_wisconsin)
    out["Link Position Bucket"] = out["Link Position"].map(bucket_link_position)
    out["Is Blog Source"] = out["From"].map(is_wi_blog)
    out["Is Content Link"] = out["Link Position Bucket"].eq("Content")
    return out


def filter_hyperlinks(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Type"].str.lower().eq("hyperlink")].copy()


def load_wi_blog_list(path: str | Path) -> pd.DataFrame:
    df = read_csv_str(path)
    if df.shape[1] != 1:
        df = df.iloc[:, [0]]
    df.columns = ["Blog URL"]
    df["Blog URL"] = df["Blog URL"].map(normalize_url)
    df = df[df["Blog URL"].ne("")]
    df = df.drop_duplicates(subset=["Blog URL"]).reset_index(drop=True)
    return df


def load_core_subservices(path: str | Path) -> pd.DataFrame:
    df = read_csv_str(path)
    df = df.rename(columns={"URLs": "URL", "CLUSTER ID": "Cluster ID", "Practice Area Type": "Type", "H1": "H1"})
    df["URL"] = df["URL"].map(normalize_url)
    df["Type"] = df["Type"].astype(str).str.strip()
    df["Cluster ID"] = df["Cluster ID"].astype(str).str.strip()
    df["H1"] = df["H1"].astype(str).str.strip()
    df = df[df["URL"].ne("")]

    df["Tier"] = df["Type"].map(lambda v: "Tier-1" if str(v).strip().lower() == "core" else "Tier-2")

    # Parent Cluster ID for Tier-2 is derived by URL path (locked requirement).
    parent_map = {
        "/wisconsin/divorce/": "DIV",
        "/wisconsin/child-custody/": "CH-CUS",
        "/wisconsin/child-support/": "CH-SUP",
        "/wisconsin/property-division/": "PROP-DIV",
    }
    df["Parent Cluster ID"] = ""
    tier2_mask = df["Tier"].eq("Tier-2")
    for prefix, parent in parent_map.items():
        df.loc[tier2_mask & df["URL"].str.contains(prefix, case=False, regex=False), "Parent Cluster ID"] = parent

    df.loc[df["Tier"].eq("Tier-1"), "Parent Cluster ID"] = df.loc[df["Tier"].eq("Tier-1"), "Cluster ID"]

    cluster_name = {
        "DIV": "Divorce",
        "CH-CUS": "Child Custody",
        "CH-SUP": "Child Support",
        "SPO-SUP": "Spousal Support/Alimony",
        "PROP-DIV": "Property Division",
        "PT": "Paternity",
        "GUARD": "Guardianship",
    }
    df["Practice Area"] = df["Parent Cluster ID"].map(cluster_name).fillna("")

    return df.reset_index(drop=True)


def wi_blog_outlinks_filtered(all_blog_outlinks_path: str | Path, wi_blogs: pd.DataFrame) -> pd.DataFrame:
    wi_blog_set = set(wi_blogs["Blog URL"].map(clean_url))
    chunks: List[pd.DataFrame] = []

    for chunk in pd.read_csv(all_blog_outlinks_path, dtype=str, keep_default_na=False, chunksize=200_000):
        if "Type" not in chunk.columns or "From" not in chunk.columns:
            continue

        type_col = chunk["Type"].astype(str)
        chunk = chunk[type_col.str.lower().eq("hyperlink")].copy()
        if chunk.empty:
            continue

        from_clean = chunk["From"].astype(str).str.strip().str.replace(r"\s+", "", regex=True)
        chunk = chunk[from_clean.isin(wi_blog_set)].copy()
        if chunk.empty:
            continue

        # Ensure expected columns exist so downstream is stable.
        for col in SF_EXPECTED_COLUMNS:
            if col not in chunk.columns:
                chunk[col] = ""
        chunk = chunk[SF_EXPECTED_COLUMNS]
        chunks.append(chunk)

    if not chunks:
        return pd.DataFrame(columns=SF_EXPECTED_COLUMNS)
    return pd.concat(chunks, ignore_index=True)


def derive_tier3_from_hub_outlinks(
    hub_outlinks: pd.DataFrame, tier1_urls: set[str], tier2_urls: set[str]
) -> pd.DataFrame:
    df = hub_outlinks.copy()
    df = df[df["Is Content Link"] & df["Is Internal"]].copy()
    df = df[df["To"].str.contains("/wisconsin/", case=False, regex=False)].copy()

    def _exclude(url: str) -> bool:
        p = url_path(url).lower()
        if url in tier1_urls or url in tier2_urls:
            return True
        if "/wisconsin/blog/" in p:
            return True
        if "/attorneys/" in p:
            return True
        if "/locations/" in p:
            return True
        return False

    df = df[~df["To"].map(_exclude)].copy()
    if df.empty:
        return pd.DataFrame(columns=["Tier", "URL", "Parent Cluster ID", "Practice Area", "Source Hubs", "Occurrences"])

    agg = (
        df.groupby("To", dropna=False)
        .agg(
            Occurrences=("To", "size"),
            Hub_Count=("Hub", "nunique"),
            Source_Hubs=("Hub", lambda x: ", ".join(sorted(set(x)))),
        )
        .reset_index()
        .rename(columns={"To": "URL", "Hub_Count": "Hub Count", "Source_Hubs": "Source Hubs"})
    )
    agg = agg[(agg["Occurrences"] >= 2) | (agg["Hub Count"] >= 2)].copy()
    agg.insert(0, "Tier", "Tier-3")
    agg["Parent Cluster ID"] = ""
    agg["Practice Area"] = ""
    return agg.sort_values(["Hub Count", "Occurrences", "URL"], ascending=[False, False, True]).reset_index(drop=True)


def compute_inlinks_audit(inlinks_all: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    df = inlinks_all.copy()
    df = filter_hyperlinks(df)
    df = normalize_sf_links(df)

    target_urls = targets[targets["Tier"].isin(["Tier-1", "Tier-2"])][["URL", "Tier", "Parent Cluster ID", "Practice Area", "H1"]].copy()
    target_urls = target_urls.rename(columns={"URL": "Target URL"})
    target_urls["Target URL"] = target_urls["Target URL"].map(normalize_url)
    target_set = set(target_urls["Target URL"])

    df = df[df["To"].isin(target_set)].copy()
    if df.empty:
        return pd.DataFrame()

    df["From Is WI Blog"] = df["From"].map(is_wi_blog)
    df["Anchor Clean"] = df["Anchor Text"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    df.loc[df["Anchor Clean"].eq(""), "Anchor Clean"] = "(empty)"

    pos_counts = df.pivot_table(index="To", columns="Link Position", values="From", aggfunc="size", fill_value=0)
    pos_counts.columns = [f"LP: {c}" for c in pos_counts.columns]
    pos_counts = pos_counts.reset_index().rename(columns={"To": "Target URL"})

    # Content vs template counts (locked).
    df["Template/Content"] = df["Link Position Bucket"]
    ctab = df.pivot_table(index="To", columns="Template/Content", values="From", aggfunc="size", fill_value=0)
    ctab = ctab.rename_axis(None, axis=1).reset_index().rename(columns={"To": "Target URL"})
    for col in ["Content", "Template"]:
        if col not in ctab.columns:
            ctab[col] = 0
    ctab = ctab[["Target URL", "Content", "Template"]].rename(columns={"Content": "Inlinks (Content)", "Template": "Inlinks (Template)"})

    base = (
        df.groupby("To", dropna=False)
        .agg(
            Inlink_Instances=("From", "size"),
            Unique_Linking_Pages=("From", "nunique"),
            Blog_Inlinks_All=("From Is WI Blog", "sum"),
            Blog_Linking_Pages_Unique=("From", lambda x: x[df.loc[x.index, "From Is WI Blog"]].nunique()),
            Blog_Inlinks_Content=("From", lambda x: x[(df.loc[x.index, "From Is WI Blog"]) & (df.loc[x.index, "Is Content Link"])].shape[0]),
        )
        .reset_index()
        .rename(
            columns={
                "To": "Target URL",
                "Inlink_Instances": "Inlink Instances",
                "Unique_Linking_Pages": "Unique Linking Pages",
                "Blog_Inlinks_All": "Blog Inlinks (All)",
                "Blog_Linking_Pages_Unique": "Blog Linking Pages (Unique)",
                "Blog_Inlinks_Content": "Blog Inlinks (Content)",
            }
        )
    )

    def _top_anchor(series: pd.Series) -> Tuple[str, float]:
        if series.empty:
            return ("", 0.0)
        counts = series.value_counts(dropna=False)
        top = str(counts.index[0])
        share = float(counts.iloc[0]) / float(counts.sum()) if counts.sum() else 0.0
        return (top, share)

    def _top_text(series: pd.Series) -> str:
        return _top_anchor(series)[0]

    def _top_share(series: pd.Series) -> float:
        return _top_anchor(series)[1]

    anchors_all = (
        df.groupby("To")["Anchor Clean"]
        .agg(Top_Anchor_All=_top_text, Top_Anchor_Share_All=_top_share)
        .reset_index()
        .rename(
            columns={
                "To": "Target URL",
                "Top_Anchor_All": "Top Anchor (All)",
                "Top_Anchor_Share_All": "Top Anchor Share (All)",
            }
        )
    )

    df_content = df[df["Is Content Link"]].copy()
    if df_content.empty:
        anchors_content = pd.DataFrame(columns=["Target URL", "Top Anchor (Content)", "Top Anchor Share (Content)"])
    else:
        anchors_content = (
            df_content.groupby("To")["Anchor Clean"]
            .agg(Top_Anchor_Content=_top_text, Top_Anchor_Share_Content=_top_share)
            .reset_index()
            .rename(
                columns={
                    "To": "Target URL",
                    "Top_Anchor_Content": "Top Anchor (Content)",
                    "Top_Anchor_Share_Content": "Top Anchor Share (Content)",
                }
            )
        )

    out = target_urls.merge(base, on="Target URL", how="left")
    out = out.merge(ctab, on="Target URL", how="left").merge(anchors_all, on="Target URL", how="left").merge(anchors_content, on="Target URL", how="left")
    out = out.merge(pos_counts, on="Target URL", how="left")

    out = out.fillna({"Inlink Instances": 0, "Unique Linking Pages": 0, "Inlinks (Content)": 0, "Inlinks (Template)": 0})
    out["Top Anchor Share (All)"] = out["Top Anchor Share (All)"].fillna(0.0)
    out["Top Anchor Share (Content)"] = out["Top Anchor Share (Content)"].fillna(0.0)

    out = out.sort_values(["Tier", "Parent Cluster ID", "Target URL"]).reset_index(drop=True)
    return out


def compute_core_outlinks_audit(hub_outlinks_all: pd.DataFrame, targets: pd.DataFrame, tier3: pd.DataFrame) -> pd.DataFrame:
    tier1_set = set(targets[targets["Tier"].eq("Tier-1")]["URL"])
    tier2_set = set(targets[targets["Tier"].eq("Tier-2")]["URL"])
    tier3_set = set(tier3.get("URL", pd.Series(dtype=str)).astype(str).map(normalize_url).tolist())

    df = hub_outlinks_all.copy()
    df = filter_hyperlinks(df)
    df = normalize_sf_links(df)
    df = df[df["Is Internal"]].copy()

    def classify(to_url: str) -> str:
        if to_url in tier2_set:
            return "Tier-2"
        if to_url in tier1_set:
            return "Tier-1"
        if to_url in tier3_set:
            return "Tier-3"
        p = url_path(to_url).lower()
        if "/wisconsin/" in p:
            return "Internal WI (Other)"
        if p.startswith("/") and p != "/":
            return "Internal (Other)"
        return "Other"

    df["Target Tier"] = df["To"].map(classify)
    df["Cross-State"] = df["To"].str.contains("/illinois/", case=False, regex=False) | df["To"].str.contains("/iowa/", case=False, regex=False)
    df["Has Whitespace Malform"] = df["To (Raw)"].astype(str).str.contains(r"\s", regex=True)
    df["Issue"] = ""
    df.loc[df["Status Code"].ne("200"), "Issue"] = df.loc[df["Status Code"].ne("200"), "Issue"] + "Non-200; "
    df.loc[df["Cross-State"], "Issue"] = df.loc[df["Cross-State"], "Issue"] + "Cross-state; "
    df.loc[df["Has Whitespace Malform"], "Issue"] = df.loc[df["Has Whitespace Malform"], "Issue"] + "Malformed whitespace; "
    df["Issue"] = df["Issue"].str.strip()

    # Keep a detailed content-only audit view; template links are tracked elsewhere.
    out = df[df["Is Content Link"]].copy()
    keep_cols = [
        "Hub",
        "From",
        "To (Raw)",
        "To",
        "Anchor Text",
        "Link Position",
        "Status Code",
        "Target Tier",
        "Issue",
    ]
    out = out[keep_cols].rename(columns={"From": "Hub URL", "To (Raw)": "Target URL (Raw)", "To": "Target URL (Normalized)"})
    return out.sort_values(["Hub", "Target Tier", "Target URL (Normalized)"]).reset_index(drop=True)


def compute_blog_outlinks_current(blog_outlinks_raw: pd.DataFrame, wi_blogs: pd.DataFrame) -> pd.DataFrame:
    df = blog_outlinks_raw.copy()
    df = filter_hyperlinks(df)
    df = normalize_sf_links(df)
    df = df[df["Is Internal"]].copy()

    # Only keep WI blog sources (defensive; should already be filtered).
    wi_set_norm = set(wi_blogs["Blog URL"])
    df = df[df["From"].isin(wi_set_norm)].copy()

    # Editorial view (locked policy uses Content links).
    out = df[df["Is Content Link"]].copy()
    keep_cols = [
        "From",
        "To (Raw)",
        "To",
        "Anchor Text",
        "Link Position",
        "Status Code",
        "Status",
    ]
    out = out[keep_cols].rename(
        columns={
            "From": "Blog URL",
            "To (Raw)": "Target URL (Raw)",
            "To": "Target URL (Normalized)",
            "Anchor Text": "Anchor Text",
        }
    )
    return out.sort_values(["Blog URL", "Target URL (Normalized)"]).reset_index(drop=True)


def build_qa_issues(
    blog_outlinks_current: pd.DataFrame,
    hub_outlinks_content: pd.DataFrame,
    curl: CurlResolver,
) -> pd.DataFrame:
    issues: List[Dict[str, Any]] = []

    def add_issue(
        *,
        issue_type: str,
        source_type: str,
        source_url: str,
        target_raw: str,
        target_norm: str,
        anchor: str,
        link_position: str,
        status_code: str,
        suggested_target: str = "",
        notes: str = "",
    ) -> None:
        issues.append(
            {
                "Issue Type": issue_type,
                "Source Type": source_type,
                "Source URL": source_url,
                "Target URL (Raw)": target_raw,
                "Target URL (Normalized)": target_norm,
                "Anchor Text": anchor,
                "Link Position": link_position,
                "Status Code (Export)": status_code,
                "Suggested Target URL": suggested_target,
                "Notes": notes,
            }
        )

    # Blog content-link issues.
    if not blog_outlinks_current.empty:
        for _, r in blog_outlinks_current.iterrows():
            status = str(r.get("Status Code", "")).strip()
            src = str(r.get("Blog URL", "")).strip()
            to_raw = str(r.get("Target URL (Raw)", "")).strip()
            to_norm = str(r.get("Target URL (Normalized)", "")).strip()
            anchor = str(r.get("Anchor Text", "")).strip()
            pos = str(r.get("Link Position", "")).strip()

            if status == "404":
                suggested = ""
                # Common malformed pattern: blog URL concatenated with /wisconsin/attorneys/...
                idx = to_norm.lower().find("/wisconsin/attorneys/")
                if idx != -1:
                    suggested = "https://www.sterlinglawyers.com" + to_norm[idx:]
                add_issue(
                    issue_type="INTERNAL_404_TARGET",
                    source_type="Blog",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    suggested_target=suggested,
                    notes="Internal link returns 404; replace or remove.",
                )
            elif status and status != "200":
                suggested = ""
                res = curl.resolve(to_norm)
                if res.final_status == 200 and res.effective_url:
                    suggested = res.effective_url
                    # If an attorney profile now redirects to the WI homepage, treat as retired and route to directory.
                    eff_path = url_path(res.effective_url).lower()
                    if "/wisconsin/attorneys/" in url_path(to_norm).lower() and eff_path in {"/wisconsin/", "/"}:
                        suggested = "https://www.sterlinglawyers.com/wisconsin/attorneys/"
                add_issue(
                    issue_type="NON_200_TARGET",
                    source_type="Blog",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    suggested_target=suggested,
                    notes="Internal link is non-200; update to final 200 destination.",
                )

            if "%5bactual%20attorney%20url%5d" in to_norm.lower():
                add_issue(
                    issue_type="PLACEHOLDER_URL",
                    source_type="Blog",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    notes="Placeholder URL detected; replace with the real attorney/profile URL.",
                )

            if "divorce%20lawyers%20beloit" in to_norm.lower():
                add_issue(
                    issue_type="MALFORMED_URL",
                    source_type="Blog",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    notes="Encoded-space URL appears malformed; replace with intended destination.",
                )

            if "/wisconsin/blog/" not in src.lower() and "/wisconsin/blog/" in to_norm.lower():
                add_issue(
                    issue_type="SOURCE_NOT_WI_BLOG",
                    source_type="Blog",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    notes="Source URL is not a WI blog (unexpected in this filtered view).",
                )

    # Core hub content-link issues (already filtered to content).
    if not hub_outlinks_content.empty:
        for _, r in hub_outlinks_content.iterrows():
            status = str(r.get("Status Code", "")).strip()
            src = str(r.get("Hub URL", "")).strip()
            to_raw = str(r.get("Target URL (Raw)", "")).strip()
            to_norm = str(r.get("Target URL (Normalized)", "")).strip()
            anchor = str(r.get("Anchor Text", "")).strip()
            pos = "Content"

            if status and status != "200":
                add_issue(
                    issue_type="HUB_NON_200_TARGET",
                    source_type="Core Hub",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    notes="Core hub content outlink is non-200; update to final 200 destination or replace.",
                )

            if "/illinois/" in to_norm.lower():
                # Recommend swapping to WI equivalent when obvious.
                suggested = ""
                if "/child-custody/split-orders/" in to_norm.lower():
                    suggested = "https://www.sterlinglawyers.com/wisconsin/child-custody/split-orders/"
                add_issue(
                    issue_type="CROSS_STATE_LINK",
                    source_type="Core Hub",
                    source_url=src,
                    target_raw=to_raw,
                    target_norm=to_norm,
                    anchor=anchor,
                    link_position=pos,
                    status_code=status,
                    suggested_target=suggested,
                    notes="Cross-state link from WI hub; replace with WI destination.",
                )

            if "/placement-factors/" in to_norm.lower():
                res = curl.resolve(to_norm)
                if res.final_status in {200, 301, 302} and res.effective_url:
                    add_issue(
                        issue_type="REDIRECT_TO_HUB",
                        source_type="Core Hub",
                        source_url=src,
                        target_raw=to_raw,
                        target_norm=to_norm,
                        anchor=anchor,
                        link_position=pos,
                        status_code=str(res.final_status),
                        suggested_target=res.effective_url,
                        notes="Target redirects; if it collapses into the hub, replace with a distinct relevant 200 page or remove.",
                    )

    qa = pd.DataFrame(issues)
    if qa.empty:
        return qa

    qa = qa.drop_duplicates(
        subset=[
            "Issue Type",
            "Source Type",
            "Source URL",
            "Target URL (Normalized)",
            "Anchor Text",
            "Link Position",
            "Status Code (Export)",
        ]
    )
    return qa.sort_values(["Source Type", "Issue Type", "Source URL"]).reset_index(drop=True)


def generate_add_recommendations(wi_blogs: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    tier1 = targets[targets["Tier"].eq("Tier-1")][["URL", "Parent Cluster ID", "Practice Area", "H1"]].copy()
    tier2 = targets[targets["Tier"].eq("Tier-2")][["URL", "Parent Cluster ID", "Practice Area", "H1"]].copy()

    tier1_by_cluster = {r["Parent Cluster ID"]: r["URL"] for _, r in tier1.iterrows()}
    tier2_urls = tier2["URL"].tolist()

    # Map Tier-2 URLs by slug for deterministic selection.
    tier2_by_path: Dict[str, str] = {}
    for u in tier2_urls:
        tier2_by_path[url_path(u).lower()] = u

    # Explicit Tier-2 targets are sourced from the provided core-subserv.csv (locked list).
    # Do not hardcode URLs here; derive them from `targets` so the output stays aligned with the client’s canonical pages.
    def _pick_tier2_url(
        parent_cluster_id: str,
        *,
        url_contains: str = "",
        h1_contains: str = "",
        fallback: str = "",
    ) -> str:
        c = tier2[tier2["Parent Cluster ID"].astype(str).str.strip().eq(parent_cluster_id)].copy()
        if url_contains:
            c = c[c["URL"].astype(str).str.contains(url_contains, case=False, regex=False)]
        if h1_contains:
            c = c[c["H1"].astype(str).str.contains(h1_contains, case=False, na=False)]
        if not c.empty:
            return normalize_url(c.iloc[0]["URL"])
        return normalize_url(fallback) if fallback else ""

    tier2_targets = {
        "DIV:CONTESTED": _pick_tier2_url("DIV", url_contains="contested-divorce", fallback="https://www.sterlinglawyers.com/wisconsin/divorce/contested-divorce/"),
        "DIV:UNCONTESTED": _pick_tier2_url("DIV", url_contains="uncontested-divorce", fallback="https://www.sterlinglawyers.com/wisconsin/divorce/uncontested-divorce/"),
        "DIV:MEDIATION": _pick_tier2_url("DIV", url_contains="/mediation/", fallback="https://www.sterlinglawyers.com/wisconsin/divorce/mediation/"),
        "DIV:COLLAB": _pick_tier2_url("DIV", url_contains="/collaborative/", fallback="https://www.sterlinglawyers.com/wisconsin/divorce/collaborative/"),
        "DIV:SEPARATION": _pick_tier2_url("DIV", url_contains="/separation/", fallback="https://www.sterlinglawyers.com/wisconsin/divorce/separation/"),
        "CH-CUS:MODIFY": _pick_tier2_url("CH-CUS", url_contains="/modify", fallback="https://www.sterlinglawyers.com/wisconsin/child-custody/modify-orders/"),
        "CH-CUS:PARENTING_PLAN": _pick_tier2_url("CH-CUS", url_contains="parenting-plan", fallback="https://www.sterlinglawyers.com/wisconsin/child-custody/parenting-plan/"),
        "CH-CUS:VISITATION": _pick_tier2_url(
            "CH-CUS",
            h1_contains="Visitation",
            fallback="https://www.sterlinglawyers.com/wisconsin/child-custody/no-visitation-supervised-visitation/",
        ),
        "CH-SUP:MODIFY": _pick_tier2_url("CH-SUP", url_contains="/modify", fallback="https://www.sterlinglawyers.com/wisconsin/child-support/modify-orders/"),
        "CH-SUP:ENFORCE": _pick_tier2_url("CH-SUP", url_contains="/enforce", fallback="https://www.sterlinglawyers.com/wisconsin/child-support/enforce-orders/"),
        "PROP-DIV:NON_MARITAL": _pick_tier2_url("PROP-DIV", url_contains="non-marital-property", fallback="https://www.sterlinglawyers.com/wisconsin/property-division/non-marital-property/"),
        "PROP-DIV:HIDDEN_ASSETS": _pick_tier2_url("PROP-DIV", url_contains="hidden-assets", fallback="https://www.sterlinglawyers.com/wisconsin/property-division/hidden-assets/"),
    }

    # Ordered, regex-safe matching rules (prevents uncontested->contested collisions).
    tier2_rules: List[Tuple[re.Pattern[str], str]] = [
        (re.compile(r"(?:^|[-_/])uncontested(?:[-_/]|$)", re.I), tier2_targets["DIV:UNCONTESTED"]),
        (re.compile(r"(?:^|[-_/])contested(?:[-_/]|$)", re.I), tier2_targets["DIV:CONTESTED"]),
        (re.compile(r"(?:^|[-_/])mediation(?:[-_/]|$)", re.I), tier2_targets["DIV:MEDIATION"]),
        (re.compile(r"(?:^|[-_/])collaborative(?:[-_/]|$)", re.I), tier2_targets["DIV:COLLAB"]),
        (re.compile(r"(?:^|[-_/])legal-separation(?:[-_/]|$)", re.I), tier2_targets["DIV:SEPARATION"]),
        (re.compile(r"(?:^|[-_/])separation(?:[-_/]|$)", re.I), tier2_targets["DIV:SEPARATION"]),
        (re.compile(r"(?:^|[-_/])modify(?:[-_/]|$).*(?:custody|placement)", re.I), tier2_targets["CH-CUS:MODIFY"]),
        (re.compile(r"(?:custody|placement).*(?:^|[-_/])modify(?:[-_/]|$)", re.I), tier2_targets["CH-CUS:MODIFY"]),
        (re.compile(r"(?:^|[-_/])parenting-plan(?:[-_/]|$)", re.I), tier2_targets["CH-CUS:PARENTING_PLAN"]),
        (re.compile(r"(?:^|[-_/])visitation(?:[-_/]|$)", re.I), tier2_targets["CH-CUS:VISITATION"]),
        (re.compile(r"(?:^|[-_/])modify(?:[-_/]|$).*(?:child-support|support)", re.I), tier2_targets["CH-SUP:MODIFY"]),
        (re.compile(r"(?:child-support|support).*(?:^|[-_/])modify(?:[-_/]|$)", re.I), tier2_targets["CH-SUP:MODIFY"]),
        (re.compile(r"(?:^|[-_/])enforc(?:e|ement)(?:[-_/]|$)", re.I), tier2_targets["CH-SUP:ENFORCE"]),
        (re.compile(r"(?:^|[-_/])non-marital(?:[-_/]|$)|(?:^|[-_/])nonmarital(?:[-_/]|$)", re.I), tier2_targets["PROP-DIV:NON_MARITAL"]),
        (re.compile(r"(?:^|[-_/])hidden-assets?(?:[-_/]|$)", re.I), tier2_targets["PROP-DIV:HIDDEN_ASSETS"]),
    ]

    tier1_targets = {
        "DIV": "https://www.sterlinglawyers.com/wisconsin/divorce/",
        "CH-CUS": "https://www.sterlinglawyers.com/wisconsin/child-custody/",
        "CH-SUP": "https://www.sterlinglawyers.com/wisconsin/child-support/",
        "SPO-SUP": "https://www.sterlinglawyers.com/wisconsin/spousal-support/",
        "PROP-DIV": "https://www.sterlinglawyers.com/wisconsin/property-division/",
        "PT": "https://www.sterlinglawyers.com/wisconsin/paternity/",
        "GUARD": "https://www.sterlinglawyers.com/wisconsin/guardianship/",
    }

    anchor_bank: Dict[str, List[str]] = {
        tier1_targets["DIV"]: ["Wisconsin divorce", "divorce in Wisconsin", "Wisconsin divorce lawyers", "Wisconsin divorce attorney"],
        tier2_targets["DIV:CONTESTED"]: ["contested divorce in Wisconsin", "Wisconsin contested divorce", "Wisconsin contested divorce attorney"],
        tier2_targets["DIV:UNCONTESTED"]: ["uncontested divorce in Wisconsin", "file an uncontested divorce in Wisconsin", "Wisconsin uncontested divorce"],
        tier2_targets["DIV:MEDIATION"]: ["Wisconsin divorce mediation", "divorce mediation in Wisconsin", "mediation for divorce in Wisconsin"],
        tier2_targets["DIV:COLLAB"]: ["collaborative divorce in Wisconsin", "Wisconsin collaborative divorce", "collaborative divorce attorney in Wisconsin"],
        tier2_targets["DIV:SEPARATION"]: ["legal separation in Wisconsin", "Wisconsin legal separation", "legal separation lawyer in Wisconsin"],
        tier1_targets["CH-CUS"]: ["Wisconsin child custody", "child custody in Wisconsin", "Wisconsin child custody lawyers", "Wisconsin custody and placement"],
        tier2_targets["CH-CUS:MODIFY"]: ["modify child custody in Wisconsin", "Wisconsin child custody modification", "changing custody in Wisconsin"],
        tier2_targets["CH-CUS:PARENTING_PLAN"]: ["Wisconsin parenting plan", "parenting plan template (Wisconsin)", "Wisconsin parenting plan template"],
        tier2_targets["CH-CUS:VISITATION"]: ["visitation rights in Wisconsin", "Wisconsin visitation", "visitation laws in Wisconsin"],
        tier1_targets["CH-SUP"]: ["Wisconsin child support", "child support in Wisconsin", "Wisconsin child support lawyers"],
        tier2_targets["CH-SUP:MODIFY"]: ["modify child support in Wisconsin", "Wisconsin child support modification", "changing child support in Wisconsin"],
        tier2_targets["CH-SUP:ENFORCE"]: ["child support enforcement in Wisconsin", "enforcing child support in Wisconsin", "Wisconsin child support enforcement"],
        tier1_targets["SPO-SUP"]: ["Wisconsin spousal support", "alimony in Wisconsin", "Wisconsin alimony", "spousal support in Wisconsin"],
        tier1_targets["PROP-DIV"]: ["Wisconsin property division", "property division in Wisconsin", "Wisconsin marital property division"],
        tier2_targets["PROP-DIV:NON_MARITAL"]: ["non-marital property in Wisconsin", "Wisconsin non-marital property", "what counts as non-marital property in Wisconsin"],
        tier2_targets["PROP-DIV:HIDDEN_ASSETS"]: ["hidden assets in a Wisconsin divorce", "finding hidden assets in Wisconsin divorce", "Wisconsin hidden assets in divorce"],
        tier1_targets["PT"]: ["Wisconsin paternity", "establish paternity in Wisconsin", "paternity lawyer in Wisconsin"],
        tier1_targets["GUARD"]: ["Wisconsin guardianship", "guardianship in Wisconsin", "Wisconsin guardianship lawyer"],
    }

    def infer_tier1_cluster(blog_url: str) -> str:
        p = url_path(blog_url).lower()
        # Use path keywords.
        if any(k in p for k in ["child-custody", "custody", "placement", "visitation", "parenting-plan"]):
            return "CH-CUS"
        if any(k in p for k in ["child-support", "support-order", "childsupport"]):
            return "CH-SUP"
        if any(k in p for k in ["spousal-support", "alimony", "maintenance"]):
            return "SPO-SUP"
        if any(k in p for k in ["property-division", "marital-property", "non-marital", "nonmarital", "hidden-asset", "hidden-assets", "assets", "debt"]):
            return "PROP-DIV"
        if "paternity" in p:
            return "PT"
        if "guardianship" in p or "guardian" in p:
            return "GUARD"
        if any(k in p for k in ["divorce", "separation", "annulment"]):
            return "DIV"
        # Default hub when intent is unclear.
        return "DIV"

    recs: List[Dict[str, Any]] = []
    for _, r in wi_blogs.iterrows():
        blog = r["Blog URL"]
        slug = url_path(blog).lower()

        target = ""
        matched_rule = ""
        for pattern, tier2_target in tier2_rules:
            if pattern.search(slug):
                target = normalize_url(tier2_target)
                matched_rule = pattern.pattern
                break

        if not target:
            cluster = infer_tier1_cluster(blog)
            target = normalize_url(tier1_targets[cluster])
            matched_rule = f"Tier-1:{cluster}"

        anchor = stable_pick(anchor_bank.get(target, [targets.loc[targets['URL'].eq(target), 'Practice Area'].head(1).item() if (targets['URL'] == target).any() else 'Wisconsin family law']), blog)
        if not anchor:
            anchor = "Wisconsin family law"

        recs.append(
            {
                "Action": "ADD_CONTEXTUAL",
                "Source URL": blog,
                "Current Target URL": "",
                "Suggested Target URL": target,
                "Suggested Anchor Text": anchor,
                "Placement Notes": "Place in-body within the first ~25% of the main narrative; avoid nav/footer modules.",
                "Target Tier": "Tier-2" if target in set(tier2["URL"]) else "Tier-1",
                "Rule Match": matched_rule,
                "Priority": "High",
            }
        )

    return pd.DataFrame(recs)


def generate_fix_recommendations(qa_issues: pd.DataFrame) -> pd.DataFrame:
    if qa_issues.empty:
        return pd.DataFrame(columns=["Action", "Source URL", "Current Target URL", "Suggested Target URL", "Anchor Text", "Notes", "Priority"])

    fixes: List[Dict[str, Any]] = []
    for _, r in qa_issues.iterrows():
        issue_type = r["Issue Type"]
        if str(issue_type).startswith("BLOG_SOURCE_"):
            continue
        source_url = r["Source URL"]
        current_target = r["Target URL (Normalized)"]
        suggested = r.get("Suggested Target URL", "") or ""
        anchor = r.get("Anchor Text", "") or ""
        notes = r.get("Notes", "") or ""
        status = str(r.get("Status Code (Export)", "")).strip()

        action = "REMOVE_OR_REPLACE"
        priority = "High"

        if issue_type in {"INTERNAL_404_TARGET", "HUB_NON_200_TARGET"}:
            action = "REPLACE_URL" if suggested else "REMOVE_OR_REPLACE"
        elif issue_type in {"NON_200_TARGET"}:
            action = "FIX_REDIRECT" if status in {"301", "302"} else "REPLACE_URL"
        elif issue_type in {"CROSS_STATE_LINK"}:
            action = "REPLACE_URL"
        elif issue_type in {"PLACEHOLDER_URL", "MALFORMED_URL"}:
            action = "REMOVE_OR_REPLACE"

        fixes.append(
            {
                "Action": action,
                "Source URL": source_url,
                "Current Target URL": current_target,
                "Suggested Target URL": suggested,
                "Anchor Text": anchor,
                "Notes": f"{issue_type}: {notes}".strip(),
                "Priority": priority,
            }
        )

    return pd.DataFrame(fixes).drop_duplicates().reset_index(drop=True)


def workbook_write(
    *,
    out_xlsx: Path,
    overview: pd.DataFrame,
    target_universe: pd.DataFrame,
    core_inlinks_audit: pd.DataFrame,
    core_outlinks_audit: pd.DataFrame,
    blog_outlinks_current: pd.DataFrame,
    qa_issues: pd.DataFrame,
    rec_add: pd.DataFrame,
    rec_fix: pd.DataFrame,
) -> None:
    out_xlsx.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        overview.to_excel(writer, index=False, sheet_name="Overview")
        target_universe.to_excel(writer, index=False, sheet_name="Target Universe")
        core_inlinks_audit.to_excel(writer, index=False, sheet_name="Core Inlinks Audit")
        core_outlinks_audit.to_excel(writer, index=False, sheet_name="Core Outlinks Audit")
        blog_outlinks_current.to_excel(writer, index=False, sheet_name="Blog Outlinks (Current)")
        qa_issues.to_excel(writer, index=False, sheet_name="QA Issues")
        rec_add.to_excel(writer, index=False, sheet_name="Recommendations (Add Links)")
        rec_fix.to_excel(writer, index=False, sheet_name="Recommendations (Fix Existing)")

    # Light formatting pass (column widths + freeze panes) without heavy styling.
    from openpyxl import load_workbook

    wb = load_workbook(out_xlsx)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for col_cells in ws.columns:
            max_len = 0
            col_letter = col_cells[0].column_letter
            for c in col_cells[:2000]:  # cap to keep runtime predictable
                v = "" if c.value is None else str(c.value)
                max_len = max(max_len, len(v))
            ws.column_dimensions[col_letter].width = min(max(12, max_len + 2), 70)
    wb.save(out_xlsx)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sterling Lawyers WI internal linking audit + recommendations generator.")
    parser.add_argument("--wi_blogs", required=True)
    parser.add_argument("--core_subserv", required=True)
    parser.add_argument("--all_blog_outlinks", required=True)
    parser.add_argument("--inlinks_divorce", required=True)
    parser.add_argument("--inlinks_child_custody", required=True)
    parser.add_argument("--inlinks_child_support", required=True)
    parser.add_argument("--inlinks_spousal_support", required=True)
    parser.add_argument("--inlinks_paternity", required=True)
    parser.add_argument("--inlinks_property_division", required=True)
    parser.add_argument("--inlinks_guardianship", required=True)
    parser.add_argument("--outlinks_divorce", required=True)
    parser.add_argument("--outlinks_child_custody", required=True)
    parser.add_argument("--outlinks_child_support", required=True)
    parser.add_argument("--outlinks_spousal_support", required=True)
    parser.add_argument("--outlinks_paternity", required=True)
    parser.add_argument("--outlinks_property_division", required=True)
    parser.add_argument("--outlinks_guardianship", required=True)
    parser.add_argument("--out_xlsx", required=True)
    parser.add_argument("--out_csv", required=True)
    args = parser.parse_args()

    curl = CurlResolver()

    wi_blogs = load_wi_blog_list(args.wi_blogs)
    targets = load_core_subservices(args.core_subserv)

    tier1_urls = set(targets[targets["Tier"].eq("Tier-1")]["URL"])
    tier2_urls = set(targets[targets["Tier"].eq("Tier-2")]["URL"])

    # Build core hub outlinks (all hubs) – also used for Tier-3 derivation.
    hub_outlinks_files = {
        "DIV": args.outlinks_divorce,
        "CH-CUS": args.outlinks_child_custody,
        "CH-SUP": args.outlinks_child_support,
        "SPO-SUP": args.outlinks_spousal_support,
        "PT": args.outlinks_paternity,
        "PROP-DIV": args.outlinks_property_division,
        "GUARD": args.outlinks_guardianship,
    }
    hub_outlinks_list: List[pd.DataFrame] = []
    for hub, path in hub_outlinks_files.items():
        df = read_sf_links(path)
        df["Hub"] = hub
        hub_outlinks_list.append(df)
    hub_outlinks_all = pd.concat(hub_outlinks_list, ignore_index=True) if hub_outlinks_list else pd.DataFrame(columns=SF_EXPECTED_COLUMNS + ["Hub"])
    hub_outlinks_all = normalize_sf_links(hub_outlinks_all)

    tier3 = derive_tier3_from_hub_outlinks(hub_outlinks_all, tier1_urls=tier1_urls, tier2_urls=tier2_urls)

    # Resolve Tier-3 redirect destinations (final QA evidence) – only for the shortlist.
    if not tier3.empty:
        statuses: List[int] = []
        effective: List[str] = []
        for u in tier3["URL"].tolist():
            res = curl.resolve(u)
            statuses.append(res.final_status)
            effective.append(res.effective_url)
        tier3["Curl Final Status"] = statuses
        tier3["Curl Effective URL"] = effective

    # Target Universe output (Tier-1/2 + Tier-3).
    target_universe = targets[["Tier", "URL", "Parent Cluster ID", "Practice Area", "H1"]].copy()
    if not tier3.empty:
        tier3_out = tier3[["Tier", "URL", "Parent Cluster ID", "Practice Area", "Source Hubs", "Occurrences", "Curl Final Status", "Curl Effective URL"]].copy()
        target_universe = pd.concat([target_universe, tier3_out], ignore_index=True, sort=False)

    # Inlinks: combine all practice files for a single audit table.
    inlinks_files = [
        args.inlinks_divorce,
        args.inlinks_child_custody,
        args.inlinks_child_support,
        args.inlinks_spousal_support,
        args.inlinks_paternity,
        args.inlinks_property_division,
        args.inlinks_guardianship,
    ]
    inlinks_all = pd.concat([read_sf_links(p) for p in inlinks_files], ignore_index=True)
    core_inlinks_audit = compute_inlinks_audit(inlinks_all, targets)

    # Core outlinks audit (content-only rows with issues).
    core_outlinks_audit = compute_core_outlinks_audit(hub_outlinks_all, targets, tier3)

    # Blog outlinks: filter big export to WI blog sources first, then normalize.
    blog_outlinks_raw = wi_blog_outlinks_filtered(args.all_blog_outlinks, wi_blogs)
    blog_outlinks_current = compute_blog_outlinks_current(blog_outlinks_raw, wi_blogs)

    # QA issues list + recommendation sets.
    qa_issues = build_qa_issues(blog_outlinks_current, core_outlinks_audit, curl)

    rec_add = generate_add_recommendations(wi_blogs, targets)

    # Remove/flag WI blogs missing from the outlinks export if they resolve to 404.
    # (This is also a practical safeguard against crawl gaps.)
    from_in_export = set(blog_outlinks_raw["From"].map(normalize_url)) if not blog_outlinks_raw.empty else set()
    missing_from_export = sorted(set(wi_blogs["Blog URL"]) - from_in_export)
    missing_404: List[str] = []
    missing_unknown: List[str] = []
    for blog in missing_from_export:
        res = curl.resolve(blog)
        if res.final_status == 404:
            missing_404.append(blog)
        else:
            missing_unknown.append(blog)

    qa_extra_rows: List[Dict[str, Any]] = []
    for blog in missing_404:
        qa_extra_rows.append(
            {
                "Issue Type": "BLOG_SOURCE_404",
                "Source Type": "Blog",
                "Source URL": blog,
                "Target URL (Raw)": "",
                "Target URL (Normalized)": "",
                "Anchor Text": "",
                "Link Position": "",
                "Status Code (Export)": "404",
                "Suggested Target URL": "",
                "Notes": "Source blog URL returns 404; remove from implementation list.",
            }
        )
    for blog in missing_unknown:
        qa_extra_rows.append(
            {
                "Issue Type": "BLOG_SOURCE_MISSING_FROM_EXPORT",
                "Source Type": "Blog",
                "Source URL": blog,
                "Target URL (Raw)": "",
                "Target URL (Normalized)": "",
                "Anchor Text": "",
                "Link Position": "",
                "Status Code (Export)": "",
                "Suggested Target URL": "",
                "Notes": "Blog URL not present in blog outlinks export; verify crawl coverage.",
            }
        )
    if qa_extra_rows:
        qa_issues = pd.concat([qa_issues, pd.DataFrame(qa_extra_rows)], ignore_index=True, sort=False).drop_duplicates().reset_index(drop=True)

    if missing_404:
        rec_add = rec_add[~rec_add["Source URL"].isin(missing_404)].reset_index(drop=True)

    rec_fix = generate_fix_recommendations(qa_issues)

    # Final target QA: validate every suggested target returns 200; if it redirects, swap to effective URL.
    impl_rows: List[pd.DataFrame] = [rec_add.copy(), rec_fix.copy()]
    implementation = pd.concat(impl_rows, ignore_index=True, sort=False).fillna("")

    if "Suggested Target URL" in implementation.columns:
        validated_status: List[int] = []
        validated_effective: List[str] = []
        for u in implementation["Suggested Target URL"].astype(str).tolist():
            if not u:
                validated_status.append(0)
                validated_effective.append("")
                continue
            res = curl.resolve(u)
            validated_status.append(res.final_status)
            validated_effective.append(res.effective_url)
        implementation["Curl Final Status"] = validated_status
        implementation["Curl Effective URL"] = validated_effective

        # Replace 301/302 suggested targets with their final 200 effective URL when present.
        redirect_mask = implementation["Curl Final Status"].isin([301, 302]) & implementation["Curl Effective URL"].ne("")
        implementation.loc[redirect_mask, "Suggested Target URL"] = implementation.loc[redirect_mask, "Curl Effective URL"]

    # Cross-state guardrail.
    cross_state_mask = implementation["Suggested Target URL"].astype(str).str.contains("/illinois/", case=False, regex=False)
    if cross_state_mask.any():
        implementation.loc[cross_state_mask, "Notes"] = implementation.loc[cross_state_mask, "Notes"].astype(str) + " [QA FAIL: Cross-state target]"

    # Uncontested vs contested guardrail.
    uncontested_src = implementation["Source URL"].astype(str).str.contains("uncontested", case=False, regex=False)
    uncontested_tgt_ok = implementation["Suggested Target URL"].astype(str).str.contains("/uncontested-divorce/", case=False, regex=False)
    bad_uncontested = uncontested_src & ~uncontested_tgt_ok & implementation["Action"].eq("ADD_CONTEXTUAL")
    if bad_uncontested.any():
        implementation.loc[bad_uncontested, "Notes"] = implementation.loc[bad_uncontested, "Notes"].astype(str) + " [QA FAIL: Uncontested mapping]"

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    implementation.to_csv(out_csv, index=False)

    # Overview KPIs.
    total_wi_blogs = int(wi_blogs.shape[0])
    blogs_in_outlinks_export = int(blog_outlinks_raw["From"].map(clean_url).nunique()) if not blog_outlinks_raw.empty else 0
    blog_content_links_rows = int(blog_outlinks_current.shape[0])

    # Current-state: how many blog content links point to Tier-1/2.
    tier12_set = set(targets[targets["Tier"].isin(["Tier-1", "Tier-2"])]["URL"])
    current_blog_content_to_tier12 = int(blog_outlinks_current["Target URL (Normalized)"].isin(tier12_set).sum()) if not blog_outlinks_current.empty else 0

    overview = pd.DataFrame(
        [
            {"Metric": "WI blogs (provided list)", "Value": total_wi_blogs},
            {"Metric": "WI blogs present in outlinks export (From)", "Value": blogs_in_outlinks_export},
            {"Metric": "WI blog content-link instances (internal hyperlinks)", "Value": blog_content_links_rows},
            {"Metric": "Current WI blog content links to Tier-1/2 targets", "Value": current_blog_content_to_tier12},
            {"Metric": "Add-link recommendations (1 per blog)", "Value": int(rec_add.shape[0])},
            {"Metric": "Fix-existing recommendations", "Value": int(rec_fix.shape[0])},
        ]
    )

    workbook_write(
        out_xlsx=Path(args.out_xlsx),
        overview=overview,
        target_universe=target_universe,
        core_inlinks_audit=core_inlinks_audit,
        core_outlinks_audit=core_outlinks_audit,
        blog_outlinks_current=blog_outlinks_current,
        qa_issues=qa_issues,
        rec_add=rec_add,
        rec_fix=rec_fix,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
