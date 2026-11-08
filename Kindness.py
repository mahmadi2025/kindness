#!/usr/bin/env python3
"""
Kindness for Afghans – static site builder.
Supports:
  - Canadian Banking (Interac e-Transfer, Wire Transfer)
  - Zeffy (0% fee donations) + QR Code
  - GitHub Automation (auto-push)
  - Custom Domain (CNAME generation)
  - Blog/News section
  - Home Page Slideshow
"""

import argparse
import importlib
import subprocess
import shutil
import os
from pathlib import Path
import time
import random
import stat

# Optional: Pillow for image processing (if used for complex generation)
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

# --- Configuration: News/Blog Posts ---
NEWS_POSTS = [
    {
        "date": "2026-07-26",
        "title": "Field Activity & Transparency Report: AFN 41,200 Distributed in Direct Aid",
        "content": """
<p>We are grateful to report the successful completion of our latest direct humanitarian assistance initiative in Afghanistan. Totaling <strong>AFN 41,200</strong> in donor funds, assistance was deployed directly on the ground to address urgent, life-threatening needs:</p>
<ul style="line-height: 1.8; margin: 15px 0 15px 20px;">
  <li><strong>Medical Assistance (AFN 12,000):</strong> Financial aid provided to a female beneficiary to cover part of the cost of a critical surgical operation at a local hospital.</li>
  <li><strong>Emergency Food Relief (AFN 23,220):</strong> Essential food packages purchased and distributed directly to six vulnerable families to meet their immediate nutritional needs and alleviate hardship.</li>
  <li><strong>Essential Medicines (AFN 5,470):</strong> Life-essential prescription medicines purchased and provided to two vulnerable patients requiring urgent medical treatment.</li>
  <li><strong>Transportation and Delivery (AFN 510):</strong> Direct transport costs incurred to deliver food assistance directly to the recipient families.</li>
</ul>
<p><strong>Governance & Transparency:</strong> All expenditures were carried out under our formal agency agreement and are fully supported by vendor receipts, beneficiary lists with thumbprints, and field video documentation. Thank you to our generous donors for making this life-changing assistance possible!</p>
""".strip()
    },
    {
        "date": "2025-10-15",
        "title": "Winter Distribution Begins",
        "content": "<p>Thanks to your generous support, we have started distributing warm clothing and heating supplies to 50 families in Kabul.</p>"
    },
    {
        "date": "2025-05-20",
        "title": "Launch of Kindness for Afghans",
        "content": "<p>We are proud to announce the official launch of our direct support initiative.</p>"
    }
]


def build_css() -> str:
    return """
/* kindnessforafghans.org — minimal responsive CSS */
:root {
  --bg: #ffffff;
  --text: #333333;
  --primary: #0077cc; /* Updated brand color */
  --accent: #00aa88;
  --light-gray: #f4f4f4;
  --border: #dddddd;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: var(--text);
  margin: 0;
  padding: 0;
  background: var(--bg);
}
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}
/* Header */
.header {
  border-bottom: 1px solid var(--border);
  padding: 20px 0;
  margin-bottom: 40px;
}
.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 15px;
  text-decoration: none;
  color: var(--text);
}
.brand img {
  height: 50px;
  width: auto;
}
.brand h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}
.nav {
  display: flex;
  gap: 20px;
}
.nav a {
  text-decoration: none;
  color: var(--text);
  font-weight: 500;
}
.nav a:hover, .nav a.active {
  color: var(--primary);
}
.btn {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}
.btn:hover {
  background: #005fa3;
}
/* Sections */
.hero {
  text-align: center;
  padding: 60px 20px;
  background: var(--light-gray);
  border-radius: 12px;
  margin-bottom: 40px;
  position: relative; /* For slideshow overlap if needed */
  overflow: hidden;
}
.hero h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  line-height: 1.2;
}
.content {
  margin-bottom: 60px;
}
.section-title {
  border-bottom: 2px solid var(--primary);
  display: inline-block;
  margin-bottom: 20px;
  padding-bottom: 5px;
}

/* Slideshow */
.slideshow-container {
  width: 100%;
  max-width: 800px;
  height: 300px; /* Reduced from 400px */
  margin: 0 auto 40px auto;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  background: #eee;
}
@media (max-width: 600px) {
  .slideshow-container { height: 180px; } /* Smaller on mobile */
}
.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}
.slide.active {
  opacity: 1;
}
.slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Donation Methods */
.donation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 30px;
}
.method-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 25px;
  background: white;
}
.method-card h3 {
  margin-top: 0;
  color: var(--primary);
  border-bottom: 1px solid var(--light-gray);
  padding-bottom: 10px;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  border-bottom: 1px dashed #eee;
  padding-bottom: 5px;
}
.detail-label {
  font-weight: 600;
  color: #666;
}
.detail-value {
  text-align: right;
  font-family: monospace;
  font-size: 1.1em;
}
/* QR Code */
.qr-container {
    text-align: center;
    margin-top: 15px;
}
.qr-container img {
    max-width: 150px;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 5px;
}

/* News */
.news-list { display: flex; flex-direction: column; gap: 40px; }
.news-item { padding-bottom: 40px; border-bottom: 1px solid var(--border); }
.news-item:last-child { border-bottom: none; }
.news-meta { color: #666; font-size: 0.9rem; display: block; margin-bottom: 5px; }
.news-title { margin: 0 0 15px 0; color: var(--text); font-size: 1.5rem; }
.news-content { line-height: 1.8; }
.news-empty { text-align: center; color: #888; font-style: italic; padding: 40px; }
/* Footer */
.footer {
  margin-top: 60px;
  border-top: 1px solid var(--border);
  padding: 40px 0;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}
@media (max-width: 600px) {
  .header .container { flex-direction: column; text-align: center; }
  .nav { margin-top: 10px; }
  .detail-row { flex-direction: column; text-align: left; }
  .detail-value { text-align: left; margin-top: 2px; }
  .slideshow-container { height: 250px; }
}
"""


