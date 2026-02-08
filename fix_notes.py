import csv
import os
import re

base_dir = '/Applications/Antigravity/ROCKET CLICKS/Content Gap & Analysis'
analysis_path = os.path.join(base_dir, 'TDE_Law_Content_Gap_Analysis.csv')

updated_rows = []

with open(analysis_path, 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    rows = list(reader)
    
    # Header row
    headers = rows[0]
    updated_rows.append(headers)
    
    for row in rows[1:]:
        if not row or len(row) < 11:
            continue
        
        notes = row[10]  # Column K (index 10)
        
        # 1. Remove "and is optimized" claims
        notes = notes.replace(' and is optimized', '')
        notes = notes.replace('Homepage exists and is optimized', 'Homepage exists')
        
        # 2. Remove old MSV references like "(MSV: 4400)", "(MSV: 9900)" etc.
        notes = re.sub(r'\s*\(MSV:\s*\d+\)', '', notes)
        
        # 3. Clean up specific notes
        # Change "High-value content opportunity" to just "Content gap" since MSV is now in own column
        notes = re.sub(r'High-value content opportunity$', 'Content gap', notes)
        notes = re.sub(r'High-value tool opportunity$', 'Tool gap', notes)
        
        row[10] = notes.strip()
        updated_rows.append(row)

# Write
with open(analysis_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(updated_rows)

print("Notes column cleaned up - removed incorrect MSV references and optimization claims.")
