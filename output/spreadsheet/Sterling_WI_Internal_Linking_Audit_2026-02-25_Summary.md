# Sterling WI: Blog Internal Linking Audit (Core Pages + Blogs)

## Inputs used
- wi_blogs: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/Copy of Sterling Lawyers WI _ Content Mapping  - Sheet25.csv`
- core_subserv: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/Copy of Sterling Lawyers WI _ Content Mapping  - core-subserv.csv`
- all_blog_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/all_blog_outlinks.csv`
- divorce_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-divorce-all-inlinks.csv`
- child_custody_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-child-custody-all-inlinks.csv`
- child_support_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-child-support-inlinks.csv`
- spousal_alimony_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-spousal-alimony-inlinks.csv`
- paternity_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-paternity-all-inlinks.csv`
- property_division_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-property-division-inlinks.csv`
- guardianship_inlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/core-guardianship-all-inlinks.csv`
- divorce_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/divorce-outlinks.csv`
- child_custody_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/child-custody-outlinks.csv`
- child_support_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/child-support-outlinks.csv`
- spousal_support_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/spousal-support-outlinks.csv`
- paternity_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/paternity-outlinks.csv`
- property_division_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/property-division-outlinks.csv`
- guardianship_outlinks: `/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/guardianship-all-outlinks.csv`

## Key findings (data-backed)
- WI blog URLs provided: **317**
- WI blogs found in `all_blog_outlinks.csv`: **316** (missing **1**)
  - Missing example: `https://www.sterlinglawyers.com/wisconsin/blog/clients-journey-racine-child-support-lawyer`
- WI blog → core/subservice *content* links (to the 19 provided target URLs): **0**
- Target URLs linked from WI blogs at all (any position): **8/19**
- Subservice URLs linked from WI blogs at all (any position): **1/12**

## Where WI blog *content* hyperlinks currently go (internal only; top buckets)
- `/wisconsin/locations`: **630**
- `/wisconsin/blog`: **320**
- `/reviews`: **316**
- `/wisconsin/attorneys`: **314**
- `/wisconsin/divorce`: **11**
- `/case-law`: **3**
- `/news`: **2**
- `/flourishing-families`: **2**
- `/wisconsin/child-support`: **1**
- `/wisdom-from-attorney-knighton`: **1**

## QA
- Outlinks vs inlinks instance counts match for WI blogs on the target URLs present in both datasets (see `QA_TargetCounts` sheet).
- WI blog internal *content* hyperlinks include **58** redirects (301) and **1** broken internal link (404) (see `WI_Blog_Content_Internal` sheet).

## Next info I’d want from you (to make link-add recommendations per blog)
- A blog→practice-area mapping (even 1 column: blog URL + primary practice area), or your intended rule (e.g., each blog must link to its primary hub + 1 relevant subservice).
- Any link/anchor constraints (exact-match limits, preferred anchors, whether to avoid footer/nav links in reporting).
