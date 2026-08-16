import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def remove_search_from_html_files():
    count = 0
    pattern = re.compile(r'\s*<li class="header-search-item">.*?</li>', re.DOTALL)
    pattern2 = re.compile(r'\s*<div class="search-container"[^>]*>.*?</div>', re.DOTALL)

    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = pattern.sub('', content)
                new_content = pattern2.sub('', new_content)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Removed header search bar from: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total HTML files updated: {count}")

def remove_search_from_navbar_js():
    js_files = [
        FRONTEND_DIR / "js" / "navbar.js",
        FRONTEND_DIR / "js" / "navbar.min.js"
    ]
    for file_path in js_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            new_content = re.sub(r'<div class="search-container"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
            new_content = re.sub(r'<li class="header-search-item">.*?</li>', '', new_content, flags=re.DOTALL)

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated JS navbar file: {file_path.name}")

def update_css_hide_header_search():
    css_files = [
        FRONTEND_DIR / "css" / "global.css",
        FRONTEND_DIR / "css" / "style.css",
        FRONTEND_DIR / "css" / "style.min.css",
        FRONTEND_DIR / "css" / "bundle.css"
    ]
    hide_rule = "\n/* Hide Header Search Bar */\n.header-search-item, .header-search-wrap, #header .search-container { display: none !important; }\n"

    for file_path in css_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "Hide Header Search Bar" not in content:
                content += hide_rule
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Added CSS hide rule in: {file_path.name}")

def main():
    print("Removing header search bar across all HTML files...")
    remove_search_from_html_files()
    print("Updating navbar JS files...")
    remove_search_from_navbar_js()
    print("Adding CSS hide rule...")
    update_css_hide_header_search()
    print("Header search bar removal completed successfully.")

if __name__ == "__main__":
    main()
