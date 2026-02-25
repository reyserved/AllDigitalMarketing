import os
import re
import csv
import argparse
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, unquote

def find_files(directory, extensions):
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                matched_files.append(os.path.join(root, file))
    return matched_files

def extract_links_from_html(file_path):
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                links.append({'url': a_tag['href'], 'line': getattr(a_tag, 'sourceline', 'N/A')})
            for img_tag in soup.find_all('img', src=True):
                links.append({'url': img_tag['src'], 'line': getattr(img_tag, 'sourceline', 'N/A')})
    except Exception as e:
        print(f"Error reading HTML file {file_path}: {e}")
    return links

def extract_links_from_md(file_path):
    links = []
    # Match markdown links: [text](url) and images: ![text](url)
    md_link_pattern = re.compile(r'\]\(([^)]+)\)')
    # Match basic href and src inside html tags
    html_link_pattern = re.compile(r'(?:href|src)=[\'"]([^\'"]+)[\'"]')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                # Check for standard markdown links/images
                for match in md_link_pattern.findall(line):
                    links.append({'url': match.strip(), 'line': i + 1})
                # Check for nested HTML links/images
                for match in html_link_pattern.findall(line):
                    links.append({'url': match.strip(), 'line': i + 1})
    except Exception as e:
         print(f"Error reading MD file {file_path}: {e}")
    return links

def check_url(url, base_dir, current_file):
    # Ignore fragment-only links, mailto, tel
    if not url or url.startswith('#') or url.startswith('mailto:') or url.startswith('tel:'):
        return None
    
    parsed = urlparse(url)
    
    # External link
    if parsed.scheme in ('http', 'https'):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
            }
            # Many sites block standard requests or HEAD requests. 
            # Give a timeout of 10s.
            resp = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            if resp.status_code >= 400 and resp.status_code != 405:
                # Retry with GET if HEAD fails or gives an error (some block HEAD)
                resp_get = requests.get(url, headers=headers, stream=True, timeout=10)
                if resp_get.status_code >= 400:
                    return f"HTTP {resp_get.status_code}"
            elif resp.status_code == 405: # Method Not Allowed
                resp_get = requests.get(url, headers=headers, stream=True, timeout=10)
                if resp_get.status_code >= 400:
                    return f"HTTP {resp_get.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error: {type(e).__name__}"
    else:
        # Internal file link
        path = parsed.path
        if not path:
            return None
            
        local_path = unquote(path)
        
        # Determine target file path based on whether it's absolute (to base_dir) or relative
        if local_path.startswith('/'):
            target_path = os.path.join(base_dir, local_path.lstrip('/'))
        else:
            target_path = os.path.join(os.path.dirname(current_file), local_path)
            
        if not os.path.exists(target_path):
            return "Local file not found"
            
    return None # URL is OK

def process_file(file_path, base_dir):
    broken_links = []
    
    if file_path.endswith('.html'):
        links = extract_links_from_html(file_path)
    elif file_path.endswith('.md'):
        links = extract_links_from_md(file_path)
    else:
        links = []
        
    for link_info in links:
        url = link_info['url']
        error = check_url(url, base_dir, file_path)
        if error is not None:
            broken_links.append({
                'file': os.path.relpath(file_path, base_dir),
                'line': link_info['line'],
                'url': url,
                'error': error
            })
            
    return broken_links

def main():
    parser = argparse.ArgumentParser(description="Check broken links in Markdown and HTML files.")
    parser.add_argument('--dir', default='.', help="Directory to scan (default: current directory)")
    parser.add_argument('--output', default='broken_links_report.csv', help="Output CSV file path")
    parser.add_argument('--max-workers', type=int, default=20, help="Max concurrent requests (default: 20)")
    
    args = parser.parse_args()
    base_dir = os.path.abspath(args.dir)
    
    print(f"Scanning '{base_dir}' for .md and .html files...")
    files = find_files(base_dir, ['.md', '.html'])
    print(f"Found {len(files)} files to process.")
    
    all_broken_links = []
    
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_file = {executor.submit(process_file, f, base_dir): f for f in files}
        
        processed_count = 0
        for future in as_completed(future_to_file):
            broken = future.result()
            if broken:
                all_broken_links.extend(broken)
                
            processed_count += 1
            if processed_count % 10 == 0:
                print(f"Processed {processed_count}/{len(files)} files...")
                
    if all_broken_links:
        print(f"\nFound {len(all_broken_links)} broken links. Writing to {args.output}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
        with open(args.output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['file', 'line', 'url', 'error'])
            writer.writeheader()
            for row in all_broken_links:
                writer.writerow(row)
        print("Done!")
    else:
        print("\nGreat job! No broken links found.")

if __name__ == '__main__':
    main()
