import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def update_logo_references():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith((".html", ".js", ".css", ".json", ".md")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content
                # Replace Dlogo.png and oldlogo.png with newlogo.svg
                new_content = re.sub(r'images/(Dlogo|oldlogo)\.png', 'images/newlogo.svg', new_content)
                new_content = new_content.replace('Dlogo.png', 'newlogo.svg')
                new_content = new_content.replace('oldlogo.png', 'newlogo.svg')

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Updated logo in: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total files updated with newlogo.svg: {count}")

def update_brand_colors_in_css():
    css_dir = FRONTEND_DIR / "css"
    for root, _, files in os.walk(css_dir):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content
                # Replace old teal #088178 with vibrant light purple #a855f7
                new_content = new_content.replace("#088178", "#a855f7")
                new_content = new_content.replace("#065f5b", "#9333ea")
                new_content = new_content.replace("#06655e", "#7e22ce")
                new_content = new_content.replace("#06b6d4", "#c084fc")
                new_content = new_content.replace("#10b991", "#f472b6")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated brand colors in CSS: {file}")

def update_global_css_variables():
    global_css = FRONTEND_DIR / "css" / "global.css"
    if global_css.exists():
        with open(global_css, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Update root variables
        old_root = """:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #222;
    --text-secondary: #465b52;
    --header-bg: #ffffff;
    --card-bg: #ffffff;
    --border-color: #cce7d0;
    --shadow: rgba(0, 0, 0, 0.02);
    --shadow-hover: rgba(0, 0, 0, 0.25);
    --accent: #088178;
    --feature-bg-1: #fddde4;
    --feature-bg-2: #cdebbc;
    --feature-bg-3: #d1e8f2;
    --feature-bg-4: #cdd4f6;
    --feature-bg-5: #f6dbf6;
    --feature-bg-6: #fff2e5;
    --input-bg: #ffffff;
    --footer-text: #222;
    --cart-icon-bg: #e8f6ea;
    --feature-label-color: #088178;
}"""

        new_root = """:root {
    --bg-primary: #f9fafb;
    --bg-secondary: #f3f4f6;
    --text-primary: #111827;
    --text-secondary: #4b5563;
    --header-bg: rgba(255, 255, 255, 0.95);
    --card-bg: #ffffff;
    --border-color: #e5e7eb;
    --shadow: rgba(0, 0, 0, 0.04);
    --shadow-hover: rgba(168, 85, 247, 0.25);
    --accent: #a855f7;
    --accent-hover: #9333ea;
    --pink-accent: #f472b6;
    --pink-hover: #ec4899;
    --feature-bg-1: #fbcfe8;
    --feature-bg-2: #e9d5ff;
    --feature-bg-3: #f3f4f6;
    --feature-bg-4: #f472b6;
    --feature-bg-5: #c084fc;
    --feature-bg-6: #e5e7eb;
    --input-bg: #ffffff;
    --footer-text: #111827;
    --cart-icon-bg: #f3e8ff;
    --feature-label-color: #9333ea;
}"""

        old_dark = """[data-theme="dark"] {
    --bg-primary: #0f1419;
    --bg-secondary: #1a1f26;
    --text-primary: #e6eef8;
    --text-secondary: #94a3b8;
    --header-bg: #0f1419;
    --card-bg: #1a1f26;
    --border-color: #2d3748;
    --shadow: rgba(0, 0, 0, 0.4);
    --shadow-hover: rgba(124, 58, 237, 0.3);
    --accent: #06b6d4;
    --feature-bg-1: #7c3aed;
    --feature-bg-2: #10b991;
    --feature-bg-3: #3b82f6;
    --feature-bg-4: #8b5cf6;
    --feature-bg-5: #ec4899;
    --feature-bg-6: #f59e0b;
    --input-bg: #1a1f26;
    --footer-text: #e6eef8;
    --cart-icon-bg: #2d3748;
    --feature-label-color: #06b6d4;
}"""

        new_dark = """[data-theme="dark"], body.dark, body[data-theme="dark"] {
    --bg-primary: #111827;
    --bg-secondary: #1f2937;
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --header-bg: rgba(17, 24, 39, 0.95);
    --card-bg: #1f2937;
    --border-color: #374151;
    --shadow: rgba(0, 0, 0, 0.4);
    --shadow-hover: rgba(192, 132, 252, 0.35);
    --accent: #c084fc;
    --accent-hover: #d8b4fe;
    --pink-accent: #f472b6;
    --pink-hover: #f687b3;
    --feature-bg-1: #831843;
    --feature-bg-2: #581c87;
    --feature-bg-3: #374151;
    --feature-bg-4: #9d174d;
    --feature-bg-5: #7e22ce;
    --feature-bg-6: #4b5563;
    --input-bg: #1f2937;
    --footer-text: #f9fafb;
    --cart-icon-bg: #374151;
    --feature-label-color: #c084fc;
}"""

        content = content.replace(old_root, new_root)
        content = content.replace(old_dark, new_dark)

        # Add logo filter rule for dark mode
        logo_filter_rule = """
/* Theme Adaptable Logo Rules */
#siteLogo, img.logo {
    transition: filter 0.3s ease, transform 0.3s ease;
}

[data-theme="dark"] #siteLogo,
[data-theme="dark"] img.logo,
body.dark #siteLogo,
body.dark img.logo {
    filter: invert(1) brightness(1.8) drop-shadow(0 2px 4px rgba(255, 255, 255, 0.15)) !important;
}
"""
        if "Theme Adaptable Logo Rules" not in content:
            content += "\n" + logo_filter_rule

        with open(global_css, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated global.css brand color tokens and adaptable logo filters.")

def main():
    print("Updating logo references to newlogo.svg...")
    update_logo_references()
    print("Updating brand color tokens across CSS files...")
    update_brand_colors_in_css()
    print("Updating global CSS variables...")
    update_global_css_variables()
    print("Brand color and logo update completed successfully.")

if __name__ == "__main__":
    main()
