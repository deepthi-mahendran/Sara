import os
import shutil
import glob
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PAGES_MAPPING = {
    'shop': [
        'shop.html', 'singleProduct.html', 'cart.html', 'checkout.html', 'wishlist.html',
        'compare.html', 'deals.html', 'crazy-deals.html', 'promotions.html', 'tshirt.html',
        'footware-collection.html', 'winter-collection.html', 'winter-sale.html',
        'outfit-compatibility.html', 'try-on.html', 'visual-search.html'
    ],
    'user': [
        'login.html', 'register.html', 'forgotPassword.html', 'order-history.html', 'track-order.html'
    ],
    'info': [
        'about.html', 'contact.html', 'faq.html', 'community.html', 'contributors.html',
        'authenticity.html', 'delivery.html', 'deliveryInformation.html', 'privacy.html',
        'terms.html', 'license.html', '404page.html', 'offline.html', 'sara.html'
    ],
    'blog': [
        'blog.html', 'blog-aw20-menswear.html', 'blog-cotton-jersey-hoodie.html',
        'blog-quiff-styling.html', 'blog-runway-trends.html', 'blog-skater-girls.html'
    ]
}

# Reverse lookup: filename -> category ('shop', 'user', 'info', 'blog')
FILE_TO_CATEGORY = {}
for category, files in PAGES_MAPPING.items():
    for f in files:
        FILE_TO_CATEGORY[f] = category

def step_1_create_directories_and_move():
    pages_base = os.path.join(ROOT_DIR, 'pages')
    for cat in PAGES_MAPPING.keys():
        cat_dir = os.path.join(pages_base, cat)
        os.makedirs(cat_dir, exist_ok=True)

    for cat, files in PAGES_MAPPING.items():
        for f in files:
            src = os.path.join(ROOT_DIR, f)
            dest = os.path.join(pages_base, cat, f)
            if os.path.exists(src):
                shutil.move(src, dest)
                print(f"Moved {f} -> pages/{cat}/{f}")

def step_2_cleanup_temp_files():
    temp_files = ['test.db', 'test2.txt', 'dummy.test.js']
    for f in temp_files:
        path = os.path.join(ROOT_DIR, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed temporary file {f}")

def rewrite_html_file(file_path, is_root=False, current_cat=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    if not is_root:
        # Asset prefixes for files in pages/<cat>/<filename>.html (2 levels deep)
        # Fix css/, js/, images/, assets/, img/
        content = re.sub(r'(href=["\'])(?!\.\./)(css/|images/|assets/|img/|\.\./css/|\.\./js/|\.\./images/)', r'\g<1>../../\2', content)
        content = re.sub(r'(src=["\'])(?!\.\./)(js/|images/|assets/|img/|\.\./css/|\.\./js/|\.\./images/)', r'\g<1>../../\2', content)

    # Rewrite page navigation links
    for page_name, target_cat in FILE_TO_CATEGORY.items():
        if is_root:
            # From root index.html -> pages/<target_cat>/<page_name>
            new_href = f"pages/{target_cat}/{page_name}"
        else:
            if target_cat == current_cat:
                # Same folder link
                new_href = page_name
            else:
                # Cross category link
                new_href = f"../{target_cat}/{page_name}"

        # Match href="page_name" or href="./page_name" or href="pages/..."
        # avoid matching already formatted or absolute links
        pattern = r'href=["\'](?:\./)?(?:pages/[^/\'\"]+/)?' + re.escape(page_name) + r'["\']'
        replacement = f'href="{new_href}"'
        content = re.sub(pattern, replacement, content)

    # Rewrite root index.html link in subpages
    if not is_root:
        content = re.sub(r'href=["\'](?:\./)?index\.html["\']', 'href="../../index.html"', content)

    if content != orig:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated routes in: {os.path.relpath(file_path, ROOT_DIR)}")

def step_3_update_all_html_routes():
    # 1. Update root index.html
    root_index = os.path.join(ROOT_DIR, 'index.html')
    if os.path.exists(root_index):
        rewrite_html_file(root_index, is_root=True)

    # 2. Update subpages in pages/*/*.html
    for cat in PAGES_MAPPING.keys():
        cat_dir = os.path.join(ROOT_DIR, 'pages', cat)
        if os.path.exists(cat_dir):
            for html_file in glob.glob(os.path.join(cat_dir, '*.html')):
                rewrite_html_file(html_file, is_root=False, current_cat=cat)

if __name__ == '__main__':
    print("--- Starting HTML Reorganization & Routing Update ---")
    step_1_create_directories_and_move()
    step_2_cleanup_temp_files()
    step_3_update_all_html_routes()
    print("--- Completed Reorganization ---")
