# Construction Loan Special 4.590% - Paid Landing Page Copy and Elementor Guide

## 1. Paid Landing Page Copy (Google Paid-Search Optimized)

### Page Meta
- **SEO Title:** Construction Loan Special 4.590% Rate | Wisconsin Construction Loan | Bank Five Nine
- **Meta Description:** Build your dream home with Bank Five Nine's Construction Loan Special: 11-month term, 4.590% rate, 5.718% APR. Talk to a Wisconsin lender today.
- **Recommended URL Slug:** `/construction-loan-special-459`
- **Robots:** noindex, nofollow

### Ad-Intent Copy Positioning
This page is designed to match paid search intent for:
- `construction loan`
- `4.59 construction loan`
- `Wisconsin construction loan`

### Hero Section
**H1:**
Construction Loan Special - 11-Month Term with 4.590% Rate and 5.718% APR

**Subheadline:**
Build in Wisconsin with a portfolio construction loan designed for owner-occupied, single-family homes. Lock in a limited-time rate and work directly with a Bank Five Nine lender.

**Body Copy:**
If you are actively searching for a Wisconsin construction loan, this offer is built for qualified borrowers who want a clear path from lot + build financing to completion. After construction is complete, the loan is typically refinanced, and lender credits based on the rate at that time can be used to offset fees.

**Primary CTA (button):**
Talk to a Bank Five Nine Lender

**Primary CTA link placeholder:**
`[LENDER_EMAIL_OR_FORM_URL]`

**Secondary CTA (text link):**
Call a Lender: `[LENDER_PHONE]`

---

### Section: Why This Construction Loan Stands Out
**H2:**
A Focused Construction Loan Offer for Qualified Wisconsin Buyers

**Body Copy:**
Not many lenders offer this unique construction loan product. This special includes a competitive fixed rate, an 11-month term structure, and flexible draw mechanics so you can focus on your build timeline.

**Support bullets:**
- 11-month term construction loan
- 4.590% interest rate
- 5.718% APR
- Interest-only payments during construction
- Flexible draw process with no set schedules

---

### Section: How Payment Works
**H2:**
How the Payment Scenario Works

**Body Copy:**
The sample scenario assumes a **half-drawn construction loan** with a closing date of **2/1/2026** and a maturity date of **1/1/2027**. The first 10 monthly payments are interest-only based on the dollar amount drawn at that time. The final balloon payment equals the principal balance plus interest.

In this sample scenario, a **$500,000 purchase price** with a **15% down payment** creates a **$425,000 loan amount** at **4.590%**, resulting in the payment snapshot shown here.

Payment estimates do not include amounts for taxes and hazard insurance.

**Plain-language payment summary:**
Payment snapshot values:
- **10 payments at $811.40**
- **1 final payment at $425,811.40**

---

### Section: Qualification Snapshot
**H2:**
Construction Loan Special Qualifications

**Body Copy:**
This offer is designed for qualified borrowers who meet credit, occupancy, and relationship requirements.

**Qualification list:**
- 700 minimum credit score
- Maximum 85% loan to value, up to $832,750 loan size
- Single-family, owner-occupied construction in Wisconsin only
- Consolidate construction and lot purchase for only one set of closing costs and fees
- If the lot is already owned, the equity can be used for meeting down payment requirements
- Simple and flexible draw process with no set schedules
- Pay just interest-only payments during construction
- Depository relationship required prior to closing

---

### Final Conversion Section
**H2:**
Ready to Discuss Your Construction Loan Options?

**Body Copy:**
Other options are available. Call for more details and speak directly with a Bank Five Nine lender about your timeline, property, and qualification profile.

**Primary CTA (button):**
Talk to a Lender Today

**Button link placeholder:**
`[LENDER_EMAIL_OR_FORM_URL]`

**Secondary CTA:**
For more information, contact your Bank Five Nine lender today. Call: `[LENDER_PHONE]`

**Trust Line:**
Member FDIC | BFN NMLS # 410817

---

## 2. Offer Table/Chart Content and Qualification Bullets

### OfferData (Implementation Reference)
```text
OfferData {
  rate: "4.590%"
  apr: "5.718%"
  price: "$500,000"
  down_payment_pct: "15%"
  loan_amount: "$425,000"
  payment_schedule: "10 @ $811.40; 1 @ $425,811.40"
  term: "11-month"
}
```

### Quick Offer Snapshot Table (for Elementor Table or 2-column cards)

| Field | Value |
|---|---|
| Term | 11-month |
| Rate | 4.590% |
| APR (Annual Percentage Rate) | 5.718% |
| Price | $500,000 |
| Down Payment Percentage | 15% |
| Loan Amount | $425,000 |
| Payment/Month | 10 @ $811.40; 1 @ $425,811.40 |
| Baseline Qualification Callout | Minimum credit score of 700 and 85% LTV |

### Qualification Bullets (V2 Flyer-Aligned)
1. 700 minimum credit score
2. Maximum 85% loan to value, up to $832,750 loan size
3. Single-family, owner-occupied construction in Wisconsin only
4. Consolidate construction and lot purchase for only one set of closing costs and fees
5. If the lot is already owned, the equity can be used for meeting down payment requirements
6. Simple and flexible draw process with no set schedules
7. Pay just interest-only payments during construction
8. Depository relationship required prior to closing

---

## 3. Full Disclosure Block (Compliance-Safe)

> **Important Disclosure (Use as small-print disclosure block near page bottom):**
>
> Using a $500,000 purchase price and 15% down payment, the $425,000 loan amount at a rate of 4.590% would be a monthly payment of $811.40 for the first 10 payments followed by a final payment of $425,811.40.
>
> The payment scenario assumes a half-drawn construction loan. The scenario is based on a closing date of 2/1/2026 with a 1/1/2027 maturity date. The actual first 10 payments are interest only based on the dollar amount drawn at that time. The final balloon payment will equal the principal balance plus interest. The payments quoted above are based on a fixed interest rate. The payment estimates above do not include amounts for taxes and hazard insurance.
>
> Rates are effective for applications dated from 2/4/2026. The interest rates and mortgage products displayed are subject to change and availability. Examples above are based on customers with good credit (including have not been late on any mortgage payment, been recently discharged in bankruptcy, or subject to recent foreclosure) with a 45 day lock period for loan application and processing. The actual mortgage product you qualify for will depend on verification of the value of your home, your credit score and other considerations including whether any subsequent loan will qualify for secondary market.
>
> Construction Loan Special Qualifications:
> - 700 minimum credit score
> - Maximum 85% loan to value, up to $832,750 loan size
> - Single-family, owner-occupied construction in Wisconsin only
> - Consolidate construction and lot purchase for only one set of closing costs and fees
> - If the lot is already owned, the equity can be used for meeting down payment requirements
> - Simple and flexible draw process with no set schedules
> - Pay just interest-only payments during construction
> - Depository relationship required prior to closing
>
> Other options are available. Call for more details.
>
> Member FDIC
>
> BFN NMLS # 410817

