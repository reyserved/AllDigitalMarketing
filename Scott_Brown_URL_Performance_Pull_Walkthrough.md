# URL & Performance Pull Walkthrough
## Scott M. Brown & Associates (sbrownlawyer.com)

**Task Owner:** SEO Specialist  
**Date:** January 22, 2026  
**Client:** Scott M. Brown & Associates  
**Website:** https://sbrownlawyer.com/

---

## 📋 Task Overview

**Done Statement:** Pull performance data for all pages identified in the content mapping file, comparing:
- Last 3 months vs. Previous 3 months
- Last 3 months vs. Same 3 months last year (if applicable)

**Metrics Required:**
| Metric | Source |
|--------|--------|
| Impressions | Google Search Console |
| Clicks | Google Search Console |
| New Users | GA4 |
| Key Event Conversions | GA4 |
| Top Keyword Rankings | SEMrush |

---

## 🔢 URLs to Pull (From Content Mapping)

Based on the Gap Analysis file, there are **31 existing URLs** that need performance data:

```
https://sbrownlawyer.com/attorneys/
https://sbrownlawyer.com/texas/locations/
https://sbrownlawyer.com/divorce/
https://sbrownlawyer.com/child-custody/
https://sbrownlawyer.com/child-support/
https://sbrownlawyer.com/attorneys-working-to-achieve-your-alimony-goals/
https://sbrownlawyer.com/division-of-property/
https://sbrownlawyer.com/paternity/
https://sbrownlawyer.com/complex-and-contested-divorce-attorneys/
https://sbrownlawyer.com/uncontested-divorce-lawyer-in-pearland/
https://sbrownlawyer.com/modification-of-custody/
https://sbrownlawyer.com/child-support-modifications/
https://sbrownlawyer.com/enforcing-child-support-orders/
https://sbrownlawyer.com/creative-custody-agreements/
https://sbrownlawyer.com/how-is-community-property-divided/
https://sbrownlawyer.com/paternity-attorney/
https://sbrownlawyer.com/child-custody/emergency/
https://sbrownlawyer.com/assets-and-liability/
https://sbrownlawyer.com/the-unique-aspects-of-alimony-spousal-maintenance-in-texas/
https://sbrownlawyer.com/parental-relocation/
https://sbrownlawyer.com/business-owner-divorce/
https://sbrownlawyer.com/contested-custody/
https://sbrownlawyer.com/gray-divorce/
https://sbrownlawyer.com/business-and-professional-practices-in-divorce/
https://sbrownlawyer.com/family-law/visitation/
https://sbrownlawyer.com/high-net-worth-divorce/
https://sbrownlawyer.com/hidden-assets/
```

---

## 🛠️ Tools Required

| Tool | Purpose | Access Required |
|------|---------|-----------------|
| **Google Search Console** | Impressions, Clicks, CTR, Position | Owner/Full User access to property |
| **Google Analytics 4** | New Users, Sessions, Key Events | Analyst+ access |
| **SEMrush** | Keyword rankings, Position tracking | Paid account |
| **Screaming Frog** | Bulk data integration (optional) | License for 500+ URLs |
| **Google Sheets/Excel** | Final output compilation | N/A |

---

## 📊 STEP-BY-STEP WALKTHROUGH

---

### PHASE 1: Google Search Console Data Pull (Impressions + Clicks)

#### Step 1.1: Access GSC
1. Go to https://search.google.com/search-console
2. Select the property: `sbrownlawyer.com` (or `sc-domain:sbrownlawyer.com`)

#### Step 1.2: Set Date Ranges
You need THREE exports:

| Export | Date Range | Label |
|--------|------------|-------|
| **Export A** | Last 3 months (Oct 22, 2025 - Jan 21, 2026) | `L3M_Current` |
| **Export B** | Previous 3 months (Jul 22, 2025 - Oct 21, 2025) | `L3M_Previous` |
| **Export C** | Same 3 months last year (Oct 22, 2024 - Jan 21, 2025) | `L3M_YoY` |

#### Step 1.3: Export Page Performance
For EACH date range:

1. Click **Performance** in left sidebar
2. Click **+ New** filter → **Page**
3. Set date range (top date picker)
4. Click **Pages** tab
5. Click **Export** (top right) → **Download CSV**
6. Rename file to: `GSC_[Label]_Pages.csv`