def build_nav(active: str) -> str:
    links = {
        "home": ("Home", "index.html"),
        "donate": ("Donate", "donate.html"),
        "news": ("News", "news.html"),
    }
    items = []
    for key, (label, url) in links.items():
        cls = ' class="active"' if key == active else ""
        items.append(f'<a href="{url}"{cls}>{label}</a>')
    return "\n".join(items)


def build_slideshow_html(image_files: list) -> str:
    if not image_files:
        return ""
    
    slides = []
    for i, img_path in enumerate(image_files):
        active_class = " active" if i == 0 else ""
        # img_path is relative to assets/slideshow/
        slides.append(f"""
        <div class="slide{active_class}">
            <img src="{img_path}" alt="Slide {i+1}">
        </div>
        """)
    
    script = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        let slides = document.querySelectorAll(".slide");
        let current = 0;
        if (slides.length > 1) {
            setInterval(function() {
                slides[current].classList.remove("active");
                current = (current + 1) % slides.length;
                slides[current].classList.add("active");
            }, 4000); // Change image every 4 seconds
        }
    });
    </script>
    """
    
    return f"""
    <div class="slideshow-container">
        {''.join(slides)}
    </div>
    {script}
    """


def build_home_html(name: str, logo_src: str = "assets/heart.svg", slideshow_images: list = None) -> str:
    nav_html = build_nav("home")
    
    slideshow_html = ""
    if slideshow_images:
        slideshow_html = build_slideshow_html(slideshow_images)
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{name} — Dignity through direct support</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
<header class="header">
  <div class="container">
    <div class="brand">
      <img src="{logo_src}" alt="Logo" />
      <h1>{name}</h1>
    </div>
    <nav class="nav">
      {nav_html}
    </nav>
  </div>
</header>

<main class="container">
  {slideshow_html}

  <section class="hero">
    <h2>Dignity through direct support.</h2>
    <p>We provide food, heating, and essential supplies directly to families in need across Afghanistan.</p>
    <br/>
    <a href="donate.html" class="btn">Make a Donation</a>
  </section>

  <section class="content">
    <h3 class="section-title">Latest Direct Impact</h3>
    <p>
      In July 2026, <strong>Kindness for Afghans</strong> completed another direct aid mission, deploying <strong>AFN 41,200</strong> in emergency relief directly on the ground:
    </p>
    <ul style="line-height: 1.8; margin-left: 20px;">
      <li><strong>Emergency Surgery:</strong> Financial assistance for a critical hospital surgery for a vulnerable female patient.</li>
      <li><strong>Food Packages:</strong> Essential food rations delivered directly to 6 vulnerable households.</li>
      <li><strong>Prescription Medicines:</strong> Urgent medication supplied to 2 patients requiring continuous treatment.</li>
    </ul>
    <p style="margin-top: 15px;">
      <a href="news.html" style="font-weight: 600; color: var(--primary); text-decoration: none;">Read the full July 2026 Field Report &rarr;</a>
    </p>
  </section>

  <section class="content">
    <h3 class="section-title">Our Mission</h3>
    <p>
      At <strong>Kindness for Afghans</strong>, our mission is to bring hope and relief to the most vulnerable families in Afghanistan, including widows, orphans, and households without income. We collect charitable donations from Canada, the United States, and other countries to provide food and essential supplies to individuals and families in urgent need.
    </p>
    <p>
      Our dedicated team operates within Afghanistan, working directly with local communities to identify families in crisis and deliver immediate assistance. This hands-on approach helps ensure that contributions reach those most in need.
    </p>
    <p>
      Kindness for Afghans is a registered charity in Ontario, Canada (Ontario Corporation Number: <strong>1001294785</strong>).
    </p>
    <p class="mission-note">
       We accept donations via Interac e-Transfer (Canada), Zeffy (online), and international wire transfer. Every contribution, regardless of size, makes a meaningful difference.
    </p>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <p>&copy; 2025–2026 {name}. All rights reserved.</p>
    <p>Contact us: <a href="mailto:info@kindnessforafghans.org">info@kindnessforafghans.org</a></p>
  </div>
</footer>
</body>
</html>
""".strip()


