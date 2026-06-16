const fs = require('fs');
const path = require('path');

const rootDir = 'd:/CODEX2025-2026/june2026-destini';
const distDirs = [
  path.join(rootDir, 'dist-hostinger'),
  path.join(rootDir, 'dist-hostinger-verify')
];

// List of files to copy directly
const filesToCopy = [
  '.htaccess',
  'index.html',
  'about-diipeshh-barara.html',
  'numerology-astrology-services.html',
  'spiritual-store.html',
  'free-alignment-report.html',
  'contact-us.html',
  '404.html',
  'robots.txt',
  'sitemap.xml',
  'hero-section.mp4',
  '2-logo-dn.png',
  'favicon.ico'
];

// Helper to recursively copy directories
function copyDirSync(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      // Exclude git and dist folders
      if (entry.name === '.git' || entry.name.startsWith('dist-')) continue;
      copyDirSync(srcPath, destPath);
    } else {
      // Exclude private credentials text file, docx, zip, log files, scripts, mp4 from images etc.
      if (entry.name.endsWith('.zip') || entry.name.endsWith('.txt') || entry.name.endsWith('.docx') || entry.name.endsWith('.md')) {
        continue;
      }
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Clean and Sync for each dist directory
distDirs.forEach(distDir => {
  console.log(`Syncing ${distDir}...`);
  
  if (fs.existsSync(distDir)) {
    // Delete old HTML files that are no longer used
    const oldFiles = ['about.html', 'contact.html', 'services.html', 'store.html', 'tools.html'];
    oldFiles.forEach(oldFile => {
      const p = path.join(distDir, oldFile);
      if (fs.existsSync(p)) {
        fs.unlinkSync(p);
        console.log(`Deleted old file ${oldFile} from ${path.basename(distDir)}`);
      }
    });
  } else {
    fs.mkdirSync(distDir, { recursive: true });
  }

  // Copy root files
  filesToCopy.forEach(file => {
    const srcPath = path.join(rootDir, file);
    const destPath = path.join(distDir, file);
    if (fs.existsSync(srcPath)) {
      fs.copyFileSync(srcPath, destPath);
    } else {
      console.warn(`Warning: Source file ${file} does not exist.`);
    }
  });

  // Copy assets folder recursively
  const srcAssets = path.join(rootDir, 'assets');
  const destAssets = path.join(distDir, 'assets');
  if (fs.existsSync(srcAssets)) {
    copyDirSync(srcAssets, destAssets);
  }
});

console.log('Dist folders successfully synced!');
