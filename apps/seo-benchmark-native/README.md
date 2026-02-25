# SEO Benchmark Native (Streamlit)

Workspace-native app for deterministic SEO benchmark analysis across L3M, MoM, and YoY windows.

## What It Does
- Ingests 9 performance CSVs (`L3M/MoM/YoY x Service/Location/Supporting`) plus required metadata/H1 CSV.
- Reclassifies pages using:
  - provided `Type` (kept when present),
  - deterministic inference from URL + title + meta + H1,
  - optional custom bucket rules entered per run.
- Supports default buckets (`Service`, `Location`, `Supporting`) plus custom buckets and `Unclassified` fallback.
- Produces:
  - `benchmark-analysis.csv`
  - `benchmark-qa.csv`
  - `benchmark-qa-summary.txt`
- Generates a copy-ready prompt template in app after each run.

## Quick Start (One Click)
1. Finder launch (recommended):
   - Double-click `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/launch-seo-benchmark.command`
2. Terminal shortcut launch:
   - `bash "/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/apps/seo-benchmark-native/run_app.sh"`
3. Manual fallback (debug mode):
   - `cd "/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING"`
   - `streamlit run apps/seo-benchmark-native/app.py`

The launcher auto-creates/uses a local virtual environment at:
- `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/apps/seo-benchmark-native/.venv`

The launcher auto-selects a port starting at `8501` and opens the URL in your browser.

## Install (Manual)
```bash
cd "/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/apps/seo-benchmark-native"
python3 -m pip install -r requirements.txt
```

## Input Requirements
Required files each run:
- `L3M-services.csv`
- `mom-services.csv`
- `yoy-services.csv`
- `L3M-location.csv`
- `mom-location.csv`
- `yoy-location.csv`
- `L3M-supporting.csv`
- `mom-supporting.csv`
- `yoy-supporting.csv`
- `metadata-h1.csv`

Custom rule format:
```text
BucketName: url_contains=...; title_contains=...; meta_contains=...; h1_contains=...; exclude=...
```

Example:
```text
Blog: url_contains=/blog/,/insights/; title_contains=blog,guide; h1_contains=insights
Service Area: url_contains=/service-area/,/locations/; h1_contains=service area
```

## Output Location
Each run writes to:
- `output/spreadsheet/seo-benchmark/<YYYYMMDD-HHMMSS>/`

Files:
- `benchmark-analysis.csv`
- `benchmark-qa.csv`
- `benchmark-qa-summary.txt`

## Validation Behavior
If required columns are missing or URL sets mismatch:
- Main analysis CSV is still created with bucket rows,
- metric fields are left blank,
- `Data Coverage Notes` contains explicit validation explanation,
- QA files capture exact issues and suggested fixes.

## Codex Note
The launcher and "Copy Prompt" button are not in the Codex chat pane.
- Launch the app via `.command` or `run_app.sh`
- In the Streamlit app, run the benchmark and scroll to the `Prompt Template` section

## Future Threads
Open future Codex threads in the same workspace path:
- `/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING`

## Tests
```bash
cd "/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/apps/seo-benchmark-native"
pytest -q
```
