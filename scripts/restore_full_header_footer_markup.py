import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

PAGE_KEY_MAP = {
    "index.html": "home",
    "shop.html": "shop",
    "blog.html": "blog",
    "about.html": "about",
    "try-on.html": "try-on",
    "authenticity.html": "authenticity",
    "community.html": "community",
    "promotions.html": "promotions",
    "order-history.html": "orders",
    "contact.html": "contact",
    "login.html": "login",
    "wishlist.html": "wishlist",
    "cart.html": "cart",
}

def get_page_key(filename):
    basename = os.path.basename(filename)
    return PAGE_KEY_MAP.get(basename, "home")

def generate_header_html(prefix, page_key):
    def is_act(key):
        return 'class="active" aria-current="page"' if page_key == key else ''

    return f"""<section id="header" role="banner">
    <a href="{prefix}index.html" aria-label="Sara Home">
      <img id="siteLogo" class="logo" src="{prefix}images/Dlogo.png" alt="Sara Logo" />
    </a>
    <div>
      <ul id="navbar" role="navigation" aria-label="Main navigation">
        <li><a {is_act('home')} href="{prefix}index.html" title="Home">Home</a></li>
        <li><a {is_act('shop')} href="{prefix}pages/shop/shop.html" title="Shop">Shop</a></li>
        <li><a {is_act('blog')} href="{prefix}pages/blog/blog.html" title="Blog">Blog</a></li>
        <li><a {is_act('about')} href="{prefix}pages/info/about.html" title="About">About</a></li>
        <li><a {is_act('try-on')} href="{prefix}pages/shop/try-on.html" title="Try-On">Try-On</a></li>
        <li><a {is_act('authenticity')} href="{prefix}pages/info/authenticity.html" title="Authenticity">Authenticity</a></li>
        <li><a {is_act('community')} href="{prefix}pages/info/community.html" title="Community">Community</a></li>
        <li><a {is_act('promotions')} href="{prefix}pages/shop/promotions.html" title="Promotions">Promotions</a></li>
        <li><a {is_act('orders')} href="{prefix}pages/user/order-history.html" title="My Orders">My Orders</a></li>
        <li class="nav-icon"><a {is_act('contact')} href="{prefix}pages/info/contact.html" title="Contact Us" aria-label="Contact"><i class="ri-customer-service-2-line"></i></a></li>
        <li class="nav-icon"><a {is_act('login')} href="{prefix}pages/user/login.html" title="Sign In" aria-label="Login"><i class="ri-user-3-line"></i></a></li>
        <li class="nav-icon"><a {is_act('wishlist')} href="{prefix}pages/shop/wishlist.html" title="View Wishlist" aria-label="Wishlist"><i class="ri-heart-line"></i><span class="wishlist-count hidden">0</span></a></li>
        <li class="nav-icon"><a {is_act('cart')} href="{prefix}pages/shop/cart.html" id="lg-bag" title="View Cart" aria-label="Cart"><i class="ri-shopping-bag-4-line"></i><span class="cart-count" id="desktopCartCount">0</span></a></li>
        <li class="nav-icon">
          <button class="theme-toggle" id="themeToggleDesktop" aria-label="Toggle dark mode">
            <i class="ri-moon-line" id="themeIcon"></i>
          </button>
        </li>
        <li class="nav-close"><a href="javascript:void(0)" id="close" aria-label="Close menu"><i class="fa-solid fa-xmark"></i></a></li>
      </ul>
    </div>
    <div id="mobile">
      <a href="{prefix}pages/shop/cart.html" aria-label="Cart"><i class="ri-shopping-bag-4-line"></i></a>
      <i id="bar" class="fas fa-outdent"></i>
    </div>
  </section>"""

