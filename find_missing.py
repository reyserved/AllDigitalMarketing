import csv
import os

base_dir = '/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis'
site_data_path = os.path.join(base_dir, 'Copy of TDE Law - site-data.csv')
analysis_path = os.path.join(base_dir, 'TDE_Law_Content_Gap_Analysis.csv')

# Read all URLs from site data
site_urls = set()
with open(site_data_path, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('Address', '').strip()
        if url:
            # Normalize URL (remove trailing slash variations)
            url = url.rstrip('/')
            site_urls.add(url)

print(f"Total URLs in site-data: {len(site_urls)}")

# Read URLs from analysis
analysis_urls = set()
with open(analysis_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('Existing Client URL', '').strip()
        if url:
            url = url.rstrip('/')
            analysis_urls.add(url)

print(f"Total URLs mapped in analysis: {len(analysis_urls)}")

# Find missing URLs
missing_urls = site_urls - analysis_urls
print(f"\n--- MISSING from analysis ({len(missing_urls)} URLs) ---")
for url in sorted(missing_urls):
    print(url)
