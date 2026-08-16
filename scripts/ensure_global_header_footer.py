import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

# Map file basenames to active page keys
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

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    rel_to_frontend = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
    depth = rel_to_frontend.count("/")
    js_prefix = "../../js/" if depth > 0 else "js/"

    page_key = get_page_key(file_path)
    modified = False

    # 1. Ensure navbar.js script tag exists
    navbar_script_tag = f'<script type="module" src="{js_prefix}navbar.js"></script>'
    if "navbar.js" not in content:
        # Insert before </body> or before app.js
        if "</body>" in content:
            content = content.replace("</body>", f"{navbar_script_tag}\n</body>")
            modified = True

    # 2. Ensure loadNavbar(page_key) call exists
    load_navbar_call = f"<script>document.addEventListener('DOMContentLoaded', function() {{ if (typeof loadNavbar === 'function') loadNavbar('{page_key}'); }});</script>"
    if "loadNavbar" not in content:
        if "</body>" in content:
            content = content.replace("</body>", f"{load_navbar_call}\n</body>")
            modified = True

    # 3. Ensure header container tag exists
    if 'id="header"' not in content and 'id="navbar-container"' not in content:
        # Insert header container after <body>
        body_match = re.search(r"<body[^>]*>", content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.end()
            header_container = '\n<section id="header" role="banner"></section>\n'
            content = content[:insert_pos] + header_container + content[insert_pos:]
            modified = True

    # 4. Ensure footer container tag exists
    if '<footer' not in content:
        if "</body>" in content:
            footer_container = '\n<footer class="section-p1" role="contentinfo"></footer>\n'
            content = content.replace("</body>", f"{footer_container}\n</body>")
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {rel_to_frontend}")
    else:
        print(f"Already configured: {rel_to_frontend}")

def main():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                process_html_file(full_path)
                count += 1
    print(f"Finished processing {count} HTML files.")

if __name__ == "__main__":
    main()
