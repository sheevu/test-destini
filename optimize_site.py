import re
import os

base_dir = "d:\\CODEX2025-2026\\june2026-destini"

# Files to process in the root folder
html_files = [
    "index.html",
    "spiritual-store.html",
    "numerology-astrology-services.html",
    "about-diipeshh-barara.html",
    "contact-us.html",
    "free-alignment-report.html"
]

def fix_duplicate_links(content):
    # Pattern for navigation header duplicate blog link
    pattern_header = r'<a\s+<a\s+href="([^"]+)"([^>]*)>(Blog)</a>\s+href="([^"]+)"([^>]*)>([^<]+)</a>'
    
    def repl_header(m):
        url1, attrs1, text1, url2, attrs2, text2 = m.groups()
        indent = "        "
        return f'<a href="{url1}"{attrs1}>{text1}</a>\n{indent}<a href="{url2}"{attrs2}>{text2}</a>'
        
    content = re.sub(pattern_header, repl_header, content, flags=re.IGNORECASE)

    # Pattern for footer duplicate blog link
    pattern_footer = r'<a\s+<a\s+href="([^"]+)"([^>]*)>(Blog\s+Insights)</a>\s+href="([^"]+)"([^>]*)>([^<]+)</a>'
    
    def repl_footer(m):
        url1, attrs1, text1, url2, attrs2, text2 = m.groups()
        indent = "          "
        return f'<a href="{url1}"{attrs1}>{text1}</a>\n{indent}<a href="{url2}"{attrs2}>{text2}</a>'

    content = re.sub(pattern_footer, repl_footer, content, flags=re.IGNORECASE)
    
    # Catch any remaining single <a <a href=...
    pattern_catchall = r'<a\s+<a\s+href='
    if re.search(pattern_catchall, content):
        print("Warning: found residual <a <a href in content, fixing manually...")
        # General backup fix for free-alignment-report/contact-us which might have slightly different spacing
        content = re.sub(
            r'<a\s+<a\s+href="([^"]+)"\s+target="_blank"\s+rel="noopener">Blog</a>\s*href="([^"]+)"\s+data-nav="contact">Contact</a>',
            r'<a href="\1" target="_blank" rel="noopener">Blog</a>\n        <a href="\2" data-nav="contact">Contact</a>',
            content
        )
        content = re.sub(
            r'<a\s+<a\s+href="([^"]+)"\s+target="_blank"\s+rel="noopener">Blog\s+Insights</a>\s*href="([^"]+)">([^<]+)</a>',
            r'<a href="\1" target="_blank" rel="noopener">Blog Insights</a>\n          <a href="\2">\3</a>',
            content
        )
        
    return content

def inject_lcp_preloads(content):
    # Preloads to inject
    preloads = (
        '  <link rel="preload" href="2-logo-dn.png" as="image">\n'
        '  <link rel="preload" href="assets/css/styles.css?v=20260306b" as="style">\n'
    )
    
    # Check if preloads already present
    if 'rel="preload" href="2-logo-dn.png"' in content:
        return content
        
    # Inject right after <head> or after meta charset
    if "<head>" in content:
        content = content.replace("<head>", "<head>\n" + preloads, 1)
    return content

def add_video_poster(content, filename):
    if filename != "index.html":
        return content
        
    # Check if poster already added
    if 'poster="assets/img/hero-poster.jpg"' in content:
        return content
        
    content = content.replace(
        '<video class="hero-video" autoplay loop muted playsinline>',
        '<video class="hero-video" autoplay loop muted playsinline poster="assets/img/hero-poster.jpg">',
        1
    )
    return content

def main():
    for filename in html_files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename}: not found.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = fix_duplicate_links(content)
        content = inject_lcp_preloads(content)
        content = add_video_poster(content, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Optimized and fixed {filename}")

if __name__ == "__main__":
    main()
