import csv
import re
from datetime import datetime
import os

blogs_csv = '/Users/reymartjansarigumba/Desktop/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/Copy of Sterling Lawyers Illinois _ Internal Linking Structure & Recommendations - Current Pages.csv'

# Output inside the valid workspace
output_csv = '/Applications/Antigravity/ROCKET CLICKS/ALL DIGITAL MARKETING/Sterling_Lawyers_Topic_Clustering.csv'

# Mappings based on core-subserv.csv
mappings = [
    {'keywords': ['contested-divorce'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/contested/', 'cluster_id': '', 'h1': 'Contested Divorce in Illinois', 'anchor': 'contested divorce in Illinois'},
    {'keywords': ['uncontested-divorce'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/uncontested-divorce/', 'cluster_id': '', 'h1': 'Uncontested Divorce in Illinois', 'anchor': 'uncontested divorce in Illinois'},
    {'keywords': ['divorce-mediation'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/mediation/', 'cluster_id': '', 'h1': 'Illinois Divorce Mediation', 'anchor': 'Illinois divorce mediation'},
    {'keywords': ['collaborative-divorce'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/collaborative/', 'cluster_id': '', 'h1': 'Illinois Collaborative Divorce', 'anchor': 'Illinois collaborative divorce'},
    {'keywords': ['military-divorce'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/', 'cluster_id': 'DIV', 'h1': 'Illinois Divorce Laws', 'anchor': 'Illinois military divorce representation'}, # maps to core divorce, specific anchor
    {'keywords': ['property-division', 'hidden-assets'], 'target': 'https://www.sterlinglawyers.com/illinois/property-division/hidden-assets/', 'cluster_id': '', 'h1': 'How to Find Hidden Assets During a Divorce in Illinois', 'anchor': 'finding hidden assets during a divorce'},
    {'keywords': ['property-division', 'marital-property'], 'target': 'https://www.sterlinglawyers.com/illinois/property-division/marital-property/', 'cluster_id': '', 'h1': 'Marital Property in Illinois', 'anchor': 'Illinois marital property division'},
    {'keywords': ['property-division'], 'target': 'https://www.sterlinglawyers.com/illinois/property-division/', 'cluster_id': 'PROP-DIV', 'h1': 'Illinois Property Division Laws', 'anchor': 'Illinois property division laws'},
    {'keywords': ['child-custody', 'paternity'], 'target': 'https://www.sterlinglawyers.com/illinois/child-custody/paternity/', 'cluster_id': '', 'h1': 'Establishing Paternity in Illinois', 'anchor': 'establishing paternity for child custody in Illinois'},
    {'keywords': ['child-custody', 'parenting-plan'], 'target': 'https://www.sterlinglawyers.com/illinois/child-custody/parenting-plan/', 'cluster_id': '', 'h1': 'Illinois Parenting Plan Template', 'anchor': 'Illinois parenting plan'},
    {'keywords': ['child-custody'], 'target': 'https://www.sterlinglawyers.com/illinois/child-custody/', 'cluster_id': 'CH-CUS', 'h1': 'Illinois Child Custody Laws', 'anchor': 'Illinois child custody laws'},
    {'keywords': ['child-support', 'enforce'], 'target': 'https://www.sterlinglawyers.com/illinois/child-support/enforce-orders/', 'cluster_id': '', 'h1': 'Child Support Enforcement in Illinois', 'anchor': 'child support enforcement in Illinois'},
    {'keywords': ['child-support'], 'target': 'https://www.sterlinglawyers.com/illinois/child-support/', 'cluster_id': 'CH-SUP', 'h1': 'Illinois Child Support Laws', 'anchor': 'Illinois child support requirements'},
    {'keywords': ['spousal-support', 'alimony'], 'target': 'https://www.sterlinglawyers.com/illinois/spousal-support/', 'cluster_id': 'SPO-SUP', 'h1': 'Illinois Alimony Laws', 'anchor': 'Illinois spousal support laws'},
    {'keywords': ['paternity'], 'target': 'https://www.sterlinglawyers.com/illinois/paternity/', 'cluster_id': 'PT', 'h1': 'Illinois Paternity Laws', 'anchor': 'Illinois paternity rights'},
    {'keywords': ['divorce', 'separation'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/separation/', 'cluster_id': '', 'h1': 'Legal Separation in Illinois', 'anchor': 'legal separation in Illinois'},
    {'keywords': ['divorce'], 'target': 'https://www.sterlinglawyers.com/illinois/divorce/', 'cluster_id': 'DIV', 'h1': 'Illinois Divorce Laws', 'anchor': 'Illinois divorce laws'},
]

def map_url(url):
    url_lower = url.lower()
    
    # Simple logic to extract city names dynamically from the slug
    # We strip "https://www.sterlinglawyers.com/illinois/blog/" to get the slug
    slug = url_lower.replace("https://www.sterlinglawyers.com/illinois/blog/", "").strip("/")
    
    # Common cities in IL we care about based on the URLs
    cities = ['evanston', 'hoffman-estates', 'naperville', 'schaumburg', 'arlington-heights', 'chicago', 'cook-county']
    city_prefix = ""
    for city in cities:
        if city in slug:
            if city == 'cook-county':
                city_prefix = "Cook County "
            else:
                city_prefix = city.replace('-', ' ').title() + " "
            break
            
    # Need to find the FIRST matching keywords list since some are more specific combinations (like property-division AND marital-property)
    # Wait, my logic was `any(kw in url_lower for kw in mapping['keywords'])`.
    # This means if I have 'child-custody' AND 'paternity', both keywords should be present.
    # Ah, `any()` means if ANY keyword is present. I should probably use `all()` for multiple keywords.
    # Actually, most of my mappings above only have one keyword anyway, but for 'child-custody', 'paternity', I'll use `all()`.
    
    for mapping in mappings:
        keywords = mapping['keywords']
        if all(kw in url_lower for kw in keywords):
            anchor = mapping['anchor']
            # Prepend city if appropriate
            if city_prefix and anchor.lower().startswith('illinois '):
                # Replace 'Illinois ' with 'City ' 
                # E.g. 'Illinois contested divorce' -> 'Evanston contested divorce'
                anchor = city_prefix + anchor[9:]
            elif city_prefix and anchor.lower().startswith('establishing ') and 'illinois' in anchor.lower():
                # E.g. establishing paternity for child custody in Illinois
                anchor = anchor.replace('in Illinois', f'in {city_prefix.strip()}')
            elif city_prefix and anchor.lower().startswith('finding '):
                 anchor = anchor + f' in {city_prefix.strip()}'
            elif city_prefix and 'illinois' in anchor.lower():
                 anchor = anchor.replace('illinois', city_prefix.strip(), 1)
            elif city_prefix:
                anchor = city_prefix + anchor.replace('Illinois ', '')
                
            return mapping['target'], mapping['cluster_id'], anchor
            
    # Default to Divorce if nothing else matches
    default_anchor = 'divorce laws'
    if city_prefix:
        default_anchor = city_prefix + default_anchor
    else:
        default_anchor = 'Illinois ' + default_anchor
        
    return 'https://www.sterlinglawyers.com/illinois/divorce/', 'DIV', default_anchor

def process_blogs():
    blogs = []
    with open(blogs_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if row and len(row) > 0 and row[0].strip():
                blogs.append(row[0].strip())
    
    date_added = datetime.now().strftime('%m/%d/%Y')  # commonly preferred MM/DD/YYYY format
    output_rows = []
    
    # Header mapping to example sheet
    header = ['Source URL', 'Target URL', 'Target Cluster ID', 'Link Type', 'Suggested Anchor Text', 'Placement Notes', 'Reason', 'Priority', 'Status', 'Assignee', 'Date Added', 'Date Completed', 'Notes']
    
    for blog in blogs:
        target_url, cluster_id, anchor = map_url(blog)
        
        row = [
            blog,
            target_url,
            cluster_id, # Can be blank for subservices
            'Contextual',
            anchor,
            'Add a contextual link near the first 25% of content and (if appropriate) a CTA near the end.',
            'Support pillar + route qualified users to conversion',
            'P1', # Arbitrarily setting to P1 standard
            'To Do',
            '', # Assignee
            date_added,
            '', # Date Completed
            'Verify whether a contextual link already exists; avoid duplicating nav/sidebar links only.'
        ]
        output_rows.append(row)
        
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(output_rows)
        
    print(f"Clustering complete. Processed {len(blogs)} blogs. Saved to: {output_csv}")

if __name__ == '__main__':
    process_blogs()
