# Sterling WI — High-Performer ADD_CONTEXTUAL + Anchor Diversification (Augmented Backlink Set, Verified Missing-Only) — QA Report

## Files validated
- Updated XLSX: `output/spreadsheet/sterling_wi_internal_linking_dashboard_highperf_anchors_augmented_backlinks_verified_missing_only.xlsx`
- Updated implementation CSV: `output/spreadsheet/sterling_wi_internal_linking_dashboard_highperf_anchors_augmented_backlinks_verified_missing_only_implementation.csv`
- Anchor rationale CSV: `output/spreadsheet/sterling_wi_highperf_add_anchor_rationale_augmented_backlinks_verified_missing_only.csv`
- Baseline (augmented, verified missing-only) implementation CSV: `output/spreadsheet/sterling_wi_internal_linking_dashboard_implementation_augmented_backlinks_verified_missing_only.csv`
- GA4 export: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/wi_Page_path_and_screen_class.csv`
- GSC export: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/wi-gsc.csv`
- Ahrefs export: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/wi-ahrefs-blog.csv`
- Extra high-performer URL list (actionable only): `tmp/spreadsheets/sterling_wi_extra_high_perf_urls_backlinks_actionable.csv`
- Excluded sources list (404): `tmp/spreadsheets/sterling_wi_exclude_404_sources.csv`

## Key validated counts
- Updated implementation rows: **88**
  - ADD_CONTEXTUAL: **50**
  - FIX_REDIRECT: **36**
  - REMOVE_OR_REPLACE: **1**
  - REPLACE_URL: **1**

## High performer selection (recomputed)
- GA4 Top30 (Views) within audited sources: **30** (cutoff Views ≥ **56**) 
- GSC Top20 (Impressions) within audited sources: **20** (cutoff Impressions ≥ **756**) 
- Ahrefs Top20 (Live backlinks) within audited sources: **4**
- Extra (forced) sources added: **6**
- Excluded sources (QA 404 list): **1**
- Final high-performer union size: **50**

### Overlap (informational)
- GA4 ∩ GSC overlap: **4**
- GA4 ∩ Ahrefs overlap: **0**
- GSC ∩ Ahrefs overlap: **0**

## Core target scope (no subservices as targets)
- Unique Suggested Target URLs in ADD_CONTEXTUAL output: **6**
- Targets used:
  - https://www.sterlinglawyers.com/wisconsin/child-custody/
  - https://www.sterlinglawyers.com/wisconsin/child-support/
  - https://www.sterlinglawyers.com/wisconsin/divorce/
  - https://www.sterlinglawyers.com/wisconsin/paternity/
  - https://www.sterlinglawyers.com/wisconsin/property-division/
  - https://www.sterlinglawyers.com/wisconsin/spousal-support/

## Guardianship as a core target
- ADD_CONTEXTUAL rows targeting Guardianship: **0**
- Recommendation: keep Guardianship in the anchor bank, but treat as conditional until WI blog/content inventory includes guardianship-relevant pages.

## IL/WI separation check
- /illinois/ present in ADD_CONTEXTUAL Source URL: **False**
- /illinois/ present in ADD_CONTEXTUAL Suggested Target URL: **False**

## Curl/HTTP validation
- Full curl validation could not be re-run end-to-end at generation time due to intermittent DNS/network restrictions in this environment (curl intermittently returned `Could not resolve host`).
- The excluded 404 source is tracked in `tmp/spreadsheets/sterling_wi_exclude_404_sources.csv` and was removed from the final high-performer output.

## Result
- Passed: internal consistency checks (counts, scopes, targets, no IL contamination).
