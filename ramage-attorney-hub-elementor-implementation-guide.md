# Ramage Attorney Hub - Elementor Pro Containers Implementation Guide

This guide is written to rebuild the mockup at:

- `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/ramage-attorney-hub-mockup.html`

Source references:

- `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/Texas Family Law & Divorce Attorneys _ The Ramage Law Group.html`
- `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/ramage-css.txt`

Target build scope:

- Main content only (no global header/footer)
- Intro block
- Attorney grid
- "Why Work With The Ramage Law Group?" trust block
- "How We Help Clients" icon section

---

## 1. Pre-Flight Setup (Do This First)

### 1.1 Plugin + editor assumptions

1. Confirm `Elementor Pro` is active.
2. Confirm the page is using `Container` layout, not old sections/columns.
3. Work in staging or draft mode.

### 1.2 Open target page

1. Go to `Pages` in WP Admin.
2. Open the attorney page you want to rebuild.
3. Click `Edit with Elementor`.

### 1.3 Page-level settings

1. Click the Elementor gear icon (`Page Settings`) in the lower-left.
2. Set `Page Layout`: `Elementor Full Width`.
3. Set `Hide Title`: `Yes` (only if your theme prints the page title above content).
4. Save draft.

Why this matters:

- Prevents theme wrappers from fighting your spacing and width controls.

---

## 2. Global Design Tokens (Site Settings)

Open `☰ (hamburger menu) -> Site Settings`.

### 2.1 Global Colors

Create these named colors:

| Token Name | Hex | Usage |
|---|---:|---|
| Ramage Navy | `#032436` | Headings, borders, secondary buttons |
| Ramage Gold | `#E2C383` | Primary CTAs, accent rules |
| Ink | `#0F1419` | Primary body text |
| Muted Slate | `#5A6A77` | Supporting text |
| Warm Canvas | `#F9F6F3` | Light section background |
| White | `#FFFFFF` | Card and panel backgrounds |

### 2.2 Global Typography

Set typography tokens:

| Token | Family | Weight | Size (Desktop) | Line Height |
|---|---|---:|---:|---:|
| Display XL | Playfair Display (or Cormorant Garamond fallback) | 600 | 52px | 1.15 |
| Display M | Playfair Display (or fallback) | 600 | 36px | 1.2 |
| Heading S | Playfair Display (or fallback) | 600 | 28px | 1.2 |
| Body | Source Sans 3 (or system sans fallback) | 400 | 18px | 1.55 |
| Body Small | Source Sans 3 | 500 | 15px | 1.5 |
| Label Caps | Source Sans 3 | 700 | 13px | 1.35 |

If the exact fonts are unavailable in Elementor:

- Use `Playfair Display` for all display/name styles.
- Use `Source Sans 3` or `Inter` for body/supporting styles.

Why this matters:

- The premium look is mostly typography + spacing discipline.

---

## 3. Required Class Contract (Do Not Skip)

You will assign these CSS classes exactly:

- `.attorney-hub`
- `.attorney-grid`
- `.attorney-card`
- `.attorney-photo`
- `.attorney-meta`
- `.attorney-actions`
- `.btn-call`
- `.btn-bio`
- `.trust-block`
- `.help-icons-grid`

Why this matters:

- These classes mirror the static mockup and make parity QA deterministic.

---

## 4. Container Tree Blueprint

Build this exact structure:

```text
attorney-hub (top wrapper container, vertical)
├── attorney-intro (container, vertical)
│   ├── Text Editor (kicker)
│   ├── Heading (H1 intro title)
│   └── Text Editor (intro paragraph)
├── attorney-grid (container, row + wrap)
│   ├── attorney-card x7
│   │   ├── attorney-photo (container)
│   │   │   └── Image (headshot)
│   │   └── attorney-meta (container)
│   │       ├── Heading (name)
│   │       ├── Text Editor (title)
│   │       ├── Text Editor (rating line)
│   │       ├── Text Editor (summary placeholder)
│   │       └── attorney-actions (container)
│   │           ├── Button (btn-call)
│   │           └── Button (btn-bio)
├── trust-block (container)
│   ├── Heading
│   └── Icon List or text rows (4 trust points)
└── how-help section wrapper (container)
    ├── Heading
    └── help-icons-grid (container, row + wrap)
        └── help-item x6 (container, linked)
            ├── Image
            ├── Heading
            └── Text Editor
```