def build_donate_html(
    name: str,
    # Canadian/International Options
    interac_email: str = None,
    zeffy_link: str = None,
    zeffy_qr_src: str = None,
    bank_account: str = None,
    transit_number: str = None,
    institution_number: str = None,
    swift_bic: str = None,
    bank_name: str = None,
    wire_contact: bool = False, # New Flag
    # European Options
    iban: str = None,
    bic: str = None,
    # Common
    reference: str = None,
    logo_src: str = "assets/heart.svg"
) -> str:
    nav_html = build_nav("donate")

    # --- Construct Payment Sections ---
    payment_sections = []

    # 1. Zeffy (Primary Online Method)
    if zeffy_link:
        # ... (Zeffy code remains same) ...
        qr_html = ""
        if zeffy_qr_src:
            qr_html = f"""
            <div class="qr-container">
                <img src="{zeffy_qr_src}" alt="Scan to Donate via Zeffy">
                <p style="font-size:0.8rem; color:#666;">Scan to Donate</p>
            </div>
            """
            
        full_link = zeffy_link if zeffy_link.startswith('http') else f"https://{zeffy_link}"

        payment_sections.append(f"""
        <div class="method-card">
          <h3>Donate Online (Zeffy)</h3>
          <p>Secure online donation with <strong>0% platform fees</strong>.</p>
          <div style="text-align: center; margin-top: 20px;">
            <a href="{full_link}" target="_blank" class="btn">Donate Securely</a>
            {qr_html}
            <p style="margin-top: 10px; font-size: 0.9em;">Credit Card and other methods accepted.</p>
          </div>
        </div>
        """)

    # 2. Interac e-Transfer (Canada)
    if interac_email:
        payment_sections.append(f"""
        <div class="method-card">
          <h3>Interac e-Transfer <small>(Canada)</small></h3>
          <p>The fastest way to donate from a Canadian bank account.</p>
          <div class="detail-row">
            <span class="detail-label">Send to Email:</span>
            <span class="detail-value">{interac_email}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Message/Note:</span>
            <span class="detail-value">Donation for {name}</span>
          </div>
        </div>
        """)

    # 3. Bank Transfer (Wire / Direct Deposit)
    if wire_contact:
        payment_sections.append(f"""
        <div class="method-card">
          <h3>Wire Transfer</h3>
          <p>For international wire transfer details, please contact us directly.</p>
          <div style="text-align: center; margin-top: 15px;">
             <a href="mailto:info@kindnessforafghans.org" class="btn" style="background:#555">Email Us</a>
          </div>
        </div>
        """)
    elif bank_account and transit_number and institution_number:
        # Canadian Format
        section = f"""
        <div class="method-card">
          <h3>Direct Deposit / Wire</h3>
          <div class="detail-row">
            <span class="detail-label">Bank Name:</span>
            <span class="detail-value">{bank_name or 'N/A'}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Account Number:</span>
            <span class="detail-value">{bank_account}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Transit No.:</span>
            <span class="detail-value">{transit_number}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Institution No.:</span>
            <span class="detail-value">{institution_number}</span>
          </div>
        """
        if swift_bic:
             section += f"""
             <div class="detail-row">
                <span class="detail-label">SWIFT/BIC:</span>
                <span class="detail-value">{swift_bic}</span>
             </div>
             """
        section += "</div>"
        payment_sections.append(section)
    
    # 4. European SEPA (Fallback or if specifically requested)
    elif iban:
        section = f"""
        <div class="method-card">
          <h3>Bank Transfer (SEPA/EU)</h3>
          <div class="detail-row">
            <span class="detail-label">IBAN:</span>
            <span class="detail-value">{iban}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">BIC:</span>
            <span class="detail-value">{bic}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Reference:</span>
            <span class="detail-value">{reference}</span>
          </div>
        </div>
        """
        payment_sections.append(section)

    if not payment_sections:
        content_area = "<p>No payment details configured.</p>"
    else:
        content_area = f'<div class="donation-grid">{"".join(payment_sections)}</div>'

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Donate — {name}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
<header class="header">
  <div class="container">
    <div class="brand">
      <img src="{logo_src}" alt="Logo" />
      <h1>{name}</h1>
    </div>
    <nav class="nav">
      {nav_html}
    </nav>
  </div>
