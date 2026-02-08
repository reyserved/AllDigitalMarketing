# TDE Paid Landing Page — Divi Visual Builder Implementation Guide

**Applicable To:**
- `original_tde-fam_law.html` (Family Law Hub Lander)
- `TDE_Divorce_Paid_LP_Mockup.html` (Divorce Spoke Lander)

**Divi Version:** 4.x+ (2024/2025 Visual Builder)

---

## EXISTING TDE CSS VARIABLES (Reference)

The TDE site already has these CSS variables defined. Use these values to maintain brand consistency:

| Variable | Value | Usage |
|---|---|---|
| `--rc-sticky-cta-bg` | `#e41c24` | Sticky CTA background |
| `--rc-sticky-cta-theme` | `#e41c24` | Accent color |
| `--rc-sticky-cta-fg` | `#ffffff` | CTA text color |
| `--rpi-star-color` | `#fb8e28` | Review star color |
| `--sby-color-9` | `#F9F9FA` | Background alt color |

**Typography Already Set:**
- **Heading Font Family:** `'Cinzel', Georgia, "Times New Roman", serif`
- **Body Font Family:** `Montserrat, Helvetica, Arial, Lucida, sans-serif`
- Body Font Size: `16px`
- Body Line Height: `1.8em` / `28.8px`
- Body Font Weight: `500`
- Primary Text Color: `#01021d`
- Secondary Text Color: `#666`

---

## GLOBAL SETUP (Do This First)

### 1. No Theme Customizer Changes Needed

The TDE site already has Montserrat and the correct typography configured globally. Do NOT override these settings.

### 2. Page-Level CSS

When you create the page:
1. Go to **Page Settings** (gear icon at bottom of Visual Builder)
2. Under **Advanced** tab, find **Custom CSS**
3. In the **Page Custom CSS** box, paste ALL CSS from **Section 15** of this document

---

## SECTION 1: HERO SECTION

### 1.1 Create the Section

1. Add a new **Regular Section**
2. Open **Section Settings**

**Content Tab:**
- Background: **Gradient**
  - Gradient Start: `rgba(1, 2, 29, 0.85)`
  - Gradient End: `rgba(1, 2, 29, 0.85)`
  - Gradient Type: Linear
  - Gradient Direction: 180deg
- Background Image: 
  - URL: `https://images.unsplash.com/photo-1589829085413-56de8ae18c73?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80`
  - Background Image Size: Cover
  - Background Image Position: Center

**Design Tab:**
- Padding:
  - Desktop: 80px top, 80px bottom
  - Tablet: 60px top, 60px bottom
  - Phone: 50px top, 50px bottom

**Advanced Tab:**
- CSS Class: `tde-hero-section`

---

### 1.2 Create Two-Column Hero Row

1. Add a **2-Column Row** inside the section (use 60% | 40% split, or closest Divi preset)
2. Open **Row Settings**

**Design Tab:**
- Max Width: 1200px
- Column Spacing: 4%
- Equalize Column Heights: No (allow form to be taller)

**Advanced Tab:**
- CSS Class: `tde-hero-grid`

---

## LEFT COLUMN (Content)

### 1.3 Proof Bar (Using Blurb Modules)

Create a **nested row** inside the Left Column for the proof items.

1. Add a **3-Column Row** inside the Left Column (equal thirds: 1/3 | 1/3 | 1/3)

**Row Settings > Design Tab:**
- Column Spacing: 2%
- Text Alignment: Left

**Row Settings > Advanced Tab:**
- CSS Class: `tde-proof-bar-row`

#### Column 1: Proof Item 1 (Reviews)

1. Add a **Blurb Module**

**Content Tab:**
- Title: Leave empty
- Body: `<strong>4.5★</strong> from 153 Google Reviews`
- Use Icon: Yes
- Icon: Select **star** icon from Divi icon picker

**Design Tab:**
- Icon Color: `#fb8e28`
- Icon Font Size: 16px
- Icon Placement: Left
- Body Font: Montserrat
- Body Font Size: 13px
- Body Font Weight: 500
- Body Text Color: `#ffffff`

**Advanced Tab:**
- CSS Class: `tde-proof-item`

#### Column 2: Proof Item 2 (Experience)

1. Add a **Blurb Module**

**Content Tab:**
- Body: `<strong>15+ Years</strong> Serving Atlanta`
- Icon: Select **clock** icon from Divi icon picker

*(Use same Design settings as Column 1)*

#### Column 3: Proof Item 3 (Consultation)

1. Add a **Blurb Module**

**Content Tab:**
- Body: `<strong>$25 Consultation</strong> (Applied to Retainer)`
- Icon: Select **tag/price** icon from Divi icon picker

*(Use same Design settings as Column 1)*

---

### 1.4 Headline (H1)

1. Add a **Text Module** below the Proof Bar

**Content Tab:**
- Body: 
```html
<h1>Atlanta Divorce Lawyers Who Fight Smart for Your Next Chapter</h1>
```

**Design Tab:**
- Heading Font: Cinzel
- Heading Font Weight: Bold (700)
- H1 Font Size: 
  - Desktop: 42px
  - Tablet: 34px
  - Phone: 28px
- H1 Line Height: 1.15em
- H1 Text Color: `#ffffff`
- Text Alignment: Left
- Text Shadow: Horizontal 0px, Vertical 2px, Blur 4px, Color `rgba(0, 0, 0, 0.5)`

**Spacing:**
- Margin Bottom: 20px