**Pro Tip:** If you want to filter ONLY the mapped pages:
1. Click **+ New** filter → **Page** → **Regex matches**
2. Paste this regex:
```regex
^https:\/\/sbrownlawyer\.com\/(attorneys|texas\/locations|divorce|child-custody|child-support|attorneys-working|division-of-property|paternity|complex-and-contested|uncontested-divorce|modification-of-custody|child-support-modifications|enforcing-child-support|creative-custody|how-is-community|paternity-attorney|assets-and-liability|the-unique-aspects|parental-relocation|business-owner|contested-custody|gray-divorce|business-and-professional|family-law\/visitation|high-net-worth|hidden-assets)
```

#### Step 1.4: GSC Output Format
Your CSV will have these columns:
| Page | Clicks | Impressions | CTR | Position |
|------|--------|-------------|-----|----------|

---

### PHASE 2: GA4 Data Pull (New Users + Conversions)

#### Step 2.1: Access GA4
1. Go to https://analytics.google.com
2. Select the Scott M. Brown property

#### Step 2.2: Create Custom Report
1. Go to **Explore** (left sidebar)
2. Click **+ Blank** exploration

#### Step 2.3: Configure Exploration
**Dimensions (drag to Rows):**
- Page path and screen class

**Metrics (drag to Values):**
- New users
- Sessions
- Key events (all)
- Key event rate

**Date Comparison:**
1. Click the date range at top
2. Select "Last 3 months"
3. Enable **Compare** toggle
4. Select "Previous period" for Export B
5. OR Select "Same period last year" for Export C

#### Step 2.4: Export GA4 Data
1. Right-click on the exploration table
2. Select **Export** → **CSV**
3. Rename: `GA4_[Label]_Pages.csv`

#### Alternative: Use GA4 Looker Studio Report
If Explore is too slow:
1. Create a Looker Studio dashboard
2. Connect GA4
3. Set up table with: Page Path, New Users, Key Events
4. Add date range controls for easy comparison

---

### PHASE 3: SEMrush Keyword Rankings

#### Step 3.1: Domain Overview
1. Go to https://semrush.com
2. Enter `sbrownlawyer.com` in Domain Overview
3. Select "Organic Research" → "Positions"

#### Step 3.2: Export All Keywords
1. Click **Export** → **Full Export (CSV)**
2. This gives you ALL keywords the domain ranks for

#### Step 3.3: Filter to Mapped URLs
In the export:
1. Open in Excel/Sheets
2. Filter "URL" column by the 31 target URLs from your content mapping
3. Keep columns: Keyword, Position, Volume, URL, Traffic %

#### Step 3.4: Alternative - Position Tracking
For ongoing monitoring:
1. Go to **Position Tracking** in SEMrush
2. Create new project for `sbrownlawyer.com`
3. Add the target seed keywords from content mapping:
   - divorce lawyer texas
   - child custody lawyer texas
   - child support lawyer texas
   - etc.
4. Set location: Texas, USA
5. Export weekly position data

---

### PHASE 4: Screaming Frog Integration (EXPEDITED METHOD)

This method pulls GSC + GA4 data in ONE crawl → **SAVES 30+ MINUTES**

#### Step 4.1: Configure Screaming Frog
1. Open Screaming Frog SEO Spider
2. Go to **Configuration** → **API Access**

#### Step 4.2: Connect Google Search Console
1. Click **Google Search Console** tab
2. Click **Connect to new account**
3. Authenticate with Google account that has GSC access
4. Select property: `sbrownlawyer.com`

#### Step 4.3: Connect GA4
1. Click **Google Analytics** tab
2. Click **Connect to new account**
3. Select GA4 property for Scott M. Brown

#### Step 4.4: Configure Metrics to Pull
**GSC Metrics:**
- ☑️ Clicks
- ☑️ Impressions
- ☑️ CTR
- ☑️ Position
- Date Range: Last 3 months

**GA4 Metrics:**
- ☑️ New Users
- ☑️ Sessions
- ☑️ Key Events
- Date Range: Last 3 months

#### Step 4.5: Run the Crawl
1. Enter: `https://sbrownlawyer.com/`
2. Click **Start**
3. Wait for crawl to complete

#### Step 4.6: Export Combined Data
1. Go to **Bulk Export** → **All** → **Internal**
2. This CSV will include ALL metrics from GSC + GA4 per URL