---

## 4. Elementor Implementation Guide (Desktop + Mobile)

### A. Page Setup
1. In WordPress, create a new page (draft or private while staging).
2. Set template to **Elementor Canvas**.
3. Add noindex, nofollow (as currently done in your workflow).
4. Set global content width:
   - Desktop max width: **1200px**
   - Mobile max width: **92vw**
5. Use a red-forward visual system (deeper red tints in Hero/Offer/Payment/CTA sections).
6. Set **all section cards/grids/containers** to max border radius **4px**.
7. Keep CTA button styling exactly as approved (including current hover behavior).
8. Hero section uses **Bank Five Nine red background** with high-contrast white typography.
9. Use the **CSS-first implementation path** below for exact visual fidelity (recommended).

### A1. Read This First (Avoid Common Confusion)
1. The guide uses **two implementation modes**:
   - **Exact mode (recommended):** assign CSS classes in Elementor, then paste Section **C7 Custom CSS**. This supports multi-layer hero gradients and precise styling.
   - **UI-only mode (approximate):** use Elementor Style controls only. This is easier but cannot reproduce all layered effects exactly.
2. For the Hero background in exact mode, **do not paste multi-gradient strings into Elementor's Background picker**. Elementor UI usually supports one gradient layer at a time.
3. In exact mode, set a simple temporary preview color in UI (for editing comfort), then let C7 CSS render the final layered background.
4. Wherever a step says "CSS Class", add it in **Advanced > CSS Classes** (without the leading dot).

### A2. CSS Class Checklist (Copy Exactly)
- Section containers: `b59-ppc-hero-wrap`, `b59-ppc-offer-wrap`, `b59-ppc-qual-wrap`, `b59-ppc-payment-wrap`, `b59-ppc-disclosure-wrap`, `b59-ppc-final-cta-wrap`
- Hero text widgets: `b59-ppc-hero-subheadline`, `b59-ppc-hero-body`, `b59-ppc-hero-secondary-link`
- Hero CTA button: `b59-ppc-hero-primary`
- Hero right-column interactive wrapper (inside HTML widget): `b59-ppc-hero-kpi-card`
- Qualification Icon List widgets: `b59-ppc-qual-list`
- Payment callout container: `b59-ppc-payment-callout`
- Payment callout row helpers (inside Text Editor HTML): `b59-ppc-pay-row`, `b59-ppc-pay-label`, `b59-ppc-pay-value`, `b59-ppc-pay-note`

### B. Section Order (Exact)
1. Hero
2. Offer snapshot chart/table
3. Qualification bullets
4. Payment explainer
5. Disclosure
6. Final CTA/contact block

### C. Detailed Widget Mapping by Section (Drag-and-Drop + Colors + Direction)
If you are using **Exact mode**, treat Elementor Style controls as layout helpers only (spacing/structure). Let **C7 Custom CSS** control final colors, gradients, and hover states.

#### C0) Brand Tokens to Use (from `b59_css.txt`)
- Primary red: `#BB2031`
- Secondary light gray: `#F4F4F4`
- Body text charcoal: `#373838`
- Accent green: `#A4C15B`
- White: `#FFFFFF`
- Neutral light border/background: `#E9E9E9`
- Optional cool accent: `#83CDD0`
- Heading font: `Century Gothic`
- Body font: `Minion Pro`
- Card/container/grid radius: `4px`
- CTA/button radius: `8px` (unchanged)

#### C1) Hero (Section 1)
1. Drag a top-level **Container** and set:
   - Width: Full Width
   - CSS Class: `b59-ppc-hero-wrap`
   - Background (Elementor UI): set **Classic color `#BB2031`** as temporary editor preview
   - Final layered background: applied by **C7 CSS** via `.b59-ppc-hero-wrap`
   - Padding: `56px 0 40px 0` (Desktop)
   - Overflow: Hidden (Layout > Overflow)
2. Drag one inner **Container** inside it and set:
   - Content Width: Boxed `1200px`
   - Direction: `Row`
   - Align Items: `Center`
   - Justify Content: `Space Between`
   - Gap: `40px`
3. Drag two child containers inside the inner row:
   - Left container: Width `58%`, Direction `Column`, Gap `16px`, CSS Class `b59-ppc-hero-copy`
   - Right container: Width `42%`, Direction `Column`, CSS Class `b59-ppc-hero-visual`
4. In left container, drag widgets in this order:
   - **Heading** (H1)
   - **Text Editor** (subheadline, CSS Class: `b59-ppc-hero-subheadline`)
   - **Text Editor** (body copy, CSS Class: `b59-ppc-hero-body`)
   - **Button** (primary CTA, CSS Class: `b59-ppc-hero-primary`)
   - **Text Editor** (secondary phone CTA, CSS Class: `b59-ppc-hero-secondary-link`)
5. Style requirements:
   - H1 color `#FFFFFF`, size `52px`, line-height `1.1`, font `Century Gothic`, weight `600`
   - Subheadline color `#FFF3F5`; body color `#F9E9EC`; size `20px` (subheadline) / `18px` (body), line-height `1.5`
   - Hero primary button: background `#FFFFFF`, text `#BB2031`, border radius `8px`, padding `14px 24px`, hover `#FBF1F2`
   - Hero secondary CTA: if using a text link, use white text + subtle underline; if using a button, use white text with white border and subtle translucent fill
   - Ensure all hero text and CTAs pass contrast check in both default and hover states
