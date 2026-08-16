/**
 * Shared frontend config loaded early by most HTML pages.
 * Values mirror the defaults also set in app.js so pages that do not
 * load app.js still get API base URL, tax/shipping, and coupon codes.
 */
(() => {
  if (typeof window.SARA_API_BASE_URL === 'undefined') {
    window.SARA_API_BASE_URL = '';
  }

  window.SARA_CONFIG = window.SARA_CONFIG || {
    TAX_RATE: 0.18,
    SHIPPING: {
      FEE: 150,
      FREE_THRESHOLD: 3000,
    },
    URGENCY_DISCOUNT_PCT: 0.05,
    GIFT_WRAP_CHARGE: 99,
    LOYALTY: {
      POINTS_PER_RUPEE: 10,
      DEFAULT_BALANCE: 150,
    },
  };

  window.SARA_COUPONS = window.SARA_COUPONS || {
    SARA20: 20,
    WELCOME10: 10,
  };
})();
