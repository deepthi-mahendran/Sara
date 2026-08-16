import { createRequire } from 'node:module';
import { beforeAll, describe, expect, it, vi } from 'vitest';

beforeAll(() => {
  globalThis.self = globalThis;
  globalThis.self.addEventListener = vi.fn();
  globalThis.self.skipWaiting = vi.fn();
  globalThis.self.clients = { claim: vi.fn() };
  globalThis.self.location = { origin: 'https://sara.example' };
});

const require = createRequire(import.meta.url);
const {
  isApiRequest,
  isNavigationRequest,
  isStaticAsset,
  shouldBypassCache,
  CACHE_NAME,
} = require('../../frontend/service-worker.js');

describe('service-worker cache strategy', () => {
  it('bumps cache version past v1', () => {
    expect(CACHE_NAME).not.toBe('sara-cache-v1');
  });

  it('treats /api paths as network-only', () => {
    const url = new URL('https://sara.example/api/products/');
    expect(isApiRequest(url)).toBe(true);
    expect(
      shouldBypassCache({ mode: 'cors', headers: new Headers() }, url),
    ).toBe(true);
  });

  it('treats navigations as network-first', () => {
    const url = new URL('https://sara.example/shop.html');
    expect(
      isNavigationRequest({
        mode: 'navigate',
        headers: new Headers({ accept: 'text/html' }),
      }),
    ).toBe(true);
    expect(
      shouldBypassCache(
        { mode: 'navigate', headers: new Headers({ accept: 'text/html' }) },
        url,
      ),
    ).toBe(true);
  });

  it('allows cache-first for static assets only', () => {
    expect(isStaticAsset(new URL('https://sara.example/style.css'))).toBe(true);
    expect(isStaticAsset(new URL('https://sara.example/api/orders'))).toBe(false);
  });

  describe('isStaticAsset classification', () => {
    it('classifies all supported static extensions as assets', () => {
      const extensions = [
        '.css',
        '.js',
        '.png',
        '.jpg',
        '.jpeg',
        '.webp',
        '.gif',
        '.svg',
        '.ico',
        '.woff',
        '.woff2',
      ];
      extensions.forEach((ext) => {
        expect(
          isStaticAsset(new URL('https://sara.example/bundle' + ext)),
        ).toBe(true);
      });
    });

    it('classifies dynamic paths as non-assets', () => {
      expect(isStaticAsset(new URL('https://sara.example/api/orders'))).toBe(
        false,
      );
      expect(
        isStaticAsset(new URL('https://sara.example/admin/dashboard')),
      ).toBe(false);
      expect(isStaticAsset(new URL('https://sara.example/shop'))).toBe(false);
      expect(
        isStaticAsset(new URL('https://sara.example/index.html')),
      ).toBe(false);
    });

    it('handles URLs with query strings on static assets', () => {
      expect(
        isStaticAsset(
          new URL('https://sara.example/bundle.js?v=1.2.3'),
        ),
      ).toBe(true);
      expect(
        isStaticAsset(
          new URL('https://sara.example/image.png?width=300&height=200'),
        ),
      ).toBe(true);
    });
  });
});
