import os
import re
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara")

EXCLUDE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".gemini", "dist", ".brain"}

FILE_EXTENSIONS = (
    ".html", ".js", ".css", ".md", ".json", ".py", ".txt",
    ".yml", ".yaml", ".sql", ".sh", ".env", ".mjs", ".ts", ".xml"
)

REPLACEMENTS = [
    ("SARA", "SARA"),
    ("Sara", "Sara"),
    ("sara", "sara"),
    ("SaRa", "SaRa"),
]

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        new_content = content
        for search, repl in REPLACEMENTS:
            new_content = new_content.replace(search, repl)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(FILE_EXTENSIONS) or file.startswith(".env") or file == "Dockerfile":
                file_path = os.path.join(root, file)
                if process_file(file_path):
                    count += 1
                    print(f"Rebranded in: {os.path.relpath(file_path, PROJECT_ROOT)}")
    print(f"Total files rebranded: {count}")

if __name__ == "__main__":
    main()