</header>

<main class="container">
  <section class="hero" style="background: transparent; padding: 40px 0 20px;">
    <h2>Support Our Work</h2>
    <p>Your contribution directly impacts lives. Choose your preferred method below.</p>
  </section>
  
  {content_area}
  
  <div style="margin-top: 40px; background: #fffbe6; padding: 20px; border-radius: 8px; border: 1px solid #ffe58f; text-align: center; color: #856404;">
    <p><strong>Transparency Note:</strong> We are currently operating as a non-profit while our registered charity application is being processed. While this means we cannot provide tax-deductible receipts just yet, please know that 100% of your support goes directly toward our mission.</p>
  </div>

  <div style="margin-top: 60px; text-align: center; color: #666;">
    <p>Thank you for your kindness and trust.</p>
  </div>
</main>

<footer class="footer">
  <div class="container">
    <p>&copy; 2025–2026 {name}. All rights reserved.</p>
    <p>Contact: info@kindnessforafghans.org</p>
  </div>
</footer>
</body>
</html>
""".strip()


def build_news_html(name: str, posts: list, logo_src: str = "assets/heart.svg") -> str:
    nav_html = build_nav("news")
    if not posts:
        content = '<div class="news-empty">No news posts yet. Check back soon!</div>'
    else:
        post_items = []
        for post in posts:
            post_items.append(f"""
        <article class="news-item">
          <span class="news-meta">{post['date']}</span>
          <h2 class="news-title">{post['title']}</h2>
          <div class="news-content">{post['content']}</div>
        </article>
            """.strip())
        content = '<div class="news-list">' + "\n".join(post_items) + '</div>'

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>News — {name}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
<header class="header">
  <div class="container">
    <div class="brand">
      <img src="{logo_src}" alt="Logo" />
      <h1>{name}</h1>
    </div>
    <nav class="nav">
      {nav_html}
    </nav>
  </div>
</header>
<main class="container">
  <section class="hero" style="background: transparent; padding: 40px 0 20px;">
    <h2>Latest Updates</h2>
    <p>Stories from the field and transparency reports.</p>
  </section>
  {content}
</main>
<footer class="footer">
  <div class="container">
    <p>&copy; 2025–2026 {name}. All rights reserved.</p>
    <p>Contact: info@kindnessforafghans.org</p>
  </div>
</footer>
</body>
</html>
    """.strip()

