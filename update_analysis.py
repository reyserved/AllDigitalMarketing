import csv
import os

base_dir = '/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis'

# Read keyword search volume data
kw_volume_path = os.path.join(base_dir, 'KW Search Volume - Family Law Content Map template  - Sheet28.csv')
intent_aio_path = os.path.join(base_dir, ' intent-ai-overviews.csv')
analysis_path = os.path.join(base_dir, 'TDE_Law_Content_Gap_Analysis.csv')

# Build volume lookup
volume_map = {}
with open(kw_volume_path, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        kw = row.get('Keywords', '').strip().lower()
        vol = row.get('Search Volume', '').strip()
        if kw:
            volume_map[kw] = vol if vol else 'N/A'

print(f"Loaded {len(volume_map)} search volume entries.")

# Build intent/AIO lookup
intent_map = {}
with open(intent_aio_path, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_kw = row.get('Keyword', '').strip()
        intent = row.get('Intent', '').strip()
        aio = row.get('AI Overview?', '').strip()
        
        # Normalize {state} -> Georgia, {brand} -> TDE Law
        norm_kw = raw_kw.replace('{state}', 'Georgia')
        norm_kw = norm_kw.replace('{brand}', 'TDE Law')
        norm_kw = norm_kw.strip().lower()
        
        if norm_kw:
            intent_map[norm_kw] = (intent, aio)

print(f"Loaded {len(intent_map)} intent/AIO entries.")

# Read and update analysis
updated_rows = []
with open(analysis_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    rows = list(reader)
    
    if not rows:
        exit(1)
    
    # Header row
    headers = rows[0]
    
    # Determine if columns already exist, else add
    # Current columns end at: Notes, Keyword Intent, AI Overview (indices 10, 11, 12)
    # We need to add: Monthly Search Volume (MSV)
    
    # First, find Target Seed Keyword index
    try:
        kw_idx = headers.index('Target Seed Keyword')
    except ValueError:
        kw_idx = 7
    
    # Check if MSV column exists
    if 'MSV' not in headers and 'Monthly Search Volume' not in headers:
        # We'll add 3 new columns: Keyword Intent, AI Overview, MSV
        # But looking at existing data, Intent/AIO are already cols 11-12
        # So just add MSV
        new_headers = headers[:13] + ['MSV']
    else:
        new_headers = headers
    
    # Actually let's rebuild cleanly to ensure consistency
    # Keep cols 0-10 (Map ID through Notes), then add: Keyword Intent, AI Overview, MSV
    base_headers = ['Map ID', 'Content Phase', 'Content Category', 'Content Type', 'Content Role', 
                    'Page Title Structure', 'Idealized URL', 'Target Seed Keyword', 
                    'Existing Client URL', 'Gap Status', 'Notes', 'Keyword Intent', 'AI Overview', 'MSV']
    
    updated_rows.append(base_headers)
    
    for row in rows[1:]:
        if not row or len(row) < 8:
            continue
        
        # Extract keyword
        curr_kw = row[kw_idx].strip().lower()
        
        # Get volume
        vol = volume_map.get(curr_kw, 'N/A')
        
        # Get intent/AIO - check both new file and preserve existing if better
        intent_data = intent_map.get(curr_kw)
        if intent_data:
            intent, aio = intent_data
        else:
            # Keep existing from row if available
            intent = row[11] if len(row) > 11 else 'N/A'
            aio = row[12] if len(row) > 12 else 'N/A'
        
        # Build new row
        new_row = row[:11]  # Cols 0-10
        new_row.append(intent)
        new_row.append(aio)
        new_row.append(vol)
        
        updated_rows.append(new_row)

# Write
with open(analysis_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(updated_rows)

print("Analysis updated with fresh MSV, Intent, and AIO data.")
