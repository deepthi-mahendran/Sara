/**
 * Sanitize user input strings to prevent XSS payloads and HTML injection.
 * Escapes common HTML special characters and filters dangerous attributes.
 */
export function sanitizeHTML(input) {
  if (typeof input !== 'string') {
    return input;
  }

  // Strip inline event handlers and scripting protocols
  let clean = input
    .replace(/on\w+\s*=/gi, '')
    .replace(/javascript\s*:/gi, '')
    .replace(/data\s*:/gi, '');

  // Escape HTML special characters
  return clean
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

export function sanitizeDOMNode(element) {
  if (!element || typeof element.querySelectorAll !== 'function') return;
  const scriptTags = element.querySelectorAll('script, iframe, object, embed');
  scriptTags.forEach((tag) => tag.remove());
}

if (typeof window !== 'undefined') {
  window.sanitizeHTML = sanitizeHTML;
}
