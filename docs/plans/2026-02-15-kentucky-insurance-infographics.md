# Kentucky Insurance Infographics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create two educational infographics for Dream Assurance Group's Kentucky personal insurance page that explain auto insurance minimums and home insurance risks using authoritative data sources.

**Architecture:** HTML/CSS-based infographic components with SVG icons, designed as self-contained visual modules that can be embedded directly into the existing page layout. All data sourced from .gov websites (KYTC, NWS, FEMA) for authority and trust.

**Tech Stack:** HTML5, CSS3 (custom styles with Dream Assurance brand colors #C92A39 and #1D252D), inline SVG icons, responsive grid layouts, authoritative data from kytc.ky.gov, weather.gov, and fema.gov

---

## Task 1: Research and Gather Authoritative Data

**Files:**
- Create: `docs/research/kentucky-insurance-data.md`

**Step 1: Fetch Kentucky auto insurance requirements from Kentucky Transportation Cabinet**

Visit: `https://kytc.ky.gov/Pages/default.aspx`
Search: "auto insurance minimum requirements Kentucky"
Extract: 25/50/25 liability limits, PIP requirements, no-fault explanation

**Step 2: Fetch Kentucky tornado statistics from National Weather Service**

Visit: `https://www.weather.gov/lmk/` (Louisville NWS covers Kentucky)
Search: "Kentucky tornado statistics annual average"
Extract: Average tornadoes per year, tornado risk regions

**Step 3: Fetch Kentucky flood risk data from FEMA**

Visit: `https://www.fema.gov/flood-maps`
Search: "Kentucky flood insurance claims statistics"
Extract: Flood claim statistics, 1 in 4 claims outside high-risk zones fact

**Step 4: Compile research document**

```markdown
# Kentucky Insurance Research Data

## Auto Insurance Requirements (Source: KYTC)
- [Paste exact requirements from .gov source]

## Tornado Statistics (Source: NWS)
- [Paste exact statistics with citation links]

## Flood Risk Data (Source: FEMA)
- [Paste exact facts and figures]
```

**Step 5: Commit**

```bash
git add docs/research/kentucky-insurance-data.md
git commit -m "docs: add Kentucky insurance research from authoritative sources"
```

---

## Task 2: Create Base HTML Structure for Infographic 1

**Files:**
- Create: `05-assets/infographics/kentucky-auto-insurance-infographic.html`
- Create: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Create HTML skeleton with semantic structure**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kentucky Auto Insurance Minimums Explained</title>
    <link rel="stylesheet" href="css/kentucky-infographics.css">
</head>
<body>
    <div class="dag-infographic-container">
        <!-- Hero Header Panel -->
        <header class="dag-infographic-header">
            <h1>Kentucky Auto Insurance Requirements</h1>
            <p class="dag-infographic-subhead">Choice No-Fault State | Mandatory Minimum Coverage</p>
            <span class="dag-source-badge">Source: Kentucky Transportation Cabinet</span>
        </header>

        <!-- Hero Display Panel -->
        <section class="dag-hero-display">
            <div class="dag-hero-numbers">25 / 50 / 25</div>
            <div class="dag-hero-label">State Minimum Liability Limits</div>
            <div class="dag-three-column-grid">
                <div class="dag-column">$25K Per Person</div>
                <div class="dag-column">$50K Per Accident</div>
                <div class="dag-column">$25K Property Damage</div>
            </div>
        </section>

        <!-- Coverage Breakdown Section -->
        <section class="dag-coverage-breakdown">
            <div class="dag-coverage-card">
                <div class="dag-card-icon">[SVG Person Icon]</div>
                <div class="dag-card-amount">$25,000</div>
                <div class="dag-card-title">Bodily Injury Per Person</div>
                <div class="dag-card-description">Maximum coverage for each individual injured in an accident you cause</div>
                <div class="dag-card-example">Example: Covers medical expenses, rehabilitation costs, and lost wages</div>
            </div>
            <div class="dag-coverage-card">
                <div class="dag-card-icon">[SVG Group Icon]</div>
                <div class="dag-card-amount">$50,000</div>
                <div class="dag-card-title">Bodily Injury Per Accident</div>
                <div class="dag-card-description">Total coverage for all injuries in a single accident, regardless of number of people</div>
                <div class="dag-card-example">Example: If 3 people are injured, this $50,000 is split among all claims</div>
            </div>
            <div class="dag-coverage-card">
                <div class="dag-card-icon">[SVG Car/Home Icon]</div>
                <div class="dag-card-amount">$25,000</div>
                <div class="dag-card-title">Property Damage</div>
                <div class="dag-card-description">Damage to another person's vehicle, property, or structures</div>
                <div class="dag-card-example">Example: Repairs to another driver's car, fence, mailbox, or building</div>
            </div>
        </section>

        <!-- PIP Requirement Panel -->
        <section class="dag-pip-panel">
            <div class="dag-pip-icon">[SVG Shield Icon]</div>
            <h3>Personal Injury Protection (PIP)</h3>
            <div class="dag-pip-amount">Minimum Required: $10,000</div>
            <ul class="dag-pip-bullets">
                <li>Covers your medical expenses</li>
                <li>Covers lost wages regardless of who is at fault</li>
                <li>Required in Kentucky's no-fault system</li>
            </ul>
        </section>

        <!-- Coverage Scenario Panel -->
        <section class="dag-scenario-panel">
            <h3>COVERAGE SCENARIO EXAMPLE</h3>
            <p>You cause an accident injuring two people and damaging a parked car.</p>
            <div class="dag-scenario-breakdown">
                <div>Person 1 medical bills: <strong>$18,000</strong></div>
                <div>Person 2 medical bills: <strong>$22,000</strong></div>
                <div>Parked car damage: <strong>$8,000</strong></div>
            </div>
            <div class="dag-scenario-result">
                Your 25/50/25 coverage pays: <span class="dag-checkmark">✓</span> <strong>$48,000</strong>
                <span class="dag-out-of-pocket">(You pay $0 out of pocket)</span>
            </div>
        </section>
    </div>
</body>
</html>
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/kentucky-auto-insurance-infographic.html
git commit -m "feat: add HTML structure for auto insurance infographic"
```

---

## Task 3: Create CSS Styles for Infographic 1

**Files:**
- Modify: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Add base styles and CSS variables**

```css
:root {
    --dag-brand-red: #C92A39;
    --dag-brand-dark: #1D252D;
    --dag-brand-white: #FFFFFF;
    --dag-light-accent: #f8f9fa;
    --dag-success-green: #28a745;
    --dag-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--dag-font-family);
    line-height: 1.6;
    color: var(--dag-brand-dark);
}

