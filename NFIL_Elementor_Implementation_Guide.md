# Elementor Implementation Guide: Executive Function Coaching Hub

This guide walks through recreating the visual mockup in Elementor Pro on WordPress.

---

## Prerequisites

- **Elementor Pro** installed and activated
- Access to **Elementor Global Colors** (Site Settings)
- Theme: Astra (or compatible theme with Elementor headers)
- Custom font "Kano Regular" already uploaded to Elementor or use fallback (Inter/Roboto)

---

## Step 1: Set Up Global Colors

Before building, configure the brand colors as Global Colors for consistency.

1. Open any page with Elementor → Click hamburger menu (☰) → **Site Settings**
2. Go to **Global Colors**
3. Add/update the following:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| `NFIL Background Primary` | `#1B252F` | Body/section backgrounds |
| `NFIL Background Secondary` | `#232428` | Alt section backgrounds |
| `NFIL Background Card` | `#1E2A36` | Card backgrounds |
| `NFIL Accent Blue` | `#0D9EFF` | Links, accents, underlines |
| `NFIL Accent Orange` | `#FF6600` | CTA buttons, badges |
| `NFIL Text White` | `#FFFFFF` | Headings |
| `NFIL Text Muted` | `#CFCFCF` | Body text |
| `NFIL Overlay Blue` | `#084D7C` | Hero overlay |

4. **Save** settings.

---

## Step 2: Create the Page Structure

1. Create a new page: **Pages → Add New → "Executive Function Coaching Services"**
2. Click **Edit with Elementor**
3. Set page layout to **Elementor Full Width** (in page settings)

---

## Step 3: Build Each Section

### Section 1: Hero Section

#### Container Setup
1. Add a **Container** (Flexbox)
2. **Layout:**
   - Direction: Row
   - Min Height: `70vh`
   - Content Width: Boxed (`1200px`)
3. **Style → Background:**
   - Type: **Classic**
   - Image: Upload hero image (coach-client photo)
   - Position: Center Center
   - Size: Cover
4. **Style → Background Overlay:**
   - Type: **Gradient**
   - Color 1: `#1B252F` (90% opacity)
   - Color 2: `#084D7C` (90% opacity)
   - Angle: 135°

> **IMPORTANT:** The overlay is CRITICAL. Always use Background Overlay, not a separate element.

#### Content Widgets (inside Container)
1. **Heading Widget** (Eyebrow):
   - Text: "Achieve Your Goals with Confidence"
   - HTML Tag: `<p>` or `<span>`
   - Style → Typography: 14px, 600 weight, uppercase, letter-spacing 2px
   - Style → Color: `NFIL Accent Blue`

2. **Heading Widget** (H1):
   - Text: "Executive Function Coaching Services"
   - HTML Tag: `<h1>`
   - Style → Typography: 48-56px, 600 weight
   - Style → Color: `NFIL Text White`

3. **Text Editor Widget**:
   - Paste the intro paragraphs
   - Style → Typography: 20px
   - Style → Color: `NFIL Text Muted`

4. **Button Widget**:
   - Text: "Schedule a Free Discovery Call"
   - Link: `https://nfil.net/contact-us/`
   - Style → Background: `NFIL Accent Orange`
   - Style → Border Radius: 6px
   - Style → Box Shadow: `0 4px 20px rgba(255,102,0,0.3)`
   - Style → Padding: 16px 32px

---

### Section 2: What is Executive Function Coaching?

#### Container Setup
1. Add a new **Container**
2. **Layout:**
   - Direction: Column
   - Content Width: Boxed
   - Padding: 80px top/bottom
3. **Style → Background:** `NFIL Background Primary`

#### Content Widgets
1. **Heading Widget** (Section Header):
   - Text: "What is Executive Function Coaching?"
   - HTML Tag: `<h2>`
   - Alignment: Center
   - **Advanced → Custom CSS:**
   ```css
   selector .elementor-heading-title::after {
       content: '';
       display: block;
       width: 60px;
       height: 4px;
       background: linear-gradient(90deg, #0D9EFF, #1C91FE);
       margin: 12px auto 0;
       border-radius: 2px;
   }
   ```

2. **Text Editor Widget**:
   - Paste intro paragraph
   - Alignment: Center
   - Max Width: 900px (use Advanced → Positioning or a nested container)

3. **Inner Container** (Two Columns):
   - Add inner container with 2 columns (50/50)
   
   **Left Column:**
   - **Heading Widget**: "What Happens in Coaching" (`<h3>`)
   - **Icon List Widget**:
     - Items: Identify, Develop, Practice
     - Icon: Circle (filled)
     - Icon Color: `NFIL Accent Blue`
     - Icon Size: 10px

   **Right Column:**
   - **Heading Widget**: "Core Skills You'll Build" (`<h3>`)
   - **Icon List Widget**:
     - Items: Planning & time management, Task initiation, etc.
     - Same styling as left column

