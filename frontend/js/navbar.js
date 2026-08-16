// Global Header & Footer Interactive Controller for Sara E-Commerce

function getPathPrefix() {
  const path = window.location.pathname.replace(/\\/g, '/');
  if (path.includes('/pages/shop/') || path.includes('/pages/user/') || path.includes('/pages/info/') || path.includes('/pages/blog/')) {
    return '../../';
  }
  return '';
}

function updateActiveTab(activePage) {
  const navbarLinks = document.querySelectorAll('#navbar li a');
  navbarLinks.forEach(link => {
    const title = (link.getAttribute('title') || link.textContent || '').toLowerCase().trim();
    if (activePage && title.includes(activePage)) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });
}

function applyTheme(theme) {
  const html = document.documentElement;
  const body = document.body;
  html.setAttribute('data-theme', theme);
  if (body) {
    body.setAttribute('data-theme', theme);
    body.classList.toggle('dark', theme === 'dark');
  }
  localStorage.setItem('theme', theme);

  const themeIcon = document.getElementById('themeIcon');
  const themeIconMobile = document.getElementById('themeIconMobile');
  const iconClass = theme === 'dark' ? 'ri-sun-line' : 'ri-moon-line';
  if (themeIcon) themeIcon.className = iconClass;
  if (themeIconMobile) themeIconMobile.className = iconClass;

  const siteLogo = document.getElementById('siteLogo');
  if (siteLogo) {
    siteLogo.src = getPathPrefix() + 'images/newlogo.svg';
  }
}

function toggleTheme() {
  const currentTheme = localStorage.getItem('theme') || 'light';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(newTheme);
}

function loadHeader(activePage) {
  updateActiveTab(activePage);
  const savedTheme = localStorage.getItem('theme') || 'light';
  applyTheme(savedTheme);

  if (typeof window.updateWishlistCount === 'function') {
    window.updateWishlistCount();
  }
  if (typeof window.updateCartCount === 'function') {
    window.updateCartCount();
  }
}

function loadFooter() {
  const copyrightYearEl = document.getElementById('footer-copyright-year');
  if (copyrightYearEl) {
    copyrightYearEl.textContent = new Date().getFullYear();
  }
}

function loadNavbar(activePage) {
  loadHeader(activePage);
  loadFooter();
}

document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  applyTheme(savedTheme);
});

document.addEventListener('click', (e) => {
  if (!e.target) return;
  if (
    e.target.closest('#themeToggleDesktop') ||
    e.target.closest('#themeToggleMobile') ||
    e.target.closest('.theme-toggle')
  ) {
    e.preventDefault();
    toggleTheme();
  }
});

window.applyTheme = applyTheme;
window.toggleTheme = toggleTheme;
window.loadHeader = loadHeader;
window.loadFooter = loadFooter;
window.loadNavbar = loadNavbar;


// Global Header Search Bar Handler
document.addEventListener('DOMContentLoaded', () => {
  const searchBars = document.querySelectorAll('#searchBar, .header-search-bar');
  searchBars.forEach((bar) => {
    bar.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const query = bar.value.trim();
        if (query) {
          const isSubpage = window.location.pathname.includes('/pages/');
          const targetPage = isSubpage ? '../shop/shop.html' : 'pages/shop/shop.html';
          window.location.href = `${targetPage}?search=${encodeURIComponent(query)}`;
        }
      }
    });
  });
});


// Global Header Search Listener
function initGlobalHeaderSearch() {
  document.querySelectorAll('#headerSearchInput, #searchBar, .header-search-input').forEach((input) => {
    if (input.dataset.searchBound === 'true') return;
    input.dataset.searchBound = 'true';

    const executeSearch = () => {
      const query = input.value.trim();
      if (!query) return;
      const isSubpage = window.location.pathname.includes('/pages/');
      const targetPage = isSubpage ? '../shop/search.html' : 'pages/shop/search.html';
      window.location.href = `${targetPage}?search=${encodeURIComponent(query)}`;
    };

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        executeSearch();
      }
    });

    const parentWrap = input.closest('.header-search-wrap, .search-box, .search-container');
    if (parentWrap) {
      const btn = parentWrap.querySelector('button, #headerSearchBtn, #searchBtn');
      if (btn && btn.dataset.searchBound !== 'true') {
        btn.dataset.searchBound = 'true';
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          executeSearch();
        });
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', initGlobalHeaderSearch);
