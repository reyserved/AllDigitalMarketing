# Sterling WI: Blog Internal Linking Audit (Core Hubs Only)

Core targets in-scope (7): Divorce, Child Custody, Child Support, Spousal Support, Property Division, Paternity, Guardianship.

## Key findings
- WI blog URLs provided: **317**
- WI blogs present in `all_blog_outlinks.csv`: **316** (missing **1**) 
  - Missing example: `https://www.sterlinglawyers.com/wisconsin/blog/clients-journey-racine-child-support-lawyer`
- WI blog → 7 core hub *content* hyperlinks: **0** (all observed links to these hubs are currently Navigation/Footer)

## Core hub coverage from WI blogs (any position)
- Child Custody: **316** WI blogs, **1264** instances (Content 0, Nav 316, Footer 948)
- Child Support: **316** WI blogs, **948** instances (Content 0, Nav 316, Footer 632)
- Divorce: **316** WI blogs, **1264** instances (Content 0, Nav 316, Footer 948)
- Guardianship: **316** WI blogs, **948** instances (Content 0, Nav 316, Footer 632)
- Paternity: **316** WI blogs, **316** instances (Content 0, Nav 316, Footer 0)
- Property Division: **316** WI blogs, **948** instances (Content 0, Nav 316, Footer 632)
- Spousal Support: **316** WI blogs, **1264** instances (Content 0, Nav 316, Footer 948)

## Guardianship: does it deserve to be a core blog target?
- WI blog slugs containing `guardianship`: **0** (containing `guardian`: **0**)
- WI blog internal content links to `/wisconsin/guardianship/*`: **0** instances across **0** WI blogs
- Interpretation: Guardianship appears to have **no observable topical footprint** in the current WI blog URL set and **no in-content internal linking** to Guardianship pages. I’d include it as a core target **only when the blog is Guardianship/guardian-related**, not as a blanket requirement for every blog post.

## QA
- Outlinks vs inlinks instance counts match for WI blogs on the 7 core hub URLs (see `QA_CoreHubCounts` sheet).