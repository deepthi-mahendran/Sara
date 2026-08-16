import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def update_favicons():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith((".html", ".json", ".js", ".md")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content
                new_content = new_content.replace("images/favicon.jpg", "images/favicon.png")
                new_content = new_content.replace("favicon.jpg", "favicon.png")
                new_content = new_content.replace('type="image/jpg"', 'type="image/png"')
                new_content = new_content.replace('type="image/jpeg"', 'type="image/png"')

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Updated favicon to PNG in: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_favicons()
