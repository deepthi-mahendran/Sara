import os
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def purge_url_encoded_teal():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith((".css", ".html", ".js")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content.replace("%23088178", "%23C483E6")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
                    print(f"Purged URL-encoded teal in: {os.path.relpath(file_path, FRONTEND_DIR)}")
    print(f"Total URL-encoded replacements: {count}")

if __name__ == "__main__":
    purge_url_encoded_teal()
