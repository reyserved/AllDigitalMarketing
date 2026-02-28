# Sterling WI — Ahrefs Backlinks Selection Report (Why Ahrefs added 0 to High-Performers)

## Inputs
- Baseline implementation (audited ADD_CONTEXTUAL sources): `output/spreadsheet/sterling_wi_internal_linking_dashboard_implementation.csv`
- Ahrefs export (UTF-16 TSV): `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/wi-ahrefs-blog.csv`

## Executive summary
- Ahrefs rows total: **61**
- Live backlinks rows (Lost blank): **30**
- Lost backlinks rows (Lost non-empty): **31**
- Live rows targeting WI blog posts: **30**
- Lost rows targeting WI blog posts: **28**
- Unique WI blog targets in this Ahrefs export (canonical): **38**
- Unique WI blog targets with ≥1 LIVE backlink: **22**
- Unique audited WI blogs with ≥1 LIVE backlink: **0**

## Why Ahrefs contributed 0 to the high-performer set
The selection uses **only LIVE backlinks** and then requires the target blog to be **in the audited WI blog universe** (baseline ADD_CONTEXTUAL sources).

1) **LIVE filter**: 30 live rows kept; 31 lost rows excluded.
2) **WI blog target filter**: 30 live rows remain after requiring canonical targets match `/wisconsin/blog/<slug>/`. 
3) **Top-20 selection**: live targets are ranked primarily by `Referring domains`, then `Quality-weighted backlinks`, then `Dofollow backlinks`, then `Live backlinks`.
4) **Audited-scope intersection**: `top20_live_targets ∩ audited_wi_blog_set` = **0** → therefore **0** were added.

### The 7 “candidate” audited WI blogs were excluded because their backlinks are LOST (not live)
- Audited WI blog targets with backlinks in this Ahrefs file: **7**
- Audited WI blog targets with LIVE backlinks in this file: **0**
Audited targets that appear in Ahrefs but have only LOST backlinks:
- `https://www.sterlinglawyers.com/wisconsin/blog/attorneys-compass-guiding-through-military-divorce-madison/`
- `https://www.sterlinglawyers.com/wisconsin/blog/complications-military-divorce-milwaukee/`
- `https://www.sterlinglawyers.com/wisconsin/blog/guidance-road-of-military-divorce-west-bend-lawyers/`
- `https://www.sterlinglawyers.com/wisconsin/blog/legal-assistance-west-bend-military-divorce-cases/`
- `https://www.sterlinglawyers.com/wisconsin/blog/military-divorce-insight-assistance-sheboygan-county/`
- `https://www.sterlinglawyers.com/wisconsin/blog/sheboygan-lawyers-illuminate-path-military-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/unpacking-military-divorce-complexity-milwaukee-attorney/`

### The WI blogs that *do* have LIVE backlinks are outside the audited WI blog set
- Unique WI blog targets with LIVE backlinks: **22**
- Of those, in audited set: **0**
Top live targets (for context):
- `https://www.sterlinglawyers.com/wisconsin/blog/methods-marketing-firm/` — ref domains 3, live rows 3, dofollow 0, nofollow 3, spam-flagged 0, quality-weighted 1.50
- `https://www.sterlinglawyers.com/wisconsin/blog/do-the-court-records-from-a-divorce-become-public-record/` — ref domains 2, live rows 4, dofollow 4, nofollow 0, spam-flagged 4, quality-weighted 0.80
- `https://www.sterlinglawyers.com/wisconsin/blog/leaving-ex-family-business/` — ref domains 1, live rows 1, dofollow 1, nofollow 0, spam-flagged 0, quality-weighted 1.00
- `https://www.sterlinglawyers.com/wisconsin/blog/sex-after-separation/` — ref domains 1, live rows 1, dofollow 1, nofollow 0, spam-flagged 0, quality-weighted 1.00
- `https://www.sterlinglawyers.com/wisconsin/blog/being-your-childs-support-system/` — ref domains 1, live rows 2, dofollow 2, nofollow 0, spam-flagged 2, quality-weighted 0.40
- `https://www.sterlinglawyers.com/wisconsin/blog/can-prenup-presiding-event-death-exercised-divorce/` — ref domains 1, live rows 2, dofollow 2, nofollow 0, spam-flagged 2, quality-weighted 0.40
- `https://www.sterlinglawyers.com/wisconsin/blog/divorce-and-the-cobra-act/` — ref domains 1, live rows 2, dofollow 2, nofollow 0, spam-flagged 2, quality-weighted 0.40
- `https://www.sterlinglawyers.com/wisconsin/blog/annulments-work-wisconsin/` — ref domains 1, live rows 1, dofollow 1, nofollow 0, spam-flagged 1, quality-weighted 0.20
- `https://www.sterlinglawyers.com/wisconsin/blog/can-claim-sons-life-insurance-knowing-wanted/` — ref domains 1, live rows 1, dofollow 1, nofollow 0, spam-flagged 1, quality-weighted 0.20
- `https://www.sterlinglawyers.com/wisconsin/blog/creating-wisconsin-parenting-plan/` — ref domains 1, live rows 1, dofollow 1, nofollow 0, spam-flagged 1, quality-weighted 0.20