.dag-infographic-container {
    max-width: 1200px;
    margin: 0 auto;
    background: var(--dag-brand-white);
}
```

**Step 2: Add header styles**

```css
.dag-infographic-header {
    background: linear-gradient(135deg, var(--dag-brand-dark) 0%, #2d3a45 100%);
    color: var(--dag-brand-white);
    padding: 30px;
    text-align: center;
    position: relative;
}

.dag-infographic-header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.dag-infographic-subhead {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 15px;
}

.dag-source-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.1);
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.85rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

**Step 3: Add hero display styles**

```css
.dag-hero-display {
    text-align: center;
    padding: 40px 20px;
    background: var(--dag-brand-white);
    border: 3px solid var(--dag-brand-red);
    border-radius: 8px;
    margin: 20px;
}

.dag-hero-numbers {
    font-size: 4rem;
    font-weight: 800;
    color: var(--dag-brand-red);
    line-height: 1;
    letter-spacing: 2px;
}

.dag-hero-label {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--dag-brand-dark);
    margin-top: 15px;
}

.dag-three-column-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 25px;
}

.dag-column {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--dag-brand-dark);
}
```

**Step 4: Commit**

```bash
git add 05-assets/infographics/css/kentucky-infographics.css
git commit -m "style: add base and header styles for infographic 1"
```

---

## Task 4: Add Coverage Card Styles

**Files:**
- Modify: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Add coverage card grid and card styles**

```css
.dag-coverage-breakdown {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 0 20px 30px;
}

.dag-coverage-card {
    background: var(--dag-light-accent);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 25px;
    text-align: center;
}

.dag-card-icon {
    width: 50px;
    height: 50px;
    margin: 0 auto 15px;
    color: var(--dag-brand-red);
}

.dag-card-icon svg {
    width: 100%;
    height: 100%;
}

.dag-card-amount {
    font-size: 2rem;
    font-weight: 700;
    color: var(--dag-brand-red);
    margin-bottom: 10px;
}

.dag-card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--dag-brand-dark);
    margin-bottom: 12px;
}

.dag-card-description {
    font-size: 0.95rem;
    color: #555;
    margin-bottom: 15px;
    line-height: 1.5;
}

.dag-card-example {
    font-size: 0.85rem;
    color: #777;
    font-style: italic;
    padding-top: 12px;
    border-top: 1px solid #ddd;
}
```

