import os
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    rel_path = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
    depth = rel_path.count("/")
    css_prefix = "../../css/" if depth > 0 else "css/"

    global_css_link = f'<link rel="stylesheet" href="{css_prefix}global.css">'
    
    if "global.css" in content:
        print(f"Already has global.css: {rel_path}")
        return

    # Insert global.css before </head> or after first <link rel="stylesheet">
    if "</head>" in content:
        content = content.replace("</head>", f"  {global_css_link}\n</head>")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Injected global.css: {rel_path}")

def main():
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                process_html_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