---

### 1.5 Subheadline

1. Add a **Text Module** below the H1

**Content Tab:**
- Body:
```html
<p>Contested, uncontested, or high-asset — we guide you through divorce with a clear plan, honest advice, and courtroom-ready preparation.</p>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 400
- Text Font Size: Desktop 18px, Tablet 16px, Phone 15px
- Text Line Height: 1.7em
- Text Color: `#ffffff`
- Text Alignment: Left

**Spacing:**
- Margin Bottom: 20px

---

### 1.6 Trust Signals (Text-Only)

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<p class="tde-trust-signals">🔒 Confidential &nbsp;|&nbsp; ✓ No Obligation &nbsp;|&nbsp; ⭐ Military & First Responder Discounts</p>
```

*Note: Using Unicode symbols (🔒, ✓, ⭐) instead of Font Awesome icons for compatibility.*

**Design Tab:**
- Text Font Size: 14px
- Text Font Weight: 500
- Text Alignment: Left
- Text Color: `#ffffff`
- Text Opacity: 80%

**Spacing:**
- Margin Bottom: 25px

---

### 1.7 Segmentation Row

1. Add a **Code Module**

**Code Module Content:**
```html
<div class="tde-segmentation-row">
    <a href="#uncontested-divorce" class="tde-seg-btn">Uncontested Divorce</a>
    <a href="#contested-divorce" class="tde-seg-btn">Contested Divorce</a>
    <a href="#high-asset-divorce" class="tde-seg-btn">High-Asset Divorce</a>
    <a href="#lgbtq-divorce" class="tde-seg-btn">LGBTQ+ Divorce</a>
    <a href="#legal-separation" class="tde-seg-btn">Legal Separation</a>
</div>
```

---

## RIGHT COLUMN (Lead Capture Form)

### 1.8 Form Container Setup

1. In the **Right Column**, add Column Settings:

**Content Tab:**
- Background Color: `rgba(255, 255, 255, 0.98)`

**Design Tab:**
- Border: Rounded Corners 10px (all)
- Box Shadow: Vertical 15px, Blur 40px, Color `rgba(0,0,0,0.3)`
- Padding: 35px top, 30px left, 30px right, 35px bottom

**Advanced Tab:**
- CSS Class: `tde-hero-form-wrapper`

---

### 1.9 Form Title

1. Add a **Text Module** inside the Right Column

**Content Tab:**
- Body:
```html
<h3>Speak With an Atlanta Divorce Attorney</h3>
<p class="tde-form-subtitle">Get a confidential case evaluation today.</p>
```

**Design Tab:**
- H3 Font: Cinzel
- H3 Font Size: 22px
- H3 Font Weight: Bold (700)
- H3 Text Color: `#01021d`
- H3 Text Alignment: Center
- Body Font Size: 14px
- Body Text Color: `#666`
- Body Text Alignment: Center

**Spacing:**
- Margin Bottom: 20px

---

### 1.10 Lead Form (Contact Form 7 - Recommended)

The TDE site already uses **Contact Form 7** in the footer. Use CF7 for the hero form to maintain consistency and ensure submissions work.

---

**Option A: Contact Form 7 (Recommended)**

#### Step 1: Create New CF7 Form

1. Go to **WordPress Admin** → **Contact** → **Add New**
2. Name the form: `Hero Lead Form`
3. Paste this form template:

```html
<div class="tde-form-group">
    <label>Full Name *</label>
    [text* your-name placeholder "Your Name"]
</div>

<div class="tde-form-group">
    <label>Email Address *</label>
    [email* your-email placeholder "you@example.com"]
</div>

<div class="tde-form-group">
    <label>Phone Number *</label>
    [tel* your-phone placeholder "(555) 123-4567"]
</div>

<div class="tde-form-group">
    <label>Type of Divorce</label>
    [select divorce-type include_blank "Select your situation..." "Uncontested Divorce" "Contested Divorce" "High-Asset Divorce" "LGBTQ+ Divorce" "Legal Separation" "Other / Not Sure"]
</div>

[submit class:tde-form-cta "Start My Divorce Consultation"]

<p class="tde-form-disclaimer">🔒 Your information is secure and confidential.</p>
<p class="tde-form-phone">Prefer to call? <a href="tel:4043308833">(404) 330-8833</a></p>
```

4. Configure the **Mail** tab:
   - To: `your-email@tdefamilylaw.com`
   - Subject: `New Divorce Consultation Request from [your-name]`
   - Message Body: Include all field data

5. **Save** and note the form ID (shown in shortcode, e.g., `id="590"`)

#### Step 2: Add CF7 Shortcode to Hero

1. In Divi, go to **Hero Section** → **Right Column** → **Code Module**
2. Replace the content with:

```html
[contact-form-7 id="YOUR_FORM_ID" title="Hero Lead Form" html_class="tde-hero-form"]
```

*Replace `YOUR_FORM_ID` with the actual form ID from Step 1.*

---

**Option B: Use Divi's Native Contact Form Module**

If you prefer not to use CF7, Divi has a built-in form module:

1. Add a **Contact Form Module**

**Content Tab > Fields:**
- Field 1: Name (Required)
- Field 2: Email (Required)
- Field 3: Phone
- Field 4: Select Field → "Type of Divorce" with options

**Design Tab:**
- Field Background: `#ffffff`
- Field Border: 1px solid `#d0d0d0`, 5px radius
- Submit Button Background: `#e41c24`
- Submit Button Text: White, Bold