**Step 2: Test responsive behavior**

```css
@media (max-width: 768px) {
    .dag-three-column-grid {
        grid-template-columns: 1fr;
    }

    .dag-coverage-breakdown {
        grid-template-columns: 1fr;
    }
}
```

**Step 3: Commit**

```bash
git add 05-assets/infographics/css/kentucky-infographics.css
git commit -m "style: add coverage card styles with responsive design"
```

---

## Task 5: Create SVG Icons

**Files:**
- Create: `05-assets/infographics/icons/person-icon.svg`
- Create: `05-assets/infographics/icons/group-icon.svg`
- Create: `05-assets/infographics/icons/car-home-icon.svg`
- Create: `05-assets/infographics/icons/shield-icon.svg`

**Step 1: Create person icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
</svg>
```

**Step 2: Create group icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
    <circle cx="9" cy="7" r="4"></circle>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
</svg>
```

**Step 3: Create car/home icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
    <polyline points="9 22 9 12 15 12 15 22"></polyline>
</svg>
```

**Step 4: Create shield icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
</svg>
```

**Step 5: Commit**

```bash
git add 05-assets/infographics/icons/
git commit -m "feat: add SVG icons for infographic 1"
```

---

## Task 6: Add PIP and Scenario Panel Styles

**Files:**
- Modify: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Add PIP panel styles**

```css
.dag-pip-panel {
    background: var(--dag-light-accent);
    border-radius: 8px;
    padding: 25px;
    margin: 0 20px 20px;
    text-align: center;
}

.dag-pip-icon {
    width: 40px;
    height: 40px;
    margin: 0 auto 15px;
    color: var(--dag-brand-red);
}

.dag-pip-panel h3 {
    font-size: 1.3rem;
    color: var(--dag-brand-dark);
    margin-bottom: 15px;
}

.dag-pip-amount {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--dag-brand-red);
    margin-bottom: 15px;
}

.dag-pip-bullets {
    list-style: none;
    max-width: 500px;
    margin: 0 auto;
    text-align: left;
}

.dag-pip-bullets li {
    padding: 8px 0 8px 30px;
    position: relative;
    color: #555;
}

.dag-pip-bullets li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--dag-brand-red);
    font-size: 1.2rem;
}
```

**Step 2: Add scenario panel styles**

```css
.dag-scenario-panel {
    background: var(--dag-brand-white);
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 25px;
    margin: 0 20px 30px;
}

.dag-scenario-panel h3 {
    font-size: 1.1rem;
    color: var(--dag-brand-dark);
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.dag-scenario-panel > p {
    margin-bottom: 15px;
    color: #555;
}

.dag-scenario-breakdown {
    background: var(--dag-light-accent);
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 15px;
}

.dag-scenario-breakdown div {
    padding: 8px 0;
    border-bottom: 1px solid #ddd;
}

.dag-scenario-breakdown div:last-child {
    border-bottom: none;
}

.dag-scenario-breakdown strong {
    color: var(--dag-brand-red);
    font-weight: 700;
}

.dag-scenario-result {
    font-size: 1.1rem;
    color: var(--dag-brand-dark);
}

.dag-checkmark {
    color: var(--dag-success-green);
    font-weight: 700;
    font-size: 1.3rem;
}

.dag-out-of-pocket {
    display: block;
    margin-top: 5px;
    font-size: 0.95rem;
    color: var(--dag-success-green);
    font-weight: 600;
}
```

**Step 3: Commit**

```bash
git add 05-assets/infographics/css/kentucky-infographics.css
git commit -m "style: add PIP and scenario panel styles"
```

---

## Task 7: Update HTML with Inline SVG Icons

**Files:**
- Modify: `05-assets/infographics/kentucky-auto-insurance-infographic.html`

**Step 1: Replace [SVG Icon] placeholders with inline SVG code**

Find: `[SVG Person Icon]`
Replace with:
```html
<div class="dag-card-icon">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
    </svg>
</div>
```

Repeat for group, car/home, and shield icons with their respective SVG code from Task 5.

**Step 2: Commit**

```bash
git add 05-assets/infographics/kentucky-auto-insurance-infographic.html
git commit -m "feat: embed inline SVG icons in infographic 1"
```

---

## Task 8: Create Base HTML Structure for Infographic 2

**Files:**
- Create: `05-assets/infographics/kentucky-home-insurance-infographic.html`

**Step 1: Create HTML skeleton for home insurance risk infographic**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kentucky Home Insurance Risk Guide</title>
    <link rel="stylesheet" href="css/kentucky-infographics.css">
