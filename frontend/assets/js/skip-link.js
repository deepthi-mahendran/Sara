/**
 * Accessibility Skip Link Handler
 * Injects a skip to main content link for keyboard navigation users.
 */
function initSkipLink() {
  if (document.querySelector('a.skip-to-content-btn')) return;

  const skipLink = document.createElement('a');
  skipLink.className = 'skip-to-content-btn';
  skipLink.href = '#main-content';
  skipLink.textContent = 'Skip to main content';
  skipLink.style.position = 'fixed';
  skipLink.style.top = '-100px';
  skipLink.style.left = '20px';
  skipLink.style.zIndex = '9999';
  skipLink.style.padding = '8px 16px';
  skipLink.style.backgroundColor = '#000';
  skipLink.style.color = '#fff';

  skipLink.addEventListener('focus', () => {
    skipLink.style.top = '20px';
  });

  skipLink.addEventListener('blur', () => {
    skipLink.style.top = '-100px';
  });

  skipLink.addEventListener('click', (e) => {
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
      if (!mainContent.hasAttribute('tabindex')) {
        mainContent.setAttribute('tabindex', '-1');
      }
      mainContent.focus();
    }
  });

  document.body.insertBefore(skipLink, document.body.firstChild);
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSkipLink);
  } else {
    initSkipLink();
  }
}
