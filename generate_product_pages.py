import csv
import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:image" content="{main_image}">
  <meta property="og:type" content="product">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="icon" href="2-logo-dn.png" type="image/png">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/css/styles.css?v=20260306c">
  
  <style>
    :root {{
      --cream:   #FAF7F2;
      --warm:    #F3EDE3;
      --sand:    #E8DDD0;
      --border:  #DDD4C6;
      --text:    #2C2420;
      --muted:   #7A6E66;
      --gold:    #B8892A;
      --gold-lt: #D4A843;
      --purple:  #6B4E8C;
      --green:   #2E7D52;
      --wa:      #25D366;
      --white:   #FFFFFF;
    }}
    body {{
      background: var(--cream);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      margin: 0; padding: 0;
    }}
    .site-header {{
      background: var(--white);
      border-bottom: 1px solid var(--border);
      padding: 15px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .site-header a {{ text-decoration: none; color: var(--text); font-weight: 500; }}
    .site-header .brand {{ display: flex; align-items: center; gap: 10px; font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; }}
    .site-header .brand img {{ width: 40px; height: 40px; }}
    .nav-links {{ display: flex; gap: 20px; }}
    
    .product-hero {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 50px;
      max-width: 1200px;
      margin: 60px auto;
      padding: 0 24px;
    }}
    .product-images {{
      background: var(--white);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
      border: 1px solid var(--border);
      text-align: center;
    }}
    .product-images img {{
      max-width: 100%;
      border-radius: 12px;
      object-fit: cover;
      aspect-ratio: 1/1;
    }}
    .image-thumbnails {{
      display: flex;
      gap: 10px;
      margin-top: 15px;
      justify-content: center;
    }}
    .image-thumbnails img {{
      width: 80px; height: 80px;
      border-radius: 8px;
      cursor: pointer;
      border: 2px solid transparent;
    }}
    .image-thumbnails img:hover {{ border-color: var(--gold); }}
    
    .product-info {{
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .badge {{
      display: inline-block;
      padding: 6px 14px;
      background: rgba(184,137,42,0.1);
      color: var(--gold);
      border-radius: 50px;
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 15px;
    }}
    .product-info h1 {{
      font-family: 'Playfair Display', serif;
      font-size: 3rem;
      margin: 0 0 15px 0;
      color: var(--text);
      line-height: 1.1;
    }}
    .short-desc {{
      font-size: 1.15rem;
      color: var(--muted);
      margin-bottom: 25px;
      line-height: 1.6;
    }}
    .price-wrap {{
      display: flex;
      align-items: center;
      gap: 15px;
      margin-bottom: 30px;
      padding-bottom: 30px;
      border-bottom: 1px solid var(--border);
    }}
    .price-now {{ font-size: 2.2rem; font-weight: 700; color: var(--text); }}
    .price-mrp {{ font-size: 1.2rem; color: var(--muted); text-decoration: line-through; }}
    .price-save {{ background: rgba(37,211,102,0.1); color: #18a34a; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 0.9rem; }}
    
    .btn-buy {{
      background: var(--wa);
      color: #fff;
      text-decoration: none;
      padding: 18px 30px;
      border-radius: 12px;
      font-size: 1.1rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.3s ease;
      box-shadow: 0 6px 20px rgba(37,211,102,0.3);
      width: 100%;
      margin-bottom: 20px;
    }}
    .btn-buy:hover {{ background: #18a34a; transform: translateY(-3px); }}
    
    .product-details {{
      max-width: 800px;
      margin: 0 auto 80px auto;
      padding: 40px;
      background: var(--white);
      border-radius: 20px;
      border: 1px solid var(--border);
      box-shadow: 0 10px 30px rgba(0,0,0,0.03);
    }}
    .product-details h2 {{
      font-family: 'Playfair Display', serif;
      font-size: 2rem;
      margin-bottom: 20px;
      color: var(--gold);
    }}
    .product-details p {{
      font-size: 1.05rem;
      line-height: 1.8;
      color: var(--muted);
      margin-bottom: 20px;
    }}
    
    /* Footer */
    footer {{
      background: var(--text);
      color: rgba(255,255,255,0.7);
      text-align: center;
      padding: 40px 24px;
    }}
    
    @media (max-width: 900px) {{
      .product-hero {{ grid-template-columns: 1fr; gap: 30px; margin: 40px auto; }}
      .product-info h1 {{ font-size: 2.2rem; }}
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <a class="brand" href="/">
      <img src="2-logo-dn.png" alt="Destini Numbers">
      <span>Destini Numbers</span>
    </a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="spiritual-store">Store</a>
    </div>
  </header>

  <main>
    <section class="product-hero">
      <div class="product-images">
        <img id="mainImage" src="{main_image}" alt="{img_alt}">
        {thumbnails_html}
      </div>
      <div class="product-info">
        <div>
          <span class="badge">{category}</span>
          <span class="badge" style="background: rgba(107,78,140,0.1); color: var(--purple); margin-left: 10px;">{combo_text}</span>
        </div>
        <h1>{h1_title}</h1>
        <p class="short-desc">{short_desc}</p>
        
        <div class="price-wrap">
          <span class="price-now">₹{sell_price}</span>
          <span class="price-mrp">₹{mrp}</span>
          <span class="price-save">Save ₹{saving}</span>
        </div>
        
        <a href="https://wa.me/917269031175?text=Hi%20Destini%20Numbers!%20I%20want%20to%20order%20{url_encoded_name}%20for%20%E2%82%B9{sell_price}.%20Please%20share%20details." class="btn-buy" target="_blank" rel="noopener">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          Buy on WhatsApp
        </a>
        
        <p style="font-size: 0.9rem; color: var(--muted); display: flex; align-items: center; gap: 8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Energetically Cleansed & Charged
        </p>
        <p style="font-size: 0.9rem; color: var(--muted); display: flex; align-items: center; gap: 8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg> Fast Delivery across India
        </p>
      </div>
    </section>

    <section class="product-details">
      <h2>About This Crystal</h2>
      <p>{long_desc}</p>
      <h2 style="margin-top: 40px;">How It Helps You</h2>
      <p>{impact_desc}</p>
    </section>
  </main>

  <footer>
    <p>Destini Numbers &copy; 2026. Vedic Numerology & Healing Crystals.</p>
    <p>By Diipeshh Barara · Lucknow, India</p>
  </footer>

  <script>
    function changeImage(src) {{
      document.getElementById('mainImage').src = src;
    }}
  </script>
</body>
</html>"""

import urllib.parse

def process_csv():
    with open('d:\\CODEX2025-2026\\june2026-destini\\products.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row['URL Slug'].strip()
            if not slug:
                continue
            
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

            # Thumbnails
            main_image = row['IMAGE LINKS 1'] if row.get('IMAGE LINKS 1') else row.get('Image Link', '')
            images = [main_image]
            if row.get('IMAGE LINKS 2'): images.append(row['IMAGE LINKS 2'])
            if row.get('IMAGE LINKS 3'): images.append(row['IMAGE LINKS 3'])
            
            thumbnails_html = ""
            if len(images) > 1:
                thumbnails_html = '<div class="image-thumbnails">'
                for img in images:
                    if img.strip():
                        thumbnails_html += f'<img src="{img.strip()}" alt="thumbnail" onclick="changeImage(\'{img.strip()}\')">'
                thumbnails_html += '</div>'
                
            # Url encode name for WA
            url_encoded_name = urllib.parse.quote(row['Original Name'])

            html = html_template.format(
                meta_title=row['Meta Title'],
                meta_description=row['Meta Description'],
                keywords=row['Top Keywords'],
                og_title=row['OG Title'],
                og_description=row['OG Description'],
                main_image=main_image,
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
            
            out_path = f"d:\\CODEX2025-2026\\june2026-destini\\{slug}.html"
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(html)
            print(f"Created {slug}.html")

if __name__ == '__main__':
    process_csv()
