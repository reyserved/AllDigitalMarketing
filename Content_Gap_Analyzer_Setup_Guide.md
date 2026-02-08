# Family Law Content Gap Analyzer - Setup & Usage Guide

## Overview

This guide walks you through building and using the Family Law Content Gap Analyzer app in Google AI Studio.

---

## Part 1: Build the App in AI Studio

### Step 1: Open Google AI Studio

1. Go to **[aistudio.google.com](https://aistudio.google.com/)**
2. Sign in with your Google account
3. Click **Build** in the left sidebar
4. Click **Start** to begin a new app

---

### Step 2: Configure the App Description

In the "Describe your idea" field, paste:

```
Analyze a family law firm's website against a comprehensive content template to identify missing service pages, blog consolidation opportunities, and SEO priorities based on search volume and keyword intent.
```

Click **Build** or press Enter.

---

### Step 3: Add System Instructions

1. After the app scaffolds, look for **System Instructions** (usually in settings/config panel)
2. Open the file: `Family_Law_Content_Gap_Analyzer_Prompt.md`
3. Copy ONLY the content between the triple backticks in the **"System Prompt"** section (starts with `# ROLE: Family Law SEO Content Gap Analyst`)
4. Paste into AI Studio's System Instructions field

---

### Step 4: Enable File Uploads

1. Look for **Tools** or **Capabilities** settings
2. Enable **File Upload** or **Document Upload**
3. Set accepted formats: `.csv`, `.xlsx`
4. Set max file size: 5MB

---

### Step 5: Save the App

1. Click **Save** or **Publish**
2. Name it: "Family Law Content Gap Analyzer"
3. Optionally add to "Your apps" for quick access

---

## Part 2: Prepare Your Input Files

Before running the analyzer, prepare these files:

### Required File 1: Client Site Data (CSV)

**Source:** Screaming Frog crawl export or Google Sheets export

**Required Columns:**
| Column | Description |
|--------|-------------|
| Address | Full URL (e.g., `https://example.com/divorce/`) |
| Title 1 | Page title |
| Meta Description 1 | Meta description |
| H1-1 | Main heading |
| H2-1, H2-2 | Subheadings (optional) |

**How to get this:**
1. Run Screaming Frog on client site
2. Export → Internal → All
3. Keep only columns: Address, Title 1, Meta Description 1, H1-1, H2-1, H2-2
4. Save as `site-data.csv`

---

### Optional File 2: Keyword Research Data (CSV)

**Source:** Ahrefs, SEMrush, or manual research

**Format Option A (Search Volume Only):**
```csv
Keywords,Search Volume
divorce in Georgia,2900
child support calculator Georgia,2900
Atlanta divorce lawyers,720
```

**Format Option B (With Intent/AIO):**
```csv
Keyword,Intent,AI Overview?
divorce in Georgia,Research,Yes
Atlanta divorce lawyers,Purchase,No
child support calculator Georgia,Commercial,Yes
```

---

### Gather Client Context

Before prompting, know these details:

| Field | Example | Your Client |
|-------|---------|-------------|
| Client Name | TDE Family Law | ____________ |
| Website | tdefamilylaw.com | ____________ |
| State | Georgia | ____________ |
| Primary City | Atlanta | ____________ |
| Secondary Cities | Gwinnett, Marietta | ____________ |

---

## Part 3: Run Your First Analysis

### Step 1: Open the App

1. Go to **Your apps** in AI Studio
2. Click **Family Law Content Gap Analyzer**

---

### Step 2: Upload Files

1. Click the attachment/upload icon
2. Upload `site-data.csv`
3. (Optional) Upload `keyword-research.csv`

---

### Step 3: Enter the Prompt

Copy and customize this prompt:

```
Analyze this family law firm's website:

**Client:** [CLIENT NAME]
**Website:** [WEBSITE URL]
**State:** [STATE]
**Primary City:** [PRIMARY CITY]
**Secondary Cities:** [CITY 2, CITY 3]

I've uploaded:
1. site-data.csv - Contains [X] URLs from their website
2. keyword-research.csv - Contains search volume data (optional)

Please provide:

1. **Content Gap Analysis CSV** with columns:
   - Map ID, Content Phase, Content Category, Content Type, Content Role
   - Page Title Structure, Idealized URL, Target Seed Keyword
   - Existing Client URL, Gap Status, Notes
   - Keyword Intent, AI Overview, MSV

2. **Executive Summary** including:
   - Content coverage stats (Mapped, Partial, Gap, Additional, Excluded)
   - Top priority gaps sorted by MSV
   - Blog consolidation opportunities (3+ posts on same topic)
   - True gaps with zero existing coverage
   - Flagged issues (duplicates, off-topic pages, URL problems)
   - Complete list of excluded URLs with reasons
   - Phased roadmap recommendation

Focus on actionable insights. Prioritize by search volume.
Flag any criminal or non-family-law pages as off-topic.
```

---

### Step 4: Review Output

The AI will return:

1. **CSV Data** - Copy into Google Sheets or Excel
2. **Executive Summary** - Markdown formatted report

**Quality Check:**
- [ ] Total URLs accounted for (Mapped + Partial + Gap + Additional + Excluded = Input Total)
- [ ] Gaps sorted by MSV descending
- [ ] Consolidation opportunities identified
- [ ] Excluded URLs listed with reasons

---

## Part 4: Export & Deliver

### Export CSV to Google Sheets

1. Copy the CSV output from AI Studio
2. Open Google Sheets → File → Import → Paste
3. Select "Comma" as separator
4. Clean up any formatting issues

### Export Summary to Client Doc

1. Copy the Markdown summary
2. Paste into Google Docs or Notion
3. Format tables as needed

---

## Part 5: Follow-Up Prompts

After initial analysis, use these follow-up prompts:

### Generate Content Brief for Top Gap
```
Based on the analysis, generate a detailed content brief for the "[Page Name]" page.

Include:
- Target keyword and secondary keywords
- Search intent
- Recommended word count
- Outline with H2/H3 structure
- Key topics to cover
- Internal linking opportunities
- CTA recommendations
```

### Create Consolidation Plan
```
Create a consolidation plan for the [TOPIC] blog posts.

Current posts:
1. [Blog Title 1]
2. [Blog Title 2]
3. [Blog Title 3]

Recommend:
- New pillar page structure
- Which sections to pull from each post
- Redirect strategy
- Internal linking plan
```

### Draft URL Redirect Map
```
Based on the URL structure issues identified, create a 301 redirect map.

Format:
| Old URL | New URL | Reason |

Include all URLs that need restructuring from /family-law/ to /{state}/ pattern.
```

---

## Troubleshooting

### "Output doesn't include all URLs"
→ Add to your prompt: "You MUST account for 100% of input URLs. Show the reconciliation count."

### "MSV data not showing"
→ Make sure your keyword-research.csv has matching keywords. Add: "If no MSV data found, mark as N/A."

### "Too generic recommendations"
→ Add: "Be specific. Reference actual page titles and URLs from the input data."

### "Missing consolidation suggestions"
→ Add: "Scan all blog posts. If 3+ posts cover the same topic cluster, flag as consolidation opportunity."

---

## Quick Reference Card

### Input Checklist
- [ ] site-data.csv uploaded
- [ ] Client name, state, cities noted
- [ ] (Optional) keyword-research.csv uploaded

### Output Checklist
- [ ] CSV with all columns populated
- [ ] Status counts match input total
- [ ] Gaps sorted by MSV
- [ ] Excluded URLs listed
- [ ] Phased roadmap included

### Status Definitions
| Status | Meaning |
|--------|---------|
| MAPPED | Full match exists |
| PARTIAL | Incomplete match |
| GAP - MISSING | No content |
| ADDITIONAL | Not in template |
| EXCLUDED | No SEO value |

---

*Guide Version 1.0 | January 2026*
