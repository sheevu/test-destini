import os
import glob
import re

root_dir = os.path.dirname(os.path.abspath(__file__))

errors = []
successes = []

def check(condition, message):
    if condition:
        successes.append(message)
    else:
        errors.append(message)

def verify_site():
    print("=== STARTING SITE INTEGRITY VERIFICATION ===\n")
    
    # 1. Check folder existence
    product_dir = os.path.join(root_dir, "product")
    check(os.path.isdir(product_dir), f"Product directory exists at {product_dir}")
    
    # 2. Check 20 product files exist
    product_files = glob.glob(os.path.join(product_dir, "*.html"))
    check(len(product_files) == 20, f"Found exactly 20 product detail HTML files (Found: {len(product_files)})")
    
    # 3. Check for duplicate anchors <a <a
    duplicate_anchors_found = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                try:
                    content = open(path, encoding='utf-8').read()
                    if '<a <a' in content:
                        duplicate_anchors_found.append(path)
                except Exception as e:
                    print(f"Error reading {path}: {e}")
                    
    check(len(duplicate_anchors_found) == 0, f"No duplicate anchor tags (<a <a) found. (Errors in: {duplicate_anchors_found})")
    
    # 4. Check for double query parameters in URLs (e.g., ?updatedAt=...?tr=...)
    double_q_found = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                try:
                    content = open(path, encoding='utf-8').read()
                    # Check for pattern of double query parameter separators like ?...?...
                    # or url parameters that contain double question marks
                    matches = re.findall(r'src="[^"]*\?[^"]*\?[^"]*"', content)
                    if matches:
                        double_q_found.append((path, matches))
                except Exception as e:
                    print(f"Error reading {path}: {e}")
                    
    check(len(double_q_found) == 0, f"No double query parameter image URLs found. (Errors: {double_q_found})")

    # 5. Check preloads in root HTML files
    root_htmls = glob.glob(os.path.join(root_dir, "*.html"))
    preloads_missing = []
    for path in root_htmls:
        try:
            content = open(path, encoding='utf-8').read()
            if 'href="2-logo-dn.png" as="image"' not in content:
                preloads_missing.append(os.path.basename(path))
        except Exception as e:
            print(f"Error reading {path}: {e}")
            
    check(len(preloads_missing) == 0, f"All root HTML files contain logo preloads. (Missing in: {preloads_missing})")

    # 6. Check video poster image
    poster_path = os.path.join(root_dir, "assets", "img", "hero-poster.jpg")
    check(os.path.isfile(poster_path), f"Video poster exists at {poster_path}")
    if os.path.isfile(poster_path):
        size = os.path.getsize(poster_path)
        check(size > 5000, f"Video poster size is valid: {size/1024:.1f} KB")

    # 7. Check compressed founder portrait
    founder_webp_path = os.path.join(root_dir, "assets", "img", "main-image-dipesh-sir.webp")
    check(os.path.isfile(founder_webp_path), f"Founder portrait WebP exists at {founder_webp_path}")
    if os.path.isfile(founder_webp_path):
        size = os.path.getsize(founder_webp_path)
        check(size < 200 * 1024, f"Founder portrait size is under 200KB: {size/1024:.1f} KB")
        
    # 8. Check that references in HTML to the founder's image point to the webp
    webp_ref_missing = []
    for path in root_htmls:
        if "about-diipeshh-barara.html" in path:
            content = open(path, encoding='utf-8').read()
            if "main-image-dipesh-sir.webp" not in content:
                webp_ref_missing.append(os.path.basename(path))
                
    check(len(webp_ref_missing) == 0, f"about-diipeshh-barara.html references the optimized webp portrait. (Missing in: {webp_ref_missing})")

    # Summary
    print("\n--- RESULTS ---")
    print(f"Passes: {len(successes)}")
    print(f"Failures: {len(errors)}")
    
    if errors:
        print("\nERRORS DETECTED:")
        for err in errors:
            print(f"[-] {err}")
        exit(1)
    else:
        print("\n[+] ALL CHECKS PASSED SUCCESSFULLY!")
        exit(0)

if __name__ == "__main__":
    verify_site()