---

## 5. Build Step-by-Step

## 5.1 Top wrapper: `.attorney-hub`

1. Add a top-level `Container`.
2. `Advanced -> CSS Classes`: `attorney-hub`.
3. `Layout`:
   - Content Width: `Full Width`
   - Width: `100%`
   - Direction: `Column`
   - Justify Content: `Start`
   - Align Items: `Stretch`
   - Gap: `0`
4. `Style -> Background`:
   - Type: `Classic`
   - Color: `#F9F6F3`

Why this value:

- It creates the page-level shell and baseline canvas.

## 5.2 Intro section

1. Inside `.attorney-hub`, add child container and name it `attorney-intro`.
2. `Layout`:
   - Content Width: `Boxed`
   - Boxed Width: `1240px`
   - Direction: `Column`
   - Align Items: `Center`
   - Justify Content: `Center`
3. `Advanced`:
   - Padding: `96px top`, `0 right`, `72px bottom`, `0 left`
4. Add Text Editor widget for kicker:
   - Content: `THE RAMAGE LAW GROUP`
   - Typography: Label Caps token
   - Letter Spacing: `3px`
   - Transform: `Uppercase`
   - Color: `#032436`
   - Margin bottom: `16px`
5. Add Heading widget (H1):
   - Text: `Meet the McKinney & Frisco Area Family Law Attorneys`
   - HTML tag: `h1`
   - Max width: `900px` (via width or custom)
   - Alignment: `Center`
   - Typography: Display XL token
   - Color: `#032436`
   - Margin bottom: `20px`
6. Add Text Editor widget (intro paragraph):
   - Text:
     `At The Ramage Law Group, we pair high-level strategy with boutique-level client care. This team is built to guide North Texas families through complex transitions with clarity, compassion, and courtroom-ready advocacy.`
   - Max width: `900px`
   - Alignment: `Center`
   - Typography: Body token
   - Color: `#5A6A77`
7. Optional decorative divider:
   - Add Divider widget below paragraph.
   - Width: `96px`
   - Weight: `2px`
   - Color: `#E2C383`
   - Margin top: `24px`

Why this value:

- The intro establishes premium tone through restraint and hierarchy.

## 5.3 Attorney grid wrapper: `.attorney-grid`

1. Add a new container under intro.
2. `Advanced -> CSS Classes`: `attorney-grid`.
3. `Layout`:
   - Content Width: `Boxed`
   - Boxed Width: `1240px`
   - Direction: `Row`
   - Wrap: `Wrap`
   - Align Items: `Stretch`
   - Gap: `34px` (row + column)
4. `Advanced`:
   - Margin bottom: `96px`

Why this value:

- Keeps a clean 3-column rhythm with high-end breathing room.

## 5.4 Build one master attorney card

### 5.4.1 Card container

1. Add container inside `.attorney-grid`.
2. `Advanced -> CSS Classes`: `attorney-card`.
3. `Layout`:
   - Width (Desktop): `calc(33.333% - 23px)` or use custom width slider to roughly one-third.
   - Direction: `Column`
   - Align Items: `Stretch`
   - Min Height: leave auto.
4. `Style -> Background`:
   - Color: `#FFFFFF`
5. `Style -> Border`:
   - Border Type: `Solid`
   - Width: `1px`
   - Color: `rgba(3,36,54,0.16)`
   - Border Radius: `4px` all sides
6. `Style -> Box Shadow`:
   - Horizontal: `0`
   - Vertical: `12`
   - Blur: `30`
   - Spread: `0`
   - Color: `rgba(3,36,54,0.08)`
7. `Advanced`:
   - Overflow: `Hidden`

### 5.4.2 Photo wrapper + image

1. Add inner container at top of card.
2. Class: `attorney-photo`.
3. `Layout`:
   - Min Height: `360px` desktop
4. Add Image widget inside `attorney-photo`.
5. Image widget settings:
   - Image Size: `Full`
   - Width: `100%`
   - Height: `100%` (if available)
   - Object Fit: `Cover`
   - Object Position: `Center Center` or `Center Top`