6. In right container, add either:
   - **HTML widget** with interactive KPI card (recommended), outer wrapper class `b59-ppc-hero-kpi-card`, or
   - **Image/Lottie** accent if you use Feature 3
   - Minimal HTML scaffold for CSS targeting:
```html
<div class="b59-ppc-hero-kpi-card">
  <div class="kpi-item"><span class="kpi-label">Rate</span><strong>4.590%</strong></div>
  <div class="kpi-item"><span class="kpi-label">APR</span><strong>5.718%</strong></div>
</div>
```
7. Right-column card style (to complement red hero):
   - Background `linear-gradient(165deg, #A61B2C 0%, #8F1524 100%)`
   - Border `1px solid rgba(255,255,255,0.18)`
   - Text `#FFFFFF`, helper text `#F4D7DD`
   - Internal KPI tiles use subtle translucent white backgrounds
   - If using HTML widget, ensure KPI tiles use class `kpi-item` and helper labels use class `kpi-label`
8. Add subtle atmosphere:
   - Add 1-2 absolutely-positioned decorative shape containers behind hero content (or use an SVG accent from Haikei), opacity `0.2-0.3`.
   - Keep decorative layers non-clickable and behind content (`z-index` lower than text/buttons).

##### C1 UI-Only Fallback (Approximate, no custom CSS)
1. Hero container > Style > Background > Gradient:
   - Type: Linear
   - Angle: `160`
   - Color: `#BB2031` at `0`
   - Second Color: `#941627` at `100`
2. Hero container > Style > Background Overlay > Gradient:
   - Type: Radial
   - Color: `rgba(255,255,255,0.14)` at `0`
   - Second Color: `rgba(255,255,255,0)` at `42`
   - Position: Top Right
3. Add heading/body text colors manually (white and off-white tones).
4. Add white primary button with red text and hover `#FBF1F2`.
5. Note: this fallback will be close, but not as precise as the CSS-first version.

#### C2) Offer Snapshot Chart/Table (Section 2)
1. Drag a new top-level **Container**:
   - CSS Class: `b59-ppc-offer-wrap`
   - Background: `linear-gradient(180deg, #FFF5F7 0%, #F8EDEF 100%)`
   - Padding: `36px 0 40px 0`
2. Add inner boxed container (`1200px`) with Direction `Column`, Gap `18px`.
3. Add **Heading** widget for section title.
4. Add one content row container:
   - Direction: `Row`
   - Gap: `24px`
   - Left column width `62%` (table card)
   - Right column width `38%` (optional chart/counter card)
5. In left column:
   - Drag **HTML widget** and paste table markup (or use Text Editor with HTML mode)
   - Wrap table in a card style with background `#FFFAFB`, 1px border `rgba(187,32,49,0.20)`, radius `4px`, shadow `0 10px 26px rgba(17,17,17,0.08)`
6. In right column (if used):
   - Drag **HTML widget** for count-up/chart block
   - Card style: background `#FFFAFB`, 1px border `rgba(187,32,49,0.20)`, radius `4px` (no left accent border)

#### C3) Qualification Bullets (Section 3)
1. Drag top-level **Container**:
   - CSS Class: `b59-ppc-qual-wrap`
   - Background `#FFF7F8`
   - Padding `40px 0`
2. Add boxed inner container (`1200px`), Direction `Column`, Gap `20px`.
3. Add **Heading** widget.
4. Add one row container with Direction `Row`, Gap `24px`.
5. Add two child containers at `50% / 50%`.
6. In each child container, drag an **Icon List** widget:
   - 4 bullets per column (total 8)
   - Icon: check-circle
   - Icon color: `#A4C15B`
   - Text color: `#373838`
   - Icon spacing: `10px`
   - Item spacing: `12px`
   - Add CSS Class `b59-ppc-qual-list` on each Icon List widget so each item can render in a subtle red-tinted card

#### C4) Payment Explainer (Section 4)
1. Drag top-level **Container**:
   - CSS Class: `b59-ppc-payment-wrap`
   - Background `linear-gradient(180deg, #FFF4F6 0%, #F5E6E9 100%)`
   - Padding `24px 0`
2. Add boxed inner container (`1200px`) with Direction `Row`, Gap `24px`.
3. Add left child container `65%` width, Direction `Column`, Gap `14px`:
   - **Heading**
   - **Text Editor** (plain-language payment explanation)
4. Add right child container `35%` width, Direction `Column`, CSS Class `b59-ppc-payment-callout`:
   - **Heading** (mini title: Payment Snapshot)
   - **Text Editor** (switch to Text/HTML mode and paste row markup below)
5. In the right-column Text Editor (HTML mode), paste:
```html
<p class="b59-ppc-pay-row">
  <span class="b59-ppc-pay-label">First 10 Payments</span>
  <strong class="b59-ppc-pay-value">$811.40</strong>
  <span class="b59-ppc-pay-note">Interest-only monthly payments during construction.</span>
</p>
<p class="b59-ppc-pay-row is-final">
  <span class="b59-ppc-pay-label">Final Balloon Payment</span>
  <strong class="b59-ppc-pay-value">$425,811.40</strong>
  <span class="b59-ppc-pay-note">Final payment includes outstanding principal plus interest.</span>
</p>
```
6. Visual target for callout (from current approved build):
   - Container background `linear-gradient(170deg, #FFF7F8 0%, #FBECEF 100%)`
   - 1px border `rgba(187, 32, 49, 0.22)`
   - Shadow `0 12px 30px rgba(84, 15, 26, 0.12)`
   - Radius `4px`, padding `20px`, internal gap `14px`
7. Copy rule for this section:
   - Do **not** use directional references like “as shown on the right”.
   - Use layout-agnostic phrasing: “resulting in the payment snapshot shown here.”

#### C5) Disclosure (Section 5)
1. Drag top-level **Container**:
   - CSS Class: `b59-ppc-disclosure-wrap`
   - Background `#F0DDE1`
   - Padding `28px 0 32px 0`
2. Add boxed inner container (`1200px`) with Direction `Column`, Gap `10px`.
3. Drag **Divider** widget first:
   - Weight `2px`
   - Color `#BB2031`
