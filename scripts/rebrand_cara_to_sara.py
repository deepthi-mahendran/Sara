import os
import re
from pathlib import Path

PROJECT_ROOT = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara")

EXCLUDE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".gemini"}

REPLACEMENTS = [
    (r"\bCara\b", "Sara"),
    (r"\bcara\b", "sara"),
    (r"\bCARA\b", "SARA"),
]

def process_file(file_path):
    # Skip binary files or specific build dirs
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        new_content = content
        for pattern, repl in REPLACEMENTS:
            new_content = re.sub(pattern, repl, new_content)

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
            if file.endswith((".html", ".js", ".css", ".md", ".json", ".py", ".txt")):
                file_path = os.path.join(root, file)
                if process_file(file_path):
                    count += 1
                    print(f"Rebranded Sara -> Sara in: {os.path.relpath(file_path, PROJECT_ROOT)}")
    print(f"Total files rebranded: {count}")

if __name__ == "__main__":
    main()
