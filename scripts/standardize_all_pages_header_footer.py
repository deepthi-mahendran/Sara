import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

PAGE_KEY_MAP = {
    "index.html": "home",
    "shop.html": "shop",
    "blog.html": "blog",
    "about.html": "about",
    "try-on.html": "try-on",
    "authenticity.html": "authenticity",
    "community.html": "community",
    "promotions.html": "promotions",
    "order-history.html": "orders",
    "contact.html": "contact",
    "login.html": "login",
    "wishlist.html": "wishlist",
    "cart.html": "cart",
}

def get_page_key(filename):
    basename = os.path.basename(filename)
    return PAGE_KEY_MAP.get(basename, "home")

def sanitize_html_page(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    rel_path = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
    depth = rel_path.count("/")
    css_prefix = "../../css/" if depth > 0 else "css/"
    js_prefix = "../../js/" if depth > 0 else "js/"
    page_key = get_page_key(file_path)

    # 1. Clean out hardcoded header inner HTML
    # Replace <section id="header"...>...</section> or <header id="header"...>...</header> with clean mount tag
    content = re.sub(
        r'<(section|header)[^>]*id=["\']header["\'][^>]*>.*?</\1>',
        '<section id="header" role="banner"></section>',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 2. Clean out hardcoded footer inner HTML
    # Replace <footer...>...</footer> with clean mount tag
    content = re.sub(
        r'<footer[^>]*>.*?</footer>',
        '<footer class="section-p1" role="contentinfo"></footer>',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 3. Ensure global.css and style.css are in head
    global_css_tag = f'<link rel="stylesheet" href="{css_prefix}global.css">'
    style_css_tag = f'<link rel="stylesheet" href="{css_prefix}style.css">'

    if "global.css" not in content and "</head>" in content:
        content = content.replace("</head>", f"  {global_css_tag}\n</head>")

    if "style.css" not in content and "</head>" in content:
        content = content.replace("</head>", f"  {style_css_tag}\n</head>")

    # 4. Ensure navbar.js and loadNavbar call exist before </body>
    navbar_script = f'<script type="module" src="{js_prefix}navbar.js"></script>'
    load_call = f"<script>document.addEventListener('DOMContentLoaded', function() {{ if (typeof loadNavbar === 'function') loadNavbar('{page_key}'); }});</script>"

    if "navbar.js" not in content and "</body>" in content:
        content = content.replace("</body>", f"{navbar_script}\n</body>")

    if "loadNavbar" not in content and "</body>" in content:
        content = content.replace("</body>", f"{load_call}\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Standardized: {rel_path} (page key: {page_key})")

def main():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                sanitize_html_page(os.path.join(root, file))
                count += 1
    print(f"Successfully standardized {count} HTML pages.")

if __name__ == "__main__":
    main()
