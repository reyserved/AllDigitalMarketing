# Family Law Content Gap Analyzer - Quick Start Walkthrough

## What You'll Build
An AI-powered app that analyzes family law firm websites and identifies content gaps, just like the TDE Law analysis we did.

---

## Step 1: Open AI Studio

1. Go to **[aistudio.google.com](https://aistudio.google.com/)**
2. Sign in with Google
3. Click **Build** (left sidebar)
4. Click **Start**

![AI Studio Start Screen](You'll see "Build your ideas with Gemini" and a text box)

---

## Step 2: Enter App Description

In the **"Describe your idea"** text box, paste this:

```
Analyze a family law firm's website against a comprehensive content template to identify missing service pages, blog consolidation opportunities, and SEO priorities based on search volume and keyword intent.
```

Press **Enter** or click **Build**.

---

## Step 3: Add System Instructions

After the app generates, find **System Instructions** (usually in a settings panel or gear icon).

1. Open the file: `/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis/Family_Law_Content_Gap_Analyzer_Prompt.md`
2. Find the section that starts with: `# ROLE: Family Law SEO Content Gap Analyst`
3. Copy EVERYTHING from that line until the closing triple backticks (```)
4. Paste into the System Instructions field

**Important:** Copy only the content INSIDE the code block, not the markdown formatting around it.

---

## Step 4: Enable File Uploads

Look for **Tools**, **Capabilities**, or **Settings** and enable:
- ✅ File Upload
- ✅ Accept: CSV files
- ✅ Max size: 5MB

---

## Step 5: Save the App

1. Click **Save** or **Create App**
2. Name: `Family Law Content Gap Analyzer`
3. The app is now in **Your Apps**

---

## Step 6: Prepare Your Files

You need 2-3 files for each analysis:

### File 1: Client Site Data (REQUIRED)
**Filename:** `site-data.csv`

**How to get it:**
1. Run Screaming Frog on client website
2. Export → Internal → All
3. Keep columns: Address, Title 1, Meta Description 1, H1-1, H2-1, H2-2
4. Save as CSV

**Example format:**
```csv
Address,Title 1,Meta Description 1,H1-1,H2-1,H2-2
https://example.com/,Brand Name | Family Law,Meta description here,Main H1 Heading,Subheading 1,Subheading 2
https://example.com/divorce/,Divorce Services,Divorce description,Divorce Lawyer,Contact Us,
```

**Your file:** `Copy of TDE Law - site-data.csv`

---

### File 2: Keyword Research Data (OPTIONAL but recommended)
**Filename:** `keyword-research.csv`

**Format Option A - Search Volume Only:**
```csv
Keywords,Search Volume
divorce in Georgia,2900
child support calculator Georgia,2900
Atlanta divorce lawyers,720
```

**Format Option B - With Intent:**
```csv
Keyword,Intent,AI Overview?
divorce in Georgia,Research,Yes
Atlanta divorce lawyers,Purchase,No
```

**Your files:** 
- `KW Search Volume - Family Law Content Map template - Sheet28.csv`
- `intent-ai-overviews.csv`

---

### File 3: Content Template (REFERENCE - Don't upload)
The Family Law Content Map template is already baked into the system prompt. You don't need to upload it.

---

## Step 7: Run Your First Analysis

### Open the App
Go to **Your Apps** → Click **Family Law Content Gap Analyzer**

### Upload Files
Click the **attachment/paperclip icon** and upload:
1. `site-data.csv` (required)
2. `keyword-research.csv` (optional)

### Enter This Prompt

Copy and paste this EXACTLY, then fill in the blanks:

```
Analyze this family law firm's website:

**Client:** [ENTER CLIENT NAME]
**Website:** [ENTER WEBSITE URL]
**State:** [ENTER STATE]
**Primary City:** [ENTER PRIMARY CITY]
**Secondary Cities:** [ENTER OTHER CITIES, comma-separated]

I've uploaded:
1. site-data.csv - Contains [X] URLs from their website
2. keyword-research.csv - Contains search volume data

Please provide:

## OUTPUT 1: Content Gap Analysis CSV

Generate a complete CSV with these exact columns:
- Map ID, Content Phase, Content Category, Content Type, Content Role
- Page Title Structure, Idealized URL, Target Seed Keyword
- Existing Client URL, Gap Status, Notes
- Keyword Intent, AI Overview, MSV

Use ONLY these status values:
- MAPPED (full match)
- PARTIAL (incomplete match)
- GAP - MISSING (no content)
- ADDITIONAL (not in template)

## OUTPUT 2: Executive Summary

Include ALL of these sections:
1. Content Coverage Overview table (counts for each status + EXCLUDED)
2. Key Strategic Insight (in a callout block)
3. Top Priority Gaps by MSV (tables for 500+ and 100-499)
4. Blog Consolidation Opportunities table
5. True Gaps with zero coverage
6. Flagged Issues (off-topic pages, duplicates, URL structure)
7. Complete list of Excluded URLs (pagination, duplicates, utility)
8. Recommended Phase Prioritization
9. Summary Metrics table

## REQUIREMENTS
- Account for 100% of input URLs (Mapped + Partial + Gap + Additional + Excluded = Total)
- Sort gaps by MSV descending
- Flag any criminal/DUI/non-family-law pages as off-topic
- Identify 3+ blogs on same topic as consolidation opportunities
- Never claim pages are "optimized" - we don't have that data
```

---

## Step 8: Review Output

The AI will generate:

### Part 1: CSV Data
- Copy this into Google Sheets
- File → Import → Paste → Comma separator
- Review for accuracy

### Part 2: Executive Summary
- Copy into Google Docs or Notion
- Format tables as needed
- Send to client/manager

---

## Quality Checklist

Before delivering, verify:

- [ ] **URL Count Matches:** Mapped + Partial + Gap + Additional + Excluded = Input Total
- [ ] **Gaps Sorted by MSV:** Highest MSV at top
- [ ] **Consolidation Found:** If client has 3+ blogs on child support, alimony, etc.
- [ ] **Off-Topic Flagged:** Criminal/DUI pages marked if present
- [ ] **Excluded Listed:** All pagination/duplicates/utility pages shown
- [ ] **No "Optimized" Claims:** Notes don't claim pages are optimized

---

## Example: TDE Law Analysis

Here's what I entered when analyzing TDE Law:

```
Analyze this family law firm's website:

**Client:** TDE Family Law
**Website:** https://tdefamilylaw.com/
**State:** Georgia
**Primary City:** Atlanta
**Secondary Cities:** Gwinnett

I've uploaded:
1. site-data.csv - Contains 128 URLs from their website
2. keyword-research.csv - Contains search volume data

[Rest of prompt as shown above...]
```

**Result:**
- 152-row CSV with all mappings
- Executive summary with 37 gaps, 67 additional pages, 15 excluded
- Top gap: Child Support Calculator (MSV: 2,900)
- Key insight: "Consolidation over Creation"

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Output cuts off mid-CSV | Ask: "Continue the CSV from row [X]" |
| Missing sections in summary | Ask: "Add the [Section Name] section" |
| MSV shows N/A everywhere | Your keyword-research.csv may not have matching keywords |
| Counts don't add up | Ask: "Reconcile the URL counts and show the breakdown" |
| Too generic insights | Ask: "Reference specific URLs and page titles in your analysis" |

---

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| System Prompt | `Family_Law_Content_Gap_Analyzer_Prompt.md` | Paste into AI Studio |
| Example Site Data | `Copy of TDE Law - site-data.csv` | Upload to test |
| Example Keywords | `KW Search Volume - Family Law Content Map template - Sheet28.csv` | Upload to test |
| Example Intent Data | `intent-ai-overviews.csv` | Upload to test |
| Example Output CSV | `TDE_Law_Content_Gap_Analysis.csv` | Reference for expected format |
| Example Output Summary | `TDE_Law_Content_Gap_Summary.md` | Reference for expected format |

---

## Next Steps After First Analysis

1. **Verify accuracy** against client site (spot-check 10 URLs)
2. **Refine if needed** with follow-up prompts
3. **Export to Sheets** for client delivery
4. **Generate content briefs** for top gaps

---

*Quick Start Guide v1.0 | January 2026*
