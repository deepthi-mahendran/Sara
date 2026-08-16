/**
 * Supabase Client Configuration & Auth Helper for Sara E-Commerce
 * Initializes Supabase JS SDK and exposes global supabaseClient.
 */
(() => {
  'use strict';

  const supabaseUrl =
    (window.SARA_CONFIG && window.SARA_CONFIG.SUPABASE_URL) ||
    window.SUPABASE_URL ||
    'https://xyzcompany.supabase.co';

  const supabaseAnonKey =
    (window.SARA_CONFIG && window.SARA_CONFIG.SUPABASE_ANON_KEY) ||
    window.SUPABASE_ANON_KEY ||
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_key';

  if (
    typeof window.supabase !== 'undefined' &&
    typeof window.supabase.createClient === 'function' &&
    supabaseUrl &&
    supabaseAnonKey
  ) {
    try {
      window.supabaseClient = window.supabase.createClient(
        supabaseUrl,
        supabaseAnonKey
      );
    } catch (err) {
      console.warn('Failed to initialize Supabase client:', err);
    }
  }
})();
