import os
from pathlib import Path

SHOP_DIR = Path(r"c:\Users\LENOVO\Downloads\Portfolio pieces\Sara\frontend\pages\shop")

DARK_RULES = {
    "footware-collection.html": """
        [data-theme="dark"], body.dark, body[data-theme="dark"] {
            background-color: #0f172a !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .footwear-hero, body.dark .footwear-hero {
            background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.85)), url("../../images/banner/b18.jpg") center/cover no-repeat !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .footwear-badge, body.dark .footwear-badge {
            background: #1e293b !important;
            color: #38bdf8 !important;
        }
        [data-theme="dark"] .pro, body.dark .pro {
            background: #1e293b !important;
            border-color: #334155 !important;
            color: #f3f4f6 !important;
        }
    """,
    "tshirt.html": """
        [data-theme="dark"], body.dark, body[data-theme="dark"] {
            background-color: #0f172a !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .tshirt-hero, body.dark .tshirt-hero {
            background: linear-gradient(120deg, #0f172a, #1e1b4b) !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .tshirt-badge, body.dark .tshirt-badge {
            background: #1e293b !important;
            color: #a78bfa !important;
        }
        [data-theme="dark"] .tshirt-content h1, body.dark .tshirt-content h1 {
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .pro, body.dark .pro {
            background: #1e293b !important;
            border-color: #334155 !important;
            color: #f3f4f6 !important;
        }
    """,
    "winter-sale.html": """
        [data-theme="dark"], body.dark, body[data-theme="dark"] {
            background-color: #0f172a !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .winter-hero, body.dark .winter-hero {
            background: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.85)), url("../../images/banner/b7.jpg") center/cover no-repeat !important;
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .winter-badge, body.dark .winter-badge {
            background: #1e293b !important;
            color: #2dd4bf !important;
        }
        [data-theme="dark"] .winter-hero-content h1, body.dark .winter-hero-content h1 {
            color: #f3f4f6 !important;
        }
        [data-theme="dark"] .pro, body.dark .pro {
            background: #1e293b !important;
            border-color: #334155 !important;
            color: #f3f4f6 !important;
        }
    """
}

def main():
    for filename, rules in DARK_RULES.items():
        file_path = SHOP_DIR / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if "</style>" in content and "[data-theme=\"dark\"]" not in content:
                content = content.replace("</style>", f"{rules}\n</style>")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Added dark theme rules to: {filename}")

if __name__ == "__main__":
    main()
