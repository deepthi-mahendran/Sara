import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

REDIRECT_MAP = {
    "singleProduct.html": "pages/shop/singleProduct.html",
    "cart.html": "pages/shop/cart.html",
    "checkout.html": "pages/shop/checkout.html",
    "wishlist.html": "pages/shop/wishlist.html",
    "shop.html": "pages/shop/shop.html",
    "try-on.html": "pages/shop/try-on.html",
    "promotions.html": "pages/shop/promotions.html",
    "compare.html": "pages/shop/compare.html",
    "deals.html": "pages/shop/deals.html",
    "crazy-deals.html": "pages/shop/crazy-deals.html",
    "outfit-compatibility.html": "pages/shop/outfit-compatibility.html",
    "tshirt.html": "pages/shop/tshirt.html",
    "footware-collection.html": "pages/shop/footware-collection.html",
    "winter-collection.html": "pages/shop/winter-collection.html",
    "winter-sale.html": "pages/shop/winter-sale.html",
    "visual-search.html": "pages/shop/visual-search.html",
    "about.html": "pages/info/about.html",
    "contact.html": "pages/info/contact.html",
    "authenticity.html": "pages/info/authenticity.html",
    "community.html": "pages/info/community.html",
    "delivery.html": "pages/info/delivery.html",
    "deliveryInformation.html": "pages/info/deliveryInformation.html",
    "faq.html": "pages/info/faq.html",
    "license.html": "pages/info/license.html",
    "offline.html": "pages/info/offline.html",
    "privacy.html": "pages/info/privacy.html",
    "terms.html": "pages/info/terms.html",
    "404page.html": "pages/info/404page.html",
    "sara.html": "pages/info/sara.html",
    "contributors.html": "pages/info/contributors.html",
    "blog.html": "pages/blog/blog.html",
    "blog-aw20-menswear.html": "pages/blog/blog-aw20-menswear.html",
    "blog-cotton-jersey-hoodie.html": "pages/blog/blog-cotton-jersey-hoodie.html",
    "blog-quiff-styling.html": "pages/blog/blog-quiff-styling.html",
    "blog-runway-trends.html": "pages/blog/blog-runway-trends.html",
    "blog-skater-girls.html": "pages/blog/blog-skater-girls.html",
    "login.html": "pages/user/login.html",
    "register.html": "pages/user/register.html",
    "order-history.html": "pages/user/order-history.html",
    "track-order.html": "pages/user/track-order.html",
    "forgotPassword.html": "pages/user/forgotPassword.html",
}

def create_root_redirects():
    for filename, target_path in REDIRECT_MAP.items():
        redirect_file = FRONTEND_DIR / filename
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirecting...</title>
    <script>
        (function() {{
            var target = "{target_path}" + window.location.search + window.location.hash;
            window.location.replace(target);
        }})();
    </script>
</head>
<body>
    <p>Redirecting to <a href="{target_path}">{filename}</a>...</p>
</body>
</html>"""
        with open(redirect_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Created root redirect page: {filename} -> {target_path}")

def update_app_js_redirection():
    app_js = FRONTEND_DIR / "js" / "app.js"
    if app_js.exists():
        with open(app_js, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Update proCard click listener in app.js
        old_click_handler = r"window\.location\.href\s*=\s*['\"]singleProduct\.html['\"]"
        new_click_handler = """const path = window.location.pathname.replace(/\\\\/g, '/');
      let targetUrl = 'pages/shop/singleProduct.html';
      if (path.includes('/pages/shop/')) {
        targetUrl = 'singleProduct.html';
      } else if (path.includes('/pages/user/') || path.includes('/pages/info/') || path.includes('/pages/blog/')) {
        targetUrl = '../../pages/shop/singleProduct.html';
      }
      window.location.href = targetUrl;"""

        content = re.sub(old_click_handler, new_click_handler, content)

        with open(app_js, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated product click redirection in app.js.")

def fix_onclick_attributes():
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
                depth = rel_path.count("/")
                prefix = "../../pages/shop/" if depth > 1 else ("pages/shop/" if depth == 0 else "")

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                orig_content = content
                # Fix onclick="window.location.href='singleProduct.html'" or similar
                if depth == 0:
                    content = re.sub(r'window\.location\.href\s*=\s*["\']singleProduct\.html["\']', "window.location.href='pages/shop/singleProduct.html'", content)
                elif "pages/shop/" in rel_path:
                    content = re.sub(r'window\.location\.href\s*=\s*["\']singleProduct\.html["\']', "window.location.href='singleProduct.html'", content)
                else:
                    content = re.sub(r'window\.location\.href\s*=\s*["\']singleProduct\.html["\']', "window.location.href='../../pages/shop/singleProduct.html'", content)

                if content != orig_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Updated product click onclick in: {rel_path}")

def main():
    print("Creating root fallback redirects for all pages...")
    create_root_redirects()
    print("Updating JS product redirection logic...")
    update_app_js_redirection()
    print("Fixing inline onclick redirection attributes...")
    fix_onclick_attributes()
    print("All redirection fallbacks and product link handlers updated.")

if __name__ == "__main__":
    main()