4. Drag **Text Editor** widget with the full disclosure block text.
5. Typography minimum:
   - Desktop `12px`, line-height `1.4`
   - Mobile `11px`, line-height `1.4`
6. Keep disclosure always visible (no tabs/accordion/hide/show).

#### C6) Final CTA / Contact (Section 6)
1. Drag top-level **Container**:
   - CSS Class: `b59-ppc-final-cta-wrap`
   - Background `linear-gradient(170deg, #BB2031 0%, #9F1828 100%)`
   - Padding `34px 0`
2. Add boxed inner container (`1200px`) with Direction `Row`, Align `Center`, Justify `Space Between`, Gap `20px`.
3. Add left child container `70%`, Direction `Column`, Gap `8px`:
   - **Heading**
   - **Text Editor**
4. Add right child container `30%`, Direction `Column`, Gap `10px`:
   - **Button** (primary CTA)
   - **Text Editor** with click-to-call link
5. CTA styling:
   - Section text `#FFFFFF`
   - Primary button background `#FFFFFF`, text `#BB2031`, radius `8px`, weight `700`
   - Keep hover style unchanged: background `#FBF1F2`
   - Phone link text `#FFFFFF`, underline on hover

#### C7) Custom CSS (Required for Exact Visual Match)
```css
:root {
  --b59-ppc-primary: #BB2031;
  --b59-ppc-secondary: #F4F4F4;
  --b59-ppc-text: #373838;
  --b59-ppc-accent: #A4C15B;
  --b59-ppc-white: #FFFFFF;
  --b59-ppc-neutral: #E9E9E9;
  --b59-ppc-alt: #83CDD0;
  --b59-ppc-radius-lg: 4px;
  --b59-ppc-radius-md: 4px;
  --b59-ppc-radius-btn: 8px;
}
.b59-ppc-hero-wrap h1,
.b59-ppc-offer-wrap h2,
.b59-ppc-qual-wrap h2,
.b59-ppc-payment-wrap h2,
.b59-ppc-final-cta-wrap h2 {
  font-family: "Century Gothic", Arial, sans-serif;
  color: var(--b59-ppc-primary);
}
.b59-ppc-hero-wrap p,
.b59-ppc-offer-wrap p,
.b59-ppc-qual-wrap p,
.b59-ppc-payment-wrap p,
.b59-ppc-disclosure-wrap p,
.b59-ppc-qual-wrap li {
  font-family: "Minion Pro", Georgia, serif;
  color: var(--b59-ppc-text);
}
.b59-ppc-hero-wrap {
  /* 3-layer hero background:
     layer 1 + 2 = soft radial highlights,
     layer 3 = base red gradient */
  background:
    radial-gradient(circle at 84% 18%, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0) 42%),
    radial-gradient(circle at 10% 88%, rgba(255, 255, 255, 0.10) 0%, rgba(255, 255, 255, 0) 50%),
    linear-gradient(160deg, #BB2031 0%, #AC1C2D 58%, #941627 100%);
}
.b59-ppc-hero-wrap h1 {
  color: #FFFFFF;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.16);
}
.b59-ppc-hero-wrap p {
  color: #F9E9EC;
}
.b59-ppc-hero-wrap .b59-ppc-hero-subheadline {
  color: #FFF3F5;
}
.b59-ppc-hero-wrap .b59-ppc-hero-secondary-link {
  color: #FFFFFF;
  text-decoration: underline;
  text-decoration-color: rgba(255, 255, 255, 0.6);
}
.b59-ppc-hero-wrap .b59-ppc-hero-secondary-link a {
  color: #FFFFFF;
}
.b59-ppc-hero-wrap .elementor-button,
.b59-ppc-hero-wrap .btn-primary,
.b59-ppc-hero-wrap .b59-ppc-hero-primary {
  border-radius: var(--b59-ppc-radius-btn);
  background: #FFFFFF;
  color: #BB2031;
}
.b59-ppc-hero-wrap .elementor-button:hover,
.b59-ppc-hero-wrap .elementor-button:focus,
.b59-ppc-hero-wrap .btn-primary:hover {
  background: #FBF1F2;
  color: #BB2031;
}
.b59-ppc-hero-wrap .btn-secondary,
.b59-ppc-hero-wrap .b59-ppc-hero-secondary {
  background: rgba(255, 255, 255, 0.06);
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.74);
}
.b59-ppc-hero-wrap .btn-secondary:hover,
.b59-ppc-hero-wrap .b59-ppc-hero-secondary:hover {
  background: rgba(255, 255, 255, 0.14);
  color: #FFFFFF;
}
.b59-ppc-offer-wrap {
  background: linear-gradient(180deg, #FFF5F7 0%, #F8EDEF 100%);
}
.b59-ppc-qual-wrap {
  background: #FFF7F8;
}
.b59-ppc-payment-wrap {
  background: linear-gradient(180deg, #FFF4F6 0%, #F5E6E9 100%);
  padding-top: 24px;
  padding-bottom: 24px;
}
.b59-ppc-disclosure-wrap {
  background: #F0DDE1;
  border-top: 2px solid rgba(187, 32, 49, 0.2);
}
.b59-ppc-final-cta-wrap {
  background: linear-gradient(170deg, #BB2031 0%, #9F1828 100%);
}
.b59-ppc-offer-wrap .elementor-widget-html,
.b59-ppc-payment-callout,
.b59-ppc-hero-visual .elementor-widget-wrap,
.b59-ppc-qual-list .elementor-icon-list-item {
  border-radius: var(--b59-ppc-radius-lg);
}
.b59-ppc-hero-kpi-card {
  background: linear-gradient(165deg, #A61B2C 0%, #8F1524 100%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #FFFFFF;
  box-shadow: 0 14px 28px rgba(61, 5, 13, 0.34);
  padding: 22px;
}
.b59-ppc-hero-kpi-card h3,
.b59-ppc-hero-kpi-card strong {
  color: #FFFFFF;
}
.b59-ppc-hero-kpi-card small,
.b59-ppc-hero-kpi-card .kpi-label {
  color: #F4D7DD;
}
.b59-ppc-hero-kpi-card .kpi-item {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.24);
}
.b59-ppc-payment-callout {
  gap: 14px;
  padding: 20px;
  border: 1px solid rgba(187, 32, 49, 0.22);
  border-radius: 4px;
  background: linear-gradient(170deg, #FFF7F8 0%, #FBECEF 100%);
  box-shadow: 0 12px 30px rgba(84, 15, 26, 0.12);
}
.b59-ppc-payment-callout h2 {
  margin: 0;
  color: #8F1524;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: clamp(24px, 2.1vw, 30px);
  line-height: 1.1;
}
.b59-ppc-payment-callout .b59-ppc-pay-row {
  margin: 0;
  padding: 12px 14px;
  border: 1px solid rgba(187, 32, 49, 0.20);
  border-radius: 4px;
  background: #FFFFFF;
}
.b59-ppc-payment-callout .b59-ppc-pay-row + .b59-ppc-pay-row {
  margin-top: 10px;
}
.b59-ppc-pay-label {
  display: block;
  color: #8F1524;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.b59-ppc-pay-value {
  display: block;
  margin-top: 4px;
  color: #BB2031;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 34px;
  font-weight: 700;
  line-height: 1.05;
}
.b59-ppc-pay-note {
  display: block;
  margin-top: 6px;
  color: #4F5052;
  font-size: 13px;
  line-height: 1.35;
}
.b59-ppc-pay-row.is-final {
  background: linear-gradient(180deg, #FFFDFD 0%, #FFF2F4 100%);
}
.b59-ppc-pay-row.is-final .b59-ppc-pay-value {
  color: #971728;
  font-size: 30px;
}
.b59-ppc-qual-list .elementor-icon-list-item {
  background: #FFFAFB;
  border: 1px solid rgba(187, 32, 49, 0.16);
  padding: 12px;
  margin-bottom: 10px;
}
.b59-ppc-disclosure-wrap p {
  color: #4A2A2F;
}
.b59-ppc-final-cta-wrap h2,
.b59-ppc-final-cta-wrap p,
.b59-ppc-final-cta-wrap a {
  color: var(--b59-ppc-white);
}
.b59-ppc-final-cta-wrap .elementor-button {
  border-radius: var(--b59-ppc-radius-btn);
  background: #FFFFFF;
  color: #BB2031;
}
.b59-ppc-final-cta-wrap .elementor-button:hover,
.b59-ppc-final-cta-wrap .elementor-button:focus {
  background: #FBF1F2;
  color: #BB2031;
}
@media (max-width: 767px) {
  .b59-ppc-payment-callout {
    padding: 16px;
  }
  .b59-ppc-pay-value {
    font-size: 30px;
  }
  .b59-ppc-pay-row.is-final .b59-ppc-pay-value {
    font-size: 26px;
  }
  .b59-ppc-pay-note {
    font-size: 12px;
  }
}
```

