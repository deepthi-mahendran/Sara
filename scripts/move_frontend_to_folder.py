import os
import shutil
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

ITEMS_TO_MOVE = [
    'index.html',
    'css',
    'js',
    'pages',
    'images',
    'assets',
    'manifest.json',
    'service-worker.js'
]

def move_to_frontend():
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    for item in ITEMS_TO_MOVE:
        src = os.path.join(ROOT_DIR, item)
        dest = os.path.join(FRONTEND_DIR, item)
        if os.path.exists(src):
            if os.path.exists(dest):
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                else:
                    os.remove(dest)
            shutil.move(src, dest)
            print(f"Moved {item} -> frontend/{item}")

def update_test_imports():
    tests_dir = os.path.join(ROOT_DIR, 'tests')
    if os.path.exists(tests_dir):
        for js_file in glob.glob(os.path.join(tests_dir, '**', '*.js'), recursive=True):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '../../js/' in content:
                new_content = content.replace('../../js/', '../../frontend/js/')
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated test imports in: {os.path.relpath(js_file, ROOT_DIR)}")

if __name__ == '__main__':
    print("--- Encapsulating Frontend into frontend/ Directory ---")
    move_to_frontend()
    update_test_imports()
    print("--- Encapsulation Complete ---")
