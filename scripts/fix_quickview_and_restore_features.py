import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

FEATURE_RESTORE_CSS = """
/* ============================================================
   RESTORE ORIGINAL FEATURE BOX BADGES (#feature .fe-box h6)
   ============================================================ */
#feature .fe-box:nth-child(1) h6 { background-color: #fddde4 !important; color: #111827 !important; }
#feature .fe-box:nth-child(2) h6 { background-color: #cdebbc !important; color: #111827 !important; }
#feature .fe-box:nth-child(3) h6 { background-color: #d1e8f2 !important; color: #111827 !important; }
#feature .fe-box:nth-child(4) h6 { background-color: #cdd4f6 !important; color: #111827 !important; }
#feature .fe-box:nth-child(5) h6 { background-color: #f6dbf6 !important; color: #111827 !important; }
#feature .fe-box:nth-child(6) h6 { background-color: #fff2e5 !important; color: #111827 !important; }

[data-theme="dark"] #feature .fe-box h6,
body.dark #feature .fe-box h6 {
    color: #111827 !important;
}

/* ============================================================
   BEAUTIFUL & USER-FRIENDLY QUICK VIEW OVERLAY & BUTTON
   ============================================================ */
.pro-img-wrap {
    position: relative !important;
    overflow: hidden !important;
}

.pro-quick-view-overlay {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background: rgba(0, 0, 0, 0.28) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 0 !important;
    visibility: hidden !important;
    transition: opacity 0.3s ease, visibility 0.3s ease !important;
    z-index: 10 !important;
    border-radius: 12px !important;
    pointer-events: none !important;
}

.pro-img-wrap:hover .pro-quick-view-overlay,
.pro:hover .pro-quick-view-overlay {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
}

.pro-quick-view-btn {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    padding: 8px 18px !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
    transition: all 0.25s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    outline: none !important;
    position: relative !important;
    z-index: 11 !important;
}

.pro-quick-view-btn:hover {
    background: #C483E6 !important;
    color: #ffffff !important;
    border-color: #C483E6 !important;
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(196, 131, 230, 0.45) !important;
}

[data-theme="dark"] .pro-quick-view-btn,
body.dark .pro-quick-view-btn {
    background: #1f1924 !important;
    color: #f8eef9 !important;
    border-color: #3b2b42 !important;
}

[data-theme="dark"] .pro-quick-view-btn:hover,
body.dark .pro-quick-view-btn:hover {
    background: #ED9AE9 !important;
    color: #111827 !important;
    border-color: #ED9AE9 !important;
}
"""

def update_stylesheets():
    css_files = [
        FRONTEND_DIR / "css" / "style.css",
        FRONTEND_DIR / "css" / "global.css",
        FRONTEND_DIR / "css" / "index.css",
        FRONTEND_DIR / "css" / "bundle.css",
        FRONTEND_DIR / "css" / "style.min.css"
    ]

    for file_path in css_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "RESTORE ORIGINAL FEATURE BOX BADGES" not in content:
                content += "\n" + FEATURE_RESTORE_CSS
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated stylesheets with Quick View redesign & Feature restore: {file_path.name}")

def update_app_js_quick_view_injector():
    app_js = FRONTEND_DIR / "js" / "app.js"
    if app_js.exists():
        with open(app_js, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        injector_code = """
  // Global Quick View Overlay Injector for Static Cards
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.pro').forEach((card) => {
      const imgWrap = card.querySelector('.pro-img-wrap');
      if (!imgWrap) return;
      if (imgWrap.querySelector('.pro-quick-view-overlay')) return;

      const qvOverlay = document.createElement('div');
      qvOverlay.className = 'pro-quick-view-overlay';
      const qvBtn = document.createElement('button');
      qvBtn.className = 'pro-quick-view-btn';
      qvBtn.type = 'button';
      qvBtn.innerHTML = '<i class="ri-eye-line"></i> Quick View';

      const nameElem = card.querySelector('.des h3, .des h5');
      const priceElem = card.querySelector('.des h4');
      const imgElem = card.querySelector('.pro-img-wrap img');
      const brandElem = card.querySelector('.pro-brand-row span');

      const name = nameElem ? nameElem.textContent.trim() : 'Product';
      const price = priceElem ? priceElem.textContent.trim() : '₹0';
      const img = imgElem ? imgElem.src : 'images/products/f1.jpg';
      const brand = brandElem ? brandElem.textContent.trim() : 'Sara';

      qvBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
        if (typeof window.openQuickViewModal === 'function') {
          window.openQuickViewModal({ name, price, brand, img, rating: 4.5 });
        }
      });

      qvOverlay.appendChild(qvBtn);
      imgWrap.appendChild(qvOverlay);
    });
  });
"""
        if "Global Quick View Overlay Injector for Static Cards" not in content:
            content += "\n" + injector_code
            with open(app_js, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated app.js with Quick View overlay injector.")

def main():
    update_stylesheets()
    update_app_js_quick_view_injector()
    print("Quick View button redesign and feature box restoration completed.")

if __name__ == "__main__":
    main()
