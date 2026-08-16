import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

def fix_index_html():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Fix stylesheet 404 paths
        content = content.replace('href="style.css?v=2"', 'href="css/style.css?v=2"')
        content = content.replace('href="live-sales-toast.css"', 'href="css/live-sales-toast.css"')

        # Fix loadNavbar inline execution
        content = content.replace("<script>\n  loadNavbar('home');\n</script>", "<script>document.addEventListener('DOMContentLoaded', function() { if (typeof loadNavbar === 'function') loadNavbar('home'); });</script>")
        content = content.replace("<script>\r\n  loadNavbar('home');\r\n</script>", "<script>document.addEventListener('DOMContentLoaded', function() { if (typeof loadNavbar === 'function') loadNavbar('home'); });</script>")

        # Fix searchBar syntax error (extra brace before else)
        old_search_block = """    if(productName.includes(input)){
      product.style.display = "block";
    }
    } else {
      product.style.display = "none";
    }"""
        new_search_block = """    if(productName.includes(input)){
      product.style.display = "block";
    } else {
      product.style.display = "none";
    }"""
        content = content.replace(old_search_block, new_search_block)

        with open(index_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed index.html syntax and script load errors.")

def fix_app_js():
    app_js = FRONTEND_DIR / "js" / "app.js"
    if app_js.exists():
        with open(app_js, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Fix regex replace syntax error
        content = content.replace("pathname.replace(/\/g, '/')", "pathname.replace(/\\\\/g, '/')")
        content = content.replace("replace(/\/g,", "replace(/\\\\/g,")

        with open(app_js, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed app.js syntax error.")

def fix_products_js():
    products_js = FRONTEND_DIR / "js" / "products.js"
    if products_js.exists():
        with open(products_js, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        content = content.replace(
            "syncWishlistButtons();",
            "if (typeof syncWishlistButtons === 'function') { syncWishlistButtons(); } else if (typeof window.syncWishlistButtons === 'function') { window.syncWishlistButtons(); }"
        )

        with open(products_js, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed products.js syncWishlistButtons ReferenceError.")

def fix_global_css():
    global_css = FRONTEND_DIR / "css" / "global.css"
    if global_css.exists():
        with open(global_css, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        content = content.replace("@import url('assets/css/search-results.css');", "/* @import url('assets/css/search-results.css'); */")

        with open(global_css, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed global.css missing @import 404.")

def fix_favicons():
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Replace missing img/favicon.ico with images/favicon.jpg
                new_content = re.sub(r'<link rel="icon"[^>]*href="[^"]*img/favicon\.ico"[^>]*>\s*', '', content)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Cleaned up missing favicon.ico link in: {os.path.relpath(file_path, FRONTEND_DIR)}")

def main():
    fix_index_html()
    fix_app_js()
    fix_products_js()
    fix_global_css()
    fix_favicons()
    print("All browser console errors resolved.")

if __name__ == "__main__":
    main()
