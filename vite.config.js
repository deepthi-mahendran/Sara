import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';

const frontendDir = resolve(__dirname, 'frontend');

// Helper to recursively discover all HTML files in frontend/ directory
function getHtmlFiles(dir, fileList = {}) {
  if (!fs.existsSync(dir)) return fileList;
  const files = fs.readdirSync(dir);
  files.forEach((file) => {
    const filePath = resolve(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      if (file !== 'node_modules' && file !== 'dist' && file !== '.git') {
        getHtmlFiles(filePath, fileList);
      }
    } else if (file.endsWith('.html')) {
      const relName = filePath
        .replace(frontendDir + '\\', '')
        .replace(frontendDir + '/', '')
        .replace('.html', '')
        .replace(/[\\/]/g, '_');
      fileList[relName] = filePath;
    }
  });
  return fileList;
}

const htmlFiles = getHtmlFiles(frontendDir);

export default defineConfig({
  root: 'frontend',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: htmlFiles
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    chunkSizeWarningLimit: 1000
  }
});