### D. Responsive Rules (Detailed by Breakpoint)
- **1440 and up**
  - Max content width `1200px`
  - Hero column split `58/42`
  - H1 `52px`
- **1024 to 1439**
  - Keep row layout for Hero/Offer/Payment
  - Change split to `55/45` (hero), `60/40` (offer), `60/40` (payment)
  - H1 `44px`, section headings `34px`
- **768 to 1023**
  - Hero switches to single column (`Column`)
  - Offer row switches to single column (table first, chart second)
  - Final CTA switches to single column
  - Primary buttons full width
- **480 to 767**
  - All major containers single column
  - H1 `34-36px`
  - Body text `16px`
  - Section vertical padding reduced to `24-28px`
- **390 to 479**
  - H1 `30-32px`
  - Card padding `16px`
  - Disclosure font `11px`
  - Verify no horizontal overflow (`overflow-x: hidden` on wrapper if needed)

### E. Sticky Header CTA (Detailed Implementation)
Use this instead of a bottom mobile sticky bar so there is one consistent sticky CTA pattern across desktop and mobile.

1. In the **top logo header container** (Elementor container that already holds the logo):
   - Add CSS Class: `b59-ppc-topbar`
2. In its inner child container (the one with the logo image widget):
   - Add CSS Class: `b59-ppc-topbar-inner`
   - Layout: Direction `Row`, Justify `Space Between`, Align `Center`
3. Drag a **Button widget** into that same row (to the right of logo):
   - Button text: `Talk to a Lender`
   - Link: `[LENDER_EMAIL_OR_FORM_URL]` or lender page URL
   - Advanced > CSS Classes: `b59-ppc-header-cta js-b59-ppc-talk-lender-header`
   - Optional wrapper/container class: `b59-ppc-header-cta-wrap`
4. Add this CSS in page-level custom CSS or an HTML widget `<style>` block:
```css
.b59-ppc-topbar {
  position: sticky;
  top: 0;
  z-index: 10020;
  background: #FFFFFF;
  border-bottom: 1px solid rgba(187, 32, 49, 0.12);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}
body.admin-bar .b59-ppc-topbar { top: 32px; }

.b59-ppc-topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.b59-ppc-topbar-inner > .elementor-widget-image img {
  width: auto;
  max-height: 52px;
}

.b59-ppc-header-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 18px;
  border-radius: 8px;
  background: #BB2031;
  color: #FFFFFF;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.1;
  text-decoration: none;
  white-space: nowrap;
}
.b59-ppc-header-cta:hover,
.b59-ppc-header-cta:focus {
  background: #9F1B2A;
  color: #FFFFFF;
}

@media (max-width: 782px) {
  body.admin-bar .b59-ppc-topbar { top: 46px; }
}
@media (max-width: 767px) {
  .b59-ppc-topbar-inner { gap: 10px; }
  .b59-ppc-topbar-inner > .elementor-widget-image img { max-height: 44px; }
  .b59-ppc-header-cta {
    min-height: 38px;
    padding: 8px 12px;
    font-size: 13px;
  }
}
```
5. If you previously added a bottom mobile sticky CTA, disable/remove it:
```css
.b59-ppc-mobile-sticky-cta { display: none !important; }
```
6. Add this JS once (same HTML widget) for UTM carryover + event tracking:
```html
<script>
(function () {
  var headerCtas = document.querySelectorAll(".js-b59-ppc-talk-lender-header");
  if (!headerCtas.length) return;

  window.dataLayer = window.dataLayer || [];
  headerCtas.forEach(function (link) {
    try {
      var url = new URL(link.getAttribute("href"), window.location.origin);
      var incoming = new URLSearchParams(window.location.search);
      incoming.forEach(function (val, key) {
        if (!url.searchParams.has(key)) url.searchParams.set(key, val);
      });
      link.setAttribute("href", url.toString());
    } catch (e) {}

    link.addEventListener("click", function () {
      window.dataLayer.push({ event: "cta_talk_lender_click", placement: "header_sticky" });
    });
  });
})();
</script>
```
7. QA checks:
   - Desktop (1366 and 1920): header stays pinned and CTA remains visible.
   - Mobile (390 and 430 widths): logo + CTA fit in one row and remain tappable.
   - No bottom overlay covers disclosure or final CTA content.

