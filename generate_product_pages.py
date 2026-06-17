import csv
import os
import shutil
import urllib.parse
import re

# Slugs mapping for SEO optimization
slugs_map = {
    "amethyst-crystal-bracelet": "amethyst-crystal-bracelet",
    "black-tourmaline-crystal-bracelet": "black-tourmaline-crystal-bracelet",
    "rose-quartz-crystal-bracelet": "rose-quartz-crystal-bracelet",
    "tiger-s-eye-crystal-bracelet": "tiger-eye-crystal-bracelet",
    "green-aventurine-crystal-bracelet": "green-aventurine-crystal-bracelet",
    "pyrite-crystal-bracelet": "pyrite-money-magnet-bracelet",
    "clear-quartz-crystal-bracelet": "clear-quartz-crystal-bracelet",
    "citrine-crystal-bracelet": "citrine-success-crystal-bracelet",
    "selenite-crystal-bracelet": "selenite-cleansing-crystal-bracelet",
    "lapis-lazuli-crystal-bracelet": "lapis-lazuli-crystal-bracelet",
    "wealth-duo-crystal-bracelet": "aventurine-quartz-wealth-bracelet",
    "success-spirituality-crystal-bracelet": "citrine-rudraksha-success-bracelet",
    "self-love-trio-crystal-bracelet": "rose-quartz-amethyst-love-bracelet",
    "the-protective-shield-crystal-bracelet": "tourmaline-selenite-protection-bracelet",
    "focus-career-crystal-bracelet": "pyrite-tigers-eye-career-bracelet",
    "anti-anxiety-calm-crystal-bracelet": "amethyst-howlite-calm-bracelet",
    "evil-eye-protection-crystal-bracelet": "obsidian-hematite-protection-bracelet",
    "chakra-balance-crystal-bracelet": "7-chakra-lava-stone-bracelet",
    "communication-boost-crystal-bracelet": "lapis-amazonite-communication-bracelet",
    "grounding-energy-crystal-bracelet": "smoky-quartz-hematite-grounding-bracelet"
}

# Paths
base_dir = "d:\\CODEX2025-2026\\june2026-destini"
csv_path = os.path.join(base_dir, "products.csv")
product_dir = os.path.join(base_dir, "product")
store_html_path = os.path.join(base_dir, "spiritual-store.html")

# Create product folder if not exists
os.makedirs(product_dir, exist_ok=True)

