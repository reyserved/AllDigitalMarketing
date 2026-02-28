# Sterling WI — High Performers Breakdown (GA4 + GSC + Ahrefs)

Definition used (per your instructions):
- GA4: Top 30 WI **blog posts** by Views (`/wisconsin/blog/...`)
- GSC: Top 20 WI **blog URLs** by Impressions (`/wisconsin/blog/...`)
- Ahrefs: Top 20 WI **blog URLs** by *live* backlinks (ranked by live Ref Domains, then quality-weighted, then dofollow, then live rows)

- Output breakdown CSV: `output/spreadsheet/sterling_wi_high_performer_breakdown_ga4_gsc_ahrefs_2026-02-28.csv`

## Counts
- GA4 Top30 (blog posts): **30**
- GSC Top20 (blog URLs by impressions): **20**
- Ahrefs Top20 (blog URLs by live ref domains): **20**
- GA4∩GSC: **4**
- GA4∩Ahrefs: **0**
- GSC∩Ahrefs: **0**
- GA4∩GSC∩Ahrefs: **0**
- Union (GA4 ∪ GSC ∪ Ahrefs): **66**
- Union ∩ audited set (317): **46**
- Union outside audited set: **20**

## Cutoffs (from provided exports)
- GA4 Top30 cutoff views (rank 30): **56**
- GSC Top20 cutoff impressions (rank 20): **715**
- Ahrefs Top20 cutoff ref domains (rank 20): **1**

## Notes
- “Union outside audited set” means those URLs appear in GA4/GSC/Ahrefs top-lists but are not in `Copy of Sterling Lawyers WI _ Content Mapping  - Sheet25.csv` (317 audited WI blogs).
- If you want those outside-audit URLs included for ADD_CONTEXTUAL recommendations, we need to expand the audited content list and regenerate the baseline dashboard recommendations for those additional sources.