---

### 1.11 Contact Form 7 Styling (Add to Page CSS)

Add this CSS to style the CF7 form within the hero:

```css
/* --- Contact Form 7 Hero Styling --- */
.tde-hero-form-wrapper .wpcf7 {
    width: 100%;
}
.tde-hero-form-wrapper .wpcf7-form-control:not([type="submit"]) {
    width: 100% !important;
    padding: 12px 15px !important;
    border: 1px solid #d0d0d0 !important;
    border-radius: 5px !important;
    font-size: 1rem !important;
    font-family: Montserrat, Helvetica, Arial, sans-serif !important;
}
.tde-hero-form-wrapper .wpcf7-form-control:focus {
    border-color: #e41c24 !important;
    outline: none !important;
}
.tde-hero-form-wrapper .wpcf7-submit {
    width: 100% !important;
    padding: 15px !important;
    background-color: #e41c24 !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    margin-top: 10px !important;
    font-family: Montserrat, Helvetica, Arial, sans-serif !important;
}
.tde-hero-form-wrapper .wpcf7-submit:hover {
    background-color: #b81219 !important;
}
.tde-hero-form-wrapper .tde-form-group {
    margin-bottom: 0.5em;
}
.tde-hero-form-wrapper .tde-form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    color: #01021d;
    margin-bottom: 5px;
}
.tde-hero-form-wrapper .wpcf7-response-output {
    margin: 15px 0 0 0 !important;
    padding: 10px !important;
    border-radius: 5px !important;
}
```

---

## SECTION 2: TRUST BAR (Why Atlanta Families Choose TDE)

### 2.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#f9f9fa` (uses existing `--sby-color-9`)
- Padding: 40px top, 40px bottom
- Border: 
  - Bottom Border Width: 1px
  - Bottom Border Color: `#e1e1e1`

### 2.2 Create 4-Column Row

1. Add a **4-Column Row** (equal: 1/4 | 1/4 | 1/4 | 1/4)

**Row Settings > Design Tab:**
- Max Width: 1200px
- Column Spacing: 3%
- Equalize Column Heights: Yes

**Row Settings > Advanced Tab:**
- CSS Class: `tde-trust-grid`

### 2.3 Each Column: Trust Item

For each of the 4 columns, add a **Blurb Module**:

#### Column 1 Example:

**Content Tab:**
- Title: `15+ Years of Experience:`
- Body: `Deep knowledge of Georgia divorce courts and judges.`
- Use Icon: Yes
- Icon: Scale/Balance icon from Divi picker

**Design Tab:**
- Icon Color: `#e41c24` (uses `--rc-sticky-cta-theme`)
- Icon Font Size: 36px
- Title Font: Montserrat
- Title Font Weight: Bold (700)
- Title Font Size: 16px
- Title Text Color: `#01021d`
- Body Font: Montserrat
- Body Font Size: 14px
- Body Font Weight: 500
- Body Text Color: `#666`
- Text Alignment: Center
- Icon Placement: Top

**Spacing:**
- Icon Margin Bottom: 15px

**Repeat for other 3 columns** with:
- Column 2: Gavel icon + "Georgia Family Law Focus:" + "Divorce is not a sideline—it's our core practice."
- Column 3: Comments icon + "Honest Case Assessments:" + "We tell you what to expect, not what you want to hear."
- Column 4: Tag icon + "Affordable & Transparent:" + "$25 consultation fee applied to your retainer if hired within 7 days."

---

## SECTION 3: THE STAKES (Bridging Section)

### 3.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#ffffff`
- Padding: 60px top, 60px bottom
- Text Alignment: Center

### 3.2 Create 1-Column Row

1. Add a **1-Column Row**

**Row Settings > Design Tab:**
- Max Width: 900px

### 3.3 Headline

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h2>Divorce Decisions Today Shape Your Life for Years.</h2>
```
(For Family Law Hub: `You Shouldn't Have to Guess About Your Future.`)

**Design Tab:**
- Heading Font: Cinzel
- Heading Font Weight: Bold (700)
- H2 Font Size:
  - Desktop: 40px
  - Tablet: 32px
  - Phone: 26px
- H2 Text Color: `#01021d`
- Text Alignment: Center
- Margin Bottom: 20px

### 3.4 Body Copy

1. Add a **Text Module**

**Content Tab:**
- Body: (verbatim from copy)
```
The terms of your divorce—property division, debt allocation, custody schedules, support orders—will define your financial freedom and family relationships long after the paperwork is signed. You need an advocate who doesn't just "process" your case, but builds a strategy to protect your future.
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 500
- Text Font Size:
  - Desktop: 18px
  - Tablet: 16px
  - Phone: 15px
- Text Line Height: 1.8em
- Text Color: `#01021d`
- Max Width: 800px
- Module Alignment: Center
- Text Alignment: Center

### 3.5 Tagline (Accent)

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<p class="tde-accent-tagline">We help you get organized, get strategic, and get a resolution.</p>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: Bold (700)
- Text Font Size: 20px
- Text Color: `#e41c24` (uses `--rc-sticky-cta-theme`)
- Text Alignment: Center
- Margin Top: 20px

---

## SECTION 4: PRACTICE AREA CARDS

### 4.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#f9f9fa`
- Padding: 80px top, 80px bottom

