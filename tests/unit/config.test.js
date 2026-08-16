/**
 * @vitest-environment jsdom
 */
import { beforeEach, describe, expect, it, vi } from 'vitest';

describe('js/config.js', () => {
  beforeEach(() => {
    vi.resetModules();
    delete window.SARA_API_BASE_URL;
    delete window.SARA_CONFIG;
    delete window.SARA_COUPONS;
  });

  it('defines API base URL, checkout config, and coupon codes', async () => {
    await import('../../frontend/js/config.js');

    expect(window.SARA_API_BASE_URL).toBe('');
    expect(window.SARA_CONFIG.TAX_RATE).toBe(0.18);
    expect(window.SARA_CONFIG.SHIPPING.FREE_THRESHOLD).toBe(3000);
    expect(window.SARA_COUPONS.SARA20).toBe(20);
    expect(window.SARA_COUPONS.WELCOME10).toBe(10);
  });

  it('does not overwrite a pre-set API base URL', async () => {
    window.SARA_API_BASE_URL = 'http://localhost:8000';
    await import('../../frontend/js/config.js');
    expect(window.SARA_API_BASE_URL).toBe('http://localhost:8000');
  });

  it('does not overwrite pre-set config values or coupon codes', async () => {
    window.SARA_CONFIG = { TAX_RATE: 0.10, SHIPPING: { FEE: 99, FREE_THRESHOLD: 999 } };
    window.SARA_COUPONS = { CUSTOM10: 10 };
    await import('../../frontend/js/config.js');
    expect(window.SARA_CONFIG.TAX_RATE).toBe(0.10);
    expect(window.SARA_CONFIG.SHIPPING.FREE_THRESHOLD).toBe(999);
    expect(window.SARA_COUPONS.CUSTOM10).toBe(10);
    expect(window.SARA_COUPONS.SARA20).toBeUndefined();
  });
});

describe('js/coupon-config.js', () => {
  beforeEach(() => {
    vi.resetModules();
    delete window.SARA_COUPONS;
  });

  it('exposes known coupon codes for the cart page', async () => {
    await import('../../frontend/js/coupon-config.js');
    expect(window.SARA_COUPONS.SARA20).toBe(20);
  });
});
