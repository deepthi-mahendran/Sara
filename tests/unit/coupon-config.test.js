import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('coupon-config.js — window.SARA_COUPONS initialization', () => {
  beforeEach(() => {
    delete window.SARA_COUPONS;
  });

  afterEach(() => {
    // Global teardown
  });

  it('initializes window.SARA_COUPONS with SARA20 and WELCOME10', async () => {
    await import('../../frontend/js/coupon-config.js');
    expect(window.SARA_COUPONS).toBeDefined();
    expect(window.SARA_COUPONS.SARA20).toBe(20);
    expect(window.SARA_COUPONS.WELCOME10).toBe(10);
  });

  it('does not overwrite an existing SARA_COUPONS object', async () => {
    window.SARA_COUPONS = { CUSTOM50: 50 };
    await import('../../frontend/js/coupon-config.js');
    expect(window.SARA_COUPONS.CUSTOM50).toBe(50);
  });
});