### 4.2 Create the Card Grid (Hybrid Native + Code Method)
 
 We will use **Divi Columns** as the "Card" wrappers. This allows you to use standard **Image Modules** (easy to swap) combined with **Text Modules** for the content.
 
 **Structure for Divorce Lander (5 Cards):**
 1. **Row 1:** Add a **3-Column Row** (Cards 1-3).
 2. **Row 2:** Add a **2-Column Row** (Cards 4-5).
    - *To center Row 2:* Go to Row Settings > Design > Sizing > Width: 70% (or fixed px) > Module Alignment: Center.
 
 **Structure for Family Law Hub (7 Cards):**
 1. **Row 1:** Add a **3-Column Row** (Cards 1-3).
 2. **Row 2:** Add a **3-Column Row** (Cards 4-6).
 3. **Row 3:** Add a **1-Column Row** (Card 7).
    - *To center Row 3:* Row Settings > Design > Sizing > Max Width: 350px > Module Alignment: Center.
 
 ---
 
 ### 4.3 Styling the Columns (The "Card" Look)
 
 **Apply these settings to EVERY Column (Card) individually:**
 
 1. **Column Settings > Content:**
    - Background Color: `#ffffff`
 
 2. **Column Settings > Design > Border:**
    - Rounded Corners: 8px (All corners)
    - Border Styles: All sides
    - Border Width: 1px
    - Border Color: `#e1e1e1`
 
 3. **Column Settings > Design > Box Shadow:**
    - Styles: First option (subtle drop shadow)
    - Vertical Position: 4px
    - Blur Strength: 6px
    - Shadow Color: `rgba(0,0,0,0.05)`
 
 4. **Column Settings > Advanced > CSS Class:**
    - Class: `tde-hybrid-card`
    - Vertical Overflow: Hidden (Important! Prevents image from poking out corners)
    - Horizontal Overflow: Hidden
 
 ---
 
 ### 4.4 Add Modules to Each Column
 
 **Module A: Image Module (The Header)**
 1. Settings > Content > Image: Upload image (Use roughly 600x300px).
 2. Settings > Design > Sizing > Force Fullwidth: Yes.
 3. Settings > Design > Spacing > Margin: Bottom 0px.
 4. Settings > Advanced > CSS Class: `tde-card-img`
 
 **Module B: Text Module (The Content)**
 1. Settings > Content > Body: Paste the HTML below.
 2. Settings > Design > Spacing > Padding: 25px Left, 25px Right, 25px Bottom, 15px Top.
 
 **HTML for Text Module:**
 ```html
 <h3>[Card Title]</h3>
 <p class="tde-card-stakes">[Stakes Text]</p>
 <ul class="tde-card-list">
    <li>[Bullet Text]</li>
 </ul>
 <p class="tde-card-why"><strong>The Difference:</strong> [Difference Text]</p>
 <a href="#" class="tde-btn-small">Talk to a Lawyer</a>
 ```
 
 ---
 
 ### 4.5 Card Content Reference
 
 *Refer to the tables below for copy. Use unique images for each card.*
 
 **Divorce Lander (5 Cards):**
 | Title | Stakes | Action | Difference | CTA Button Text |
 |---|---|---|---|---|
 | Uncontested Divorce | Agree on terms? One error can still cost thousands. | We file correctly for the fastest resolution. | Done right the first time. | **Start My Uncontested Divorce** |
 | Contested Divorce | Disputes over assets or custody can drag on. | We build a litigation-ready case. | Trial-ready leverage. | **Build My Litigation Strategy** |
 | High-Asset Divorce | Complex assets require forensic attention. | We identify & value high-value assets. | We don't leave money on the table. | **Protect My Assets Today** |
 | LGBTQ+ Divorce | Unique considerations for property/parents. | Specialized support for our community. | Judgment-free representation. | **Speak with an LGBTQ+ Ally** |
 | Legal Separation | Need boundaries without dissolving marriage? | We draft agreements while married. | Clarity and protection. | **Draft My Separation Agreement** |
 
 **Family Law Hub (7 Cards):**
 | Title | Stakes | Action | Difference | CTA Button Text |
 |---|---|---|---|---|
 | Divorce | Terms set today define future finances. | Asset protection strategy. | Prepare every case for trial leverage. | **Get A Divorce Strategy** |
 | Child Custody | Relationship with child is worth fighting for. | Advocating for your bond. | Bias-free advocacy. | **Fight For My Custody Rights** |
 | Child Support | Support orders must reflect reality. | Accurate income calculation. | Transparency—no hidden income. | **Calculate Fair Support** |
 | Alimony | Often the most subjective disputed part. | Fair terms for stability. | Defensible, fact-based arguments. | **Discuss Alimony Options** |
 | Property Division | "Equitable" doesn't always mean "Equal". | Valuing marital assets. | We find, value, and fight for assets. | **Secure My Property Share** |
 | Paternity | Legal fatherhood grants visitation. | Establishing Rights. | Validated standing for you/child. | **Establish Legal Paternity** |
 | Guardianship | When a loved one can't protect themselves. | Urgent Filings. | Legal authority with compassion. | **Consult on Guardianship** |

---

## SECTION 5: WHY CHOOSE TDE (Calm, Dangerous Competence)

### 5.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#ffffff`
- Padding: 80px top, 80px bottom

### 5.2 Create 1-Column Row

1. Add a **1-Column Row**

**Row Settings > Design Tab:**
- Max Width: 900px

### 5.3 Headline

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h2>Calm, Dangerous Competence.</h2>
```

**Design Tab:**
- Heading Font: Cinzel
- Heading Font Weight: Bold (700)
- H2 Font Size:
  - Desktop: 40px
  - Tablet: 32px
  - Phone: 26px
- H2 Text Color: `#01021d`
- Text Alignment: Center
- Margin Bottom: 30px