4. **Text Editor Widget** (Bottom):
   - Closing paragraph
   - Centered, max-width 800px

---

### Section 3: Who We Help (Two Cards)

#### Container Setup
1. Add **Container** with `NFIL Background Secondary`
2. Padding: 80px top/bottom

#### Content Widgets
1. **Heading Widget** (Eyebrow): "Tailored Pathways"
2. **Heading Widget** (H2): "Who We Help" + custom CSS underline
3. **Text Editor Widget**: Intro paragraph

4. **Inner Container** (Two Columns):
   
   **For Each Card Column:**
   - Add a Container styled as a card:
     - Background: `NFIL Background Card`
     - Padding: 32px
     - Border Radius: 12px
     - Border Left: 4px solid `NFIL Accent Blue`
   
   - Inside each card:
     - **Icon Widget**: Rocket (students) / Cog (adults)
       - Color: `NFIL Accent Blue`
       - Background: `rgba(13,158,255,0.15)`
       - Size: 48px
       - Border Radius: 10px
     - **Heading Widget** (`<h3>`): "For Students" / "For Adults"
     - **Heading Widget** (`<h4>`): Subheading (blue color)
     - **Text Editor Widget**: Description
     - **Text Editor Widget**: Ideal for / Outcome (use `<strong>` for labels)
     - **Button Widget** (link style):
       - Text: "Learn More About Student Coaching →"
       - Style: Link / Text color: `NFIL Accent Orange`

---

### Section 4: Real-World Outcomes (4-Card Grid)

#### Container Setup
1. Add **Container** with `NFIL Background Primary`
2. Padding: 80px

#### Content Widgets
1. **Eyebrow + H2 Heading** (centered, with underline CSS)

2. **Inner Container** (Grid Layout):
   - 4 columns on desktop, 2 on tablet, 1 on mobile
   - Gap: 32px

3. **For Each Outcome Card:**
   - Add a Container:
     - Background: `NFIL Background Card`
     - Padding: 32px
     - Border Radius: 12px
     - Position: Relative
   
   - **Heading Widget** (Number Badge):
     - Text: "01" / "02" / etc.
     - **Advanced → Custom CSS:**
     ```css
     selector {
         position: absolute !important;
         top: -16px;
         left: 24px;
         width: 40px;
         height: 40px;
         background: linear-gradient(135deg, #FF6600, #E55A00);
         border-radius: 8px;
         display: flex;
         align-items: center;
         justify-content: center;
         box-shadow: 0 0 20px rgba(255,102,0,0.3);
     }
     selector .elementor-heading-title {
         color: #fff;
         font-size: 16px;
         font-weight: 700;
     }
     ```
   
   - **Heading Widget** (`<h3>`): Outcome title
   - **Text Editor Widget**: Description
   - **Skill Chips** (use **HTML Widget** or styled Text Editor):
     ```html
     <span style="display:inline-block; padding:4px 12px; background:rgba(13,158,255,0.15); color:#0D9EFF; border-radius:20px; font-size:13px; font-weight:500; margin-right:6px; margin-bottom:6px;">Planning</span>
     ```
     Or create a **Global Widget** for reusable chips.

---

### Section 5: Our Process (4 Steps)

#### Container Setup
1. **Container** with `NFIL Background Secondary`
2. Padding: 80px

#### Content Widgets
1. **Eyebrow + H2** centered

2. **Inner Container** (4 Columns):
   - Each column contains:
     - **Icon Box Widget** OR custom structure:
       
       **Number Circle:**
       - Use **Heading Widget** with custom CSS:
       ```css
       selector {
           width: 64px;
           height: 64px;
           background: linear-gradient(135deg, #0D9EFF, #1C91FE);
           border-radius: 50%;
           display: flex;
           align-items: center;
           justify-content: center;
           margin: 0 auto 20px;
           box-shadow: 0 0 30px rgba(13,158,255,0.25);
       }
       selector .elementor-heading-title {
           color: #fff;
           font-size: 24px;
           font-weight: 700;
       }
       ```
       
       - **Heading Widget** (`<h4>`): Step title
       - **Text Editor Widget**: Step description

---

### Section 6: Why Choose New Frontiers (3 USP Cards)

#### Container Setup
1. **Container** with `NFIL Background Primary`
2. Padding: 80px

