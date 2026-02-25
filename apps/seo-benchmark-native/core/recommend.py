from __future__ import annotations

from typing import Dict, List, Sequence

from .schemas import ALLOWED_TAGS


def _append_unique(target: List[str], value: str) -> None:
    if value not in target:
        target.append(value)


def compute_tags(
    l3m: Dict[str, float],
    mom: Dict[str, float],
    yoy: Dict[str, float],
    weak_high_impr_pages: int,
    coverage_ratio_users: float,
    coverage_ratio_events: float,
) -> List[str]:
    tags: List[str] = []

    l3m_click_delta = l3m.get("click_delta_pct")
    yoy_click_delta = yoy.get("click_delta_pct")
    l3m_impr_delta = l3m.get("impr_delta_pct")
    yoy_impr_delta = yoy.get("impr_delta_pct")
    l3m_ctr_pp = l3m.get("ctr_pp")
    yoy_ctr_pp = yoy.get("ctr_pp")
    mom_impr_delta = mom.get("impr_delta_pct")

    fundamentals_trigger = (
        (l3m_click_delta is not None and yoy_click_delta is not None and l3m_click_delta <= -10 and yoy_click_delta <= -10)
        or (l3m_impr_delta is not None and l3m_impr_delta <= -15)
        or (yoy_impr_delta is not None and yoy_impr_delta <= -15)
    )
    if fundamentals_trigger:
        _append_unique(tags, "Fundamentals")

    refresh_trigger = (
        (
            l3m_impr_delta is not None
            and l3m_impr_delta > 0
            and ((l3m_click_delta is not None and l3m_click_delta <= 0) or (l3m_ctr_pp is not None and l3m_ctr_pp <= 0))
        )
        or (l3m_ctr_pp is not None and l3m_ctr_pp <= -0.10)
        or (yoy_ctr_pp is not None and yoy_ctr_pp <= -0.10)
    )
    if refresh_trigger:
        _append_unique(tags, "Content Refresh")

    technical_trigger = (
        (coverage_ratio_users < 0.70)
        or (coverage_ratio_events < 0.70)
        or (mom_impr_delta is not None and mom_impr_delta <= -25)
    )
    if technical_trigger:
        _append_unique(tags, "Technical Assessment")

    if weak_high_impr_pages >= 3:
        _append_unique(tags, "Internal Linking")

    # Guardrails: return 2-4 tags and ensure vocabulary.
    fallback = ["Content Refresh", "Internal Linking", "Technical Assessment", "Fundamentals"]
    for item in fallback:
        if len(tags) >= 2:
            break
        _append_unique(tags, item)

    tags = [t for t in tags if t in ALLOWED_TAGS][:4]
    return tags


def build_why_recommendation(
    l3m: Dict[str, float],
    mom: Dict[str, float],
    yoy: Dict[str, float],
    weak_high_impr_pages: int,
) -> str:
    def pct(v: float) -> str:
        if v is None:
            return "N/A"
        return f"{v:.2f}%"

    def pp(v: float) -> str:
        if v is None:
            return "N/A"
        sign = "+" if v > 0 else ""
        return f"{sign}{v:.2f} pp"

    return (
        "Tag rationale: "
        f"L3M click/impression deltas {pct(l3m.get('click_delta_pct'))}/{pct(l3m.get('impr_delta_pct'))}, "
        f"YoY deltas {pct(yoy.get('click_delta_pct'))}/{pct(yoy.get('impr_delta_pct'))}, "
        f"MoM impression shift {pct(mom.get('impr_delta_pct'))}, "
        f"CTR shifts L3M {pp(l3m.get('ctr_pp'))} and YoY {pp(yoy.get('ctr_pp'))}. "
        f"Weak high-impression pages detected: {weak_high_impr_pages}."
    )


def build_action_plan(bucket: str) -> str:
    lower = bucket.lower()

    if lower == "service":
        return (
            "1) Align intent for declining service URLs by tightening title/H1 focus and adding high-intent supporting sections. "
            "2) Upgrade conversion blocks on high-traffic pages (offer clarity, trust proof, and CTA placement). "
            "3) Validate service schema and fix metadata length/consistency issues. "
            "4) Add contextual internal links from supporting pages into priority service pages."
        )

    if lower == "location":
        return (
            "1) Expand local uniqueness on branch/location pages with city-specific details and proof points. "
            "2) Improve local SERP alignment using geo-focused title/meta variants and branch FAQs. "
            "3) Validate LocalBusiness/NAP consistency and event tracking coverage. "
            "4) Strengthen links from relevant service pages to location pages with geo anchors."
        )

    if lower == "supporting":
        return (
            "1) Add stronger CTA pathways from informational pages into target service/location pages. "
            "2) Refresh content sections to better match observed query intent and click behavior. "
            "3) Improve hub-style internal linking from resources/about pages to demand-driving URLs. "
            "4) Expand instrumentation for supporting-page engagement to improve attribution confidence."
        )

    if "blog" in lower:
        return (
            "1) Refresh top-decay blog posts for intent match and freshness signals. "
            "2) Add conversion-aware CTAs and contextual links from blogs into service pages. "
            "3) Consolidate overlapping posts and strengthen topical clustering by theme. "
            "4) Improve snippet targeting with clearer headings and entity-rich summaries."
        )

    if "service area" in lower or "practice" in lower:
        return (
            "1) Improve geo-intent and legal-intent alignment with unique localized copy and FAQs. "
            "2) Clarify differentiation between service area and core practice pages. "
            "3) Reinforce internal linking between location intent pages and core conversion pages. "
            "4) Validate local/practice schema and consistency of entity references."
        )

    return (
        "1) Prioritize declining URLs in this bucket for intent and metadata alignment updates. "
        "2) Strengthen conversion pathways to business-critical pages through clearer CTAs and internal links. "
        "3) Fix tracking/measurement blind spots for users and key events where coverage is low. "
        "4) Re-evaluate this bucket monthly using the same benchmark framework for trend confirmation."
    )