### 5.4 Body Paragraph

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<p>We believe the best divorce attorney isn't the one who yells the loudest—it's the one who is most prepared. We push for amicable resolution to minimize your stress and expense, but <strong>we do not back down</strong> from litigation when your rights are threatened.</p>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 500
- Text Font Size: 16px
- Text Line Height: 1.8em
- Text Color: `#01021d`
- Text Alignment: Left

### 5.5 Subheadline

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h3>We Handle the Tough Cases:</h3>
```

**Design Tab:**
- Heading Font: Cinzel
- Heading Font Weight: Bold (700)
- H3 Font Size: 24px
- H3 Text Color: `#01021d`
- Margin Top: 30px
- Margin Bottom: 15px

### 5.6 Bullet List

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<ul class="tde-checkmark-list">
<li><strong>Complex Asset Division:</strong> Business valuations, hidden assets, retirement accounts.</li>
<li><strong>Custody Disputes:</strong> Protecting your parenting time and relationship.</li>
<li><strong>High-Conflict Situations:</strong> When "fair" isn't on the table, we fight until it is.</li>
</ul>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 500
- Text Font Size: 16px
- Text Color: `#01021d`

---

## SECTION 6: OUR PROCESS (3-Step Timeline)

### 6.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#01021d`
- Padding: 100px top, 100px bottom

### 6.2 Create 2-Column Row

1. Add a **2-Column Row** (40% | 60% or 1/3 | 2/3)

**Row Settings > Design Tab:**
- Max Width: 1200px
- Column Spacing: 5%

---

### 6.3 Left Column: Title

1. Add a **Text Module** in Column 1

**Content Tab:**
- Body:
```html
<h2>Our Process:<br>What to Expect</h2>
```

**Design Tab:**
- Heading Font: Cinzel
- Heading Font Weight: Bold (700)
- H2 Font Size:
  - Desktop: 48px
  - Tablet: 36px
  - Phone: 28px
- H2 Line Height: 1.1em
- H2 Text Color: `#ffffff`

---

### 6.4 Right Column: Timeline Steps

Add a **Code Module** in Column 2:

```html
<div class="tde-process-timeline">
    <div class="tde-timeline-item">
        <span class="tde-timeline-step">Step 1</span>
        <span class="tde-timeline-title">Start Your Consultation</span>
        <div class="tde-timeline-desc">Tell us your situation, your goals, and your concerns. We'll explain your rights under Georgia law and give you an honest assessment.</div>
    </div>
    <div class="tde-timeline-item">
        <span class="tde-timeline-step">Step 2</span>
        <span class="tde-timeline-title">Get Your Strategy</span>
        <div class="tde-timeline-desc">We build a tailored plan—whether that's negotiation, mediation, or litigation—so you know exactly what to expect and what to prepare.</div>
    </div>
    <div class="tde-timeline-item">
        <span class="tde-timeline-step">Step 3</span>
        <span class="tde-timeline-title">Take Action</span>
        <div class="tde-timeline-desc">We execute the strategy, advocating for you every step of the way until your divorce is finalized and your future is protected.</div>
    </div>
</div>
```

---

## SECTION 7: MEET YOUR LEGAL TEAM (Divorce Lander Only)

### 7.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#f9f9fa`
- Padding: 80px top, 80px bottom

### 7.2 Headline

1. Add a **1-Column Row**
2. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h2>Meet Your Legal Team</h2>
<p class="tde-team-intro">Our experienced divorce and family law team provides compassionate, client-focused representation tailored to your needs.</p>
```

**Design Tab:**
- H2 Font: Cinzel Bold
- H2 Font Size: 40px
- H2 Text Alignment: Center
- H2 Text Color: `#01021d`
- Body Font Size: 16px
- Body Font Weight: 500
- Body Font Style: Italic
- Body Text Color: `#666`
- Margin Bottom: 40px

### 7.3 Team Grid

1. Add a **5-Column Row** (equal widths)

For each column, add a **Blurb Module**:

**Column 1:**
- Title: `Tessie D. Edwards`
- Body: `Managing Attorney`
- Icon: None

**Design Tab:**
- Title Font: Montserrat Bold (700)
- Title Font Size: 16px
- Title Color: `#01021d`
- Body Font Size: 14px
- Body Font Weight: 500
- Body Color: `#666`
- Text Alignment: Center

**Repeat for:**
- Column 2: Lolita K. Beyah | Attorney
- Column 3: John Evans | Attorney
- Column 4: Barry Eidex | Attorney
- Column 5: McCoy G. Martinez | Attorney

### 7.4 CTA Link

1. Add a **Text Module** below the team row

**Content Tab:**
- Body:
```html
<p style="text-align: center;"><a href="#" class="tde-btn-small">SEE OUR FULL TEAM</a></p>
```

---

## SECTION 8: FAQ SECTION

### 8.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#ffffff`
- Padding: 80px top, 80px bottom

### 8.2 Headline

1. Add a **1-Column Row**
2. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h2>Frequently Asked Questions</h2>
```

**Design Tab:**
- Heading Font: Cinzel Bold (700)
- H2 Font Size: 40px
- H2 Text Color: `#01021d`
- Text Alignment: Center
- Margin Bottom: 50px

### 8.3 FAQ Items

Use **Toggle Modules** for each FAQ.