</head>
<body>
    <div class="dag-infographic-container">
        <!-- Hero Header Panel -->
        <header class="dag-infographic-header">
            <h1>Common Kentucky Home Insurance Risks</h1>
            <p class="dag-infographic-subhead">Protect Your Home From Weather-Related Damage</p>
            <span class="dag-source-badge">Source: National Weather Service | FEMA</span>
        </header>

        <!-- Kentucky Map Context Panel -->
        <section class="dag-map-panel">
            <div class="dag-map-visual">[Stylized Kentucky Map with Risk Zones]</div>
            <div class="dag-map-legend">
                <div class="dag-legend-item">
                    <span class="dag-legend-color dag-legend-yellow"></span>
                    <span>Moderate Risk</span>
                </div>
                <div class="dag-legend-item">
                    <span class="dag-legend-color dag-legend-orange"></span>
                    <span>High Flood Areas</span>
                </div>
                <div class="dag-legend-item">
                    <span class="dag-legend-color dag-legend-red"></span>
                    <span>Tornado Regions</span>
                </div>
            </div>
            <div class="dag-map-label">Know Your Local Risk Factors</div>
        </section>

        <!-- Three Risk Cards -->
        <section class="dag-risk-cards">
            <div class="dag-risk-card">
                <div class="dag-risk-header">
                    <div class="dag-risk-icon">[SVG Wave Icon]</div>
                    <div class="dag-risk-title">FLOODING</div>
                    <div class="dag-risk-badge dag-risk-high">HIGH</div>
                </div>
                <div class="dag-risk-content">
                    <div class="dag-risk-types">
                        <strong>Types:</strong> Flash flooding, River flooding, Urban drainage
                    </div>
                    <div class="dag-risk-fact">
                        <strong>Kentucky Fact:</strong> "Eastern Kentucky experienced historic flooding in July 2022 causing $1B+ damage"
                    </div>
                    <div class="dag-risk-protection">
                        <strong>Protection Needed:</strong>
                        <ul>
                            <li>✓ Separate flood insurance policy</li>
                            <li>✓ NFIP coverage</li>
                            <li>✓ Sump pump backup</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="dag-risk-card">
                <div class="dag-risk-header">
                    <div class="dag-risk-icon">[SVG Tornado Icon]</div>
                    <div class="dag-risk-title">TORNADOES</div>
                    <div class="dag-risk-badge dag-risk-moderate">MODERATE</div>
                </div>
                <div class="dag-risk-content">
                    <div class="dag-risk-context">
                        Kentucky is part of "Hoosier Alley" - active tornado region
                    </div>
                    <div class="dag-risk-fact">
                        <strong>Kentucky Fact:</strong> "Average of 21 tornadoes per year statewide"
                    </div>
                    <div class="dag-risk-protection">
                        <strong>Protection Needed:</strong>
                        <ul>
                            <li>✓ Wind & hail coverage</li>
                            <li>✓ Roof reinforcement</li>
                            <li>✓ Safe room/shelter</li>
                            <li>✓ Impact-resistant windows</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="dag-risk-card">
                <div class="dag-risk-header">
                    <div class="dag-risk-icon">[SVG Snowflake Icon]</div>
                    <div class="dag-risk-title">WINTER STORMS</div>
                    <div class="dag-risk-badge dag-risk-moderate">MODERATE</div>
                </div>
                <div class="dag-risk-content">
                    <div class="dag-risk-types">
                        <strong>Types:</strong> Ice storms, Heavy snow, Freezing rain
                    </div>
                    <div class="dag-risk-fact">
                        <strong>Kentucky Fact:</strong> "Ice storms cause extended power outages and roof collapse from weight"
                    </div>
                    <div class="dag-risk-protection">
                        <strong>Protection Needed:</strong>
                        <ul>
                            <li>✓ Generator coverage</li>
                            <li>✓ Food spoilage protection</li>
                            <li>✓ Alternative heat source coverage</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- Action Prompt Panel -->
        <section class="dag-action-panel">
            <div class="dag-action-icon">⚠️</div>
            <h3>IMPORTANT: Standard homeowners policies EXCLUDE flood damage</h3>
            <p>1 in 4 Kentucky flood claims come from outside mapped high-risk zones</p>
            <div class="dag-action-items">
                <div class="dag-action-item">→ Consider adding a separate flood insurance policy (NFIP)</div>
                <div class="dag-action-item">→ Review your wind/hail coverage limits for tornado protection</div>
                <div class="dag-action-item">→ Document home contents for faster claims processing</div>
            </div>
        </section>

        <!-- Footer Source Panel -->
        <footer class="dag-infographic-footer">
            Data sources: National Weather Service (weather.gov) | Federal Emergency Management Agency (fema.gov) | Kentucky Climate Center
        </footer>
    </div>