# HTML Template for Single Product Pages
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="{keywords}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:image" content="{main_image}">
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="Destini Numbers">
  
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../2-logo-dn.png" type="image/png">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="../assets/css/styles.css?v=20260306c">
  
  <style>
    :root {{
      --ink: #0b1b2b;
      --ink-soft: #1c3144;
      --gold: #d4a74b;
      --gold-soft: #f1dbaf;
      --sand: #f7f1e7;
      --white: #ffffff;
      --muted: #5a6578;
      --green: #25d366;
    }}
    
    body {{
      background: radial-gradient(circle at 12% 8%, #fff3de 0, transparent 34%),
                  radial-gradient(circle at 88% 12%, #d8f6f2 0, transparent 28%),
                  linear-gradient(180deg, #fffdf8 0%, #f9f3e8 100%);
      color: var(--ink);
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }}

    .site-header {{
      background: rgba(11, 17, 41, 0.95);
      border-bottom: 1px solid rgba(212, 167, 75, 0.26);
      padding: 12px 24px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(10px);
    }}
    .header-wrap {{
      max-width: 1120px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .header-wrap a {{ text-decoration: none; color: #fff8e2; font-weight: 500; }}
    .header-wrap .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: 0.6px;
    }}
    .header-wrap .brand img {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #ffc043;
    }}
    .header-wrap .brand-title {{
      color: #ffc043;
    }}
    .nav-links {{ display: flex; gap: 20px; }}
    .nav-links a {{
      font-size: 0.93rem;
      color: rgba(255, 255, 255, 0.86);
      padding: 4px 0;
      transition: color 0.3s;
    }}
    .nav-links a:hover {{
      color: #ffcb5e;
    }}
    
    .product-hero {{
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 40px;
      max-width: 1120px;
      margin: 40px auto;
      padding: 0 24px;
    }}
    
    .product-images {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    
    .main-image-container {{
      background: var(--white);
      border-radius: var(--radius-lg, 22px);
      padding: 12px;
      box-shadow: 0 15px 40px rgba(11, 27, 43, 0.06);
      border: 1px solid rgba(11, 27, 43, 0.08);
      position: relative;
      aspect-ratio: 1/1;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    
    .main-image-container img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: var(--radius-md, 14px);
      transition: transform 0.5s ease;
    }}
    
    .main-image-container:hover img {{
      transform: scale(1.03);
    }}
    
    .image-thumbnails {{
      display: flex;
      gap: 12px;
      justify-content: center;
    }}
    
    .image-thumbnails img {{
      width: 90px;
      height: 90px;
      border-radius: var(--radius-sm, 10px);
      cursor: pointer;
      object-fit: cover;
      border: 2px solid transparent;
      background: var(--white);
      box-shadow: 0 4px 12px rgba(11, 27, 43, 0.04);
      transition: all 0.3s ease;
    }}
    
    .image-thumbnails img:hover,
    .image-thumbnails img.active {{
      border-color: var(--gold);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(212, 167, 75, 0.2);
    }}
    
    .product-info {{
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      padding: 10px 0;
    }}
    
    .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }}
    
    .badge {{
      display: inline-block;
      padding: 6px 14px;
      background: rgba(212, 167, 75, 0.1);
      color: var(--ink);
      border: 1px solid rgba(212, 167, 75, 0.25);
      border-radius: 50px;
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }}
    
    .badge-combo {{
      background: rgba(92, 59, 140, 0.08);
      color: #5c3b8c;
      border-color: rgba(92, 59, 140, 0.2);
    }}
    
    .product-info h1 {{
      font-family: 'Cinzel', serif;
      font-size: 2.2rem;
      margin: 0 0 10px 0;
      color: var(--ink);
      line-height: 1.25;
      font-weight: 700;
    }}
    
    .rating-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 18px;
      font-size: 0.9rem;
    }}
    
    .stars {{
      color: #ffb703;
      font-size: 1.1rem;
      letter-spacing: 1px;
    }}
    
    .verified-count {{
      color: var(--muted);
      font-weight: 500;
    }}
    
    .short-desc {{
      font-size: 1.05rem;
      color: var(--ink-soft);
      margin-bottom: 24px;
      line-height: 1.6;
    }}
    
    .price-card {{
      background: rgba(255, 255, 255, 0.8);
      border: 1px solid rgba(212, 167, 75, 0.2);
      border-radius: var(--radius-md, 14px);
      padding: 20px;
      margin-bottom: 28px;
      box-shadow: 0 8px 25px rgba(11, 27, 43, 0.03);
    }}
    
    .price-wrap {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 12px;
    }}
    
    .price-now {{
      font-size: 2.4rem;
      font-weight: 800;
      color: var(--ink);
      letter-spacing: -0.5px;
    }}
    
    .price-mrp {{
      font-size: 1.3rem;
      color: var(--muted);
      text-decoration: line-through;
    }}
    
    .price-save-badge {{
      background: rgba(31, 182, 170, 0.1);
      color: var(--aqua, #1fb6aa);
      padding: 6px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.85rem;
      border: 1px solid rgba(31, 182, 170, 0.2);
      margin-left: auto;
      align-self: center;
    }}
    
    .trust-bullets {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      font-size: 0.85rem;
      color: var(--muted);
      font-weight: 500;
    }}
    
    .trust-bullet {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    
    .trust-bullet svg {{
      color: var(--gold);
      flex-shrink: 0;
    }}
    
    .btn-buy {{
      background: #25d366;
      color: #fff;
      text-decoration: none;
      padding: 16px 28px;
      border-radius: var(--radius-sm, 10px);
      font-size: 1.1rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.3s ease;
      box-shadow: 0 8px 24px rgba(37, 211, 102, 0.3);
      width: 100%;
      margin-bottom: 14px;
      border: none;
      cursor: pointer;
      position: relative;
    }}
    
    .btn-buy:hover {{
      background: #20ba59;
      transform: translateY(-2px);
      box-shadow: 0 10px 28px rgba(37, 211, 102, 0.4);
    }}
    
    .btn-ask {{
      background: var(--white);
      color: var(--ink-soft);
      text-decoration: none;
      padding: 14px 28px;
      border-radius: var(--radius-sm, 10px);
      font-size: 0.95rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.3s ease;
      width: 100%;
      border: 1px solid rgba(11, 27, 43, 0.12);
    }}
    
    .btn-ask:hover {{
      background: rgba(212, 167, 75, 0.08);
      border-color: var(--gold);
      color: var(--gold);
    }}
    
    .details-section {{
      background: var(--white);
      border-radius: var(--radius-lg, 22px);
      border: 1px solid rgba(11, 27, 43, 0.08);
      box-shadow: 0 15px 40px rgba(11, 27, 43, 0.04);
      max-width: 1120px;
      margin: 0 auto 80px auto;
      padding: 40px;
      box-sizing: border-box;
    }}
    
    .details-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
    }}
    
    .details-col h2 {{
      font-family: 'Cinzel', serif;
      font-size: 1.6rem;
      color: var(--ink);
      margin-top: 0;
      margin-bottom: 20px;
      border-bottom: 2px solid var(--gold-soft);
      padding-bottom: 10px;
    }}
    
    .details-col p {{
      color: var(--muted);
      font-size: 1.02rem;
      line-height: 1.8;
      margin-bottom: 20px;
    }}
    
    /* Footer */
    footer {{
      background: #0b1129;
      color: rgba(255, 255, 255, 0.75);
      text-align: center;
      padding: 50px 24px;
      border-top: 1px solid rgba(212, 167, 75, 0.2);
    }}
    footer p {{ margin: 5px 0; font-size: 0.95rem; }}
    footer .brand-logo {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      font-family: 'Cinzel', serif;
      color: #ffc043;
      font-size: 1.4rem;
      font-weight: 700;
      margin-bottom: 15px;
    }}
    footer .brand-logo img {{
      width: 44px; height: 44px; border-radius: 50%; background: #ffc043;
    }}
    
    @media (max-width: 900px) {{
      .product-hero {{ grid-template-columns: 1fr; gap: 30px; margin: 20px auto; }}
      .product-info h1 {{ font-size: 1.8rem; }}
      .details-grid {{ grid-template-columns: 1fr; gap: 30px; }}
      .details-section {{ padding: 25px; margin-bottom: 40px; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-wrap">
      <a class="brand" href="../">
        <img src="../2-logo-dn.png" alt="Destini Numbers">
        <span class="brand-title">Destini Numbers</span>
      </a>
      <nav class="nav-links">
        <a href="../">Home</a>
        <a href="../numerology-astrology-services">Services</a>
        <a href="../spiritual-store">Store</a>
        <a href="../about-diipeshh-barara">About</a>
        <a href="../free-alignment-report">Tools</a>
        <a href="https://www.perplexity.ai/page/-.fgnfnoQTs2BynzZnbWSeA" target="_blank" rel="noopener">Blog</a>
        <a href="../contact-us">Contact</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="product-hero">
      <div class="product-images">
        <div class="main-image-container">
          <img id="mainImage" src="{main_image}" alt="{img_alt}">
        </div>
        {thumbnails_html}
      </div>
      <div class="product-info">
        <div class="badge-row">
          <span class="badge">{category}</span>
          <span class="badge badge-combo">{combo_text}</span>
        </div>
        <h1>{h1_title}</h1>
        
        <div class="rating-row">
          <span class="stars">★★★★★</span>
          <span class="verified-count">(48+ Verified Reviews)</span>
        </div>
        
        <p class="short-desc">{short_desc}</p>
        
        <div class="price-card">
          <div class="price-wrap">
            <span class="price-now">₹{sell_price}</span>
            <span class="price-mrp">₹{mrp}</span>
            <span class="price-save-badge">Save ₹{saving}</span>
          </div>
          <div class="trust-bullets">
            <div class="trust-bullet">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span>Vedic Suitability Verified</span>
            </div>
            <div class="trust-bullet">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span>100% Charged & Cleansed</span>
            </div>
          </div>
        </div>
        
        <a href="https://wa.me/917269031175?text=Hi%20Destini%20Numbers!%20I%20want%20to%20order%20{url_encoded_name}%20for%20%E2%82%B9{sell_price}.%20Please%20share%20details%20and%20suitability." class="btn-buy" target="_blank" rel="noopener">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          Buy on WhatsApp
        </a>
        
        <a href="https://wa.me/917269031175?text=Hi!%20I%20have%20a%20query%20about%20{url_encoded_name}." class="btn-ask" target="_blank" rel="noopener">
          Ask Astro-Numerologist Suitability
        </a>
      </div>
    </section>

    <section class="details-section">
      <div class="details-grid">
        <div class="details-col">
          <h2>About This Remedial Crystal</h2>
          <p>{long_desc}</p>
        </div>
        <div class="details-col">
          <h2>How It Helps Your Life Path</h2>
          <p>{impact_desc}</p>
          
          <div style="background: var(--sand); border-radius: var(--radius-sm, 10px); padding: 18px; border: 1px solid rgba(212, 167, 75, 0.2); margin-top: 25px;">
            <h4 style="margin: 0 0 8px 0; font-family: 'Cinzel', serif; color: var(--ink);">Vedic Cleansing Ritual</h4>
            <p style="margin: 0; font-size: 0.9rem; line-height: 1.5; color: var(--ink-soft);">Every crystal bracelet from Destini Numbers is purified using pure sandalwood incense and chanted upon with Vedic mantra before packaging. We cleanse all existing energies so the crystal aligns specifically to your chart.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="brand-logo">
      <img src="../2-logo-dn.png" alt="Destini Numbers Logo">
      <span>Destini Numbers</span>
    </div>
    <p>Vedic Numerology, Astrology consultations & Authentic Crystal Healing Remedies.</p>
    <p>By Diipeshh Barara · Lucknow, India</p>
    <p style="margin-top: 20px; font-size: 0.8rem; opacity: 0.65;">&copy; 2026 Destini Numbers. All rights reserved.</p>
  </footer>

  <script>
    function changeImage(src, element) {{
      document.getElementById('mainImage').src = src;
      document.querySelectorAll('.image-thumbnails img').forEach(function(img) {{
        img.classList.remove('active');
      }});
      element.classList.add('active');
    }}
  </script>
</body>
</html>"""

def clean_url_slug(slug_name):
    # Standardize slugs by converting to lowercase and replacing space/chars
    slug = slug_name.strip().lower()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'\-+', '-', slug)
    return slug

def clean_image_url(url):
    if not url:
        return ""
    return url.split('?')[0].strip()

def process_csv():
    # Read CSV records
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            original_name = row['Original Name'].strip()
            if not original_name:
                continue
            
            # Match using our optimized mapping
            matched_slug = None
            for key, val in slugs_map.items():
                if key in clean_url_slug(row['URL Slug']) or clean_url_slug(original_name) in key:
                    matched_slug = val
                    break
            
            if not matched_slug:
                matched_slug = clean_url_slug(row['URL Slug'])
            
            row['URL Slug'] = matched_slug
            rows.append(row)
            
    # Save optimized CSV back
    fieldnames = reader.fieldnames
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("CSV file updated with optimized slugs.")
    
    # Generate HTML pages
    product_cards_html = ""
    for idx, row in enumerate(rows, 1):
        slug = row['URL Slug']
        original_name = row['Original Name']
        
        # Calculate savings
        try:
            mrp = float(row['MRP'])
            sell = float(row['Offer Selling Price (INR)'])
            saving = int(mrp - sell)
            mrp_str = "{:,.0f}".format(mrp)
            sell_str = "{:,.0f}".format(sell)
        except:
            mrp_str = row['MRP']
            sell_str = row['Offer Selling Price (INR)']
            saving = "0"
 
        # Handle Images
        main_image_raw = row['IMAGE LINKS 1'].strip() if row.get('IMAGE LINKS 1') else row.get('Image Link', '').strip()
        main_image = clean_image_url(main_image_raw)
        
        # Build thumbnails
        images = []
        if main_image: images.append(main_image)
        if row.get('IMAGE LINKS 2') and row['IMAGE LINKS 2'].strip(): images.append(clean_image_url(row['IMAGE LINKS 2'].strip()))
        if row.get('IMAGE LINKS 3') and row['IMAGE LINKS 3'].strip(): images.append(clean_image_url(row['IMAGE LINKS 3'].strip()))
        
        thumbnails_html = ""
        if len(images) > 1:
            thumbnails_html = '<div class="image-thumbnails">'
            for i, img in enumerate(images):
                active_class = ' class="active"' if i == 0 else ''
                thumbnails_html += f'<img{active_class} src="{img}?tr=w-120,h-120,fo-auto" alt="thumbnail" onclick="changeImage(\'{img}?tr=w-600,h-600,fo-auto\', this)">'
            thumbnails_html += '</div>'
            
        # Optimize main image for detail page
        optimized_main_image = f"{main_image}?tr=w-600,h-600,fo-auto" if main_image else ""

        url_encoded_name = urllib.parse.quote(original_name)

        # Generate HTML
        html = html_template.format(
            meta_title=row['Meta Title'],
            meta_description=row['Meta Description'],
            keywords=row['Top Keywords'],
            og_title=row['OG Title'],
            og_description=row['OG Description'],
            main_image=optimized_main_image,
            category=row['Category'],
            combo_text=row['Combination'],
            h1_title=row['H1 Title'],
            short_desc=row['Short Description'],
            sell_price=sell_str,
            mrp=mrp_str,
            saving=saving,
            url_encoded_name=url_encoded_name,
            img_alt=row['Image Alt Text'],
            long_desc=row['Long Description'],
            impact_desc=row['Impact Description'],
            thumbnails_html=thumbnails_html
        )
        
        out_path = os.path.join(product_dir, f"{slug}.html")
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(html)
        print(f"Created product/{slug}.html")
        
        # Build card HTML for store grid
        # We append ?tr=w-400,h-400,fo-auto to make store thumbnail very lightweight and fix LCP!
        # Hover image uses Image 2 (or Image 1 if only 1 exists)
        hover_image = images[1] if len(images) > 1 else main_image
        
        percent_off = ""
        try:
            percent_off_val = int((saving / mrp) * 100)
            percent_off = f'<span class="badge badge-off">{percent_off_val}% OFF</span>'
        except:
            percent_off = f'<span class="badge badge-off">31% OFF</span>'
            
        product_cards_html += f"""
          <!-- {idx} {original_name} -->
          <article class="product-card" data-type="{row['Type']}">
            <div class="img-box">
              <div class="badges">
                <span class="badge badge-type-{'single' if row['Type'].lower() == 'single' else 'combo'}">{row['Type']}</span>
                {percent_off}
              </div>
              <div class="img-placeholder">
                <svg viewBox="0 0 56 56" fill="none"><path d="M28 4L52 28L28 52L4 28Z" stroke="#B8892A" stroke-width="1.5" fill="rgba(184,137,42,.1)"/><path d="M28 14L42 28L28 42L14 28Z" stroke="#B8892A" stroke-width="1" fill="rgba(184,137,42,.2)"/></svg>
                <span>{row['Main Label']}</span>
              </div>
              <a href="product/{slug}" style="display:block; width:100%; height:100%; position:absolute; z-index:4;">
                <img class="main-img" src="{main_image}?tr=w-400,h-400,fo-auto" alt="{row['Image Alt Text']}" loading="lazy">
                <img class="hover-img" src="{hover_image}?tr=w-400,h-400,fo-auto" alt="{original_name} India" loading="lazy">
              </a>
            </div>
            <div class="card-body">
              <div class="combo-tag">{row['Combination']}</div>
              <h3 class="card-title"><a href="product/{slug}">{row['H1 Title']}</a></h3>
              <p class="card-desc">{row['Short Description']}</p>
              <div class="price-row">
                <span class="price-now">₹{sell_str}</span>
                <span class="price-mrp">₹{mrp_str}</span>
                <span class="price-save">Save ₹{saving}</span>
              </div>
            </div>
            <div class="card-cta">
              <a class="btn-buy" href="https://wa.me/917269031175?text=Hi%20Destini%20Numbers!%20I%20want%20to%20order%20the%20{url_encoded_name}%20%E2%82%B9{sell_str}.%20Please%20share%20details." target="_blank" rel="noopener">💬 Buy on WhatsApp</a>
              <a class="btn-ask" href="https://wa.me/917269031175?text=Hi!%20Query%20about%20{url_encoded_name}." target="_blank" rel="noopener">Ask</a>
            </div>
          </article>
"""
    return product_cards_html

def update_store_html(cards_html):
    if not os.path.exists(store_html_path):
        print("spiritual-store.html not found in root.")
        return
        
    with open(store_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract static items (21 to 26) from the original file
    static_section = ""
    match = re.search(r'(<!-- 21 Rudraksha 1-14 Mukhi -->.*?)</article>\s*</div>', content, re.DOTALL)
    if match:
        static_section = match.group(1) + "</article>"
        print("Extracted static items from spiritual-store.html.")
    else:
        print("Warning: Could not extract static items from spiritual-store.html.")
        
    # Build complete store grid HTML
    complete_grid_html = "<div class=\"store-grid\" id=\"storeGrid\">\n" + cards_html + "\n" + static_section + "\n        </div>"
    
    # Replace content between <div class="store-grid" id="storeGrid"> and the matching closing </div>
    # Using regex to find the storeGrid container and replace it
    new_content = re.sub(
        r'<div class="store-grid" id="storeGrid">.*?</div>\s*</section>',
        complete_grid_html + "\n    </section>",
        content,
        flags=re.DOTALL
    )
    
    with open(store_html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("spiritual-store.html updated with new product cards.")

if __name__ == '__main__':
    cards_html = process_csv()
    update_store_html(cards_html)
