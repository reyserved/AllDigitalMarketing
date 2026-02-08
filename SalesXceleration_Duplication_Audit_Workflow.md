# Sales Xceleration Blog Duplication Audit Workflow

**Task:** Review & audit for duplication  
**Client:** Sales Xceleration  
**Date:** February 7, 2026  
**Analyst:** [Your Name]

---

## 📋 Task Definition

### Done Criteria:
> You have reviewed all published Amplify blogs (now in the Sales Recruiting category) and determined any that are duplicates of existing SalesX blogs. Any duplicate SalesX blogs (non-Amplify migration blogs) are then **canonicalized to the newest version** (the Amplify blog).

### Key Understanding:
| Blog Type | Count | Action |
|-----------|-------|--------|
| **Amplify Migration Blogs** (Sales Recruiting category) | 30 | These are the **KEEP/CANONICAL** versions |
| **Original SalesX Blogs** (non-Amplify) | 162 | Check for duplicates → If duplicate, **add canonical to Amplify version** |

---

## 📊 URL Lists

### List A: Amplify Migration Blogs (30 URLs) — THE CANONICAL TARGETS
These are the "newest versions" that should receive canonicals if duplicates exist.

```
https://salesxceleration.com/the-rise-of-skills-based-hiring/
https://salesxceleration.com/hiring-trends-forecast-for-2025/
https://salesxceleration.com/the-power-of-smart-goals-in-recruiting/
https://salesxceleration.com/the-competitive-advantage-of-hiring-sales-talent-in-a-slow-economy/
https://salesxceleration.com/why-remote-sales-teams-have-a-competitive-advantage-in-2025-and-beyond/
https://salesxceleration.com/hiring-a-salesperson-consider-recruiting-outside-your-industry/
https://salesxceleration.com/the-surprising-data-behind-sales-team-effectiveness/
https://salesxceleration.com/talent-acquisition-trends-for-small-to-mid-sized-businesses/
https://salesxceleration.com/5-tips-to-sales-leaders-to-kickstart-hiring/
https://salesxceleration.com/the-high-potential-myth-how-comfort-zones-hinder-hiring-progress/
https://salesxceleration.com/sales-hiring-strategy-how-to-hire-top-sales-talent/
https://salesxceleration.com/hiring-a-sales-team-the-dos-and-donts-of-finding-the-right-candidates/
https://salesxceleration.com/how-firing-your-top-salesperson-might-fire-up-overall-sales-performance/
https://salesxceleration.com/improving-your-sales-recruitment-and-hiring-process/
https://salesxceleration.com/the-importance-of-building-a-top-performing-sales-team/
https://salesxceleration.com/your-most-valuable-resource-the-right-people-in-the-right-positions/
https://salesxceleration.com/compensation-plan-errors-to-avoid/
https://salesxceleration.com/attract-top-talent-by-preparing-ahead-of-the-interview/
https://salesxceleration.com/a-professional-paradox-sales-careers-are-fulfilling-but-sales-jobs-go-unfilled/
https://salesxceleration.com/sales-talent-in-short-supply-how-to-hire-keep-and-manage-top-performers/
https://salesxceleration.com/hiring-basics-tips-to-help-you-get-started/
https://salesxceleration.com/hiring-during-a-recession-3-strategies-to-attract-the-right-candidates/
https://salesxceleration.com/strategies-for-finding-the-best-fit-when-hiring-for-sales-roles/
https://salesxceleration.com/hiring-in-the-remote-workplace-essential-tips-and-advice/
https://salesxceleration.com/the-impact-of-the-great-resignation-on-hiring-and-recruiting/
https://salesxceleration.com/the-benefits-of-offering-a-flexible-working-environment/
https://salesxceleration.com/adapting-to-the-new-workforce-how-employers-must-evolve-to-meet-changing-employee-expectations/
https://salesxceleration.com/quiet-quitting-how-employers-can-avoid-hiring-mistakes/
https://salesxceleration.com/investing-in-growth-why-budgeting-for-new-hires-is-crucial/
https://salesxceleration.com/effective-recruiting-and-hiring-strategies-for-small-to-mid-size-businesses/
```

### List B: Original SalesX Blogs (162 URLs) — CHECK FOR DUPLICATES
See separate file: `SalesX_Original_Blogs_162.txt`

---

## 🔍 STEP 1: Run Screaming Frog Crawl

### Configuration Recap:
1. **Mode:** List Mode
2. **URLs:** All 192 URLs (both lists combined)
3. **Near Duplicates:** Enabled, 75% threshold
4. **Semantic Embeddings:** Enabled, 0.85 similarity threshold
5. **Custom Extraction:** `div.elementor-widget-theme-post-content`

---

## 🔍 STEP 2: Export Screaming Frog Data

After crawl completes, export these reports:

| Report | Location | Purpose |
|--------|----------|---------|
| **Near Duplicates** | Content → Near Duplicates → Export | Text-based similarity |
| **Semantic Duplicates** | Content → Semantic Similarity → Export | AI/Embedding similarity |

---

## 🔍 STEP 3: Filter & Analyze Results

