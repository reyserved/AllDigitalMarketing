# Content Gap & Analysis

## Overview
Working hub for SEO content gap audits, landing page copy, client content deliverables, and implementation assets. This folder mixes analysis datasets, draft copy, mockups, and helper scripts used to turn audits into publishable pages.

## What Is Inside
- Markdown drafts and audits: `*.md`
- HTML mockups and landers: `*.html`
- Audit datasets and content maps: `*.csv`, `*.xlsx`
- PDFs and source references: `*.pdf`
- Images and screenshots: `*.png`, `*.jpg`
- Utilities and snippets: `*.py`, `*.txt`, `*.css`, `*.php`

## Common Client Clusters
- Family Law: `TDE_*`, `Divorce*`, `Custody*`, `Alimony*`, `Prenuptial*`, `Vasquez de Lara*`
- Nonprofit / Chisholm: `Chisholm_*`, `Nonprofit_*`, `501(c)(3)*`
- LJP Waste Solutions: `LJP*`, `Zero Landfill*`, `waste-to-energy*`, `pharma*`
- Sales Xceleration: `Sales Xceleration*`, `SalesXceleration_*`, `Top_25_Sales_Agility_*`
- Executive Function Coaching: `Executive Function*`, `EF_*`
- Banking: `Bank_Five_Nine_*`
- Sterling Lawyers: `Sterling Lawyers*`, `Sterling_Lawyers_*`
- Lancaster Law: `Lancaster_*`
- Moran Wealth: `Moran Wealth*`, `Tax Strategies*`

## Key Reference Files
- Core directive: `SEO_CORE_BRAIN.md`
- Content gap prompt: `SEO_Content_Gap_Analyzer_Prompt.md`
- Setup guide: `Content_Gap_Analyzer_Setup_Guide.md`
- Audit prompt: `enhanced-audit-prompt.md`
- Family law paid lander checklist: `Family_Law_Paid_Lander_Checklist.md`
- Feedback memory store: `BEST_PRACTICES.json`

## Folders
- `atf_content/` and `atf_mockups/` contain above-the-fold assets and working mockups.
- `schemas/` holds schema-related files and audits.

## Utilities
- `update_analysis.py` adjusts or regenerates analysis outputs.
- `find_missing.py` and `add_missing_urls.py` identify and fix URL gaps.
- `md_to_docx.py` converts markdown drafts into Word documents.

## Organized Project Structure (New)

```
├── 01-clients/                 # Client-specific work
│   ├── bank-five-nine/        # Bank Five Nine project files
│   ├── l3m/                   # L3M project files
│   ├── law-lancaster/         # Law Lancaster project files
│   ├── tde-law/               # TDE Law project files
│   ├── moran-wealth-management/ # Moran Wealth Management project files
│   ├── yoy/                   # Year Over Year project files
│   ├── mom/                   # Mom project files
│   └── other/                 # Other client work
│
├── 02-audits/                  # SEO audit reports
│   ├── schema/                # Schema markup audits
│   ├── technical/             # Technical SEO audits
│   └── content/               # Content gap audits
│
├── 03-research/                # Research materials
│   ├── keywords/              # Keyword research data
│   ├── competitors/           # Competitor analysis
│   └── serp/                  # SERP analysis
│
├── 04-deliverables/            # Client deliverables
│   ├── landing-pages/         # Landing page HTML/CSS
│   ├── content-strategies/    # Content strategy documents
│   └── internal-linking/      # Internal linking recommendations
│
├── 05-assets/                  # Reusable assets
│   ├── css/                   # CSS files
│   ├── images/                # Images and graphics
│   └── templates/             # HTML templates
│
└── 06-archives/                # Archived/completed work

```

### File Organization Guidelines

#### Client Files
- Place all client-specific files in appropriate `01-clients/` subfolder
- Include: audits, deliverables, research, communications

#### Audit Files
- Schema audits → `02-audits/schema/`
- Technical audits → `02-audits/technical/`
- Content audits → `02-audits/content/`

#### Deliverables
- Landing pages → `04-deliverables/landing-pages/`
- Content strategies → `04-deliverables/content-strategies/`
- Internal linking → `04-deliverables/internal-linking/`

### Naming Conventions
- Files: Use kebab-case `client-name-document-type-date.ext`
- Folders: Use kebab-case, keep names descriptive

### Git Guidelines
**Commit:** ✅ HTML deliverables, ✅ Markdown docs, ✅ CSV analysis, ✅ CSS files
**Don't Commit:** ❌ PDFs, ❌ Client sensitive data, ❌ Personal notes, ❌ Temporary files

See `.gitignore` for complete exclusion list.

## Notes
- `BEST_PRACTICES.json` is the workspace memory file referenced by `SEO_CORE_BRAIN.md`.
- Use `Family_Law_Paid_Lander_Checklist.md` as a reusable QA gate for paid landing pages.
- Always maintain client confidentiality
- Use descriptive commit messages
- Keep working files separate from deliverables

---

*Last Updated: 2026-02-15*