def handle_remove_readonly(func, path, exc):
    """Clear the readonly bit and reattempt the removal"""
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def force_delete(path):
    """Robustly delete a directory or file, dealing with Windows locks."""
    path = Path(path)
    if not path.exists():
        return

    # Try simple DELETE first
    for i in range(3):
        try:
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path, onerror=handle_remove_readonly)
            return
        except PermissionError:
            print(f"  ... file locked, retrying ({i+1}/3)...")
            time.sleep(0.5)
        except Exception as e:
            print(f"  ... error deleting {path}: {e}")
            break
            
    # If still exists, try MOVING it out of the way
    if path.exists():
        # Don't rename if it's already trash (prevents zzz_trash_zzz_trash...)
        if path.name.startswith("zzz_trash"):
            print(f"⚠️ Locked trash file '{path.name}' could not be deleted. Skipping.")
            return

        try:
            new_name = path.parent / f"zzz_trash_{path.name}_{random.randint(1000,9999)}"
            path.rename(new_name)
            print(f"⚠️ Could not delete '{path}', renamed to '{new_name.name}' to continue.")
        except Exception as e:
            print(f"❌ CRITICAL: Could not delete or move '{path}': {e}")
            raise

def run_git_automation(target_dir: Path):
    """Adds, commits, and pushes changes to GitHub."""
    print("\n--- GitHub Automation ---")
    try:
        # Check status
        print("Running: git add .")
        subprocess.run(["git", "add", "."], cwd=target_dir, check=True)
        
        print('Running: git commit -m "Update site via Kindness.py"')
        # We allow commit to fail if there are no changes to commit
        subprocess.run(["git", "commit", "-m", "Update site via Kindness.py"], cwd=target_dir)
        
        print("Running: git push --force")
        subprocess.run(["git", "push", "--force"], cwd=target_dir, check=True)
        
        print("✅ Successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
    except FileNotFoundError:
        print("❌ Error: 'git' command not found. Is Git installed?")


def main():
    parser = argparse.ArgumentParser(description="Generate Kindness for Afghans Static Site")
    # General
    parser.add_argument("--name", default="Kindness for Afghans", help="Organization name")
    parser.add_argument("--out", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--logo", default="branding/Kindness Logo English.png", help="Path to custom logo image file (optional).")
    parser.add_argument("--photos", default="website_photos", help="Path to folder containing slideshow images")
    
    # Canadian / International
    parser.add_argument("--interac", default="info@kindnessforafghans.org", help="Email for Interac e-Transfer")
    parser.add_argument("--zeffy", default="https://www.zeffy.com/en-CA/donation-form/donate-to-change-lives-6250", help="Zeffy Donation Link")
    parser.add_argument("--zeffy-qr", default="assets/zeffy_qr.png", help="Path to Zeffy QR Code Image")
    
    parser.add_argument("--bank-account", help="Bank Account Number")
    parser.add_argument("--transit", help="Bank Transit Number (5 digits)")
    parser.add_argument("--institution", help="Bank Institution Number (3 digits)")
    parser.add_argument("--swift", help="SWIFT/BIC Code (for international wire)")
    parser.add_argument("--bank-name", help="Name of the Bank")
    parser.add_argument("--wire-contact", action="store_true", default=True, help="Show 'Contact us for Wire' instead of details")
    
    # Legacy / European
    parser.add_argument("--iban", help="IBAN for SEPA")
    parser.add_argument("--bic", help="BIC for SEPA")
    parser.add_argument("--reference", default="Donation", help="Payment reference")
    
    # Automation & Config
    parser.add_argument("--github", action="store_true", help="Automatically git add/commit/push after generation")
    parser.add_argument("--cname", default="kindnessforafghans.org", help="Custom domain (e.g., kindnessforafghans.org) to create CNAME file")

    args = parser.parse_args()

    out = Path(args.out)
    assets = out / "assets"
    
    # Safe protection list so build never wipes out source/governance/media files
    PROTECTED_ITEMS = {
        "legal_and_governance",
        "field_reports",
        "branding",
        "website_photos",
        "Kindness.py",
        ".gitignore",
        ".git",
        "CNAME",
    }

    # Create directories safely
    is_current_dir = out.resolve() == Path.cwd().resolve()
    if is_current_dir:
        # Target is current directory: preserve source, governance, and repository files
        pass
    elif out.exists():
        if (out / ".git").exists():
            for item in out.iterdir():
                if item.name not in PROTECTED_ITEMS and item.name != ".git":
                    force_delete(item)
        else:
            force_delete(out)
            out.mkdir(parents=True)
    else:
        out.mkdir(parents=True)

    assets.mkdir(parents=True, exist_ok=True)
    print(f"Generating site in: {out.resolve()}")

    # Handle CNAME
    if args.cname:
        (out / "CNAME").write_text(args.cname, encoding="utf-8")
        print(f"✅ CNAME created for: {args.cname}")

    # Handle Logo
    logo_filename = "heart.svg"
    if args.logo:
        logo_path = Path(args.logo)
        if logo_path.exists():
            dest_name = f"logo{logo_path.suffix}"
            dest_file = assets / dest_name
            if logo_path.resolve() != dest_file.resolve():
                shutil.copy(logo_path, dest_file)
            logo_filename = dest_name
            print(f"✅ Custom logo configured: {dest_name}")
        else:
            print(f"⚠️ Warning: Logo file not found at {args.logo}, checking fallback.")
            args.logo = None

    if not args.logo:
        if (assets / "logo.png").exists():
            logo_filename = "logo.png"
        else:
            # Default Logo placeholder
            (assets / "heart.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0b6"><path d="M12 21s-6.716-4.237-9.33-6.85C-1.06 12.61.11 8.73 3.2 7.19c2.19-1.08 4.7-.3 6.03 1.24C10.1 7.07 12.6 6.3 14.79 7.38c3.09 1.55 4.26 5.43.53 6.96C18.716 16.763 12 21 12 21z"/></svg>',
                encoding="utf-8"
            )

    logo_web_path = f"assets/{logo_filename}"
    
    # Handle Slideshow Images
    slideshow_images = []
    if args.photos:
        photo_dir = Path(args.photos)
        if photo_dir.exists() and photo_dir.is_dir():
            slideshow_dir = assets / "slideshow"
            slideshow_dir.mkdir(exist_ok=True)
            
            # Supported extensions
            extensions = {".jpg", ".jpeg", ".png", ".webp"}
            
            for f in sorted(photo_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in extensions:
                    dest = slideshow_dir / f.name
                    if f.resolve() != dest.resolve():
                        shutil.copy(f, dest)
                    slideshow_images.append(f"assets/slideshow/{f.name}")
            
            print(f"✅ Slideshow: Loaded {len(slideshow_images)} images.")
        else:
            print(f"⚠️ Warning: Photo directory not found: {args.photos}")

    # Handle Zeffy QR
    zeffy_qr_web_path = None
    if args.zeffy_qr:
        qr_path = Path(args.zeffy_qr)
        if qr_path.exists():
            dest = assets / "zeffy_qr.png"
            if qr_path.resolve() != dest.resolve():
                shutil.copy(qr_path, dest)
            zeffy_qr_web_path = "assets/zeffy_qr.png"
            print("✅ Zeffy QR code configured: zeffy_qr.png")
        else:
             print(f"⚠️ Warning: QR Code file not found at {args.zeffy_qr}")

    today_version = int(time.time())

    # Write Pages
    (out / "styles.css").write_text(build_css(), encoding="utf-8")
    
    (out / "index.html").write_text(
        build_home_html(args.name, logo_src=logo_web_path, slideshow_images=slideshow_images).replace("styles.css", f"styles.css?v={today_version}"), 
        encoding="utf-8"
    )

    (out / "donate.html").write_text(
        build_donate_html(
            name=args.name,
            interac_email=args.interac,
            zeffy_link=args.zeffy,
            zeffy_qr_src=zeffy_qr_web_path,
            bank_account=None if args.wire_contact else args.bank_account, # Hide details if contact mode
            transit_number=args.transit,
            institution_number=args.institution,
            swift_bic=args.swift,
            bank_name=args.bank_name,
            wire_contact=args.wire_contact, # Pass new flag
            iban=args.iban,
            bic=args.bic,
            reference=args.reference,
            logo_src=logo_web_path
        ).replace("styles.css", f"styles.css?v={today_version}"),
        encoding="utf-8"
    )
    
    (out / "news.html").write_text(
        build_news_html(args.name, NEWS_POSTS, logo_src=logo_web_path).replace("styles.css", f"styles.css?v={today_version}"), 
        encoding="utf-8"
    )

    print("✅ Site generated successfully:")
    print(f"  - {out / 'index.html'}")
    print(f"  - {out / 'donate.html'}")
    print(f"  - {out / 'news.html'}")

    # Create .gitignore if not present, ensuring privacy rules
    gitignore_path = out / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(
            "legal_and_governance/\nfield_reports/\n*.pdf\n*.docx\n*.mp4\nzzz_trash*\n__pycache__\n*.pyc\n",
            encoding="utf-8"
        )

    # GitHub Automation
    if args.github:
        run_git_automation(out)

if __name__ == "__main__":
    main()
