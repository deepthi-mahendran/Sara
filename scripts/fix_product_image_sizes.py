import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

NEW_IMG_WRAP_CSS = """.pro-img-wrap {
    width: 100%;
    height: 230px;
    max-height: 230px;
    background: var(--bg-secondary, #f8f9fa);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    box-sizing: border-box;
}

[data-theme="dark"] .pro-img-wrap {
    background: rgba(255, 255, 255, 0.05);
}

.pro-img-wrap img,
.pro img {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
    transition: transform 0.35s ease;
}

#product1 .pro:hover .pro-img-wrap img,
.pro:hover .pro-img-wrap img {
    transform: scale(1.05);
}"""

def update_css_image_styles():
    css_dir = FRONTEND_DIR / "css"
    for root, _, files in os.walk(css_dir):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content

                # Replace old full-bleed aspect ratio / cover image blocks
                pattern = r"\.pro-img-wrap\s*\{[^}]*\}\s*(?:\[data-theme=\"dark\"\]\s*\.pro-img-wrap\s*\{[^}]*\}\s*)?\.pro-img-wrap\s*img\s*\{[^}]*\}"
                if re.search(pattern, new_content):
                    new_content = re.sub(pattern, NEW_IMG_WRAP_CSS, new_content)

                # Ensure pro img max-height
                if ".pro img {" in new_content:
                    new_content = new_content.replace("object-fit: cover;", "object-fit: contain;")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated product image sizes in: {file}")

def main():
    print("Updating CSS files to make product showcase images normal sized and clean...")
    update_css_image_styles()
    print("Product image sizing update complete.")

if __name__ == "__main__":
    main()