#### Toggle 1:

**Content Tab:**
- Title: `Q: How long does a divorce take in Georgia?`
- Body: `A: Uncontested divorces can finalize in as little as 31 days. Contested cases vary depending on complexity, but we work to resolve issues as efficiently as possible.`
- State: Closed

**Design Tab:**
- Toggle Title Font: Montserrat Bold (700)
- Toggle Title Font Size: 18px
- Toggle Title Color: `#01021d`
- Toggle Body Font: Montserrat
- Toggle Body Font Weight: 500
- Toggle Body Font Size: 16px
- Toggle Body Color: `#666`
- Toggle Icon Color: `#e41c24`
- Border Bottom: 1px solid `#e1e1e1`
- Padding Bottom: 20px
- Margin Bottom: 30px

---

## SECTION 9: CLOSING CTA SECTION

### 9.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#e41c24` (uses `--rc-sticky-cta-bg`)
- Padding: 40px top, 40px bottom

### 9.2 Create 1-Column Row

1. Add a **1-Column Row**

**Design Tab:**
- Text Alignment: Center

### 9.3 Headline

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<h2>Ready to Move Forward? Let's Talk.</h2>
```
(For Family Law Hub: `Ready to Turn the Page? Let's Talk.`)

**Design Tab:**
- H2 Font: Montserrat Bold (700)
- H2 Font Size: 32px
- H2 Text Color: `#ffffff`
- Text Alignment: Center
- Margin Bottom: 10px

### 9.4 Subheadline

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<p>The first step is a confidential conversation. No obligation. Just clear answers about your situation and your options.</p>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 500
- Text Font Size: 18px
- Text Color: `#ffffff`
- Text Alignment: Center

### 9.5 Primary CTA Button

1. Add a **Button Module**

**Content Tab:**
- Button Text: `START MY DIVORCE CONSULTATION`
- Button Link: `#`

**Design Tab:**
- Button Alignment: Center
- Button Text Color: `#e41c24`
- Button Background Color: `#ffffff`
- Button Border Radius: 4px
- Button Font: Montserrat Bold (700)
- Button Font Size: 16px
- Button Padding: 15px top/bottom, 30px left/right

**Spacing:**
- Margin Top: 20px
- Margin Bottom: 10px

### 9.6 Secondary CTA (Phone Link)

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<a href="tel:4043308833" class="tde-phone-link-white">Call Now: (404) 330-8833</a>
```

**Design Tab:**
- Text Font Size: 14px
- Text Font Weight: 500
- Text Color: `#ffffff`
- Text Alignment: Center

### 9.7 Trust Signals

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<div class="tde-trust-signals">
<i class="fa-solid fa-lock"></i> Confidential &nbsp;|&nbsp;
<i class="fa-solid fa-check-circle"></i> No Obligation &nbsp;|&nbsp;
<i class="fa-solid fa-clock"></i> We respond within 24 business hours &nbsp;|&nbsp;
<i class="fa-solid fa-tag"></i> $25 Consultation (Applied to Retainer)
</div>
```

**Design Tab:**
- Text Font Size: 14px
- Text Font Weight: 500
- Text Color: `#ffffff`
- Text Alignment: Center

---

## SECTION 10: FOOTER DISCLAIMERS

### 10.1 Create the Section

1. Add a new **Regular Section**

**Design Tab:**
- Background Color: `#000000`
- Padding: 40px top, 40px bottom

### 10.2 Create 1-Column Row

1. Add a **1-Column Row**

**Design Tab:**
- Text Alignment: Center

### 10.3 Disclaimer Text

1. Add a **Text Module**

**Content Tab:**
- Body:
```html
<p><strong>Disclaimer:</strong> Prior results do not guarantee similar outcomes. The information on this page is for general purposes and does not constitute legal advice.</p>
<p><strong>Relationship:</strong> No attorney-client relationship is formed until a written fee agreement is signed.</p>
<p><strong>Location:</strong> Serving Atlanta, Georgia and surrounding communities.</p>
<p style="margin-top: 20px;">&copy; 2026 TDE Family Law. All Rights Reserved.</p>
```

**Design Tab:**
- Text Font: Montserrat
- Text Font Weight: 500
- Text Font Size: 13px
- Text Color: `#666`
- Text Alignment: Center
- Text Line Height: 1.8em

---

## SECTION 15: COMPLETE PAGE CSS

**Paste this into Page Settings > Advanced > Custom CSS**

All class names are prefixed with `tde-` to avoid conflicts with existing site styles.

