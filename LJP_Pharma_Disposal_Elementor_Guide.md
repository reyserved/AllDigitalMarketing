# Elementor Implementation Guide: Non-Hazardous Pharmaceutical Waste Disposal Landing Page

This guide provides step-by-step instructions for recreating the pharma_disposal.html mockup in Elementor Pro on WordPress, based on the existing LJP Product Destruction page patterns.

---

## Prerequisites

- **Elementor Pro** installed and activated
- Access to **Elementor Global Colors** (Site Settings)
- Theme: Hello Elementor (LJP's current theme)
- Fonts: Poppins (headings) and Roboto (body) already configured in Elementor
- Reference mockup: `pharma_disposal.html`

---

## Step 1: Set Up Global Colors

Before building, verify the brand colors are configured as Global Colors for consistency.

1. Open any page with Elementor → Click hamburger menu (☰) → **Site Settings**
2. Go to **Global Colors**
3. Verify/add the following:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| `LJP Primary Blue` | `#18509B` | Primary brand color, headings, backgrounds |
| `LJP Secondary Orange` | `#EB9B1A` | CTA buttons, accents |
| `LJP Accent Green` | `#018846` | Sustainability accents, checkmarks |
| `LJP Text Dark` | `#333333` | Body text |
| `LJP Text Light` | `#666666` | Secondary text |
| `LJP Off-White` | `#F8F8F8` | Section backgrounds |
| `LJP White` | `#FFFFFF` | Cards, overlays |

4. **Save** settings.

---

## Step 2: Create the Page Structure

1. Create a new page: **Pages → Add New → "Non-Hazardous Pharmaceutical Waste Disposal"**
2. Click **Edit with Elementor**
3. Set page layout to **Elementor Full Width** (in page settings)
4. Set page template to use the **Elementor Header #1659** (LJP standard header)

---

## Step 3: Build Each Section

### Section 1: Hero Section (Split Panel Layout)

This is a simple 2-column split layout matching the LJP Product Destruction page hero style.

#### Parent Container Setup
1. Add a **Container** (Flexbox)
2. **Layout:**
   - Direction: **Row**
   - Align Items: Stretch
   - Content Width: **Full Width**
   - Min Height: `600px`
3. **Style → Background:** None (children will have backgrounds)

#### Left Content Panel (Child Container)
1. Add a **Container** inside the parent
2. **Layout:**
   - Width: `50%` (use Advanced → Custom Width)
   - Direction: Column
   - Justify Content: Center
   - Padding: 60px 50px
3. **Style → Background:**
   - Type: **Classic**
   - Color: `#18509B` (LJP Primary Blue)

> **Note:** This is a simple rectangular split layout with a straight vertical edge between the blue content panel and the image. No clip-path or diagonal effects needed.

#### Hero Content Widgets
1. **Heading Widget** (H1):
   - Text: "Secure, Sustainable Non-Hazardous Pharmaceutical Waste Disposal"
   - HTML Tag: `<h1>`
   - Style → Typography: 48px, 700 weight, Poppins
   - Style → Color: White
   - Line Height: 1.15

2. **Text Editor Widget** (Subhead):
   - Text: "Protect your brand and the environment. We convert your bulk pharmaceutical waste into renewable energy—100% Zero Landfill, 100% Verified."
   - Style → Typography: 18px, 300 weight, Roboto
   - Style → Color: `rgba(255, 255, 255, 0.9)`

3. **Button Widget** (Primary CTA):
   - Text: "Request a Consultation"
   - Link: `#form` (anchor to form section)
   - Style → Background: `#EB9B1A` (LJP Secondary Orange)
   - Style → Typography: 600 weight, uppercase
   - Style → Padding: 15px 35px
   - Style → Border Radius: 5px
   - **Hover:** Background `#d68b15`, Transform translateY(-2px)

4. **Button Widget** (Secondary CTA):
   - Text: "Learn Our Process"
   - Style → Background: Transparent
   - Style → Border: 2px solid white
   - Style → Color: White
   - **Hover:** Background white, color `#18509B`

5. **Trust Badges Section** (Inner Container):
   - Add a **Container** with Direction: Row, Gap: 15px, Wrap: Yes
   - Margin Top: 35px
   
   **For Each Badge (4 total):**
   - Add an **Inner Container** with:
     - Direction: Row
     - Align Items: Center
     - Padding: 8px 16px
     - Background: `rgba(255, 255, 255, 0.15)`
     - Border Radius: 50px
     - Border: 1px solid `rgba(255, 255, 255, 0.2)`
   
   - **Image Widget** (inside):
     - Image: Upload transparent PNG icon (check mark)
     - Image Size: Custom (16x16px)
     - Note: Ensure the PNG is white or light-colored to match the design
   
   - **Text Editor Widget** (inside):
     - Text: "ISO Certified" / "DEA Compliant" / "Zero Landfill Verified" / "DOT Compliant"
     - Typography: 14px, 600 weight
     - Color: `rgba(255, 255, 255, 0.95)`

#### Right Image Panel (Child Container)
1. Add a **Container** inside the parent (after the left panel)
2. **Layout:**
   - Width: `45%` (use Advanced → Custom Width)
3. **Style → Background:**
   - Type: **Classic**
   - Image: Upload hero image (pharmaceutical facility/waste management)
   - Position: Center Center
   - Size: Cover

---

### Section 2: Form Section (2-Column Layout)

This matches the existing LJP Product Destruction page pattern.

#### Parent Container Setup
1. Add a **Container** (Flexbox)
2. **Layout:**
   - Direction: Row
   - Content Width: Boxed (`1200px`)
   - Gap: 60px
   - Padding: 60px 0
3. **Style → Background:** `#F8F8F8` (LJP Off-White)

#### Left Column: Benefits (Child Container)
1. **Width:** 50%
2. **Heading Widget** (H2):
   - Text: "Why Choose LJP for Non-Hazardous Pharmaceutical Waste Disposal?"
   - HTML Tag: `<h2>`
   - Style → Typography: 32px, 700 weight
   - Style → Color: `#18509B`

3. **Icon List Widget** (Benefits):
   - Icon: Check (fas fa-check)
   - Icon Color: `#018846` (LJP Accent Green)
   - Icon Size: 20px
   
   **Items:**
   - **Absolute Brand Protection:** Your expired, off-spec, or discontinued products are a liability. We guarantee complete destruction, preventing black market resale and protecting your reputation.
   - **100% Zero Landfill Verified:** Don't just dispose of waste; transform it. We process your non-hazardous pharmaceuticals through our Waste-to-Energy program, contributing to your sustainability goals and providing full reporting for your ESG metrics.
   - **Total Compliance Confidence:** Navigating the line between RCRA hazardous vs. non-hazardous waste is complex. Our experts ensure your non-hazardous specific manufacturing waste streams (NIOSH, DOT) are managed in full compliance with federal and state regulations.
   - **Bulk Liquid & Solid Disposal:** From drums to tankers, we handle large-scale disposal needs with GPS-tracked fleets and secure chain-of-custody protocols.
   - **Witnessed Destruction & Custom Reporting:** Verified destruction reports and detailed sustainability data on waste diverted from landfills and converted to energy.

4. **Certifications Section** (NEW - fills lower whitespace):
   - Add a **Container** with:
     - Margin Top: 40px
     - Padding Top: 30px
     - Border Top: 1px solid `rgba(24, 80, 155, 0.1)`
   
   - **Heading Widget** (H4):
     - Text: "OUR CERTIFICATIONS & COMPLIANCE"
     - Typography: 16px, 600 weight, uppercase, letter-spacing 1px
     - Color: `#18509B`
     - Margin Bottom: 20px
   
   - **Inner Container** (2x2 Grid):
     - Display: Grid
     - Columns: 2
     - Gap: 15px
   
   **For Each Certification Badge (4 total):**
   - Add a **Container** with:
     - Direction: Row
     - Align Items: Center
     - Gap: 12px
     - Padding: 15px 18px
     - Background: `rgba(255, 255, 255, 0.85)`
     - Border Radius: 10px
     - Border: 1px solid `rgba(24, 80, 155, 0.12)`
     - Box Shadow: `0 4px 15px rgba(0, 0, 0, 0.05)`
   
   - **Image Widget** (for the icon wrapper):
     - Image: Upload PNG icon (Shield, Checkmark, Truck, Recycle)
     - Image Size: Custom (24x24px)
     - Background: Gradient `#18509B` to `#0e3a6b` (set in Advanced → Background)
     - Padding: 10px (to create spacing around the icon)
     - Border Radius: 50%
     - Width: Custom (44px)
   
   - **Container** (text wrapper inside):
     - Direction: Column
     - **Heading** (Title): "ISO Certified" - 14px, 700 weight, `#18509B`
     - **Text** (Subtitle): "Quality Management" - 12px, `#666666`

#### Right Column: Form (Child Container)
1. **Width:** 50%
2. **Style:**
   - Background: White
   - Padding: 35px 40px
   - Border Radius: 8px
   - Box Shadow: `0 5px 20px rgba(0, 0, 0, 0.08)`
3. **CSS ID:** `form` (for anchor link)

4. **Content Widgets:**
   - **Heading Widget** (H3/H4):
     - Text: "Get Your Custom Pharmaceutical Waste Disposal Plan"
     - HTML Tag: `<h3>` or `<h4>`
     - Typography: 24px, 700 weight
     - Color: `#18509B`
     - Class: `blueText` (matches existing LJP pattern)
   
   - **Text Editor Widget**:
     - Text: "Complete our secure form, and an expert will reach out to discuss a clear strategy for your pharmaceutical waste streams."
     - Typography: 14px
     - Color: `#666666`
     - Margin Bottom: 25px
   
   - **Form Widget** (Elementor Pro):
     - **Fields:**
       - Name (Text) - Label: Name, Placeholder: Your name
       - Address (Text) - Label: Address, Placeholder: Your address, Required
       - Number (Tel) - Label: Number, Placeholder: Your number, Required
       - Email (Email) - Label: Email, Placeholder: Your email, Required
       - Message (Textarea) - Label: Message, Placeholder: Message, Rows: 4
     
     - **Submit Button:**
       - Text: "Send"
       - Width: Custom (25%)
       - Background: `#018846` (LJP Accent Green)
       - Typography: 600 weight
       - Padding: 14px 35px
       - Border Radius: 5px
       - Hover: Background `#006030`, Transform translateY(-2px)
     
     - **Actions After Submit:** Configure email notifications and redirect
     
     - **Add Hidden Fields for UTM tracking:**
       - utm_source, utm_medium, utm_campaign, utm_term, matchtype, gclid

---

### Section 3: Value Propositions (3-Card Grid)

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px 0
3. **Style → Background:** White

#### Content Widgets
1. **Heading Widget** (H2):
   - Text: "Beyond Disposal. A Strategic Partnership."
   - Alignment: Center
   - Typography: 40px, 700 weight
   - Color: `#18509B`
   - Margin Bottom: 60px

2. **Inner Container** (3-Column Grid):
   - Display: Grid
   - Columns: 3 (desktop), 1 (mobile)
   - Gap: 40px

**For Each Value Prop Card (3 total):**
- Add a **Container** with:
  - Padding: 40px
  - Border Radius: 8px
  - Box Shadow: `0 10px 30px rgba(0, 0, 0, 0.05)`
  - Border Top: 4px solid `#EB9B1A`
  - **Hover:** Transform translateY(-10px)

- **Image Widget** (inside):
  - Image: Upload PNG icon (Shield / Checkbox / Verified badge)
  - Image Size: Medium (approx 60px)
  - Alignment: Left
  - Style → CSS Filters: Can be used to recolor if needed, otherwise use pre-colored PNGs
  - Background: `#F0F0F0` (set in Advanced → Background, with padding)
  - Border Radius: 50%
  - Width: Custom (60px) or set padding to create the circle effect

- **Heading Widget** (H3):
  - Text: "1. Absolute Brand Protection" / "2. 100% Zero Landfill Verified" / "3. Total Compliance Confidence"
  - Typography: 24px, 700 weight
  - Color: `#18509B`

- **Text Editor Widget**:
  - Description text
  - Typography: 16px
  - Color: `#666666`

---

### Section 4: Process Section (4-Step Grid)

This matches the existing LJP "Here's how it works" pattern.

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px 0
3. **Style → Background:** `#18509B` (LJP Primary Blue)

#### Content Widgets
1. **Heading Widget** (H2/H3):
   - Text: "Here's how it works:"
   - HTML Tag: `<h3>` (matches existing pattern)
   - Alignment: Center
   - Typography: 32px, 700 weight
   - Color: White
   - Margin Bottom: 60px

2. **Inner Container** (4-Column Grid):
   - Display: Grid
   - Columns: 4 (desktop), 2 (tablet), 1 (mobile)
   - Gap: 30px

**For Each Process Step (4 total):**
Use the **Image Box Widget** with:
- **Image:** Upload corresponding PNG Icon
  - Step 1: Laptop/Request icon
  - Step 2: Checklist/Document icon
  - Step 3: Calendar/Clock icon
  - Step 4: Certificate/Shield icon
- **Image Position:** Top
- **Image Width:** 50px

- **Title & Description:**
  - Title: "1. Request a Consultation" (etc.)
  - Title Typography: 18px, 700 weight, White
  - Description: Process text
  - Description Typography: 15px, 400 weight, `rgba(255, 255, 255, 0.85)`
  - Description Max Width: 250px

---

### Section 5: Educational Section (2-Column Layout)

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Row
   - Content Width: Boxed
   - Gap: 60px
   - Align Items: Center
   - Padding: 80px 0
3. **Style → Background:** `#18509B` (continue blue background)

#### Left Column: Content
1. **Heading Widget** (H2):
   - Text: "Is Your Pharmaceutical Waste Really 'Non-Hazardous'?"
   - Typography: 40px, 700 weight
   - Color: White

2. **Text Editor Widget**:
   - Educational content paragraphs
   - Typography: 18px
   - Color: `rgba(255, 255, 255, 0.9)`

#### Right Column: Image/Graphic
1. **Image Widget** or **Container**:
   - Upload graphic: waste classification flowchart
   - Or use placeholder with dashed border
   - Border Radius: 10px

---

### Section 6: Service Features (4-Card Grid)

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px 0
3. **Style → Background:** `#F8F8F8` (LJP Off-White)

#### Content Widgets
1. **Heading Widget** (H2):
   - Text: "Comprehensive Capabilities for Pharma Manufacturers & Healthcare"
   - Alignment: Center
   - Margin Bottom: 40px

2. **Inner Container** (2-Column Grid):
   - Display: Grid
   - Columns: 2 (desktop), 1 (mobile)
   - Gap: 30px

**For Each Feature Card (4 total):**
- Add a **Container** with:
  - Background: White
  - Padding: 30px
  - Border Radius: 8px
  - Border Left: 4px solid `#018846` (LJP Accent Green)
  - Box Shadow: `0 4px 6px rgba(0, 0, 0, 0.02)`

- **Heading Widget** (H4):
  - Text: Feature title
  - Typography: 20px, 700 weight
  - Color: `#18509B`

- **Text Editor Widget**:
  - Feature description
  - Typography: 16px
  - Color: `#666666`

---

### Section 7: Testimonial Section

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px 0
   - Text Align: Center
3. **Style → Background:** White

#### Content Widgets
1. **Text Editor Widget** (Quote):
   - Text: Full testimonial quote
   - Typography: 24px, italic, Poppins
   - Color: `#18509B`
   - Max Width: 900px (centered)

2. **Text Editor Widget** (Author):
   - Text: "— Director of Facilities, Biotechnology Firm"
   - Typography: 16px, 500 weight
   - Color: `#666666`
   - Margin Top: 20px

> **Alternative:** Use the **Testimonial Carousel Widget** if you have multiple testimonials.

---

### Section 8: Final CTA Section

#### Container Setup
1. Add a **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px 0
   - Text Align: Center
3. **Style → Background:**
   - Type: **Gradient**
   - Color 1: `#018846` (LJP Accent Green)
   - Color 2: `#006030` (Darker green)
   - Angle: 135°

#### Content Widgets
1. **Heading Widget** (H2):
   - Text: "Ready to Upgrade Your Pharmaceutical Waste Strategy?"
   - Typography: 40px, 700 weight
   - Color: White

2. **Text Editor Widget**:
   - Text: "Safe, secure, and sustainable solutions are one call away."
   - Typography: 20px
   - Color: `rgba(255, 255, 255, 0.9)`
   - Margin Bottom: 30px

3. **Button Widget**:
   - Text: "Get a Custom Quote"
   - Link: `#form` or contact page
   - Style → Background: White
   - Style → Color: `#018846`
   - Style → Padding: 16px 40px
   - **Hover:** Transform translateY(-2px), box-shadow

---

## Step 4: Responsive Adjustments

For each section, click the **Responsive Mode** icon (bottom-left) and adjust:

| Breakpoint | Adjustments |
|------------|-------------|
| **Tablet** | Hero: Stack to column, reduce heading to 36px, 2-column grids |
| **Mobile** | All stacked columns, reduce padding to 48px, center text, 1-column grids |

### Key Responsive Rules:
- Hero section: Stack vertically (blue panel on top, image below)
- Form section: Stack vertically, form goes below benefits
- Process grid: 2 columns on tablet, 1 column on mobile
- Trust badges: Wrap to multiple rows

---

## Step 5: Custom CSS (Global)

Add this to **Elementor → Custom CSS** (site-wide) or per-widget for consistent effects:

```css
/* Blue underline accent for H2 (optional) */
.ljp-h2-underline .elementor-heading-title::after {
    content: '';
    display: block;
    width: 60px;
    height: 4px;
    background: #EB9B1A;
    margin-top: 12px;
    border-radius: 2px;
}

/* Card hover lift effect */
.ljp-card-hover:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}

/* Button hover glow (orange) */
.ljp-btn-orange .elementor-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(235, 155, 26, 0.3);
}

/* Button hover glow (green) */
.ljp-btn-green .elementor-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(1, 136, 70, 0.3);
}

/* Trust badge styling */
.ljp-trust-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 50px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(4px);
}

/* Certification badge hover */
.ljp-cert-badge:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(24, 80, 155, 0.1);
    border-color: #18509B;
}

/* Process step icons */
.ljp-process-icon .elementor-icon {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 50%;
}
```

Then apply CSS classes (e.g., `ljp-card-hover`) to widgets via **Advanced → CSS Classes**.

---

## Step 6: UTM Tracking Setup

Ensure the form captures UTM parameters by:

1. Add hidden fields to the form for: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `matchtype`, `gclid`
2. The existing LJP snippet in the header will auto-populate these fields
3. Verify the snippet exists in **Elementor → Custom Code** or **Theme Options**

---

## Step 7: Save as Template (Optional)

1. Click hamburger menu → **Save as Template**
2. Name: "LJP - Pharma Waste Disposal LP"
3. Reuse this layout for similar service landing pages

---

## Pre-Publish Checklist

- [ ] All Global Colors applied (no hardcoded hex values where possible)
- [ ] Hero diagonal edge displays correctly on desktop
- [ ] Responsive views tested (tablet + mobile)
- [ ] Form submissions working (test with email)
- [ ] UTM tracking capturing correctly
- [ ] All anchor links working (`#form`)
- [ ] Page title and meta description set in Yoast SEO
- [ ] Featured image set for OG tags
- [ ] Custom CSS added to site-wide or page-level
- [ ] Mobile: Hero stacks correctly, trust badges wrap
- [ ] Mobile: Form section accessible
- [ ] Certifications section displays correctly (2x2 grid on desktop, 1 column mobile)

---

## Reference Files

- [pharma_disposal.html](file:///Applications/Antigravity/ROCKET%20CLICKS/Content%20Gap%20%26%20Analysis/pharma_disposal.html) – Static mockup for exact styling reference
- [Product Destruction LP](https://ljpzlf.com/protect-your-brand-with-a-secure-product-destruction-service/) – Live reference for Elementor patterns
- [Certifications Section Screenshot](file:///Applications/Antigravity/ROCKET%20CLICKS/Content%20Gap%20%26%20Analysis/pharma%20waste%20disposal.png) – Visual reference for certifications badges

---

## Section Summary Table

| # | Section Name | Background | Key Widgets |
|---|--------------|------------|-------------|
| 1 | Hero | Blue gradient + image | H1, Text, Buttons, Trust Badges |
| 2 | Form Section | Off-white | Icon List, Certifications Grid, Form |
| 3 | Value Props | White | 3x Icon Boxes / Cards |
| 4 | Process | Primary Blue | 4x Icon Boxes (horizontal) |
| 5 | Educational | Primary Blue | 2-column: Text + Image |
| 6 | Features | Off-white | 2x2 Feature Cards |
| 7 | Testimonial | White | Quote Box |
| 8 | Final CTA | Green gradient | H2, Text, CTA Button |

---

## Notes for Developer

1. **Hero Layout:** Simple 2-column split with a straight vertical edge. Blue content panel on left, image on right. Stacks vertically on mobile.

2. **Certifications Section:** This is a NEW addition below the form benefits list. Reference the mockup screenshot for exact visual styling.

3. **Form ID:** Ensure the form container has CSS ID `form` for the anchor link from hero CTA.

4. **Existing LJP Patterns:** Use the Product Destruction page as a direct reference – the structure is nearly identical. You can duplicate that page and modify content.

6. **PNG Assets:** SVG icons have been replaced with PNGs. Ensure you export/download transparent PNG versions of all icons (Trust bar, Certifications, Value Props, Process steps) before starting. Use 2x resolution (@2x) for sharp display on retina screens.
