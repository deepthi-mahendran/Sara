import os
import re
from pathlib import Path

FRONTEND_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend")

BANNER_READABILITY_CSS = """
/* ============================================================
   BANNER READABILITY & HIGH CONTRAST OVERLAY (Light & Dark Theme)
   ============================================================ */
#sm-banner .banner-box,
#banner3 .banner-box,
.banner-box {
    position: relative;
    overflow: hidden;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

#sm-banner .banner-box::before,
#banner3 .banner-box::before,
.banner-box::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(15, 14, 23, 0.68) 0%, rgba(15, 14, 23, 0.45) 100%);
    z-index: 1;
    border-radius: 14px;
    pointer-events: none;
}

#sm-banner .banner-box > *,
#banner3 .banner-box > *,
.banner-box > * {
    position: relative;
    z-index: 2;
}

#sm-banner h4,
#sm-banner h2,
#sm-banner span,
#banner3 h2,
.banner-box h2,
.banner-box h4 {
    color: #ffffff !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7) !important;
}

#sm-banner h2,
#banner3 h2,
.banner-box h2 {
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}

#banner3 h3,
.banner-box h3 {
    color: #ED9AE9 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7) !important;
    margin-bottom: 12px !important;
}

#sm-banner .banner-box button.white,
#banner3 .banner-box button.white,
.banner-box button.white,
.banner-box button {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #ffffff !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 22px !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
    text-decoration: none !important;
}

#sm-banner .banner-box button.white:hover,
#banner3 .banner-box button.white:hover,
.banner-box button.white:hover,
.banner-box button:hover {
    background-color: #C483E6 !important;
    color: #ffffff !important;
    border-color: #C483E6 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(196, 131, 230, 0.45) !important;
}
"""

def apply_banner_readability():
    css_files = [
        FRONTEND_DIR / "css" / "style.css",
        FRONTEND_DIR / "css" / "global.css",
        FRONTEND_DIR / "css" / "index.css",
        FRONTEND_DIR / "css" / "bundle.css",
        FRONTEND_DIR / "css" / "style.min.css"
    ]

    for file_path in css_files:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "BANNER READABILITY & HIGH CONTRAST OVERLAY" not in content:
                content += "\n" + BANNER_READABILITY_CSS
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Applied banner readability fixes in: {file_path.name}")

if __name__ == "__main__":
    apply_banner_readability()
