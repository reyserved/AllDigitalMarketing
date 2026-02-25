# Live Audit Report: Idaho Fundraising Services Page

- URL: `https://chisholmfirm.com/idaho/fundraising-services/`
- Audit date: `2026-02-20`
- Method: live fetch + rendered browser validation + desktop/mobile section screenshots
- Scope: hero through final CTA

## Severity Key

- `P1`: broken CTA/link or legal-content risk
- `P2`: layout/spec mismatch or structural implementation issue
- `P3`: visual polish or UX quality issue

## Section-by-Section Audit

| Section | Status | Severity | Observation | Remediation |
|---|---|---:|---|---|
| Hero (headline, value props, trust logos, right-side consultation form) | Shipped correctly | - | Two-column hero structure is live and aligned with intended IA. Trust badges and form module render as expected. | No corrective action required. |
| Understanding the Fundraising Environment in Idaho | Shipped correctly | - | Heading, explanatory copy, and supporting bullet list render in sequence with expected spacing and hierarchy. | No corrective action required. |
| Our Fundraising Services in Idaho | Shipped correctly | - | Dark section with three service cards shipped with expected content blocks and imagery. | No corrective action required. |
| Common Fundraising Challenges Facing Idaho Nonprofits (compliance box + challenge cards) | Partially shipped | `P2` | Compliance card is correctly positioned above challenges. Challenge cards render as wrapped rows (3+2) on desktop rather than strict single horizontal five-card layout. | Update card container to a true five-column desktop grid or horizontal track behavior based on approved spec. |
| Common Fundraising Challenges card visual emphasis | Partially shipped | `P3` | Challenge cards are visually muted and lower-contrast than target mockup direction; hierarchy between title/body/icon is weaker than intended. | Increase card contrast, title weight, and icon/number prominence while preserving brand color constraints. |
| Nonprofits We Commonly Support in Idaho | Shipped correctly | - | Dark support section with five category tiles shipped and content order is correct. | No corrective action required. |
| Areas We Serve Across Idaho | Partially shipped | `P2` | "Central Idaho" includes a descriptive line rendered as heading text (`H4`) instead of paragraph body, creating semantic and style inconsistency. | Convert description to paragraph/body text and normalize heading hierarchy across all area cards. |
| Why Nonprofits in Idaho Work With Chisholm Law Firm | Partially shipped | `P1` | "Meet the Team" button resolves to `#` anchor instead of destination URL; this is a broken CTA path. | Replace placeholder anchor with correct target URL and verify click-through behavior. |
| Read Our Success Stories | Shipped correctly | - | Testimonial cards and supporting CTA appear in expected section order with working external links. | No corrective action required. |
| Book Promo Band (Bestselling Book CTA) | Shipped correctly | - | Book banner and CTA copy are live and visually coherent with existing brand section treatment. | No corrective action required. |
| FAQs | Shipped correctly | - | FAQ block renders with expected list/accordion rows and consistent section placement. | No corrective action required. |
| Final CTA ("Explore Fundraising Support Options") | Shipped correctly | - | Final CTA section and button are present and visually consistent with theme. | No corrective action required. |

## Cross-Section UX Notes

- Sticky bottom conversion bar (`Read Reviews` / `Book My Consult`) is persistently visible and can compete with lower-page CTAs and content comprehension.
- Headings are largely consistent, but the areas section contains one confirmed semantic mismatch described above.

## Priority Fix Queue

1. `P1`: Fix broken `Meet the Team` CTA destination.
2. `P2`: Enforce approved desktop layout behavior for five challenge cards.
3. `P2`: Correct heading/body semantic mismatch in Central Idaho area card.
4. `P3`: Increase challenge card visual hierarchy to match approved design intent.
5. `P3`: Reassess sticky bottom bar behavior to reduce distraction on long-form sections.
