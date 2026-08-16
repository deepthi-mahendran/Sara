import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def fix_wishlist_check_in_js():
    js_files = [
        FRONTEND_DIR / "js" / "app.js",
        FRONTEND_DIR / "js" / "app.min.js",
        FRONTEND_DIR / "js" / "products.js"
    ]
    for file_path in js_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Replace strict href="wishlist.html" with contains check href*="wishlist.html"
            new_content = content.replace("!navbar.querySelector('a[href=\"wishlist.html\"]')", "!navbar.querySelector('a[href*=\"wishlist.html\"]')")
            new_content = new_content.replace('!navbar.querySelector("a[href=\\"wishlist.html\\"]")', '!navbar.querySelector("a[href*=\\"wishlist.html\\"]")')
            new_content = new_content.replace('a[href="wishlist.html"]', 'a[href*="wishlist.html"]')
            new_content = new_content.replace('a[href=\\"wishlist.html\\"]', 'a[href*=\\"wishlist.html\\"]')

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed wishlist selector check in: {file_path.name}")

def update_html_cart_and_wishlist():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Fix cart count spans to default to hidden 0 so no flicker occurs
                new_content = re.sub(
                    r'<span class="cart-count"[^>]*id="desktopCartCount"[^>]*>.*?</span>',
                    '<span class="cart-count hidden" id="desktopCartCount">0</span>',
                    content
                )
                new_content = re.sub(
                    r'<span class="cart-count"[^>]*id="mobileCartCount"[^>]*>.*?</span>',
                    '<span class="cart-count hidden" id="mobileCartCount">0</span>',
                    new_content
                )

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Updated cart count span in: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total HTML files updated for cart span: {count}")

def main():
    print("Fixing wishlist query selector in JS files...")
    fix_wishlist_check_in_js()
    print("Updating static HTML cart count spans...")
    update_html_cart_and_wishlist()
    print("Header duplicate wishlist and cart count flicker fixes applied successfully.")

if __name__ == "__main__":
    main()