### F. Performance Guardrails
- No autoplay video
- Use optimized images (WebP if possible)
- Keep each SVG/Lottie asset below 300KB
- Limit third-party libraries to only what is used
- Lazy-load below-the-fold decorative assets

### G. Paid Tracking Readiness
- Preserve UTM parameters on first landing and CTA clickthroughs.
- Recommended event names:
  - `lp_view`
  - `cta_talk_lender_click`
  - `qualification_expand`
  - `calculator_interaction`
- Ensure sticky header CTA emits `cta_talk_lender_click` before navigation.

### H. QA Checklist Before Launch
1. Rate/APR/payment figures match flyer exactly.
2. Disclosure includes all required assumptions and qualifiers.
3. No clipping at 1366x768 and 1920x1080.
4. No horizontal scroll at 390x844 and 430x932.
5. Sticky header CTA is visible and clickable on desktop and mobile, with no overlap issues.
6. Color contrast is AA compliant.

---

## 5. Top 3 Interactive/Animated Features (Free Sources + Elementor Integration)

### Feature 1: Interactive Offer Snapshot Counter (Template Family: Trust KPI Strip / R07)
**Why it fits this page:** Highlights rate and APR fast for paid users with low attention window, then immediately explains the 11-payment shape visually.

**Free sources:**
- CountUp.js: https://inorganik.github.io/countUp.js/
- Chart.js: https://www.chartjs.org/

**Elementor implementation (no paid plugin needed):**
1. Create a section titled "Quick Offer Snapshot".
2. Add an **HTML widget** with containers for **Rate** and **APR** only.
3. Load CountUp.js and animate numbers on scroll into view.
4. Place the **11-payment scenario bar graph directly under the two counters** (10 interest-only + final balloon).
5. Fire `calculator_interaction` event when users toggle/hover scenario elements.

**Feature 1 CSS (paste once in global CSS):**
```css
/* Feature 1 (PPC KPI counter card) */
.b59-ppc-hero-wrap .b59-ppc-hero-kpi-card {
  background: linear-gradient(165deg, #A61B2C 0%, #8F1524 100%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 4px;
  box-shadow: 0 14px 28px rgba(61, 5, 13, 0.34);
  color: #FFFFFF;
  padding: 22px;
}

.b59-ppc-hero-wrap .b59-ppc-hero-kpi-card h3 {
  margin: 0 0 10px 0;
  color: #FFFFFF;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 22px;
}

.b59-ppc-hero-wrap .b59-ppc-kpi-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.b59-ppc-hero-wrap .b59-ppc-hero-kpi-card .kpi-item {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 4px;
  padding: 10px;
}

.b59-ppc-hero-wrap .b59-ppc-hero-kpi-card .kpi-label {
  display: block;
  color: #F4D7DD;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 11px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.b59-ppc-hero-wrap .b59-ppc-hero-kpi-card .js-b59-ppc-counter {
  display: block;
  margin-top: 6px;
  color: #FFFFFF;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.1;
}

@media (max-width: 767px) {
  .b59-ppc-hero-wrap .b59-ppc-kpi-grid {
    grid-template-columns: 1fr 1fr;
  }

  .b59-ppc-hero-wrap .b59-ppc-hero-kpi-card .js-b59-ppc-counter {
    font-size: 21px;
  }
}
```

**Feature 1 mini-chart (Chart.js, exact implementation):**
1. Use Chart.js official source: https://www.chartjs.org/ (the `inorganik.github.io/chart.js` URL is not a Chart.js host).
2. In the same Feature 1 HTML widget, add this markup below your KPI rows:
```html
<div class="b59-ppc-chart-wrap">
  <div class="b59-ppc-chart-head">
    <strong>11-Payment Scenario</strong>
    <span>10 interest-only + 1 final balloon</span>
  </div>
  <div class="b59-ppc-chart-canvas">
    <canvas class="js-b59-ppc-payment-chart"></canvas>
  </div>
</div>
```
3. Add this CSS once (global CSS):
```css
.b59-ppc-hero-wrap .b59-ppc-chart-wrap {
  margin-top: 12px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.10);
  border: 1px solid rgba(255, 255, 255, 0.24);
  padding: 12px;
}

.b59-ppc-hero-wrap .b59-ppc-chart-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.b59-ppc-hero-wrap .b59-ppc-chart-head strong {
  color: #FFFFFF;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 14px;
}

.b59-ppc-hero-wrap .b59-ppc-chart-head span {
  color: #F4D7DD;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 12px;
}

.b59-ppc-hero-wrap .b59-ppc-chart-canvas {
  height: 82px;
}
```
4. Add this JS once in the same HTML widget (multi-instance-safe):
```html
<script>
(function () {
  function initCharts() {
    document.querySelectorAll(".js-b59-ppc-counter-module").forEach(function (module) {
      if (module.dataset.b59PpcChartInit === "1") return;
      module.dataset.b59PpcChartInit = "1";

      var canvas = module.querySelector(".js-b59-ppc-payment-chart");
      if (!canvas || !window.Chart) return;

      var visualData = [14,14,14,14,14,14,14,14,14,14,100];
      var actualData = [811.40,811.40,811.40,811.40,811.40,811.40,811.40,811.40,811.40,811.40,425811.40];
      var colors = ["#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#D38A95","#FFF3F5"];

      new Chart(canvas.getContext("2d"), {
        type: "bar",
        data: {
          labels: ["1","2","3","4","5","6","7","8","9","10","11"],
          datasets: [{
            data: visualData,
            backgroundColor: colors,
            borderRadius: 2,
            borderSkipped: false,
            categoryPercentage: 0.9,
            barPercentage: 0.9
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 900, easing: "easeOutQuart" },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: function(items) {
                  var i = items[0].dataIndex;
                  return i === 10 ? "Payment 11 (final)" : "Payment " + (i + 1);
                },
                label: function(ctx) {
                  var i = ctx.dataIndex;
                  var amt = actualData[i].toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                  return i === 10 ? "Final balloon: $" + amt : "Interest-only: $" + amt;
                }
              }
            }
          },
          scales: {
            x: { display: false, grid: { display: false }, border: { display: false } },
            y: { display: false, grid: { display: false }, border: { display: false }, suggestedMax: 110 }
          }
        }
      });
    });
  }

  function ensureChartJs(cb) {
    if (window.Chart) return cb();
    if (window.__b59PpcChartLoading) {
      document.addEventListener("b59-ppc-chart-ready", cb, { once: true });
      return;
    }

    window.__b59PpcChartLoading = true;
    document.addEventListener("b59-ppc-chart-ready", cb, { once: true });

    var s = document.querySelector('script[data-b59-ppc-chartjs]');
    if (!s) {
      s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js";
      s.async = true;
      s.setAttribute("data-b59-ppc-chartjs", "1");
      document.head.appendChild(s);
    }

    s.addEventListener("load", function () {
      document.dispatchEvent(new CustomEvent("b59-ppc-chart-ready"));
    }, { once: true });
  }

  ensureChartJs(initCharts);
})();
</script>
```
5. Ensure your Feature 1 outer wrapper includes `js-b59-ppc-counter-module` and `b59-ppc-hero-kpi-card` so both CountUp and Chart.js initialize.

