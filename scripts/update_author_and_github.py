import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

REPLACEMENTS = [
    ('https://github.com/deepthi-mahendran/sara', 'https://github.com/deepthi-mahendran/sara'),
    ('https://github.com/deepthi-mahendran/sara', 'https://github.com/deepthi-mahendran/sara'),
    ('github.com/deepthi-mahendran/sara', 'github.com/deepthi-mahendran/sara'),
    ('deepthi-mahendran/sara', 'deepthi-mahendran/sara'),
    ('https://github.com/deepthi-mahendran', 'https://github.com/deepthi-mahendran'),
    ('github.com/deepthi-mahendran', 'github.com/deepthi-mahendran'),
    ('@deepthi-mahendran', '@deepthi-mahendran'),
    ('Deepthi Mahendran', 'Deepthi Mahendran'),
    ('DeepthiMahendran', 'DeepthiMahendran'),
    ('deepthi-mahendran', 'deepthi-mahendran'),
    ('deepthi-mahendrans', 'deepthi-mahendrans'),
    ('deepthi-mahendran', 'deepthi-mahendran'),
]

EXCLUDE_DIRS = {'node_modules', '.git', 'dist', '.venv', '__pycache__'}
ALLOWED_EXTENSIONS = {'.html', '.js', '.json', '.md', '.py', '.yml', '.yaml', '.conf', '.txt', '.example', 'LICENSE'}

updated_files_count = 0

for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for file in files:
        file_path = os.path.join(root, file)
        ext = os.path.splitext(file)[1]
        basename = os.path.basename(file)

        if ext in ALLOWED_EXTENSIONS or basename in ALLOWED_EXTENSIONS or basename.startswith('.env'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                orig = content
                for old_str, new_str in REPLACEMENTS:
                    content = content.replace(old_str, new_str)

                if content != orig:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files_count += 1
                    print(f"Updated author/GitHub in: {os.path.relpath(file_path, ROOT_DIR)}")
            except Exception as e:
                pass

print(f"\n--- Author and GitHub replacement complete! Updated {updated_files_count} files. ---")
