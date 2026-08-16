import os

FRONTEND_DIR = r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend"

CSS_BADGE_RULES = """
/* ============================================================
   CART & WISHLIST BADGE BUBBLE STYLING
   ============================================================ */
#navbar li.nav-icon a,
.mobile a {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#navbar .cart-count,
#navbar .wishlist-count,
.mobile .cart-count,
.mobile .wishlist-count {
    position: absolute !important;
    top: -5px !important;
    right: -9px !important;
    background-color: #ED9AE9 !important;
    color: #111827 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    min-width: 18px !important;
    height: 18px !important;
    padding: 0 4px !important;
    border-radius: 50% !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
    z-index: 10 !important;
    pointer-events: none !important;
}

/* Hide badge bubble completely when empty (0 items) or hidden class is present */
.cart-count.hidden,
.wishlist-count.hidden,
.cart-count:empty,
.wishlist-count:empty {
    display: none !important;
}
"""

def apply_badge_css():
    css_files = [
        os.path.join(FRONTEND_DIR, "css", "style.css"),
        os.path.join(FRONTEND_DIR, "css", "global.css")
    ]
    for css_path in css_files:
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "CART & WISHLIST BADGE BUBBLE STYLING" not in content:
                content += "\n" + CSS_BADGE_RULES
                with open(css_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Added cart & wishlist badge CSS to: {os.path.basename(css_path)}")
            else:
                print(f"Badge CSS already in: {os.path.basename(css_path)}")

if __name__ == "__main__":
    apply_badge_css()
