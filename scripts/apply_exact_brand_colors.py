import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

# Exact User Brand Colors
PURPLE = "#C483E6"
PINK = "#ED9AE9"
GREY = "#D9D2D2"
PURPLE_HOVER = "#b062d8"
PINK_HOVER = "#e47edc"
SOFT_TINT = "#f8e8fa"

COLOR_REPLACEMENTS = [
    (r"#088178", PURPLE),
    (r"#065f5b", PURPLE_HOVER),
    (r"#06655e", PURPLE_HOVER),
    (r"#055f59", PURPLE_HOVER),
    (r"#a855f7", PURPLE),
    (r"#9333ea", PURPLE_HOVER),
    (r"#7e22ce", PURPLE_HOVER),
    (r"#c084fc", PURPLE),
    (r"#d8b4fe", PURPLE),
    (r"#e9d5ff", SOFT_TINT),
    (r"#f3e8ff", SOFT_TINT),
    (r"#f472b6", PINK),
    (r"#ec4899", PINK),
    (r"#fbcfe8", PINK),
    (r"#cce7d0", GREY),
    (r"#e8f6ea", SOFT_TINT),
    (r"#eef6f4", SOFT_TINT),
    (r"#10b981", PURPLE),
    (r"#059669", PURPLE),
    (r"#2e7d32", PURPLE),
]

def update_global_css_theme():
    global_css = FRONTEND_DIR / "css" / "global.css"
    if global_css.exists():
        with open(global_css, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        new_root = f""":root {{
    --bg-primary: #ffffff;
    --bg-secondary: {GREY};
    --text-primary: #1f1a24;
    --text-secondary: #5e5266;
    --header-bg: rgba(255, 255, 255, 0.95);
    --card-bg: #ffffff;
    --border-color: {GREY};
    --shadow: rgba(0, 0, 0, 0.04);
    --shadow-hover: rgba(196, 131, 230, 0.3);
    --accent: {PURPLE};
    --accent-hover: {PURPLE_HOVER};
    --pink-accent: {PINK};
    --pink-hover: {PINK_HOVER};
    --feature-bg-1: {PINK};
    --feature-bg-2: {PURPLE};
    --feature-bg-3: {GREY};
    --feature-bg-4: {PINK};
    --feature-bg-5: {PURPLE};
    --feature-bg-6: {GREY};
    --input-bg: #ffffff;
    --footer-text: #1f1a24;
    --cart-icon-bg: {SOFT_TINT};
    --feature-label-color: {PURPLE_HOVER};
}}"""

        new_dark = f"""[data-theme="dark"], body.dark, body[data-theme="dark"] {{
    --bg-primary: #140e17;
    --bg-secondary: #221826;
    --text-primary: #f8eef9;
    --text-secondary: #d4c5d9;
    --header-bg: rgba(20, 14, 23, 0.95);
    --card-bg: #221826;
    --border-color: #3b2b42;
    --shadow: rgba(0, 0, 0, 0.4);
    --shadow-hover: rgba(237, 154, 233, 0.35);
    --accent: {PURPLE};
    --accent-hover: {PINK};
    --pink-accent: {PINK};
    --pink-hover: {PURPLE};
    --feature-bg-1: #4a214d;
    --feature-bg-2: #3f1d4a;
    --feature-bg-3: #2d2030;
    --feature-bg-4: #4a214d;
    --feature-bg-5: #3f1d4a;
    --feature-bg-6: #2d2030;
    --input-bg: #221826;
    --footer-text: #f8eef9;
    --cart-icon-bg: #3b2b42;
    --feature-label-color: {PINK};
}}"""

        content = re.sub(r":root\s*\{[^}]*\}", new_root, content, count=1)
        content = re.sub(r'\[data-theme="dark"\][^{]*\{[^}]*\}', new_dark, content, count=1)

        with open(global_css, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated global.css with exact #C483E6, #ED9AE9, #D9D2D2 colors.")

def purge_all_green_and_apply_exact_colors():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith((".html", ".css", ".js", ".json")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content
                for pattern, repl in COLOR_REPLACEMENTS:
                    new_content = re.sub(pattern, repl, new_content, flags=re.IGNORECASE)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Applied exact brand colors in: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total files processed for color replacement: {count}")

def main():
    print("Updating global.css theme variables with exact brand colors...")
    update_global_css_theme()
    print("Purging green and applying #C483E6 (Light Purple), #ED9AE9 (Baby Pink), #D9D2D2 (Soft Grey)...")
    purge_all_green_and_apply_exact_colors()
    print("All green purged and exact brand colors applied successfully.")

if __name__ == "__main__":
    main()