#### Content Widgets
1. **H2 Heading** centered

2. **Inner Container** (3 Columns):
   - Each column is a card container:
     - Background: `NFIL Background Card`
     - Padding: 32px
     - Border Radius: 12px
     - Border: 1px solid transparent
     - **Hover Border Color**: `NFIL Accent Blue`
   
   - Inside each:
     - **Icon Widget**: Team / Brain / Links icon
       - Size: 64px
       - Color: `NFIL Accent Blue`
       - Background: `rgba(13,158,255,0.1)`
       - Border Radius: 50%
     - **Heading Widget** (`<h3>`): USP title
     - **Text Editor Widget**: Description

3. **Virtual Banner** (after grid):
   - Add a **Container**:
     - Background: `linear-gradient(90deg, rgba(13,158,255,0.15), rgba(13,158,255,0.05))`
     - Border: 1px solid `rgba(13,158,255,0.3)`
     - Border Radius: 8px
     - Padding: 20px 32px
     - Text Align: Center
   - **Text Editor Widget**: "We coach **virtually nationwide**..."

---

### Section 7: CTA Highlight

#### Container Setup
1. **Container**:
   - Background: **Gradient**
     - Color 1: `#084D7C`
     - Color 2: `#0D9EFF`
     - Angle: 135°
   - Padding: 80px
   - Text Align: Center

#### Content Widgets
1. **Eyebrow Heading**: "Schedule a Call Today!"
2. **H2 Heading**: "Ready to Take Control?"
   - Color: White
   - Custom CSS for centered white underline
3. **Text Editor Widget**: Description (white/light text)
4. **Button Widget**: Orange CTA

---

### Section 8: Age-Specific Pathways

#### Container Setup
1. **Container** with `NFIL Background Primary`
2. Padding: 80px

#### Content Widgets
1. **Eyebrow + H2** centered

2. **Inner Container** (2 Columns):
   - Each column is a **clickable card**:
     - Use **Container** with link wrapper (Advanced → Link)
     - Background: `NFIL Background Card`
     - Border Left: 4px solid `NFIL Accent Blue`
     - Padding: 32px
     - Border Radius: 12px
     - Display: Flex, Row, Gap 24px
   
   - Inside:
     - **Icon Widget** (left): Rocket / Cog
     - **Container** (right):
       - **Heading** (`<h3>`)
       - **Text Editor**: Description
       - **Text/Button**: "Learn More →" (orange)

---

## Step 4: Responsive Adjustments

For each section, click the **Responsive Mode** icon (bottom-left) and adjust:

| Breakpoint | Adjustments |
|------------|-------------|
| **Tablet** | Reduce heading sizes by 15-20%, switch grids to 2 columns |
| **Mobile** | Stack all columns to 1, reduce padding to 48px, center-align all text |

---

## Step 5: Custom CSS (Global)

Add this to **Elementor → Custom CSS** (site-wide) for consistent effects:

```css
/* Blue underline accent for H2 */
.nfil-h2-underline .elementor-heading-title::after {
    content: '';
    display: block;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, #0D9EFF, #1C91FE);
    margin-top: 12px;
    border-radius: 2px;
}

.nfil-h2-underline.center .elementor-heading-title::after {
    margin-left: auto;
    margin-right: auto;
}

/* Card hover glow */
.nfil-card-glow:hover {
    box-shadow: 0 0 30px rgba(13, 158, 255, 0.25);
}

/* Orange button glow */
.nfil-btn-orange .elementor-button {
    background: linear-gradient(135deg, #FF6600, #E55A00) !important;
    box-shadow: 0 4px 20px rgba(255, 102, 0, 0.3);
}

.nfil-btn-orange .elementor-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(255, 102, 0, 0.4);
}
```

Then apply CSS classes (e.g., `nfil-h2-underline`) to widgets via **Advanced → CSS Classes**.

---

## Step 6: Save as Template (Optional)

1. Click hamburger menu → **Save as Template**
2. Name: "NFIL - Executive Function Hub"
3. Reuse this layout for similar service pages

---

## Checklist Before Publishing

- [ ] All Global Colors applied (no hardcoded hex values)
- [ ] Hero dark overlay in place
- [ ] Responsive views tested (tablet + mobile)
- [ ] All links correct (contact page, subpages)
- [ ] Page title and meta description set
- [ ] Custom CSS added to site-wide or page-level

---

## Reference Files

- [EF_Coaching_Hub_Mockup.html](file:///Applications/Antigravity/ROCKET%20CLICKS/Content%20Gap%20%26%20Analysis/EF_Coaching_Hub_Mockup.html) – Static mockup for exact styling reference