---

### PHASE 5: Compile Final Output

#### Step 5.1: Create Master Spreadsheet
Create: `Scott_Brown_URL_Performance_Data.xlsx`

**Tab 1: Performance Summary**
| URL | Target Keyword | L3M Clicks | Prev 3M Clicks | Δ Clicks % | L3M Impressions | Prev 3M Impressions | Δ Impr % | L3M New Users | Prev 3M New Users | Δ Users % | L3M Key Events | Prev 3M Key Events | Δ Conv % |
|-----|----------------|-----------|-----------------|------------|-----------------|---------------------|----------|---------------|-------------------|-----------|----------------|--------------------| -------- |

**Tab 2: YoY Comparison**
| URL | Target Keyword | L3M Clicks | L3M LY Clicks | YoY Δ % | L3M Impressions | L3M LY Impressions | YoY Δ % |
|-----|----------------|-----------|---------------|---------|-----------------|--------------------| ------- |

**Tab 3: Top Keyword Rankings**
| URL | Top Keyword 1 | Pos | Volume | Top Keyword 2 | Pos | Volume | Top Keyword 3 | Pos | Volume |
|-----|---------------|-----|--------|---------------|-----|--------|---------------|-----|--------|

**Tab 4: Gaps (No Data)**
List URLs with NO impressions/clicks → these are true gaps

#### Step 5.2: Calculate Deltas
Use Excel formulas:
```excel
=IF(B2>0, (A2-B2)/B2, "N/A")
```

#### Step 5.3: Color Code Performance
| Δ Range | Color | Meaning |
|---------|-------|---------|
| > +20% | 🟢 Green | Strong growth |
| +5% to +20% | 🟡 Yellow | Moderate growth |
| -5% to +5% | ⬜ Gray | Flat |
| -20% to -5% | 🟠 Orange | Decline |
| < -20% | 🔴 Red | Significant decline |

---

## ⚡ EXPEDITED WORKFLOW (15-20 mins)

If you have Screaming Frog with API access:

```
1. Configure SF with GSC + GA4 API connections (5 min one-time setup)
2. Run crawl with API integration enabled (8 min)
3. Export combined data (1 min)
4. Run domain through SEMrush Organic Positions (3 min)
5. Merge data in Excel (3 min)
```

If you DON'T have Screaming Frog:

```
1. GSC Export #1 (Current L3M) - 5 min
2. GSC Export #2 (Previous L3M) - 5 min
3. GSC Export #3 (YoY L3M) - 5 min
4. GA4 Explore Report - 10 min
5. SEMrush Export - 5 min
6. Merge all data - 15 min
TOTAL: ~45 min
```

---

## 📁 Deliverable Checklist

- [ ] `GSC_L3M_Current_Pages.csv`
- [ ] `GSC_L3M_Previous_Pages.csv`
- [ ] `GSC_L3M_YoY_Pages.csv` (if data exists)
- [ ] `GA4_L3M_Current_Pages.csv`
- [ ] `GA4_L3M_Previous_Pages.csv`
- [ ] `SEMrush_Organic_Positions.csv`
- [ ] **FINAL:** `Scott_Brown_URL_Performance_Data.xlsx` (compiled)

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| GSC shows no data for a URL | URL may not be indexed; check Index Coverage |
| GA4 date comparison is confusing | Use Explore → set explicit date ranges |
| SEMrush shows different URLs | Some pages may have parameters or redirects |
| Screaming Frog API timeout | Reduce crawl speed, check API limits |
| Low/no key events | Confirm conversion tracking is set up in GA4 |

---

## 📞 Access Requirements Checklist

Before starting, confirm you have:

- [ ] GSC Full User access to `sbrownlawyer.com`
- [ ] GA4 Analyst access (minimum) to property
- [ ] SEMrush paid account OR agency access
- [ ] Screaming Frog license (for expedited method)
- [ ] Content Mapping file for URL reference

---

## 🎯 Success Criteria

Your output is complete when:

1. ✅ All 31 mapped URLs have performance data (or noted as "No Data")
2. ✅ L3M vs Previous L3M comparison is complete with % deltas
3. ✅ YoY comparison is included (where data exists)
4. ✅ Top 3 keywords per URL are documented with positions
5. ✅ Final spreadsheet is formatted and color-coded

---

*Walkthrough created: January 22, 2026*
