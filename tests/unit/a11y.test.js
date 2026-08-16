import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';

const pagePaths = {
  'index.html': 'frontend/index.html',
  'contact.html': 'frontend/pages/info/contact.html',
  'shop.html': 'frontend/pages/shop/shop.html',
  'cart.html': 'frontend/pages/shop/cart.html',
  'about.html': 'frontend/pages/info/about.html'
};

describe('WCAG 2.1 AA Accessibility Tests', () => {
  const pages = Object.keys(pagePaths);

  pages.forEach(page => {
    describe(`Accessibility checks for ${page}`, () => {
      let html;

      beforeEach(() => {
        const filePath = path.resolve(process.cwd(), pagePaths[page]);
        html = fs.readFileSync(filePath, 'utf8');
      });

      it('should contain a skip to main content link', () => {
        expect(html).toContain('class="skip-link"');
        expect(html).toContain('href="#main-content"');
      });

      it('should contain a main landmark container with id="main-content"', () => {
        expect(html).toContain('id="main-content"');
      });

      it('should ensure cart icon has accessible label', () => {
        expect(html).toMatch(/aria-label=["'](Shopping cart|Cart)["']/i);
      });
    });
  });

  describe('Contact page form accessibility', () => {
    let contactHtml;

    beforeEach(() => {
      const filePath = path.resolve(process.cwd(), 'frontend/pages/info/contact.html');
      contactHtml = fs.readFileSync(filePath, 'utf8');
    });

    it('should have labels associated with form inputs', () => {
      expect(contactHtml).toContain('<label for="name">');
      expect(contactHtml).toContain('<label for="email">');
      expect(contactHtml).toContain('<label for="message">');
    });
  });
});