```css
h1, h2, h3 {
font-family: 'Cinzel', Georgia, "Times New Roman", serif;
}
.tde-proof-bar {
display: flex;
justify-content: center;
gap: 20px;
margin-bottom: 30px;
font-size: 14px;
opacity: 0.9;
}
.tde-proof-item {
display: flex;
align-items: center;
gap: 8px;
}
.tde-proof-item i {
color: #fb8e28;
}
.tde-subheadline {
font-weight: 300;
}
.tde-phone-link {
color: #ffffff;
text-decoration: underline;
}
.tde-phone-link:hover {
opacity: 0.8;
}
.tde-phone-link-white {
color: #ffffff;
text-decoration: underline;
}
.tde-friction-reducers {
opacity: 0.8;
font-size: 13px;
}
.tde-segmentation-row {
display: flex;
flex-wrap: wrap;
justify-content: center;
gap: 10px;
max-width: 1000px;
margin: 0 auto;
}
.tde-seg-btn {
background-color: rgba(255, 255, 255, 0.1);
border: 1px solid rgba(255, 255, 255, 0.3);
color: #ffffff;
padding: 10px 20px;
border-radius: 30px;
font-size: 14px;
font-weight: 600;
text-decoration: none;
transition: all 0.3s ease;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
}
.tde-seg-btn:hover {
background-color: #e41c24;
border-color: #e41c24;
transform: translateY(-2px);
}

/* --- Hero Grid (Two-Column Layout) --- */
.tde-hero-grid {
display: grid;
grid-template-columns: 1fr 400px;
gap: 60px;
align-items: center;
}
.tde-hero-content {
text-align: left;
}
.tde-hero-content h1 {
font-size: 2.8rem;
line-height: 1.15;
}
.tde-trust-signals {
font-size: 0.85rem;
opacity: 0.8;
margin-bottom: 25px;
}
.tde-trust-signals i {
margin-right: 5px;
}

/* --- Hero Form Wrapper --- */
.tde-hero-form-wrapper {
background: rgba(255, 255, 255, 0.98);
padding: 35px 30px;
border-radius: 10px;
box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}
.tde-hero-form-wrapper h3 {
color: #01021d;
font-size: 1.4rem;
margin-bottom: 8px;
text-align: center;
}
.tde-form-subtitle {
color: #666;
font-size: 0.9rem;
text-align: center;
margin-bottom: 20px;
}
.tde-form-group {
margin-bottom: 15px;
}
.tde-form-group label {
display: block;
font-size: 0.85rem;
font-weight: 600;
color: #01021d;
margin-bottom: 5px;
}
.tde-form-group input,
.tde-form-group select {
width: 100%;
padding: 12px 15px;
border: 1px solid #d0d0d0;
border-radius: 5px;
font-size: 1rem;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
transition: border-color 0.3s ease;
}
.tde-form-group input:focus,
.tde-form-group select:focus {
outline: none;
border-color: #e41c24;
}
.tde-form-cta {
width: 100%;
padding: 15px;
background-color: #e41c24;
color: white;
border: none;
border-radius: 5px;
font-size: 1rem;
font-weight: 700;
text-transform: uppercase;
cursor: pointer;
transition: background-color 0.3s ease;
margin-top: 10px;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
}
.tde-form-cta:hover {
background-color: #b81219;
}
.tde-form-disclaimer {
font-size: 0.75rem;
color: #888;
text-align: center;
margin-top: 15px;
line-height: 1.4;
}
.tde-form-phone {
text-align: center;
margin-top: 15px;
font-size: 0.9rem;
color: #01021d;
}
.tde-form-phone a {
color: #e41c24;
font-weight: 700;
text-decoration: none;
}
.tde-form-phone a:hover {
text-decoration: underline;
}

/* --- Accent Tagline --- */
.tde-accent-tagline {
font-weight: 700;
font-size: 20px;
color: #e41c24;
}

/* --- Hybrid Card Styles --- */
.tde-hybrid-card {
transition: all 0.3s ease;
/* Initial border/shadow handled in Divi Settings, hover handled here */
}
.tde-hybrid-card:hover {
transform: translateY(-5px);
box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1) !important; /* Force override Divi inline styles if needed */
border-color: #e41c24 !important;
}
.tde-hybrid-card h3 {
color: #e41c24;
font-size: 20px;
font-weight: 700;
margin-top: 0;
margin-bottom: 15px;
border-bottom: 2px solid #f9f9fa;
padding-bottom: 10px;
display: inline-block;
font-family: 'Cinzel', Georgia, "Times New Roman", serif;
}
.tde-card-stakes {
font-weight: 600;
font-style: italic;
margin-bottom: 15px;
color: #01021d;
font-size: 15px;
line-height: 1.5em;
}
.tde-card-list {
list-style: none !important;
list-style-type: none !important;
list-style-image: none !important;
padding-left: 0 !important;
margin-left: 0 !important;
margin-bottom: 20px;
}
.tde-card-list li {
list-style: none !important;
list-style-type: none !important;
list-style-image: none !important;
position: relative;
padding-left: 20px;
margin-bottom: 8px;
font-size: 14px;
line-height: 1.6em;
}
/* Remove browser default ::marker bullet */
.tde-card-list li::marker {
content: "" !important;
content: none !important;
font-size: 0 !important;
display: none !important;
color: transparent !important;
}
/* Custom checkmark icon */
.tde-card-list li::before {
content: "\f00c";
font-family: "Font Awesome 6 Free";
font-weight: 900;
color: #e41c24;
position: absolute;
left: 0;
}
.tde-card-why {
font-size: 14px;
margin-bottom: 20px;
color: #666;
border-top: 1px solid #f0f0f0;
padding-top: 15px;
}
.tde-btn-small {
display: inline-block;
color: #e41c24;
font-weight: 700;
text-transform: uppercase;
font-size: 13px;
text-decoration: none;
transition: color 0.3s ease;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
cursor: pointer;
}
.tde-btn-small:hover {
color: #01021d;
text-decoration: underline;
}
.tde-checkmark-list {
list-style: none !important;
list-style-type: none !important;
list-style-image: none !important;
padding-left: 0 !important;
margin-left: 20px;
}
.tde-checkmark-list li {
list-style: none !important;
list-style-type: none !important;
list-style-image: none !important;
position: relative;
padding-left: 30px;
margin-bottom: 15px;
}
/* Remove browser default ::marker bullet */
.tde-checkmark-list li::marker {
content: "" !important;
content: none !important;
font-size: 0 !important;
display: none !important;
color: transparent !important;
}
/* Custom checkmark icon (Unicode - no Font Awesome needed) */
.tde-checkmark-list li::before {
content: "✓";
position: absolute;
left: 0;
color: #e41c24;
font-weight: bold;
font-size: 1.1em;
}
.tde-process-timeline {
position: relative;
padding-left: 30px;
}
.tde-process-timeline::before {
content: '';
position: absolute;
left: 0;
top: 10px;
bottom: 30px;
width: 2px;
background-color: rgba(255, 255, 255, 0.2);
}
.tde-timeline-item {
position: relative;
padding-bottom: 40px;
padding-left: 30px;
}
.tde-timeline-item::before {
content: '';
position: absolute;
left: -6px;
top: 5px;
width: 14px;
height: 14px;
background-color: #ffffff;
border-radius: 50%;
z-index: 1;
}
.tde-timeline-step {
font-size: 14px;
text-transform: uppercase;
letter-spacing: 1px;
color: #e41c24;
font-weight: 700;
margin-bottom: 5px;
display: block;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
}
.tde-timeline-title {
font-size: 20px;
font-weight: 700;
margin-bottom: 10px;
display: block;
color: #ffffff;
font-family: 'Cinzel', Georgia, "Times New Roman", serif;
}
.tde-timeline-desc {
font-size: 16px;
line-height: 1.6;
color: #e0e0e0;
font-family: Montserrat, Helvetica, Arial, Lucida, sans-serif;
}
.tde-team-intro {
font-style: italic;
text-align: center;
max-width: 700px;
margin: 0 auto;
color: #666;
}
.tde-trust-signals {
margin-top: 20px;
font-size: 14px;
opacity: 0.9;
color: #ffffff;
}
/* --- Mobile Responsive CSS --- */
@media (max-width: 980px) {
  /* Hero Grid Stacking */
  .tde-hero-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .tde-hero-content {
    text-align: center;
  }
  .tde-hero-content h1 {
    font-size: 2.4rem;
  }
  .tde-hero-form-wrapper {
    max-width: 450px;
    margin: 0 auto;
  }
  .tde-segmentation-row {
    justify-content: center;
  }
  .tde-proof-bar {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  /* Typography Adjustments */
  h1 { font-size: 2rem !important; }
  .tde-subheadline p { font-size: 1rem !important; }
  .tde-hero-content h1 { font-size: 1.8rem; }
  .tde-hero-content .subheadline { font-size: 1rem; }

  /* Layout Adjustments */
  .tde-grid-container {
    grid-template-columns: 1fr;
    padding: 0 10px;
  }
  
  .tde-proof-bar {
    flex-direction: column;
    gap: 10px;
    align-items: center;
    text-align: center;
  }

  /* Process Timeline */
  .tde-process-timeline {
    padding-left: 20px;
  }
  .tde-process-timeline::before {
    left: 10px;
  }
  .tde-timeline-item {
    padding-left: 40px;
  }
  .tde-timeline-item::before {
    left: 4px;
  }

  /* Trust Bar */
  .tde-trust-grid {
    flex-direction: column; 
    align-items: center;
    grid-template-columns: 1fr;
  }
  
  /* Segmentation Row */
  .tde-segmentation-row {
    flex-direction: column;
    align-items: center;
  }
  .tde-seg-btn {
    width: 100%;
    max-width: 280px;
    text-align: center;
    margin-bottom: 5px;
  }

  /* Hero Form */
  .tde-hero-form-wrapper {
    padding: 25px 20px;
  }
  .tde-hero-form-wrapper h3 {
    font-size: 1.2rem;
  }
}
```