## What “quality-weighted” means (and why)
Quality-weighted backlinks = sum of per-link weights to avoid treating all backlinks equally.
This run uses exactly:
- Followed link (`Nofollow = False`) → **1.0**
- Nofollow link (`Nofollow = True`) → **0.5**
- Spam-flag multiplier (`Is spam = True`) → **× 0.2** (soft penalty; not exclusion)
This weight is used as a tie-breaker in ranking (after referring domains).

## URL lists by flagged issue
Full lists exported to: `output/spreadsheet/sterling_wi_ahrefs_backlinks_issue_urls_2026-02-27.csv`

### Redirect-chain present (canonicalization changed target)
- Unique WI blog targets with any redirect-chain row: **11**
- Row-level redirect details exported to: `output/spreadsheet/sterling_wi_ahrefs_backlinks_redirect_chains_2026-02-27.csv`
- `https://www.sterlinglawyers.com/wisconsin/blog/being-your-childs-support-system/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-failure-pay-felony/`
- `https://www.sterlinglawyers.com/wisconsin/blog/divorce-and-the-cobra-act/`
- `https://www.sterlinglawyers.com/wisconsin/blog/do-the-court-records-from-a-divorce-become-public-record/`
- `https://www.sterlinglawyers.com/wisconsin/blog/faithfully-making-marriage-fireproof-pt-1/`
- `https://www.sterlinglawyers.com/wisconsin/blog/how-can-i-collect-child-support-from-someone-who-is-self-employed/`
- `https://www.sterlinglawyers.com/wisconsin/blog/international-child-abduction/`
- `https://www.sterlinglawyers.com/wisconsin/blog/methods-marketing-firm/`
- `https://www.sterlinglawyers.com/wisconsin/blog/sex-after-separation/`
- `https://www.sterlinglawyers.com/wisconsin/blog/will-business-travel-impact-chance-of-getting-custody/`
- `https://www.sterlinglawyers.com/wisconsin/blog/wisconsin-law-question-adultery/`

### Lost-only WI blog targets (no live backlinks in this export)
- Unique lost-only targets: **16** (audited: **7**, not audited: **9**) 

Audited (these are the 7 candidates you referenced):
- `https://www.sterlinglawyers.com/wisconsin/blog/attorneys-compass-guiding-through-military-divorce-madison/`
- `https://www.sterlinglawyers.com/wisconsin/blog/complications-military-divorce-milwaukee/`
- `https://www.sterlinglawyers.com/wisconsin/blog/guidance-road-of-military-divorce-west-bend-lawyers/`
- `https://www.sterlinglawyers.com/wisconsin/blog/legal-assistance-west-bend-military-divorce-cases/`
- `https://www.sterlinglawyers.com/wisconsin/blog/military-divorce-insight-assistance-sheboygan-county/`
- `https://www.sterlinglawyers.com/wisconsin/blog/sheboygan-lawyers-illuminate-path-military-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/unpacking-military-divorce-complexity-milwaukee-attorney/`

Not audited:
- `https://www.sterlinglawyers.com/wisconsin/blog/can-child-support-increased-make-now/`
- `https://www.sterlinglawyers.com/wisconsin/blog/changing-your-name/`
- `https://www.sterlinglawyers.com/wisconsin/blog/child-support-payment-lengths-and-exceptions/`
- `https://www.sterlinglawyers.com/wisconsin/blog/child-support-payments-and-exceptions/`
- `https://www.sterlinglawyers.com/wisconsin/blog/faithfully-making-marriage-fireproof-pt-1/`
- `https://www.sterlinglawyers.com/wisconsin/blog/how-can-i-collect-child-support-from-someone-who-is-self-employed/`
- `https://www.sterlinglawyers.com/wisconsin/blog/when-are-we-legally-separated/`
- `https://www.sterlinglawyers.com/wisconsin/blog/will-business-travel-impact-chance-of-getting-custody/`
- `https://www.sterlinglawyers.com/wisconsin/blog/wisconsin-law-question-adultery/`