6. Add Link:
   - Link image to attorney bio URL.

### 5.4.3 Meta wrapper

1. Add container below photo.
2. Class: `attorney-meta`.
3. `Layout`:
   - Direction: `Column`
   - Gap: `10px`
4. `Advanced` padding:
   - `24px top`, `22px right`, `22px bottom`, `22px left`

### 5.4.4 Name

1. Add Heading widget.
2. Content: attorney name.
3. HTML Tag: `h3`.
4. Typography:
   - Family: Playfair Display
   - Weight: `600`
   - Size: `30px`
   - Line-height: `1.18`
5. Color: `#032436`.
6. Margin: `0`.

### 5.4.5 Title (muted caps)

1. Add Text Editor below name.
2. Content: role (e.g., `Founder & CEO`).
3. Typography:
   - Family: Source Sans 3
   - Weight: `700`
   - Size: `13px`
   - Transform: `Uppercase`
   - Letter spacing: `2px`
4. Color: `#5A6A77`.

### 5.4.6 Rating line

1. Add Text Editor.
2. Content:
   - `★★★★★  Based on Client Reviews`
3. Style:
   - Stars color: `#B88F34`
   - "Based on Client Reviews" color: `#70808D`
   - Size around `15px`
4. Keep margin tight (`0` top, `4px` bottom).

### 5.4.7 Summary placeholder

1. Add Text Editor.
2. Content: one to two sentence placeholder summary.
3. Typography:
   - Body Small token
   - Color: `#5A6A77`
4. Add minimum height:
   - `84px` desktop
   - `0` on mobile

### 5.4.8 CTA row: `.attorney-actions`

1. Add inner container under summary.
2. Class: `attorney-actions`.
3. `Layout`:
   - Direction: `Row`
   - Gap: `10px`
4. Add `Button` widget (Call Now):
   - Class: `btn-call`
   - Text: `Call Now`
   - Link: `tel:9725769565`
   - Width: `Full`
   - Typography: 15px / 700
   - Min Height: `44px`
   - Border radius: `999px`
   - Background: `#E2C383`
   - Text Color: `#14293A`
   - Border: `1px solid #E2C383`
5. Add second Button (Read Bio):
   - Class: `btn-bio`
   - Text: `Read Bio`
   - Link: attorney bio URL
   - Width: `Full`
   - Min Height: `44px`
   - Border radius: `999px`
   - Background: `Transparent`
   - Text Color: `#032436`
   - Border: `1px solid #032436`

### 5.4.9 Hover states (UI + CSS)

In Elementor UI:

1. Card container `attorney-card -> Advanced -> Motion Effects`:
   - You can keep this off and use CSS for exact parity.

Use page-level CSS in section 9 for exact hover (lift, shadow, slight image zoom).

---

## 5.5 Duplicate card to all 7 attorneys

After one card is complete:

1. Right-click card -> `Duplicate` until you have 7 cards.
2. Replace image, name, role, bio URL, and summary per table below.

### 5.5.1 Attorney content mapping

| Name | Title | Bio URL | Image URL |
|---|---|---|---|
| Sharon Ramage | Founder & CEO | `https://www.ramagefamilylawfirm.com/attorney/ramage-sharon` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/09/Sharon-150x150.jpg` |
| Marissa Balius | Managing Attorney | `https://www.ramagefamilylawfirm.com/attorney/marissa-balius` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/09/Marissa-150x150.jpg` |
| Lisa Zahn | Senior Attorney | `https://www.ramagefamilylawfirm.com/attorney/lisa-zahn` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/11/Lisa-150x150.jpg` |
| Kaitlyn Thomas | Attorney | `https://www.ramagefamilylawfirm.com/attorney/kaitlyn-thomas` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/09/Kaitlyn-150x150.jpg` |
| Kira White | Attorney | `https://www.ramagefamilylawfirm.com/attorney/kira-white` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/09/Kira-150x150.jpg` |
| Christina Suh | Attorney | `https://www.ramagefamilylawfirm.com/attorney/christina-suh` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2025/09/Christina-150x150.jpg` |
| Kathryn Hogan | Attorney | `https://www.ramagefamilylawfirm.com/attorney/kathryn-hogan` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/01/kathryn-150x150.jpg` |

Call URL for all cards:

- `tel:9725769565`

---

## 5.6 Trust section: `.trust-block`

1. Add new container below attorney grid.
2. Class: `trust-block`.
3. `Layout`:
   - Content Width: `Boxed`
   - Boxed Width: `1240px`
   - Direction: `Column`
4. `Style`:
   - Background: gradient from `#032436` to `#0C354D`
   - Border: `1px solid rgba(255,255,255,0.14)`
   - Radius: `4px`
   - Shadow: `0 20px 44px rgba(1,18,28,0.25)`