**Mobile behavior:**
- Keep counters as a 2-up row (Rate + APR), with chart directly below
- Reduce animation duration to 1.2-1.5s for quick read

---

### Feature 2: Qualification Stepper (Template Family: Stepper Flow / R10)
**Why it fits this page:** Converts complex qualification criteria into digestible decision steps.

**Free source:**
- Vanilla JS only (no paid tools)

**Elementor implementation (exact copy/paste):**
1. Add one **HTML widget** under the Qualifications section.
2. Paste this HTML + JS in that widget:
```html
<div class="b59-ppc-stepper js-b59-ppc-stepper" data-current-step="0">
  <div class="b59-ppc-stepper-head">
    <h3>Do I Qualify?</h3>
    <div class="b59-ppc-step-dots" aria-hidden="true">
      <span class="b59-ppc-dot is-active"></span>
      <span class="b59-ppc-dot"></span>
      <span class="b59-ppc-dot"></span>
    </div>
  </div>

  <div class="b59-ppc-step-tabs" role="tablist" aria-label="Qualification steps">
    <button type="button" class="b59-ppc-step-tab js-b59-ppc-step-tab is-active" data-step="0" aria-selected="true">1. Credit &amp; LTV</button>
    <button type="button" class="b59-ppc-step-tab js-b59-ppc-step-tab" data-step="1" aria-selected="false">2. Property &amp; Use</button>
    <button type="button" class="b59-ppc-step-tab js-b59-ppc-step-tab" data-step="2" aria-selected="false">3. Process &amp; Relationship</button>
  </div>

  <div class="b59-ppc-step-items">
    <article class="b59-ppc-step-item is-active" data-step="0">
      <button type="button" class="b59-ppc-acc-toggle js-b59-ppc-acc-toggle" aria-expanded="true">Step 1: Credit &amp; LTV baseline</button>
      <div class="b59-ppc-step-content">
        <h4>Step 1: Credit &amp; LTV baseline</h4>
        <ul>
          <li>700 minimum credit score</li>
          <li>Maximum 85% loan to value</li>
        </ul>
      </div>
    </article>

    <article class="b59-ppc-step-item" data-step="1">
      <button type="button" class="b59-ppc-acc-toggle js-b59-ppc-acc-toggle" aria-expanded="false">Step 2: Property/use requirements</button>
      <div class="b59-ppc-step-content">
        <h4>Step 2: Property/use requirements</h4>
        <ul>
          <li>Single-family, owner-occupied construction in Wisconsin only</li>
          <li>Loan size up to $832,750</li>
        </ul>
      </div>
    </article>

    <article class="b59-ppc-step-item" data-step="2">
      <button type="button" class="b59-ppc-acc-toggle js-b59-ppc-acc-toggle" aria-expanded="false">Step 3: Construction process + relationship</button>
      <div class="b59-ppc-step-content">
        <h4>Step 3: Construction process + relationship</h4>
        <ul>
          <li>Simple and flexible draw process with no set schedules</li>
          <li>Depository relationship required prior to closing</li>
        </ul>
        <p style="margin-top:12px;">
          <a class="btn btn-primary js-b59-ppc-stepper-cta" href="[LENDER_EMAIL_OR_FORM_URL]">Talk to a Bank Five Nine Lender</a>
        </p>
      </div>
    </article>
  </div>

</div>

<script>
(function () {
  window.dataLayer = window.dataLayer || [];

  function toArray(list) { return Array.prototype.slice.call(list); }

  document.querySelectorAll(".js-b59-ppc-stepper").forEach(function (module) {
    if (module.dataset.bound === "1") return;
    module.dataset.bound = "1";

    var tabs = toArray(module.querySelectorAll(".js-b59-ppc-step-tab"));
    var items = toArray(module.querySelectorAll(".b59-ppc-step-item"));
    var toggles = toArray(module.querySelectorAll(".js-b59-ppc-acc-toggle"));
    var dots = toArray(module.querySelectorAll(".b59-ppc-dot"));
    var tabWrap = module.querySelector(".b59-ppc-step-tabs");
    var current = 0;
    var engaged = false;

    function track(action, payload) {
      var data = { event: "qualification_expand", action: action };
      if (payload) Object.keys(payload).forEach(function (k) { data[k] = payload[k]; });
      window.dataLayer.push(data);
    }

    function engageOnce() {
      if (engaged) return;
      engaged = true;
      track("first_interaction", { step: current + 1 });
    }

    function setStep(nextIndex) {
      current = Math.max(0, Math.min(nextIndex, items.length - 1));
      module.dataset.currentStep = String(current);

      tabs.forEach(function (tab, i) {
        var active = i === current;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
      });

      items.forEach(function (item, i) {
        item.classList.toggle("is-active", i === current);
      });

      toggles.forEach(function (btn, i) {
        btn.setAttribute("aria-expanded", i === current ? "true" : "false");
      });

      dots.forEach(function (dot, i) {
        dot.classList.toggle("is-active", i <= current);
      });

    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () {
        engageOnce();
        setStep(i);
      });
    });

    if (tabWrap) {
      tabWrap.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        e.preventDefault();
        var focused = tabs.indexOf(document.activeElement);
        if (focused < 0) focused = current;
        var next = e.key === "ArrowRight" ? (focused + 1) % tabs.length : (focused - 1 + tabs.length) % tabs.length;
        tabs[next].focus();
        tabs[next].click();
      });
    }

    toggles.forEach(function (btn, i) {
      btn.addEventListener("click", function () {
        engageOnce();
        setStep(i);
      });
    });

    module.querySelectorAll(".js-b59-ppc-stepper-cta").forEach(function (cta) {
      cta.addEventListener("click", function () {
        window.dataLayer.push({ event: "cta_talk_lender_click", placement: "qualification_stepper" });
      });
    });

    setStep(0);
  });
})();
</script>
```
3. Replace `[LENDER_EMAIL_OR_FORM_URL]` with your real CTA URL.
4. Paste this CSS once in global CSS:
```css
.b59-ppc-stepper {
  margin-top: 24px;
  padding: 18px;
  border-radius: 4px;
  background: #fffafb;
  border: 1px solid rgba(187, 32, 49, 0.18);
  box-shadow: 0 10px 26px rgba(17, 17, 17, 0.08);
}

.b59-ppc-stepper-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.b59-ppc-stepper-head h3 {
  margin: 0;
  color: #272728;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 24px;
}

.b59-ppc-step-dots { display: flex; gap: 7px; }
.b59-ppc-dot { width: 12px; height: 12px; border-radius: 999px; background: #dfdfdf; }
.b59-ppc-dot.is-active { background: #BB2031; }

.b59-ppc-step-tabs {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.b59-ppc-step-tab {
  border: 1px solid rgba(187,32,49,0.25);
  border-radius: 4px;
  background: #fff;
  color: #BB2031;
  font: 700 13px/1.2 "Century Gothic", Arial, sans-serif;
  padding: 10px 12px;
  min-height: 46px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: normal;
  overflow-wrap: anywhere;
  cursor: pointer;
}

.b59-ppc-step-tab.is-active {
  background: #BB2031;
  color: #fff;
}

.b59-ppc-step-item { display: none; margin-top: 12px; }
.b59-ppc-step-item.is-active { display: block; }
.b59-ppc-acc-toggle { display: none; }

.b59-ppc-step-content {
  border-radius: 4px;
  background: #f7e9ec;
  border: 1px solid rgba(187, 32, 49, 0.16);
  padding: 14px;
}

.b59-ppc-step-content h4 {
  margin: 0;
  color: #BB2031;
  font-family: "Century Gothic", Arial, sans-serif;
  font-size: 22px;
  line-height: 1.25;
  overflow-wrap: anywhere;
}

.b59-ppc-step-content ul {
  margin: 10px 0 0 18px;
  color: #373838;
}

.b59-ppc-step-content li {
  overflow-wrap: anywhere;
}

@media (max-width: 767px) {
  .b59-ppc-step-tabs { display: none !important; }

  .b59-ppc-step-item {
    display: block !important;
    margin-top: 8px;
    border: 1px solid rgba(187, 32, 49, 0.16);
    border-radius: 4px;
    background: #fffafb;
    overflow: hidden;
  }

  .b59-ppc-acc-toggle {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 0;
    background: transparent;
    padding: 12px 14px;
    color: #BB2031;
    font: 700 13px/1.35 "Century Gothic", Arial, sans-serif;
    text-align: left;
    white-space: normal;
    overflow-wrap: anywhere;
    cursor: pointer;
  }

  .b59-ppc-step-content {
    display: none;
    border: 0;
    border-top: 1px solid rgba(187,32,49,0.14);
    padding: 14px 14px;
  }
  .b59-ppc-step-item.is-active .b59-ppc-step-content { display: block; }

  .b59-ppc-step-content h4 {
    font-size: 20px;
  }

}
```
5. QA events in browser console/DataLayer:
   - `qualification_expand` on first interaction
   - `cta_talk_lender_click` with placement `qualification_stepper` when stepper CTA is clicked