### Live-only WI blog targets (live backlinks exist; but outside audited set)
- Unique live-only targets: **16**
- `https://www.sterlinglawyers.com/wisconsin/blog/annulments-work-wisconsin/`
- `https://www.sterlinglawyers.com/wisconsin/blog/being-your-childs-support-system/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-claim-sons-life-insurance-knowing-wanted/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-prenup-presiding-event-death-exercised-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/custody-shift-parental-rights/`
- `https://www.sterlinglawyers.com/wisconsin/blog/divorce-and-the-cobra-act/`
- `https://www.sterlinglawyers.com/wisconsin/blog/do-the-court-records-from-a-divorce-become-public-record/`
- `https://www.sterlinglawyers.com/wisconsin/blog/fault-grounds-for-bed-and-board-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/helping-children-divorce-separation/`
- `https://www.sterlinglawyers.com/wisconsin/blog/leaving-ex-family-business/`
- `https://www.sterlinglawyers.com/wisconsin/blog/milwakee-divorce-lawyer-question-000001/`
- `https://www.sterlinglawyers.com/wisconsin/blog/must-prove-file-claim-negligence-old-attorney/`
- `https://www.sterlinglawyers.com/wisconsin/blog/prenuptial-agreement-viewed-one-sided/`
- `https://www.sterlinglawyers.com/wisconsin/blog/refusing-visitation/`
- `https://www.sterlinglawyers.com/wisconsin/blog/survivorship-marital-property/`
- `https://www.sterlinglawyers.com/wisconsin/blog/will-prenuptial-agreement-hold-court/`

### Mixed live + lost WI blog targets
- Unique mixed targets: **6**
- `https://www.sterlinglawyers.com/wisconsin/blog/can-failure-pay-felony/`
- `https://www.sterlinglawyers.com/wisconsin/blog/child-support-and-bankruptcy/`
- `https://www.sterlinglawyers.com/wisconsin/blog/creating-wisconsin-parenting-plan/`
- `https://www.sterlinglawyers.com/wisconsin/blog/international-child-abduction/`
- `https://www.sterlinglawyers.com/wisconsin/blog/methods-marketing-firm/`
- `https://www.sterlinglawyers.com/wisconsin/blog/sex-after-separation/`

### Spam-flagged LIVE backlinks present (soft-penalized, not excluded)
- Unique targets with spam-flagged LIVE rows: **19**
- `https://www.sterlinglawyers.com/wisconsin/blog/annulments-work-wisconsin/`
- `https://www.sterlinglawyers.com/wisconsin/blog/being-your-childs-support-system/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-claim-sons-life-insurance-knowing-wanted/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-failure-pay-felony/`
- `https://www.sterlinglawyers.com/wisconsin/blog/can-prenup-presiding-event-death-exercised-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/child-support-and-bankruptcy/`
- `https://www.sterlinglawyers.com/wisconsin/blog/creating-wisconsin-parenting-plan/`
- `https://www.sterlinglawyers.com/wisconsin/blog/custody-shift-parental-rights/`
- `https://www.sterlinglawyers.com/wisconsin/blog/divorce-and-the-cobra-act/`
- `https://www.sterlinglawyers.com/wisconsin/blog/do-the-court-records-from-a-divorce-become-public-record/`
- `https://www.sterlinglawyers.com/wisconsin/blog/fault-grounds-for-bed-and-board-divorce/`
- `https://www.sterlinglawyers.com/wisconsin/blog/helping-children-divorce-separation/`
- `https://www.sterlinglawyers.com/wisconsin/blog/international-child-abduction/`
- `https://www.sterlinglawyers.com/wisconsin/blog/milwakee-divorce-lawyer-question-000001/`
- `https://www.sterlinglawyers.com/wisconsin/blog/must-prove-file-claim-negligence-old-attorney/`
- `https://www.sterlinglawyers.com/wisconsin/blog/prenuptial-agreement-viewed-one-sided/`
- `https://www.sterlinglawyers.com/wisconsin/blog/refusing-visitation/`
- `https://www.sterlinglawyers.com/wisconsin/blog/survivorship-marital-property/`
- `https://www.sterlinglawyers.com/wisconsin/blog/will-prenuptial-agreement-hold-court/`

### Nofollow-only LIVE backlinks
- Unique targets with LIVE backlinks but all nofollow: **4**
- `https://www.sterlinglawyers.com/wisconsin/blog/can-failure-pay-felony/`
- `https://www.sterlinglawyers.com/wisconsin/blog/child-support-and-bankruptcy/`
- `https://www.sterlinglawyers.com/wisconsin/blog/methods-marketing-firm/`
- `https://www.sterlinglawyers.com/wisconsin/blog/refusing-visitation/`

### Canonical targets that are NOT WI blog URLs (filtered out of the WI-blog-only step)
- Rows: **3** (all lost)
- `https://www.sterlinglawyers.com/dan-exner-no-index/faithfully-making-marriage-fireproof-pt-1/`
- `https://www.sterlinglawyers.com/jeff-hughes-no-index/methods-marketing-firm/`
- `https://www.sterlinglawyers.com/topic/will-business-travel-impact-chance-of-getting-custody/`

## QA / Repro
- Aggregated per-target metrics exported to: `output/spreadsheet/sterling_wi_ahrefs_backlinks_targets_2026-02-27.csv`
- Counts in this report match the earlier QA (61 total rows; 30 live rows; audited-live overlap = 0).