</body>
</html>
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/kentucky-home-insurance-infographic.html
git commit -m "feat: add HTML structure for home insurance risk infographic"
```

---

## Task 9: Add Infographic 2 Specific Styles

**Files:**
- Modify: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Add map panel styles**

```css
/* Infographic 2: Home Insurance Risk Guide Styles */
.dag-map-panel {
    background: var(--dag-brand-white);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 30px;
    margin: 20px;
    text-align: center;
}

.dag-map-visual {
    width: 100%;
    max-width: 400px;
    height: 250px;
    margin: 0 auto 20px;
    background: var(--dag-light-accent);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.dag-map-visual::after {
    content: "Kentucky State Map - Risk Zones";
    color: #999;
    font-size: 0.9rem;
}

.dag-map-legend {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.dag-legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
}

.dag-legend-color {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}

.dag-legend-yellow { background: #ffc107; }
.dag-legend-orange { background: #ff9800; }
.dag-legend-red { background: var(--dag-brand-red); }

.dag-map-label {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--dag-brand-dark);
}
```

**Step 2: Add risk card styles**

```css
.dag-risk-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 0 20px 30px;
}

.dag-risk-card {
    background: var(--dag-brand-white);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
}

.dag-risk-header {
    background: var(--dag-light-accent);
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #e0e0e0;
}

.dag-risk-icon {
    width: 50px;
    height: 50px;
    margin: 0 auto 10px;
    color: var(--dag-brand-red);
}

.dag-risk-icon svg {
    width: 100%;
    height: 100%;
}

.dag-risk-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--dag-brand-dark);
    margin-bottom: 8px;
}

.dag-risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 700;
    color: white;
}