### Critical Filter Logic:
You are looking for pairs where:
- **URL 1** = Original SalesX Blog (List B)
- **URL 2** = Amplify Migration Blog (List A)
- **Similarity** ≥ 75% (near duplicate) OR ≥ 0.85 (semantic)

### In Excel/Sheets:
1. Import both Screaming Frog exports
2. Add a column: `Is_URL1_Amplify` = VLOOKUP against List A
3. Add a column: `Is_URL2_Amplify` = VLOOKUP against List A
4. **Filter for:** `Is_URL1_Amplify = FALSE` AND `Is_URL2_Amplify = TRUE`
   - This shows Original → Amplify duplicate pairs

### OR Filter for:
- `Is_URL1_Amplify = TRUE` AND `Is_URL2_Amplify = FALSE`
  - Then swap columns to normalize

---

## 🔍 STEP 4: Create Canonical Recommendations

### Deliverable Format:

| Original SalesX URL (Duplicate) | Amplify URL (Canonical Target) | Similarity Score | Recommendation |
|--------------------------------|-------------------------------|------------------|----------------|
| `/old-hiring-article/` | `/hiring-trends-forecast-for-2025/` | 87% | Add canonical |
| `/recruiting-tips-2022/` | `/5-tips-to-sales-leaders-to-kickstart-hiring/` | 0.91 | Add canonical |

### For Each Duplicate Pair:
```
Action: Add rel="canonical" to Original SalesX Blog
From: https://salesxceleration.com/[original-slug]/
To: https://salesxceleration.com/[amplify-slug]/
```

---

## 🔍 STEP 5: Implementation Instructions

### WordPress Implementation (per duplicate found):

#### Option A: Via Yoast SEO
1. Edit the **Original SalesX blog** (the duplicate being canonicalized)
2. Scroll to **Yoast SEO** meta box
3. Go to **Advanced** tab
4. In **Canonical URL** field, enter the Amplify blog URL
5. Update/Publish

#### Option B: Via Rank Math
1. Edit the **Original SalesX blog**
2. Open **Rank Math** settings
3. Go to **Advanced** tab
4. Enter the Amplify URL in **Canonical URL**
5. Update/Publish

#### Option C: Direct Code (if no SEO plugin)
Add to `<head>` of the Original SalesX blog:
```html
<link rel="canonical" href="https://salesxceleration.com/[amplify-slug]/" />
```

---

## ✅ STEP 6: Final Deliverable Checklist

### Deliverable 1: Duplicate Analysis Report
- [ ] Excel/CSV with all duplicate pairs
- [ ] Columns: Original URL, Amplify URL, Similarity %, Match Type (Near/Semantic)
- [ ] Recommendation column

### Deliverable 2: Implementation Tracker
- [ ] Original SalesX URL
- [ ] Canonical Target (Amplify URL)
- [ ] Implementation Status (Not Started / In Progress / Complete)
- [ ] Date Implemented
- [ ] Verified (Y/N)

### Deliverable 3: Summary Report
- [ ] Total Amplify blogs reviewed: 30
- [ ] Total Original SalesX blogs compared: 162
- [ ] Duplicate pairs found: [X]
- [ ] Canonicals implemented: [X]
- [ ] No match / Unique content: [X]

---

## ⚠️ Edge Cases to Consider

### 1. Multiple Originals → One Amplify
If multiple Original SalesX blogs match the same Amplify blog:
- All originals should canonical to that one Amplify URL

### 2. Partial/Topical Overlap (Not True Duplicates)
- Similarity 50-75%: Flag for **content consolidation review**
- These may benefit from 301 redirect instead of canonical

### 3. No Duplicates Found
- Document that the Amplify migration blogs are unique
- No action required

---

## 📋 Post-Implementation Verification

After implementing canonicals:

1. **Re-crawl with Screaming Frog**
2. Check **Canonicals** report
3. Verify each Original SalesX blog shows:
   - `Canonical Link Element 1` = Amplify URL
   - `Canonical Link Element 1 Status` = 200
4. **GSC Coverage** check after 1-2 weeks
   - Original URLs should show "Duplicate, Google chose different canonical"

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `SalesXceleration_Duplication_Audit_Workflow.md` | This workflow document |
| `Amplify_Migration_Blogs_30.txt` | Amplify blog URLs for Screaming Frog |
| `SalesX_Original_Blogs_162.txt` | Original blog URLs for Screaming Frog |
| `All_Blogs_Combined_192.txt` | Combined list for single crawl |

---

## 📞 Status Update Template

### For Client/Team Communication:

```
DUPLICATION AUDIT STATUS - Sales Xceleration

Scope:
- Amplify Migration Blogs (Sales Recruiting): 30
- Original SalesX Blogs: 162
- Total Analyzed: 192

Findings:
- Near Duplicate Pairs Found: [X]
- Semantic Duplicate Pairs Found: [X]
- Total Unique (No Duplicates): [X]

Actions Taken:
- Canonicals Implemented: [X]
- Pending Implementation: [X]

Verification:
- All canonicals verified via Screaming Frog re-crawl: [Y/N]
```