def generate_footer_html(prefix):
    return f"""<footer class="section-p1" role="contentinfo">
    <div class="col">
      <img class="logo" src="{prefix}images/Dlogo.png" alt="Sara Logo">
      <h4>Contact</h4>
      <p><strong>Address:</strong> 562 Wellington Road, Street 32, San Francisco</p>
      <p><strong>Phone:</strong> +01 2222 365 / (+91) 01 2345 6789</p>
      <p><strong>Hours:</strong> 10:00 - 18:00, Mon - Sat</p>
      <div class="follow">
        <h4>Follow us</h4>
        <div class="icon">
          <a href="https://x.com/DeepthiMahendran" target="_blank" rel="noopener noreferrer" aria-label="X (formerly Twitter)"><i class="fa-brands fa-x-twitter"></i></a>
          <a title="GitHub" href="https://github.com/deepthi-mahendran" target="_blank" rel="noopener noreferrer" aria-label="GitHub"><i class="fab fa-github"></i></a>
          <a href="https://www.linkedin.com/in/deepthi-mahendran-80a7b2290" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
          <a href="https://www.youtube.com/@DeepthiMahendran" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
        </div>
      </div>
    </div>

    <div class="col">
      <h4>About</h4>
      <a href="{prefix}pages/info/about.html">About Us</a>
      <a href="{prefix}pages/info/delivery.html">Delivery Information</a>
      <a href="{prefix}pages/info/privacy.html">Privacy Policy</a>
      <a href="{prefix}pages/info/terms.html">Terms and Conditions</a>
      <a href="{prefix}pages/info/contact.html">Contact Us</a>
    </div>

    <div class="col">
      <h4>My Account</h4>
      <a href="{prefix}pages/user/login.html">Sign In</a>
      <a href="{prefix}pages/shop/cart.html">View Cart</a>
      <a href="{prefix}pages/shop/wishlist.html">My Wishlist</a>
      <a href="{prefix}pages/user/track-order.html">Track My Order</a>
      <a href="{prefix}pages/info/contact.html">Help</a>
    </div>

    <div class="col newsletter-footer">
      <h4>Newsletter</h4>
      <p>Get email updates about our latest shop and <span>special offers.</span></p>
      <form class="newsletter-form" role="form" aria-label="Newsletter subscription">
        <input type="email" placeholder="Your email address" aria-label="Email address for newsletter" required>
        <button type="submit" class="normal" aria-label="Sign up for newsletter">Sign Up</button>
      </form>
    </div>

    <div class="col install">
      <h4>Install App</h4>
      <p>From App Store or Google Play</p>
      <div class="row">
        <img src="{prefix}images/pay/app.jpg" alt="Download from App Store">
        <img src="{prefix}images/pay/play.jpg" alt="Get it on Google Play">
      </div>
      <p>Secured Payment Gateways</p>
      <div class="payment-icons">
        <a href="https://www.visa.com" target="_blank" rel="noopener noreferrer" aria-label="Visa"><i class="fab fa-cc-visa"></i></a>
        <a href="https://www.mastercard.com" target="_blank" rel="noopener noreferrer" aria-label="Mastercard"><i class="fab fa-cc-mastercard"></i></a>
        <a href="https://www.paypal.com" target="_blank" rel="noopener noreferrer" aria-label="PayPal"><i class="fab fa-cc-paypal"></i></a>
        <a href="https://www.americanexpress.com" target="_blank" rel="noopener noreferrer" aria-label="American Express"><i class="fab fa-cc-amex"></i></a>
        <a href="https://stripe.com" target="_blank" rel="noopener noreferrer" aria-label="Stripe"><i class="fab fa-cc-stripe"></i></a>
      </div>
    </div>

    <div class="copyright">
      <p>© Sara 2026. All rights reserved. | <a href="{prefix}pages/info/license.html" style="color: #088178">MIT License</a></p>
    </div>
  </footer>"""

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    rel_path = os.path.relpath(file_path, FRONTEND_DIR).replace("\\", "/")
    depth = rel_path.count("/")
    prefix = "../../" if depth > 0 else ""
    page_key = get_page_key(file_path)

    # 1. Clean out stray </main> tags that sit right after <section id="header">
    content = re.sub(r'</main>\s*<main', '<main', content, flags=re.IGNORECASE)

    # 2. Replace Header tag
    header_html = generate_header_html(prefix, page_key)
    if re.search(r'<(section|header)[^>]*id=["\']header["\'][^>]*>.*?</\1>', content, flags=re.DOTALL | re.IGNORECASE):
        content = re.sub(
            r'<(section|header)[^>]*id=["\']header["\'][^>]*>.*?</\1>',
            header_html,
            content,
            flags=re.DOTALL | re.IGNORECASE
        )
    elif "<body" in content:
        # Insert after <body>
        body_match = re.search(r"<body[^>]*>", content, re.IGNORECASE)
        insert_pos = body_match.end()
        content = content[:insert_pos] + "\n" + header_html + "\n" + content[insert_pos:]

    # 3. Replace Footer tag
    footer_html = generate_footer_html(prefix)
    if re.search(r'<footer[^>]*>.*?</footer>', content, flags=re.DOTALL | re.IGNORECASE):
        content = re.sub(
            r'<footer[^>]*>.*?</footer>',
            footer_html,
            content,
            flags=re.DOTALL | re.IGNORECASE
        )
    elif "</body>" in content:
        content = content.replace("</body>", f"\n{footer_html}\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Restored full header/footer markup for: {rel_path}")

def main():
    count = 0
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))
                count += 1
    print(f"Finished processing {count} HTML files.")

if __name__ == "__main__":
    main()
