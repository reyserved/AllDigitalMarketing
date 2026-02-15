# AntV Infographic Generator - Complete Guide
## Dream Assurance Group - Professional Infographic Generation System

**⚠️ IMPORTANT:** This replaces the Python PIL approach which produced basic wireframes. **AntV creates TRUE artistic, professional infographics.**

---

## 🎯 What This System Does

**Generates publication-quality infographics with:**
- Professional design with sophisticated visual elements
- 50+ artistic templates (zigzag, grids, cards, flows)
- Built-in effects: gradients, shadows, patterns, hand-drawn styles
- Professional icon library
- SVG export for scalability
- Custom fonts (Google Fonts integration)
- Dream Assurance brand colors (#C92A39, #1D252D)

**Output:** HTML files that open in any browser with SVG export button

---

## 🚀 Quick Start

### Generate Kentucky Infographics (Already Done)

```bash
cd "05-assets/infographics/python"
python3 antv_generator.py
```

**Output Files:**
- `05-assets/infographics/antv-generated/kentucky-auto-insurance.html`
- `05-assets/infographics/antv-generated/kentucky-home-risks.html`

**To View:**
1. Open HTML file in any modern browser (Chrome, Firefox, Safari, Edge)
2. Infographic renders automatically
3. Click "Export SVG" button to download high-quality vector file

---

## 📝 For Any New State or Content

### Method 1: Using the infographic-creator Skill (Recommended)

**For Auto Insurance Pages:**

```
Create a sophisticated auto insurance infographic for [STATE] using AntV Infographic.

Requirements:
- Use Dream Assurance brand colors: #C92A39 (red), #1D252D (dark)
- Template: list-zigzag-down-compact-card
- Style: Professional, bold typography, clean spacing
- Include: 25/50/25 liability limits, PIP requirements, real-world scenario
- Icons: shield, user, users, car, heart-pulse, check-circle

Data structure:
```
title: [STATE] Auto Insurance
subtitle: Mandatory Minimum Coverage
lists:
  - 25/50/25 Liability Limits
  - Bodily Injury Per Person ($XX,XXX)
  - Bodily Injury Per Accident ($XX,XXX)
  - Property Damage ($XX,XXX)
  - Personal Injury Protection ($XX,XXX)
  - Real-World Scenario (Total covered: $XX,XXX)
```

Generate HTML file with SVG export capability.

Data source: [STATE Insurance Department website URL]
```

**For Home Insurance Risk Pages:**

```
Create a sophisticated home insurance risk infographic for [STATE] using AntV Infographic.

Requirements:
- Use Dream Assurance brand colors
- Template: list-grid-badge-card
- Style: rough (hand-drawn artistic effect)
- Include: Top 3 weather risks, risk levels, protection recommendations
- Icons: water, wind, snowflake based on risk type

Risks to cover:
1. [Risk 1 - e.g., Flooding] - HIGH/MODERATE
2. [Risk 2 - e.g., Tornadoes] - MODERATE
3. [Risk 3 - e.g., Winter Storms] - MODERATE

Each risk needs: level badge, description, protection recommendations

Data source: NWS [STATE] office, FEMA regional office
```

---

### Method 2: Direct Python Script

Create config JSON file, then run:

```python
from antv_generator import AntVInfographicGenerator

# Load your data
with open('your-state-data.json', 'r') as f:
    data = json.load(f)

generator = AntVInfographicGenerator()

# Generate auto insurance
generator.generate_auto_insurance('YourState', data['auto_insurance'])

# Generate home insurance risks
generator.generate_home_insurance_risks('YourState', data['home_insurance'])
```

---

## 🎨 Available Templates

### List Templates (Great for requirements, steps, processes)

- **list-zigzag-down-compact-card** - Zigzag flow (used for auto insurance)
- **list-zigzag-up-compact-card** - Reverse zigzag
- **list-grid-badge-card** - Grid layout with badges (used for home risks)
- **list-row-horizontal-icon-arrow** - Horizontal flow with icons
- **list-column-vertical-icon-arrow** - Vertical lists
- **list-column-done-list** - Checklist style

### Comparison Templates (Great for coverage options)

- **compare-swot** - SWOT analysis
- **compare-binary-* ** - Side-by-side comparisons
- **compare-quadrant-* ** - Quadrant charts

### Chart Templates (Great for statistics, numbers)

- **chart-column-simple** - Bar charts
- **chart-pie-donut-* ** - Pie/donut charts
- **chart-line-* ** - Trend lines
- **chart-bar-plain-text** - Plain bar charts

### Sequence Templates (Great for processes, steps)

- **sequence-stairs-* ** - Step-by-step
- **sequence-timeline-* ** - Timelines
- **sequence-roadmap-* ** - Roadmaps
- **sequence-funnel-simple** - Funnels

---

## 🎨 Styling Options

### Built-in Styles

```ant
theme stylize rough           # Hand-drawn, artistic effect
theme stylize pattern         # Pattern fills
theme stylize linear-gradient # Gradient backgrounds
theme stylize radial-gradient # Radial gradients
```

### Custom Color Palettes

```ant
theme
  palette
    - #C92A39  # Dream Assurance red
    - #1D252D  # Dream Assurance dark
    - #F8F9FA  # Light accent
    - #28A745  # Success green
```

### Custom Fonts

```ant
theme
  base
    text
      font-family Roboto:wght@400;700;900
```

---

## 📋 Data Format

### Auto Insurance Data Structure

```json
{
  "liability_limits": {
    "bodily_injury_per_person": {
      "amount": 25000,
      "label": "$25,000",
      "description": "Per person injured in an accident you cause"
    },
    "bodily_injury_per_accident": {
      "amount": 50000,
      "label": "$50,000",
      "description": "Per accident total, regardless of number of people"
    },
    "property_damage": {
      "amount": 25000,
      "label": "$25,000",
      "description": "Damage to another person's car or property"
    }
  },
  "pip": {
    "amount": 10000,
    "label": "$10,000",
    "covers": ["Medical expenses", "Lost wages regardless of fault"]
  },
  "scenario": {
    "description": "You cause an accident injuring two people...",
    "breakdown": [...],
    "total": 48000
  }
}
```

### Home Insurance Risks Data Structure

```json
{
  "risks": [
    {
      "type": "Flooding",
      "level": "HIGH",
      "types": ["Flash flooding", "River flooding"],
      "fact": "Fact with statistic",
      "protection": ["Protection 1", "Protection 2"]
    }
  ]
}
```

---

## 🔧 Customization

### Create Custom Template with Custom Style

```ant
infographic list-zigzag-down-compact-card
theme
  palette
    - #C92A39
    - #1D252D
    - #FF9800
  stylize rough
  base
    text
      font-family Roboto:wght@300;500;700;900
data
  title Your Title
  subtitle Your Subtitle
  desc Your description
  lists
    - label Card 1
      desc Description
      value 25000
      icon shield check
```

---

## 📊 Icon Reference

Common icons used in insurance infographics:

**Auto Insurance:**
- `shield check` - Protection/coverage
- `user` - Per person
- `users` - Multiple people/accident
- `car` - Vehicle/property
- `heart pulse` - PIP/medical
- `check circle` - Approval/covered

**Home Insurance:**
- `water` - Flooding
- `wind` - Wind/tornadoes
- `snowflake` - Winter storms
- `warning` - Alerts
- `home` - House/property

---

## ✅ Quality Checklist

Before considering an infographic complete:

**Design Quality:**
- [ ] Dream Assurance brand colors used (#C92A39, #1D252D)
- [ ] Typography is professional and hierarchical
- [ ] Visual flow guides the eye naturally
- [ ] Design is artistic, NOT basic wireframe
- [ ] Icons render cleanly and professionally

**Content Accuracy:**
- [ ] All data from authoritative .gov sources
- [ ] Numbers and statistics verified
- [ ] Sources cited correctly
- [ ] Scenario totals are accurate

**Technical Quality:**
- [ ] HTML file opens in browser correctly
- [ ] SVG export button works
- [ ] Text is readable at default zoom
- [ ] Responsive to window resizing

---

## 🎯 Example Prompts for Future Use

### For Kansas Auto Insurance

```
Create a sophisticated auto insurance infographic for Kansas using AntV Infographic.

Template: list-zigzag-down-compact-card
Colors: Dream Assurance brand (#C92A39, #1D252D)

Data:
- Title: Kansas Auto Insurance
- 25/50/25 liability limits
- $4,500 PIP requirement (Kansas Statute 40-3107)
- Real-world scenario example

Icons: shield, user, users, car, heart-pulse, check-circle

Generate HTML with SVG export.
Data source: https://insurance.kansas.gov/consumer/auto/
```

### For Texas Home Insurance Risks

```
Create a sophisticated home insurance risk infographic for Texas using AntV Infographic.

Template: list-grid-badge-card
Style: rough (artistic hand-drawn effect)

Top 3 risks:
1. Hurricanes (HIGH) - Coastal windstorm damage, storm surge
2. Hail (HIGH) - Severe hail events, roof damage
3. Flooding (MODERATE) - Flash floods, river flooding
4. Tornadoes (MODERATE) - Tornado alley region

Icons: wind, cloud-rain, water, tornado
Colors: #C92A39, #FF9800 for risk levels

Generate HTML with SVG export.
Data source: NWS Texas office, FEMA Region 6
```

---

## 🚀 Advanced Usage

### Multi-Section Infographic

For complex infographics, you can create multiple HTML files and combine them, or use more advanced templates like:

```ant
infographic compare-binary-horizontal-badge-card-arrow
theme
  palette
    - #C92A39
    - #1D252D
    - #28A745
data
  title Coverage Options
  subtitle Standard vs Enhanced
  compares
    - label Standard Coverage
      children
        - label 25/50/25 Liability
        - label $10K PIP
    - label Enhanced Coverage
      children
        - label 100/300/100 Liability
        - label $25K PIP
        - label Comprehensive & Collision
        - label Rental Reimbursement
```

---

## 📁 File Structure

```
05-assets/infographics/
├── antv-generated/                    # HTML files with AntV infographics
│   ├── kentucky-auto-insurance.html
│   └── kentucky-home-risks.html
├── data/                             # Research data from .gov sources
│   └── kentucky-insurance-data.json
├── python/
│   ├── antv_generator.py            # Main generator script
│   └── template_system.py            # (Deprecated - use AntV instead)
└── ANTV_GENERATION_GUIDE.md          # This file
```

---

## 🔧 Troubleshooting

**HTML doesn't render:**
- Check browser console for JavaScript errors
- Ensure internet connection (loads AntV from CDN)
- Try different browser (Chrome, Firefox, Safari)

**SVG export fails:**
- Wait for infographic to fully render
- Check console for specific error messages
- Try refreshing the page

**Text looks wrong:**
- Verify Google Fonts are loading
- Check for syntax errors in AntV syntax
- Ensure proper escaping of special characters

**Icons don't show:**
- Verify icon names are correct
- Check AntV icon documentation
- Try alternative icon names

---

## 📚 References

- **AntV Infographic:** https://infographic.antv.vision/
- **Template Gallery:** https://infographic.antv.vision/gallery
- **Documentation:** https://infographic.antv.vision/docs
- **Dream Assurance Colors:** #C92A39 (red), #1D252D (dark)

---

## 💡 Pro Tips

1. **Always** research data from .gov sources first
2. **Always** verify numbers before including in infographic
3. **Always** test HTML file in browser before deploying
4. **Always** export SVG for scalable, high-quality version
5. **Always** use Dream Assurance brand colors for consistency

---

## 🎯 Success Criteria

✓ Visual quality matches or exceeds Kansas example
✓ Professional artistic design, NOT wireframe
✓ Dream Assurance brand consistent
✓ SVG export works perfectly
✓ HTML opens in any modern browser
✓ Typography is clean and professional
✓ Icons render beautifully
✓ Colors are vibrant and accurate

---

**This system produces TRUE artistic infographics worthy of Dream Assurance Group's brand!**
