import csv
import os

base_dir = '/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis'
site_data_path = os.path.join(base_dir, 'Copy of TDE Law - site-data.csv')
analysis_path = os.path.join(base_dir, 'TDE_Law_Content_Gap_Analysis.csv')

# Read site data with full info
site_data = {}
with open(site_data_path, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('Address', '').strip().rstrip('/')
        if url:
            site_data[url] = {
                'title': row.get('Title 1', ''),
                'meta': row.get('Meta Description 1', ''),
                'h1': row.get('H1-1', '')
            }

# Read current analysis
analysis_urls = set()
current_rows = []
with open(analysis_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    rows = list(reader)
    headers = rows[0]
    current_rows = rows
    
    for row in rows[1:]:
        if len(row) > 8:
            url = row[8].strip().rstrip('/')
            if url:
                analysis_urls.add(url)

# Find missing
missing_urls = set(site_data.keys()) - analysis_urls

# Categorize missing URLs
def categorize_url(url, data):
    """Categorize URL and provide appropriate notes"""
    
    # Pagination / Duplicate blog pages
    if '/blog/page/' in url or '?et_blog' in url:
        return ('EXCLUDE - Pagination', 'Blog pagination page - no unique content')
    
    # Duplicate/variant URLs
    if url == 'https://tdefamilylaw.com/contact' or url == 'https://tdefamilylaw.com//family-law/prenuptial-agreement-atlanta':
        return ('EXCLUDE - Duplicate', 'Duplicate or malformed URL')
    if url == 'https://tdefamilylaw.com/consultation':
        return ('EXCLUDE - Duplicate', 'Duplicate of /schedule-a-consultation/')
    
    # Utility/Admin pages
    if any(x in url for x in ['testing-form', 'appointment-confirmation', 'landing-page', 'happy-mothers-day', 'nomination']):
        return ('EXCLUDE - Utility', 'Utility/Admin page - not user-facing content')
    
    # Staff pages
    if '/atlanta-attorneys/' in url:
        return ('ADDITIONAL', 'Staff bio page')
    
    # Family Law hub
    if url == 'https://tdefamilylaw.com/family-law':
        return ('MAPPED', 'Family Law practice area hub page')
    
    # Blog posts - categorize by topic
    if 'divorce' in url.lower() or 'custody' in url.lower() or 'alimony' in url.lower():
        return ('ADDITIONAL', 'Blog post - Family Law topic')
    
    # Service pages
    if '/family-law/' in url:
        return ('ADDITIONAL', 'Service page not in template')
    
    # Generic blog/content
    return ('ADDITIONAL', 'Blog post or content page')

# Build new rows for missing URLs
new_rows = []
map_id = 98  # Continue from last ID

for url in sorted(missing_urls):
    data = site_data.get(url, {})
    status, note = categorize_url(url, data)
    
    # Skip excluded URLs
    if 'EXCLUDE' in status:
        print(f"EXCLUDING: {url} - {note}")
        continue
    
    map_id += 1
    
    # Extract a seed keyword from title or H1
    title = data.get('h1', data.get('title', '')).lower()
    # Simple keyword extraction
    seed_kw = title.replace(' - tde family law', '').replace(' | tde family law', '').strip()
    
    new_row = [
        str(map_id),  # Map ID
        'N/A',        # Content Phase
        'Additional Client Pages',  # Content Category
        'Blog/Content',  # Content Type
        'Supporting Content',  # Content Role
        data.get('h1', ''),  # Page Title Structure (use H1)
        'N/A',  # Idealized URL
        seed_kw[:50] if seed_kw else 'N/A',  # Target Seed Keyword (truncate)
        url + '/',  # Existing Client URL (add trailing slash to match)
        status,  # Gap Status
        note,  # Notes
        'N/A',  # Keyword Intent
        'N/A',  # AI Overview
        'N/A'   # MSV
    ]
    new_rows.append(new_row)

# Append to analysis
with open(analysis_path, 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"\nAdded {len(new_rows)} new rows to analysis.")
print(f"Excluded {len(missing_urls) - len(new_rows)} URLs (pagination, duplicates, utility pages)")
