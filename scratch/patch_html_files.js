const fs = require('fs');
const path = require('path');

const basePath = 'd:/CODEX2025-2026/june2026-destini';
const files = [
  'index.html',
  'about-diipeshh-barara.html',
  'numerology-astrology-services.html',
  'spiritual-store.html',
  'free-alignment-report.html',
  'contact-us.html',
  '404.html'
];

const filledCallIcon = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.045 15.045 0 0 1-6.59-6.59l2.2-2.2c.28-.28.36-.67.25-1.02A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>';

const filledFooterItems = `          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.045 15.045 0 0 1-6.59-6.59l2.2-2.2c.28-.28.36-.67.25-1.02A11.36 11.36 0 0 1 8.5 4c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.5c0-.55-.45-1-1-1z"/></svg>
            <a href="tel:+917269031175">+91 72690 31175</a>
          </div>
          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
            <a href="mailto:destininumbers37@gmail.com">destininumbers37@gmail.com</a>
          </div>
          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
            <span>Lucknow, Uttar Pradesh, India</span>
          </div>`;

files.forEach(file => {
  const filePath = path.join(basePath, file);
  if (!fs.existsSync(filePath)) {
    console.log(`Skipping: ${file} (does not exist)`);
    return;
  }

  let content = fs.readFileSync(filePath, 'utf8');
  let original = content;

  // 1. Replace preload stylesheets with standard stylesheets
  content = content.replace(
    /<link rel="preload" href="assets\/css\/fonts\.css\?v=20260306b" as="style" onload="this\.onload=null;this\.rel='stylesheet'">\s*<link rel="preload" href="assets\/css\/styles\.css\?v=20260306b" as="style" onload="this\.onload=null;this\.rel='stylesheet'">\s*<noscript>\s*<link rel="stylesheet" href="assets\/css\/fonts\.css\?v=20260306b">\s*<link rel="stylesheet" href="assets\/css\/styles\.css\?v=20260306b">\s*<\/noscript>/gi,
    '<link rel="stylesheet" href="assets/css/fonts.css?v=20260306b">\n  <link rel="stylesheet" href="assets/css/styles.css?v=20260306b">'
  );

  // Fallback if there is slightly different whitespace or spacing
  content = content.replace(
    /<link rel="preload" href="assets\/css\/fonts\.css\?v=20260306b" as="style" onload="this\.onload=null;this\.rel='stylesheet'">/gi,
    '<link rel="stylesheet" href="assets/css/fonts.css?v=20260306b">'
  );
  content = content.replace(
    /<link rel="preload" href="assets\/css\/styles\.css\?v=20260306b" as="style" onload="this\.onload=null;this\.rel='stylesheet'">/gi,
    '<link rel="stylesheet" href="assets/css/styles.css?v=20260306b">'
  );
  // Remove noscript block if it remains
  content = content.replace(
    /<noscript>\s*<link rel="stylesheet" href="assets\/css\/fonts\.css\?v=20260306b">\s*<link rel="stylesheet" href="assets\/css\/styles\.css\?v=20260306b">\s*<\/noscript>/gi,
    ''
  );

  // In 404.html, replace connection and custom fonts with standard ones
  if (file === '404.html') {
    content = content.replace(
      /<link rel="preconnect" href="https:\/\/fonts\.googleapis\.com">[\s\S]*?<link rel="stylesheet" href="assets\/css\/styles\.css">/gi,
      '<link rel="stylesheet" href="assets/css/fonts.css?v=20260306b">\n  <link rel="stylesheet" href="assets/css/styles.css?v=20260306b">'
    );
  }

  // 2. Remove reveal classes from hero elements
  // Target class="hero-copy surface reveal"
  content = content.replace(/class="hero-copy surface reveal"/g, 'class="hero-copy surface"');
  // Target class="hero-side hero-orbit surface reveal"
  content = content.replace(/class="hero-side hero-orbit surface reveal"/g, 'class="hero-side hero-orbit surface"');
  // Target class="hero-side surface reveal"
  content = content.replace(/class="hero-side surface reveal"/g, 'class="hero-side surface"');

  // 3. Replace the Call SVG in the sticky social bar
  // The originalCallSVG can be found by looking for class="social-icon call" and its nested svg
  // Let's replace the call svg inside class="social-icon call"
  const callIconPattern = /<a href="tel:\+917269031175" class="social-icon call" aria-label="Call Phone">\s*<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">[\s\S]*?<\/svg>\s*<\/a>/gi;
  content = content.replace(
    callIconPattern,
    `<a href="tel:+917269031175" class="social-icon call" aria-label="Call Phone">\n      ${filledCallIcon}\n    </a>`
  );

  // 4. Replace footer contact items
  const footerContactPattern = /<div class="footer-contact-info">[\s\S]*?<\/div>\s*<\/div>/i;
  content = content.replace(
    footerContactPattern,
    `<div class="footer-contact-info">\n${filledFooterItems}\n        </div>\n      </div>`
  );

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Successfully patched: ${file}`);
  } else {
    console.log(`No changes needed or matched in: ${file}`);
  }
});
console.log('HTML patching completed!');