5. `Advanced` padding:
   - `44px` all sides desktop
6. Add heading:
   - `Why Work With The Ramage Law Group?`
   - Display M style
   - Color: white
7. Add 4 trust rows (Icon List widget or 4 inner containers):
   - Each row left border: `2px solid #E2C383`
   - Left padding: `14px`
   - Title color: `#F4E2BC` bold
   - Description color: `#E8EFF5`

Trust content:

1. `Decades of Experience` - Led by Sharon Ramage, a former social worker and prosecutor with over 30 years of legal expertise.
2. `Specialized Advocacy` - Focused support for children with disabilities and families facing layered legal and educational transitions.
3. `Strategic Results` - Purpose-built strategy for complex and high-conflict family law matters where long-term outcomes matter most.
4. `Local Court Insight` - Deep familiarity with Collin, Denton, and Tarrant County court systems and procedural expectations.

---

## 5.7 How We Help section + `.help-icons-grid`

1. Add new container below trust block.
2. Keep boxed width `1240px`.
3. Add heading widget:
   - `How We Help Clients`
   - Center aligned
   - Display M token
   - Color `#032436`
4. Add inner container class `help-icons-grid`.
5. `help-icons-grid -> Layout`:
   - Direction: `Row`
   - Wrap: `Wrap`
   - Gap: `20px`
6. Build one help item container:
   - Width desktop: roughly one-third
   - Background: `#FFFFFF`
   - Border: `1px solid rgba(3,36,54,0.16)`
   - Radius: `4px`
   - Padding: `20px 18px 22px 18px`
   - Align center
   - Optional min height: `232px`
7. Add image, heading, and text widgets in that order.
8. Duplicate until you have 6 items.

### 5.7.1 How We Help content mapping

| Service | Subcopy | URL | Icon URL |
|---|---|---|---|
| Divorce | File for Divorce | `https://www.ramagefamilylawfirm.com/family-law/divorce` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/file-divorce-150x150.png` |
| Child Custody | Secure Custody & Placement | `https://www.ramagefamilylawfirm.com/family-law/child-custody` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/protect-your-child-custody-150x150.png` |
| Property Division | Protect Marital Assets | `https://www.ramagefamilylawfirm.com/family-law/property-division` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/marital-property-division-150x150.png` |
| Child Support | Ensure Fair Child Support | `https://www.ramagefamilylawfirm.com/family-law/child-support` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/family-spousal-child-support-150x150.png` |
| Alimony | Ensure Fair Spousal Support | `https://www.ramagefamilylawfirm.com/family-law/divorce/spousal-support-alimony` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/fair-alimony-spousal-support-150x150.png` |
| Guardianship | Secure Guardianship of a Child | `https://www.ramagefamilylawfirm.com/contact` | `https://www.ramagefamilylawfirm.com/wp-content/uploads/2026/02/how-guardianship-works-150x150.png` |

---

## 6. Responsive Execution (Required)

Switch Elementor responsive mode and apply these exact overrides.

## 6.1 Tablet breakpoint

1. `.attorney-grid` cards:
   - Set card width to `calc(50% - gap compensation)` or 50% in container controls.
   - Keep equal spacing.
2. `.help-icons-grid` items:
   - Set each to 50% width.
3. Intro heading:
   - Size down to around `42px`.
4. Trust section:
   - Reduce padding to `32px`.

## 6.2 Mobile breakpoint

1. `.attorney-grid` cards:
   - Each card width = `100%`.
2. `.help-icons-grid` items:
   - Each item width = `100%`.
