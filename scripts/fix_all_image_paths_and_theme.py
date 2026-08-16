import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def fix_css_files():
    css_dir = FRONTEND_DIR / "css"
    for root, _, files in os.walk(css_dir):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Replace url("images/..."), url('images/...'), url(images/...) with url("../images/...")
                new_content = re.sub(r'url\((["\']?)images/', r'url(\1../images/', content)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed CSS image paths in: {file}")

def fix_html_files():
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
                depth = rel_path.count("/")
                prefix = "../../" if depth > 0 else ""

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                orig_content = content

                if depth > 0:
                    # Fix img src="images/..." -> src="../../images/..."
                    content = re.sub(r'src=["\'](?!http|https|//|\.\./|\data:)(?!pages/)([^"\']*images/[^"\']*)["\']', r'src="' + prefix + r'\1"', content)
                    content = re.sub(r'src=["\']images/', f'src="{prefix}images/', content)
                    content = re.sub(r'src=["\']img/', f'src="{prefix}img/', content)
                    content = re.sub(r'href=["\']img/', f'href="{prefix}img/', content)

                    # Fix inline background-image url("images/...") or url('images/...')
                    content = re.sub(r'url\((["\']?)(?!http|https|//|\.\./)([^)\'"]*images/[^)]*)\)', r'url(\1' + prefix + r'\2)', content)

                    # Fix logo src
                    content = re.sub(r'id=["\']siteLogo["\'][^>]*src=["\'][^"\']*["\']', f'id="siteLogo" class="logo" src="{prefix}images/Dlogo.png"', content)
                else:
                    # Root index.html
                    content = re.sub(r'id=["\']siteLogo["\'][^>]*src=["\'][^"\']*["\']', 'id="siteLogo" class="logo" src="images/Dlogo.png"', content)

                # Fix try-on.html header commenting if present
                if "try-on.html" in file and "<!-- <section id=\"header\"" in content:
                    content = content.replace("<!-- <section id=\"header\"", "<section id=\"header\"")
                    content = content.replace("</section> -->", "</section>")

                if content != orig_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Fixed HTML asset paths in: {rel_path}")

def update_app_js_logo():
    app_js_path = FRONTEND_DIR / "js" / "app.js"
    if app_js_path.exists():
        with open(app_js_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Update updateThemeIcon in app.js to use getPathPrefix
        old_pattern = r'siteLogo\.src\s*=\s*theme\s*===\s*[\'"]dark[\'"]\s*\?\s*[\'"]images/Dlogo\.png[\'"]\s*:\s*[\'"]images/oldlogo\.png[\'"];?'
        new_replacement = 'siteLogo.src = (typeof getPathPrefix === "function" ? getPathPrefix() : "") + "images/Dlogo.png";'

        content = re.sub(old_pattern, new_replacement, content)

        with open(app_js_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated app.js theme toggle logo resolver.")

def main():
    print("Fixing CSS image paths...")
    fix_css_files()
    print("Fixing HTML image and asset paths...")
    fix_html_files()
    print("Updating app.js logo pathing...")
    update_app_js_logo()
    print("All image paths and theme toggle assets updated successfully.")

if __name__ == "__main__":
    main()