**Mobile behavior:**
- Accordion-style steps instead of horizontal tabs
- Keep one step open at a time

---

### Feature 3: Motion Accent + Trust Visual Layer (Template Family: Motion Accent Layer / R13)
**Why it fits this page:** Makes the page feel premium and modern without distracting from compliance-heavy content.

**Free sources:**
- LottieFiles free animations: https://lottiefiles.com/free-animation
- Haikei SVG backgrounds: https://haikei.app/

**Elementor integration options:**
- **If Elementor Pro:** use native Lottie widget
- **If no Pro:** use HTML widget embedding Lottie web player script

**Implementation steps:**
1. Generate subtle SVG section dividers/background blobs in Haikei (brand-aligned red/neutral palette).
2. Add SVGs as section backgrounds for Hero and CTA strips.
3. Add one lightweight Lottie accent near hero CTA (non-loop or low-frequency loop).
4. Disable or simplify motion for users with reduced-motion preference.
5. Keep decorative motion behind content layers and test for readability.

**Mobile behavior:**
- Reduce animation scale and opacity
- Hide non-essential decorative motion below 480px

---

### Practical Build Sequence (Recommended)
1. Build static compliant copy first (Sections 1-4).
2. Validate legal text and number accuracy.
3. Add Feature 1 (snapshot counter) only.
4. Add Feature 2 (qualification stepper).
5. Add Feature 3 (motion accents) last and tune performance.

This sequence ensures compliance and paid-launch readiness before design enhancements.