---

## RESPONSIVE CHECKLIST

Before publishing, preview the page on all devices and verify:

| Element | Desktop | Tablet | Phone |
|---|---|---|---|
| Hero H1 | 48px | 38px | 28px |
| Hero Subheadline | 24px | 20px | 18px |
| Proof Bar | Horizontal row | Horizontal wrap | Stacked vertical |
| Segmentation Buttons | Horizontal wrap | Horizontal wrap | Full-width stacked |
| Trust Bar Grid | 4 columns | 2 columns | 1 column |
| Card Grid | 3 columns | 2 columns | 1 column |
| Process Section | 2 columns side-by-side | Stacked | Stacked |
| Team Grid | 5 columns | 3 columns | 2 columns |
| CTA Button | 16px text | 16px text | 14px text |

**Divi Responsive Controls:**
- Click the device icons (Desktop/Tablet/Phone) at the bottom of the Visual Builder to toggle views
- Any setting with a phone/tablet icon next to it can have unique values per breakpoint
- Always set Phone values explicitly for font sizes and padding

---

## FINAL QA CHECKLIST

- [ ] All anchor links (#uncontested-divorce, etc.) scroll to correct card
- [ ] Phone number links open dialer on mobile
- [ ] All CTAs have correct destination URLs
- [ ] Font Awesome 6 icons render correctly (site already has FA6 loaded)
- [ ] No horizontal scroll on any device
- [ ] Footer disclaimers are present
- [ ] Page loads under 3 seconds (test with GTmetrix)
- [ ] Mobile tap targets are at least 44x44px
- [ ] All text uses Montserrat (inherited from theme)
- [ ] Accent color matches `#e41c24` throughout
- [ ] Secondary text color is `#666` for lighter elements