3. Intro section:
   - Top padding `68px`, bottom `36px`.
   - H1 around `34px`.
4. Trust list:
   - Single column.
5. CTA row:
   - Switch `.attorney-actions` to vertical stack if button row feels cramped.

Why this matters:

- Prevents broken card rhythm and keeps CTA readability on small screens.

---

## 7. Super-Precise Visual Parity CSS (Paste Once)

If your UI controls get close but not exact, paste this at:

- Elementor `Page Settings -> Advanced -> Custom CSS`

```css
.attorney-card{transition:transform .26s ease,box-shadow .26s ease,border-color .26s ease}
.attorney-card:hover{transform:translateY(-8px);box-shadow:0 24px 54px rgba(3,36,54,.16);border-color:rgba(226,195,131,.55)}
.attorney-photo{aspect-ratio:4/5;overflow:hidden;position:relative}
.attorney-photo img{width:100%;height:100%;object-fit:cover;object-position:center top;transition:transform .6s ease}
.attorney-card:hover .attorney-photo img{transform:scale(1.04)}
.attorney-actions .btn-call .elementor-button{background:#E2C383;border-color:#E2C383;color:#14293A}
.attorney-actions .btn-bio .elementor-button{background:transparent;border-color:#032436;color:#032436}
.attorney-actions .btn-bio .elementor-button:hover{background:#032436;color:#fff}
.attorney-actions .btn-call .elementor-button,.attorney-actions .btn-bio .elementor-button{border-radius:999px;min-height:44px}
@media (max-width:1024px){.attorney-card{width:calc(50% - 17px)!important}}
@media (max-width:767px){.attorney-card{width:100%!important}}
```

Note:

- If you use this CSS, ensure the call and bio buttons have wrapper classes `btn-call` and `btn-bio`.

---

## 8. Manual QA Checklist (Run Before Publish)

## 8.1 Layout QA

1. Desktop shows 3 cards per row.
2. Tablet shows 2 cards per row.
3. Mobile shows 1 card per row.
4. All headshots appear in consistent portrait ratio.

## 8.2 Typography QA

1. Names are visibly premium/display style.
2. Titles are muted and smaller.
3. Summary copy remains readable with generous line-height.

## 8.3 CTA QA

1. Every attorney card has both buttons.
2. `Call Now` is visually primary.
3. `Read Bio` is clearly secondary and consistent.
4. Phone links open `tel:` on mobile.

## 8.4 Trust + icon section QA

1. Trust block appears as one cohesive premium panel.
2. How We Help icons/labels align and do not break at mobile.
3. All service links are correct.

## 8.5 Interaction QA

1. Card hover lift + image zoom feels subtle and smooth.
2. Button hover states remain within brand colors.
3. Keyboard focus is visible on links/buttons.

---

## 9. Common Pitfalls + Fixes

1. Problem: cards do not align in height.
   - Fix: Set card container to flex column and summary minimum height on desktop.

2. Problem: images crop unpredictably.
   - Fix: force `object-fit: cover` and `.attorney-photo` aspect ratio.

3. Problem: mobile buttons feel cramped.
   - Fix: stack CTA row to 1 column on mobile.

4. Problem: theme CSS overrides button styles.
   - Fix: add page-level CSS classes and increase selector specificity.

5. Problem: spacing feels crowded.
   - Fix: increase section top/bottom padding first, then card gap.

---

## 10. Build Acceleration Workflow

Follow this exact order to save time and prevent style drift:

1. Build the top wrapper.
2. Build intro.
3. Build one perfect attorney card.
4. Duplicate the card 6 times.
5. Replace card content from table.
6. Build trust block.
7. Build one help icon item.
8. Duplicate help item to 6 total and replace content.
9. Apply responsive overrides.
10. Run QA checklist.

Optional speed boost:

1. Save master attorney card as a reusable template.
2. Save help-item as a reusable template.
3. Reuse in future state pages with only content swaps.

---

## 11. Completion Criteria

You are done when all are true:

1. Visual output matches `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/ramage-attorney-hub-mockup.html`.
2. Main content sections only are rebuilt.
3. Class contract is fully applied.
4. Responsive and interaction QA pass.
5. The page reads as premium, minimalist, and family-law specific.