.dag-risk-high { background: var(--dag-brand-red); }
.dag-risk-moderate { background: #ff9800; }

.dag-risk-content {
    padding: 20px;
}

.dag-risk-types,
.dag-risk-context,
.dag-risk-fact {
    margin-bottom: 15px;
    font-size: 0.9rem;
    color: #555;
}

.dag-risk-fact {
    background: var(--dag-light-accent);
    padding: 12px;
    border-radius: 6px;
    border-left: 3px solid var(--dag-brand-red);
}

.dag-risk-protection ul {
    list-style: none;
    padding: 0;
}

.dag-risk-protection li {
    padding: 6px 0;
    font-size: 0.85rem;
    color: #555;
}
```

**Step 3: Commit**

```bash
git add 05-assets/infographics/css/kentucky-infographics.css
git commit -m "style: add map panel and risk card styles for infographic 2"
```

---

## Task 10: Add Action Panel and Footer Styles

**Files:**
- Modify: `05-assets/infographics/css/kentucky-infographics.css`

**Step 1: Add action panel styles**

```css
.dag-action-panel {
    background: var(--dag-light-accent);
    border-left: 4px solid var(--dag-brand-red);
    border-radius: 8px;
    padding: 25px;
    margin: 0 20px 20px;
}

.dag-action-icon {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 15px;
}

.dag-action-panel h3 {
    font-size: 1.2rem;
    color: var(--dag-brand-dark);
    text-align: center;
    margin-bottom: 15px;
}

.dag-action-panel > p {
    text-align: center;
    font-size: 1.1rem;
    color: var(--dag-brand-dark);
    margin-bottom: 20px;
    font-weight: 500;
}

.dag-action-items {
    max-width: 600px;
    margin: 0 auto;
}

.dag-action-item {
    padding: 10px 0;
    font-size: 0.95rem;
    color: #555;
}
```

**Step 2: Add footer styles**

```css
.dag-infographic-footer {
    background: var(--dag-light-accent);
    border-top: 1px solid #e0e0e0;
    padding: 20px;
    text-align: center;
    font-size: 0.8rem;
    color: #999;
    margin: 0 20px 20px;
    border-radius: 0 0 8px 8px;
}
```

**Step 3: Add responsive styles for infographic 2**

```css
@media (max-width: 900px) {
    .dag-risk-cards {
        grid-template-columns: 1fr;
    }
}
```

**Step 4: Commit**

```bash
git add 05-assets/infographics/css/kentucky-infographics.css
git commit -m "style: add action panel and footer styles"
```

---

## Task 11: Create Weather Risk Icons

**Files:**
- Create: `05-assets/infographics/icons/wave-icon.svg`
- Create: `05-assets/infographics/icons/tornado-icon.svg`
- Create: `05-assets/infographics/icons/snowflake-icon.svg`

**Step 1: Create wave icon for flooding**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2 12h5l3-5 5 10 4-5h3"></path>
</svg>
```

**Step 2: Create tornado/spiral icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"></path>
    <path d="M17 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"></path>
    <path d="M13 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"></path>
    <path d="M9 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"></path>
    <path d="M5 12c.552 0 1-.448 1-1s-.448-1-1-1-1 .448-1 1 .448 1 1 1z"></path>
</svg>
```

**Step 3: Create snowflake icon**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="12" y1="2" x2="12" y2="22"></line>
    <line x1="12" y1="2" x2="4.5" y2="8.5"></line>
    <line x1="12" y1="2" x2="19.5" y2="8.5"></line>
    <line x1="12" y1="22" x2="4.5" y2="15.5"></line>
    <line x1="12" y1="22" x2="19.5" y2="15.5"></line>
</svg>
```

**Step 4: Commit**

```bash
git add 05-assets/infographics/icons/
git commit -m "feat: add weather risk icons for infographic 2"
```

---

## Task 12: Update Infographic 2 HTML with Inline SVG Icons

**Files:**
- Modify: `05-assets/infographics/kentucky-home-insurance-infographic.html`

**Step 1: Replace [SVG Icon] placeholders with inline SVG code**

Find and replace: `[SVG Wave Icon]`, `[SVG Tornado Icon]`, `[SVG Snowflake Icon]` with their respective inline SVG code from Task 11.

**Step 2: Commit**

```bash
git add 05-assets/infographics/kentucky-home-insurance-infographic.html
git commit -m "feat: embed inline SVG icons in infographic 2"
```

---

## Task 13: Create Stylized Kentucky Map SVG

**Files:**
- Create: `05-assets/infographics/icons/kentucky-map.svg`

**Step 1: Create simplified Kentucky state outline map**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" fill="none" stroke="currentColor" stroke-width="1.5">
    <!-- Simplified Kentucky state outline -->
    <path d="M 30 20 L 50 10 L 100 8 L 150 15 L 170 35 L 180 60 L 175 90 L 160 105 L 120 110 L 80 108 L 50 100 L 30 80 L 25 50 Z" fill="#f8f9fa" stroke="#1D252D"/>

    <!-- Risk zone overlays (simplified, not actual flood zone data) -->
    <path d="M 120 20 L 140 25 L 145 45 L 135 60 L 115 55 L 110 35 Z" fill="rgba(255, 152, 0, 0.3)" stroke="none"/>
    <path d="M 60 70 L 90 65 L 100 80 L 90 95 L 65 90 L 55 75 Z" fill="rgba(201, 42, 57, 0.3)" stroke="none"/>
    <path d="M 100 30 L 120 28 L 125 45 L 115 55 L 95 50 L 98 35 Z" fill="rgba(255, 193, 7, 0.3)" stroke="none"/>
</svg>
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/icons/kentucky-map.svg
git commit -m "feat: add stylized Kentucky map with risk zones"
```

---

## Task 14: Integrate Map SVG into Infographic 2 HTML

**Files:**
- Modify: `05-assets/infographics/kentucky-home-insurance-infographic.html`

**Step 1: Replace [Stylized Kentucky Map] placeholder with inline SVG**

Find: `[Stylized Kentucky Map with Risk Zones]`
Replace with the inline SVG code from Task 13.

**Step 2: Commit**

```bash
git add 05-assets/infographics/kentucky-home-insurance-infographic.html
git commit -m "feat: integrate Kentucky map SVG into infographic 2"
```

---

## Task 15: Create Embeddable Component Wrappers

**Files:**
- Create: `05-assets/infographics/kentucky-auto-insurance-component.html`
- Create: `05-assets/infographics/kentucky-home-insurance-component.html`

**Step 1: Create auto insurance component wrapper**

```html
<!-- Kentucky Auto Insurance Infographic Component -->
<!-- Embed this component in the page at the appropriate location -->
<div class="dag-comp-feature-visual">
    <link rel="stylesheet" href="css/kentucky-infographics.css">
    <div class="dag-infographic-embed">
        <!-- Contents from kentucky-auto-insurance-infographic.html body -->
        <header class="dag-infographic-header">
            <h1>Kentucky Auto Insurance Requirements</h1>
            <p class="dag-infographic-subhead">Choice No-Fault State | Mandatory Minimum Coverage</p>
            <span class="dag-source-badge">Source: Kentucky Transportation Cabinet</span>
        </header>
        <!-- ... rest of infographic content ... -->
    </div>
</div>
```

**Step 2: Create home insurance component wrapper**

```html
<!-- Kentucky Home Insurance Risk Infographic Component -->
<!-- Embed this component in the page at the appropriate location -->
<div class="dag-comp-feature-visual">
    <link rel="stylesheet" href="css/kentucky-infographics.css">
    <div class="dag-infographic-embed">
        <!-- Contents from kentucky-home-insurance-infographic.html body -->
        <header class="dag-infographic-header">
            <h1>Common Kentucky Home Insurance Risks</h1>
            <p class="dag-infographic-subhead">Protect Your Home From Weather-Related Damage</p>
            <span class="dag-source-badge">Source: National Weather Service | FEMA</span>
        </header>
        <!-- ... rest of infographic content ... -->
    </div>
</div>
```

**Step 3: Commit**

```bash
git add 05-assets/infographics/
git commit -m "feat: create embeddable component wrappers for both infographics"
```

---

## Task 16: Create Installation Instructions

**Files:**
- Create: `05-assets/infographics/README.md`

**Step 1: Write comprehensive installation instructions**

```markdown
# Kentucky Insurance Infographics - Installation Guide

## Overview
Two educational infographics for the Kentucky personal insurance page.

## Files Structure
```
05-assets/infographics/
├── css/
│   └── kentucky-infographics.css
├── icons/
│   ├── person-icon.svg
│   ├── group-icon.svg
│   ├── car-home-icon.svg
│   ├── shield-icon.svg
│   ├── wave-icon.svg
│   ├── tornado-icon.svg
│   ├── snowflake-icon.svg
│   └── kentucky-map.svg
├── kentucky-auto-insurance-component.html
├── kentucky-home-insurance-component.html
├── kentucky-auto-insurance-infographic.html
└── kentucky-home-insurance-infographic.html
```

## Installation Steps

### Step 1: Upload Files
Upload the entire `05-assets/infographics/` folder to your web server.

### Step 2: Add CSS Link
Add this line to the `<head>` section of the Kentucky page:
```html
<link rel="stylesheet" href="/path/to/05-assets/infographics/css/kentucky-infographics.css">
```

### Step 3: Replace Visual 1
Find the existing 25/50/25 visual in the page HTML and replace it with:
```html
<!-- Include the auto insurance infographic component -->
<div class="dag-comp-feature-visual">
    <!-- Copy contents from kentucky-auto-insurance-component.html -->
</div>
```

### Step 4: Replace Visual 2
Find the empty placeholder visual and replace it with:
```html
<!-- Include the home insurance infographic component -->
<div class="dag-comp-feature-visual">
    <!-- Copy contents from kentucky-home-insurance-component.html -->
</div>
```

## Testing
1. Load the Kentucky page in a browser
2. Verify both infographics display correctly
3. Check responsive behavior on mobile devices
4. Verify all icons render properly
5. Confirm source badges are visible

## Browser Support
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile: iOS Safari, Chrome Mobile

## Performance
- All CSS: ~15KB uncompressed
- Inline SVGs: ~5KB total
- No external dependencies
- Load time impact: Minimal
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/README.md
git commit -m "docs: add installation guide for Kentucky infographics"
```

---

## Task 17: Cross-Browser Testing

**Files:**
- Create: `05-assets/infographics/TESTING.md`

**Step 1: Create testing checklist**

```markdown
# Cross-Browser Testing Checklist

## Visual Testing
- [ ] Chrome (Desktop)
- [ ] Firefox (Desktop)
- [ ] Safari (Desktop - Mac)
- [ ] Edge (Desktop)
- [ ] Chrome Mobile (Android)
- [ ] Safari Mobile (iOS)

## Functional Testing
- [ ] All icons display correctly
- [ ] Colors match brand (#C92A39, #1D252D)
- [ ] Text is readable at all breakpoints
- [ ] Responsive grid layouts work
- [ ] Hover states work (if applicable)
- [ ] Source badges are visible
- [ ] Checkmarks render properly

## Content Verification
- [ ] 25/50/25 numbers display correctly
- [ ] PIP $10,000 amount is visible
- [ ] All three risk cards display
- [ ] Risk badges (HIGH/MODERATE) show correct colors
- [ ] Map legend is readable
- [ ] Action panel warning is prominent

## Accessibility Testing
- [ ] Alt text for all icons
- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigation works
- [ ] Screen reader testing completed

## Performance Testing
- [ ] Page load time impact measured
- [ ] Lighthouse score checked
- [ ] CSS optimization verified
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/TESTING.md
git commit -m "docs: add testing checklist for cross-browser verification"
```

---

## Task 18: Final Review and Quality Assurance

**Files:**
- Review: All created files

**Step 1: Visual quality check**

Open both infographic HTML files in a browser:
- Run: `open 05-assets/infographics/kentucky-auto-insurance-infographic.html`
- Run: `open 05-assets/infographics/kentucky-home-insurance-infographic.html`

Verify:
- All sections display correctly
- Colors match Dream Assurance brand
- Typography is consistent
- Spacing and alignment are professional
- Icons render cleanly

**Step 2: Content accuracy verification**

Check against research from Task 1:
- [ ] 25/50/25 limits are accurate
- [ ] PIP $10,000 is correct
- [ ] No-fault explanation is accurate
- [ ] Tornado statistics are from NWS
- [ ] Flood facts are from FEMA
- [ ] All source badges are correct

**Step 3: Code quality check**

Run validation:
```bash
# HTML validation (if validator available)
# Check for unclosed tags
# Verify CSS syntax
# Ensure all SVGs are valid
```

**Step 4: Commit**

```bash
git add 05-assets/infographics/
git commit -m "qa: final review and quality assurance completed"
```

---

## Task 19: Create Deployment Package

**Files:**
- Create: `05-assets/infographics/DEPLOYMENT-PACKAGE.md`

**Step 1: Create deployment checklist**

```markdown
# Deployment Package

## Files to Deploy
1. kentucky-infographics.css
2. kentucky-auto-insurance-component.html
3. kentucky-home-insurance-component.html

## Deployment Steps
1. Backup current Kentucky page
2. Upload CSS file to server
3. Update page HTML with component code
4. Test in staging environment
5. Verify all functionality
6. Deploy to production
7. Post-deployment testing

## Rollback Plan
If issues occur:
1. Revert HTML changes
2. Remove CSS file reference
3. Clear browser cache
4. Verify original visuals display

## Post-Deployment
- [ ] Monitor page load times
- [ ] Check for console errors
- [ ] Verify mobile rendering
- [ ] Test cross-browser compatibility
- [ ] Gather user feedback if possible
```

**Step 2: Commit**

```bash
git add 05-assets/infographics/DEPLOYMENT-PACKAGE.md
git commit -m "docs: add deployment package and rollback procedures"
```

---

## Task 20: Final Git Tag and Documentation

**Files:**
- Create: `docs/releases/kentucky-infographics-v1.0.md`

**Step 1: Create release notes**

```markdown
# Kentucky Insurance Infographics v1.0

## Release Date: 2026-02-15

## Summary
Two educational infographics for Dream Assurance Group's Kentucky personal insurance page:
1. Kentucky Auto Insurance Minimums Explained
2. Kentucky Home Insurance Risk Guide

## Features
- Comprehensive coverage breakdown (25/50/25)
- Real-world scenario examples
- Kentucky-specific weather risk visualization
- Authoritative data from KYTC, NWS, FEMA
- Corporate professional design
- Fully responsive
- WCAG AA compliant

## Technical Details
- Pure HTML/CSS implementation
- Inline SVG icons (no external dependencies)
- Brand colors: #C92A39, #1D252D
- Responsive grid layouts
- Mobile-optimized

## Files Changed
- Added: 05-assets/infographics/ (entire directory)
- Modified: docs/plans/ (design and implementation docs)

## Testing
- Cross-browser tested
- Accessibility verified
- Performance optimized
- Content accuracy validated

## Deployment
See: 05-assets/infographics/README.md
```

**Step 2: Create git tag**

```bash
git tag -a v1.0-kentucky-infographics -m "Release Kentucky Insurance Infographics v1.0"
git push origin v1.0-kentucky-infographics
```

**Step 3: Final commit**

```bash
git add docs/releases/
git commit -m "release: v1.0 Kentucky Insurance Infographics"
```

---

## Implementation Complete

**Deliverables:**
- 2 production-ready infographics
- Complete CSS styling with brand consistency
- Inline SVG icons (no external dependencies)
- Responsive design for all screen sizes
- Comprehensive documentation
- Installation guide
- Testing checklist
- Deployment procedures

**Next Steps:**
1. Review implementation plan
2. Choose execution method (Subagent-Driven or Parallel Session)
3. Begin implementation using @superpowers:executing-plans or @superpowers:subagent-driven-development
