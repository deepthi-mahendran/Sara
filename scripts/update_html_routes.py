import glob
import re

css_files = [
    'a11y-utilities.css', 'about.css', 'authenticity.css', 'blog.css', 'bundle.css',
    'cart.css', 'checkout.css', 'compare.css', 'contact.css', 'contributors.css',
    'currency-converter.css', 'faq.css', 'forgotPassword.css', 'global.css', 'header-fix.css',
    'index.css', 'lazyload.css', 'login.css', 'order-history.css', 'privacy.css',
    'promotions.css', 'recently-viewed.css', 'register.css', 'reviews.css', 'shop.css',
    'singleProduct.css', 'stock-alert.css', 'style.css', 'style.min.css', 'terms.css',
    'theme-engine.css', 'toast-queue.css', 'toast.css', 'track-order.css'
]

js_files = [
    'app.js', 'app.min.js', 'append_saved_items.js', 'authenticity.js', 'checkout.js',
    'compare.js', 'contributors.js', 'empty-cart.js', 'faq.js', 'forgotPassword.js',
    'login.js', 'navbar.js', 'navbar.min.js', 'order-history.js', 'outfit-compatibility.js',
    'products.js', 'register.js', 'singleProduct.js', 'track-order.js', 'try-on.js'
]

html_files = glob.glob('*.html')

updated_count = 0
for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    for css in css_files:
        pattern = r'(href=["\'])(?!(?:css/|https?://|/))' + re.escape(css) + r'(["\'])'
        content = re.sub(pattern, r'\g<1>css/' + css + r'\2', content)

    for js in js_files:
        pattern = r'(src=["\'])(?!(?:js/|https?://|/))' + re.escape(js) + r'(["\'])'
        content = re.sub(pattern, r'\g<1>js/' + js + r'\2', content)

    if content != orig:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1
        print(f'Updated {html_path}')

print(f'Finished updating HTML files. Total updated: {updated_count}')
