#!/usr/bin/env python3
"""
Kindness for Afghans – static site builder & asset optimization pipeline.
Registered Ontario Not-for-Profit Corporation (OCN: 1001294785).

Supports:
  - Automated Pillow image optimization (slashing raw photos from 7MB to ~350KB)
  - Automatic Favicon generation (.ico and .png) from brand emblem
  - Elevated humanitarian responsive CSS design with official emerald green (#1b4c36) & warm amber CTAs
  - 100% Direct Relief trust guarantee & Ontario corporate governance badges
  - 4 Tangible Giving Tiers on donate page ($35 food parcel, $75 winter warmth, $150 medicine, $300 surgery)
  - Interactive 1-click clipboard copy for Interac e-Transfer
  - Interactive donor FAQ accordion with full transparency on CRA agency agreement
  - SEO Open Graph / Twitter Card social preview tags & Schema.org JSON-LD structured data
  - Responsive slideshow with dot navigation, next/prev arrows, touch swipe, and captions
  - Zero-fee donations via Zeffy + QR code & Canadian Interac e-Transfer
  - GitHub Automation (auto-push) & custom domain CNAME generation
"""

import argparse
import subprocess
import shutil
import os
from pathlib import Path
import time
import random
import stat

# Optional: Pillow for image optimization and favicon generation
try:
    from PIL import Image
except ImportError:
    Image = None

# --- Configuration: News & Transparency Field Posts ---
NEWS_POSTS = [
    {
        "date": "2026-08-30",
        "category": "Financial Reconciliation",
        "title": "Kabul Aid Remittance Audit: AFN 122,700 ($2,836 CAD) Reconciled to TD Bank",
        "summary": "100% reconciliation between Canadian TD Bank remittances ($2,836 CAD) and on-the-ground cash distributions in Kabul across three humanitarian relief missions.",
        "content": """
<p>In accordance with our commitment to absolute financial transparency and CRA direction-and-control standards, we are pleased to report that cumulative humanitarian aid transferred to Kabul has reached <strong>AFN 122,700 ($2,836 CAD)</strong> across three direct relief missions:</p>
<ul style="line-height: 1.85; margin: 15px 0 15px 22px;">
  <li><strong>Spring 2026 Mission (TD Debit $912 CAD):</strong> <strong>AFN 40,000</strong> remitted and deployed directly for emergency family food relief.</li>
  <li><strong>Summer 2026 Mission (TD Debit $962 CAD):</strong> <strong>AFN 41,200</strong> deployed for a critical female patient surgery (AFN 12,000), food hampers for 6 families (AFN 23,220), and prescription medicines (AFN 5,470).</li>
  <li><strong>Late Summer 2026 Mission (TD Debit $962 CAD):</strong> <strong>AFN 41,500</strong> remitted and deployed for urgent family sustenance and medical relief.</li>
</ul>
<div style="background: #f0f7f3; border-left: 4px solid #1b4c36; padding: 14px 18px; margin: 20px 0; border-radius: 4px;">
  <p style="margin: 0; font-size: 0.95rem; color: #123425;">
    <strong>TD Bank & MoneyGram Three-Way Audit Match:</strong> Every single remittance (Apr 20: $912.00, May 20: $962.00, Aug 24: $962.00) matches our official Canadian TD Bank statement debits to the exact penny, with 0% platform or administrative fee deductions. Thank you to our donors for making this direct impact possible!
  </p>
</div>
""".strip()
    },
    {
        "date": "2026-07-26",
        "category": "Field Report",
        "title": "Field Activity & Transparency Report: AFN 41,200 Distributed in Direct Aid",
        "summary": "Full expenditure and distribution report covering emergency surgical assistance, food packages for 6 families, and prescription medicines in Kabul.",
        "content": """
<p>We are grateful to report the successful completion of our latest direct humanitarian assistance initiative in Afghanistan. Totaling <strong>AFN 41,200</strong> in donor funds, assistance was deployed directly on the ground to address urgent, life-threatening needs:</p>
<ul style="line-height: 1.85; margin: 15px 0 15px 22px;">
  <li><strong>Medical Assistance (AFN 12,000):</strong> Financial aid provided to a female beneficiary to cover part of the cost of a critical surgical operation at a local hospital.</li>
  <li><strong>Emergency Food Relief (AFN 23,220):</strong> Essential food packages purchased and distributed directly to six vulnerable families to meet their immediate nutritional needs and alleviate hardship.</li>
  <li><strong>Essential Medicines (AFN 5,470):</strong> Life-essential prescription medicines purchased and provided to two vulnerable patients requiring urgent medical treatment.</li>
  <li><strong>Transportation and Delivery (AFN 510):</strong> Direct transport costs incurred to deliver food assistance directly to recipient families.</li>
</ul>
<div style="background: #f0f7f3; border-left: 4px solid #1b4c36; padding: 14px 18px; margin: 20px 0; border-radius: 4px;">
  <p style="margin: 0; font-size: 0.95rem; color: #123425;">
    <strong>Governance & Transparency Verification:</strong> All expenditures were carried out under our formal CRA-compliant Agency Agreement and are 100% supported by itemized vendor receipts, beneficiary distribution sign-off lists with thumbprints, and field video documentation. Thank you to our generous donors for making this direct assistance possible!
  </p>
</div>
""".strip()
    },
    {
        "date": "2025-10-15",
        "category": "Winter Relief",
        "title": "Winter Distribution Campaign Begins in Kabul",
        "summary": "Providing warm clothing, blankets, and heating supplies to vulnerable families facing freezing temperatures.",
        "content": """
<p>As winter temperatures approach sub-zero levels in Kabul, Kindness for Afghans has initiated its 2025 Winter Relief distribution. Thanks to your generous support, warm clothing, heavy blankets, and heating fuels are being delivered directly to 50 vulnerable families, widows, and orphans facing extreme seasonal hardship.</p>
""".strip()
    },
    {
        "date": "2025-05-20",
        "category": "Milestone",
        "title": "Official Launch of Kindness for Afghans",
        "summary": "Incorporation as an Ontario Not-for-Profit Corporation dedicated to direct, transparent relief.",
        "content": """
<p>We are proud to announce the official launch and incorporation of <strong>Kindness for Afghans</strong> as a registered Ontario Not-for-Profit Corporation (OCN: 1001294785). Founded by dedicated volunteers in Canada, our mission is to eliminate administrative overhead and deliver 100% of charitable donations directly into the hands of those who need it most.</p>
""".strip()
    }
]

# Captions for homepage slideshow imagery
SLIDESHOW_CAPTIONS = [
    "Delivering hope and emergency relief directly to vulnerable households in local communities.",
    "Providing food parcels, warmth, and winter heating to widows and families facing severe hardship.",
    "100% direct humanitarian aid: essential food staples, emergency surgeries, and medicines."
]

COPY_INTERAC_SCRIPT = """
<script>
function copyInteracEmail() {
  const email = "info@kindnessforafghans.org";
  const btn = document.getElementById("copyBtn");
  
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(email).then(onSuccess).catch(fallbackCopy);
  } else {
    fallbackCopy();
  }

  function fallbackCopy() {
    const textArea = document.createElement("textarea");
    textArea.value = email;
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      onSuccess();
    } catch (err) {
      btn.innerText = "Copy manually";
    }
    document.body.removeChild(textArea);
  }

  function onSuccess() {
    btn.innerText = "Copied! ✓";
    btn.classList.add("copied");
    setTimeout(function() {
      btn.innerText = "Copy Email";
      btn.classList.remove("copied");
    }, 2500);
  }
}
</script>
""".strip()

SLIDESHOW_SCRIPT = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    let slides = document.querySelectorAll(".slide");
    let dots = document.querySelectorAll(".slide-dot");
    let prevBtn = document.querySelector(".slide-prev");
    let nextBtn = document.querySelector(".slide-next");
    let container = document.querySelector(".slideshow-wrapper");
    let current = 0;
    let timer = null;

    function showSlide(index) {
        if (!slides.length) return;
        slides.forEach(function(s) { s.classList.remove("active"); });
        dots.forEach(function(d) { d.classList.remove("active"); });
        current = (index + slides.length) % slides.length;
        slides[current].classList.add("active");
        if (dots[current]) dots[current].classList.add("active");
    }

    function nextSlide() { showSlide(current + 1); }
    function prevSlide() { showSlide(current - 1); }

    function startTimer() {
        if (!timer && slides.length > 1) {
            timer = setInterval(nextSlide, 4500);
        }
    }
    function stopTimer() {
        if (timer) { clearInterval(timer); timer = null; }
    }

    if (slides.length > 1) {
        startTimer();
        if (container) {
            container.addEventListener("mouseenter", stopTimer);
            container.addEventListener("mouseleave", startTimer);
        }
        if (nextBtn) nextBtn.addEventListener("click", function(e) { e.preventDefault(); nextSlide(); });
        if (prevBtn) prevBtn.addEventListener("click", function(e) { e.preventDefault(); prevSlide(); });
        dots.forEach(function(dot) {
            dot.addEventListener("click", function() {
                let idx = parseInt(dot.getAttribute("data-index"), 10);
                showSlide(idx);
            });
        });

        // Touch swipe support for mobile devices
        let touchStartX = 0;
        let touchEndX = 0;
        if (container) {
            container.addEventListener("touchstart", function(e) {
                touchStartX = e.changedTouches[0].screenX;
            }, {passive: true});
            container.addEventListener("touchend", function(e) {
                touchEndX = e.changedTouches[0].screenX;
                if (touchStartX - touchEndX > 40) { nextSlide(); }
                else if (touchEndX - touchStartX > 40) { prevSlide(); }
            }, {passive: true});
        }
    }
});
</script>
""".strip()


def build_css() -> str:
    return """
/* kindnessforafghans.org — Elevated Humanitarian Responsive CSS */
:root {
  --primary: #1b4c36;          /* Official Brand Emerald Green */
  --primary-hover: #143d2b;
  --primary-light: #25664a;
  --primary-subtle: #f0f7f3;
  --accent: #d97706;           /* Warm Amber for high-converting CTAs */
  --accent-hover: #b45309;
  --accent-subtle: #fef3c7;
  --bg: #f8fafc;
  --card-bg: #ffffff;
  --text: #1e293b;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  --border: #e2e8f0;
  --border-light: #f1f5f9;
  --success: #15803d;
  --success-bg: #f0fdf4;
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.06);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.06);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.04);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

*, *::before, *::after {
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  line-height: 1.65;
  color: var(--text);
  margin: 0;
  padding: 0;
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

.container {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Announcement Trust Strip */
.top-bar {
  background: var(--primary);
  color: #e2ece6;
  font-size: 0.82rem;
  padding: 9px 16px;
  text-align: center;
  font-weight: 500;
  letter-spacing: 0.01em;
}
.top-bar strong {
  color: #ffffff;
}

/* Header */
.header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border);
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}
.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  color: var(--text);
}
.brand img {
  height: 48px;
  width: auto;
  object-fit: contain;
}
.brand-text h1 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1.2;
}
.brand-text p {
  margin: 2px 0 0 0;
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 500;
}
.nav {
  display: flex;
  align-items: center;
  gap: 18px;
}
.nav a {
  text-decoration: none;
  color: var(--text);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}
.nav a:hover {
  color: var(--primary);
}
.nav a.active {
  color: var(--primary);
  background: var(--primary-subtle);
}
.nav .nav-donate-btn {
  background: var(--accent);
  color: #ffffff !important;
  padding: 8px 18px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.nav .nav-donate-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 48px 24px;
  background: linear-gradient(180deg, #ffffff 0%, var(--primary-subtle) 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin: 28px 0 36px 0;
  box-shadow: var(--shadow-sm);
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  border: 1px solid var(--border);
  color: var(--primary);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 18px;
  box-shadow: var(--shadow-sm);
}
.hero h2 {
  font-size: 2.35rem;
  font-weight: 800;
  color: var(--primary-hover);
  line-height: 1.25;
  margin: 0 0 16px 0;
  letter-spacing: -0.02em;
}
.hero p {
  font-size: 1.15rem;
  color: var(--text-muted);
  max-width: 680px;
  margin: 0 auto 28px auto;
  line-height: 1.6;
}
.hero-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--primary);
  color: #ffffff;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
  border: none;
  cursor: pointer;
}
.btn:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
.btn-accent {
  background: var(--accent);
}
.btn-accent:hover {
  background: var(--accent-hover);
}
.btn-secondary {
  background: #ffffff;
  color: var(--primary);
  border: 1px solid var(--border);
}
.btn-secondary:hover {
  background: var(--primary-subtle);
  color: var(--primary-hover);
}

/* Impact Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin: 0 0 40px 0;
}
.stat-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 22px 18px;
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.stat-number {
  font-size: 2.1rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1.1;
  margin-bottom: 6px;
}
.stat-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.stat-subtext {
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* Slideshow */
.slideshow-wrapper {
  position: relative;
  width: 100%;
  max-width: 980px;
  margin: 0 auto 40px auto;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  background: #111827;
}
.slideshow-container {
  position: relative;
  width: 100%;
  height: 380px;
  overflow: hidden;
}
@media (max-width: 768px) {
  .slideshow-container { height: 260px; }
}
@media (max-width: 480px) {
  .slideshow-container { height: 210px; }
}
.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.8s ease-in-out;
  pointer-events: none;
}
.slide.active {
  opacity: 1;
  pointer-events: auto;
}
.slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.slide-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 70%, transparent 100%);
  color: #ffffff;
  padding: 36px 24px 18px 24px;
  font-size: 0.95rem;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0,0,0,0.6);
}
.slide-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.85);
  color: #1e293b;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
  box-shadow: var(--shadow-sm);
}
.slide-nav-btn:hover {
  background: #ffffff;
  transform: translateY(-50%) scale(1.08);
}
.slide-prev { left: 16px; }
.slide-next { right: 16px; }
.slide-dots {
  position: absolute;
  bottom: 14px;
  right: 20px;
  display: flex;
  gap: 8px;
  z-index: 10;
}
.slide-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255,255,255,0.45);
  border: 1px solid rgba(255,255,255,0.8);
  cursor: pointer;
  transition: all 0.2s ease;
}
.slide-dot.active {
  background: var(--accent);
  border-color: var(--accent);
  width: 24px;
  border-radius: 12px;
}

/* Sections & Content */
.section {
  margin-bottom: 50px;
}
.section-header {
  margin-bottom: 24px;
}
.section-title {
  color: var(--primary);
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0 0 6px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin: 0;
}

/* How We Work / Three Pillars */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  margin-top: 16px;
}
.pillar-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease;
}
.pillar-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.pillar-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary-subtle);
  color: var(--primary);
  border-radius: var(--radius-sm);
  font-weight: 800;
  font-size: 1rem;
  margin-bottom: 14px;
}
.pillar-card h4 {
  margin: 0 0 10px 0;
  font-size: 1.15rem;
  color: var(--primary);
}
.pillar-card p {
  margin: 0;
  font-size: 0.92rem;
  color: var(--text-muted);
  line-height: 1.6;
}

/* Highlight / Impact Feature Box */
.feature-box {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-left: 5px solid var(--primary);
  border-radius: var(--radius-md);
  padding: 28px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 40px;
}
.feature-box h3 {
  margin: 0 0 12px 0;
  color: var(--primary);
  font-size: 1.35rem;
}

/* Donation Tiers Grid (donate.html) */
.tiers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 18px;
  margin: 24px 0 40px 0;
}
.tier-card {
  background: var(--card-bg);
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px 18px;
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}
.tier-card:hover {
  border-color: var(--primary);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.tier-card.featured {
  border-color: var(--accent);
  background: linear-gradient(180deg, #ffffff 0%, var(--accent-subtle) 150%);
}
.tier-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--accent);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 12px;
  border-radius: var(--radius-full);
}
.tier-amount {
  font-size: 2rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 4px;
}
.tier-title {
  font-size: 1.02rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 8px;
}
.tier-desc {
  font-size: 0.86rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 18px;
  flex-grow: 1;
}

/* Payment Methods Grid */
.donation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 24px;
  margin: 20px 0 40px 0;
}
.method-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 26px;
  background: var(--card-bg);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.method-card h3 {
  margin: 0 0 10px 0;
  color: var(--primary);
  font-size: 1.25rem;
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 10px;
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px dashed var(--border);
  padding-bottom: 8px;
}
.detail-label {
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.9rem;
}
.detail-value {
  text-align: right;
  font-family: monospace;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--primary);
}
.copy-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--primary-subtle);
  border: 1px solid #cce3d8;
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  margin: 12px 0 16px 0;
}
.copy-box code {
  font-family: monospace;
  font-size: 1.02rem;
  font-weight: 700;
  color: var(--primary-dark);
}
.btn-copy {
  background: var(--primary);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-copy:hover {
  background: var(--primary-hover);
}
.btn-copy.copied {
  background: var(--success);
}
.qr-container {
  text-align: center;
  margin-top: 18px;
}
.qr-container img {
  max-width: 140px;
  height: auto;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px;
  background: #ffffff;
}

/* FAQ Accordion */
.faq-section {
  margin: 40px 0;
}
.faq-item {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.faq-item summary {
  padding: 16px 20px;
  font-weight: 600;
  font-size: 1rem;
  color: var(--text);
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
}
.faq-item summary::-webkit-details-marker {
  display: none;
}
.faq-item summary::after {
  content: "+";
  font-size: 1.4rem;
  font-weight: 400;
  color: var(--primary);
  transition: transform 0.2s ease;
}
.faq-item[open] summary::after {
  content: "−";
}
.faq-item[open] summary {
  border-bottom: 1px solid var(--border);
  background: var(--primary-subtle);
  color: var(--primary);
}
.faq-content {
  padding: 16px 20px;
  font-size: 0.95rem;
  color: #475569;
  line-height: 1.7;
}

/* News Articles */
.news-list {
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.news-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 28px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease;
}
.news-card:hover {
  box-shadow: var(--shadow-md);
}
.news-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.news-badge {
  background: var(--primary-subtle);
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
}
.news-date {
  color: var(--text-muted);
  font-size: 0.88rem;
}
.news-title {
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 14px 0;
  line-height: 1.3;
}
.news-content {
  color: #334155;
  line-height: 1.75;
}
.news-empty {
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
  padding: 40px;
}

/* Footer */
.footer {
  margin-top: 60px;
  background: #ffffff;
  border-top: 1px solid var(--border);
  padding: 48px 0 32px 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 36px;
  margin-bottom: 36px;
}
@media (max-width: 768px) {
  .footer-grid { grid-template-columns: 1fr; gap: 24px; }
}
.footer-brand h4 {
  color: var(--primary);
  font-size: 1.2rem;
  margin: 0 0 8px 0;
}
.footer-brand p {
  margin: 0 0 10px 0;
  font-size: 0.88rem;
  line-height: 1.6;
}
.footer-col h5 {
  color: var(--text);
  font-size: 0.95rem;
  margin: 0 0 12px 0;
  font-weight: 700;
}
.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-col ul li {
  margin-bottom: 8px;
}
.footer-col a {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.footer-col a:hover {
  color: var(--primary);
}
.footer-bottom {
  border-top: 1px solid var(--border);
  padding-top: 24px;
  text-align: center;
  font-size: 0.82rem;
  color: var(--text-light);
}

/* Mobile Responsiveness */
@media (max-width: 640px) {
  .header .container { flex-direction: column; text-align: center; }
  .brand { flex-direction: column; text-align: center; }
  .nav { flex-wrap: wrap; justify-content: center; gap: 10px; }
  .hero h2 { font-size: 1.85rem; }
  .hero p { font-size: 1rem; }
  .hero-cta { flex-direction: column; width: 100%; }
  .hero-cta .btn { width: 100%; }
  .detail-row { flex-direction: column; text-align: left; }
  .detail-value { text-align: left; margin-top: 4px; }
}
"""


def build_head_tags(page_title: str, page_description: str, page_url: str = "") -> str:
    """Generates standard SEO meta tags, Open Graph, Twitter Cards, Favicon links, and Schema.org JSON-LD."""
    full_url = f"https://kindnessforafghans.org/{page_url}".rstrip("/")
    if not page_url:
        full_url = "https://kindnessforafghans.org"

    return f"""
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <meta name="description" content="{page_description}" />
  <link rel="canonical" href="{full_url}" />
  
  <!-- Favicon Links -->
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png" />
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
  <link rel="apple-touch-icon" href="assets/favicon.png" />

  <!-- Open Graph / Social Sharing -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{full_url}" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{page_description}" />
  <meta property="og:image" content="https://kindnessforafghans.org/assets/logo.png" />
  <meta property="og:site_name" content="Kindness for Afghans" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{page_description}" />
  <meta name="twitter:image" content="https://kindnessforafghans.org/assets/logo.png" />

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NGO",
    "name": "Kindness for Afghans",
    "alternateName": "Kindness for Afghans Corporation",
    "url": "https://kindnessforafghans.org",
    "logo": "https://kindnessforafghans.org/assets/logo.png",
    "description": "Registered Ontario Not-for-Profit Corporation (OCN: 1001294785) providing direct, verified emergency relief in Afghanistan.",
    "identifier": "1001294785",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "9 Seedland Crescent",
      "addressLocality": "Brampton",
      "addressRegion": "ON",
      "postalCode": "L6R 0Z6",
      "addressCountry": "CA"
    }},
    "contactPoint": {{
      "@type": "ContactPoint",
      "email": "info@kindnessforafghans.org",
      "contactType": "donor support"
    }}
  }}
  </script>
""".strip()


def build_header(name: str, active: str, logo_src: str = "assets/logo.png") -> str:
    links = [
        ("home", "Home", "index.html"),
        ("donate", "Donate", "donate.html"),
        ("news", "News & Transparency", "news.html"),
    ]
    nav_items = []
    for key, label, url in links:
        cls = ' class="active"' if key == active else ""
        nav_items.append(f'<a href="{url}"{cls}>{label}</a>')
    
    # Always include prominent Donate CTA button in header
    nav_items.append('<a href="donate.html" class="nav-donate-btn">Donate Now</a>')
    nav_html = "\n      ".join(nav_items)

    return f"""
<div class="top-bar">
  🇨🇦 <strong>Registered Ontario Not-for-Profit Corporation</strong> (OCN: 1001294785) • 100% Volunteer-Run • Zero Admin Fee Deductions
</div>
<header class="header">
  <div class="container">
    <a href="index.html" class="brand">
      <img src="{logo_src}" alt="{name} Logo" />
      <div class="brand-text">
        <h1>{name}</h1>
        <p>Dignity through direct support</p>
      </div>
    </a>
    <nav class="nav">
      {nav_html}
    </nav>
  </div>
</header>
""".strip()


def build_footer(name: str) -> str:
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h4>{name}</h4>
        <p>A registered Ontario Not-for-Profit Corporation (Ontario Corporation Number: <strong>1001294785</strong>). Dedicated to delivering emergency food, surgical aid, and life-essential supplies directly to the most vulnerable families in Afghanistan.</p>
        <p><strong>100% Direct Relief Promise:</strong> 100% of donor funds are deployed on the ground under strict CRA agency agreements with zero executive salary overhead.</p>
      </div>
      <div class="footer-col">
        <h5>Quick Links</h5>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="donate.html">Donate Securely</a></li>
          <li><a href="news.html">Field Reports & Transparency</a></li>
          <li><a href="donate.html#faq">Donor FAQ</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Contact & Head Office</h5>
        <ul>
          <li><strong>Email:</strong> <a href="mailto:info@kindnessforafghans.org">info@kindnessforafghans.org</a></li>
          <li><strong>Address:</strong> 9 Seedland Crescent, Brampton, ON, L6R 0Z6, Canada</li>
          <li><strong>Domain:</strong> <a href="https://kindnessforafghans.org">kindnessforafghans.org</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025–2026 {name}. All rights reserved. Registered Ontario Not-for-Profit Corporation No. 1001294785.</p>
    </div>
  </div>
</footer>
""".strip()


def build_slideshow_html(image_files: list) -> str:
    if not image_files:
        return ""
    
    slides = []
    dots = []
    for i, img_path in enumerate(image_files):
        active_class = " active" if i == 0 else ""
        caption_text = SLIDESHOW_CAPTIONS[i % len(SLIDESHOW_CAPTIONS)]
        loading_attr = "eager" if i == 0 else "lazy"
        slides.append(f"""
        <div class="slide{active_class}">
          <img src="{img_path}" alt="Kindness for Afghans humanitarian relief {i+1}" loading="{loading_attr}" />
          <div class="slide-caption">{caption_text}</div>
        </div>
        """.strip())
        dots.append(f'<span class="slide-dot{active_class}" data-index="{i}"></span>')

    return f"""
    <div class="slideshow-wrapper">
      <div class="slideshow-container">
        {"\n        ".join(slides)}
      </div>
      <button class="slide-nav-btn slide-prev" aria-label="Previous slide">&#10094;</button>
      <button class="slide-nav-btn slide-next" aria-label="Next slide">&#10095;</button>
      <div class="slide-dots">
        {"".join(dots)}
      </div>
    </div>
    {SLIDESHOW_SCRIPT}
    """.strip()


def build_home_html(name: str, logo_src: str = "assets/logo.png", slideshow_images: list = None) -> str:
    header_html = build_header(name, "home", logo_src)
    footer_html = build_footer(name)
    slideshow_html = build_slideshow_html(slideshow_images) if slideshow_images else ""
    head_tags = build_head_tags(
        f"{name} — Dignity Through Direct Support",
        "Kindness for Afghans delivers emergency food parcels, critical surgeries, and prescription medicines directly to vulnerable families and widows across Afghanistan. Over AFN 122,700 ($2,836 CAD) transferred directly to Kabul with 100% financial reconciliation."
    )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  {head_tags}
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
{header_html}

<main class="container">
  {slideshow_html}

  <section class="hero">
    <div class="hero-badge">
      <span>🤝 100% Volunteer-Run • Zero Admin Fee Deductions</span>
    </div>
    <h2>Dignity Through Direct Support</h2>
    <p>We deliver emergency food parcels, critical surgeries, vital medicines, and winter heating directly to widows, orphans, and vulnerable families across Afghanistan.</p>
    <div class="hero-cta">
      <a href="donate.html" class="btn btn-accent">Make a Direct Donation</a>
      <a href="news.html" class="btn btn-secondary">View Verified Field Impact &rarr;</a>
    </div>
  </section>

  <!-- Impact Statistics Counter -->
  <section class="stats-grid">
    <div class="stat-card">
      <div class="stat-number">AFN 122.7K+</div>
      <div class="stat-label">Total Aid to Kabul</div>
      <div class="stat-subtext">AFN 122,700 ($2,836 CAD) transferred</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3</div>
      <div class="stat-label">Relief Missions</div>
      <div class="stat-subtext">100% matched to TD Bank statement</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">18+</div>
      <div class="stat-label">Families & Patients</div>
      <div class="stat-subtext">Food hampers, surgeries & medicines</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">100%</div>
      <div class="stat-label">Direct Aid Guarantee</div>
      <div class="stat-subtext">Zero administrative salary overhead</div>
    </div>
  </section>

  <!-- Cumulative Direct Impact Spotlight -->
  <section class="feature-box">
    <h3>Direct Aid Transferred to Kabul: AFN 122,700 ($2,836 CAD)</h3>
    <p>
      Through generous donor support, <strong>Kindness for Afghans</strong> has transferred and deployed a cumulative <strong>AFN 122,700 ($2,836 CAD)</strong> in direct emergency relief across three field missions, 100% reconciled against our TD Canada Trust bank statement:
    </p>
    <ul style="line-height: 1.85; margin: 15px 0 15px 22px;">
      <li><strong>Spring 2026 Mission (TD Debit $912 CAD):</strong> <strong>AFN 40,000</strong> deployed for emergency food parcels and household relief.</li>
      <li><strong>Summer 2026 Mission (TD Debit $962 CAD):</strong> <strong>AFN 41,200</strong> deployed for life-saving surgery assistance, multi-week food hampers for 6 families, and prescription medicines.</li>
      <li><strong>Late Summer 2026 Mission (TD Debit $962 CAD):</strong> <strong>AFN 41,500</strong> deployed for continued emergency food and urgent medical care.</li>
    </ul>
    <p style="margin: 18px 0 0 0;">
      <a href="news.html" style="font-weight: 700; color: var(--primary); text-decoration: none;">
        Read our full field reports and financial reconciliation details &rarr;
      </a>
    </p>
  </section>

  <!-- How We Work: The Three-Pillar Direct Model -->
  <section class="section">
    <div class="section-header">
      <h3 class="section-title">How We Work</h3>
      <p class="section-subtitle">A direct, accountable humanitarian model that eliminates middleman friction.</p>
    </div>
    <div class="pillars-grid">
      <div class="pillar-card">
        <div class="pillar-number">1</div>
        <h4>Community Identification</h4>
        <p>Our trusted local field coordinators assess communities directly, identifying families in acute distress—prioritizing widows, orphans, and households without income earners.</p>
      </div>
      <div class="pillar-card">
        <div class="pillar-number">2</div>
        <h4>Zero-Middleman Delivery</h4>
        <p>Relief supplies (food staples, pharmacy prescriptions, and winter fuels) are purchased directly from local vendors and hand-delivered directly to recipient households.</p>
      </div>
      <div class="pillar-card">
        <div class="pillar-number">3</div>
        <h4>Full Audit Verification</h4>
        <p>Under our CRA-compliant Agency Agreement, every expenditure is documented with itemized vendor receipts, recipient sign-off sheets with thumbprints, and field documentation.</p>
      </div>
    </div>
  </section>

  <!-- Mission & Legal Incorporation -->
  <section class="section">
    <div class="section-header">
      <h3 class="section-title">Our Mission & Governance</h3>
    </div>
    <p>
      At <strong>Kindness for Afghans</strong>, our mission is to restore dignity, hope, and relief to the most vulnerable families in Afghanistan. We collect charitable contributions from Canada, the United States, and internationally to deliver immediate, life-sustaining aid.
    </p>
    <p>
      Kindness for Afghans is an incorporated Ontario Not-for-Profit Corporation (Ontario Corporation Number: <strong>1001294785</strong>). We operate with complete financial transparency, maintaining formal agency agreements that satisfy Canada Revenue Agency (CRA) overseas direction-and-control standards.
    </p>
    <div style="margin-top: 24px; text-align: center;">
      <a href="donate.html" class="btn btn-accent">Support Our Mission Today</a>
    </div>
  </section>
</main>

{footer_html}
</body>
</html>
""".strip()


def build_donate_html(
    name: str,
    interac_email: str = None,
    zeffy_link: str = None,
    zeffy_qr_src: str = None,
    bank_account: str = None,
    transit_number: str = None,
    institution_number: str = None,
    swift_bic: str = None,
    bank_name: str = None,
    wire_contact: bool = True,
    iban: str = None,
    bic: str = None,
    reference: str = None,
    logo_src: str = "assets/logo.png"
) -> str:
    header_html = build_header(name, "donate", logo_src)
    footer_html = build_footer(name)
    head_tags = build_head_tags(
        f"Donate — {name}",
        "Support emergency food parcels, critical surgeries, and vital medicines in Afghanistan. 100% direct relief with 0% platform fee options via Zeffy and Interac e-Transfer.",
        "donate.html"
    )

    full_zeffy_link = zeffy_link if (zeffy_link and zeffy_link.startswith('http')) else f"https://{zeffy_link}" if zeffy_link else "#"

    # Donation Tiers Data
    tiers = [
        {
            "amount": "$35",
            "title": "Emergency Food Parcel",
            "desc": "Provides staple food supplies (flour, rice, cooking oil, lentils, tea) to feed a family for 2–3 weeks.",
            "link": full_zeffy_link,
            "featured": False
        },
        {
            "amount": "$75",
            "title": "Winter Warmth & Fuel",
            "desc": "Supplies heating coal, firewood, and warm blankets to protect widows and children from sub-zero winter temperatures.",
            "link": full_zeffy_link,
            "featured": True
        },
        {
            "amount": "$150",
            "title": "Essential Prescription Medicines",
            "desc": "Covers critical medications and medical supplies for patients with urgent or chronic clinical health conditions.",
            "link": full_zeffy_link,
            "featured": False
        },
        {
            "amount": "$300+",
            "title": "Critical Surgical Support",
            "desc": "Directly subsidizes emergency hospital surgery costs for vulnerable patients who cannot afford life-saving procedures.",
            "link": full_zeffy_link,
            "featured": False
        }
    ]

    tier_cards = []
    for t in tiers:
        featured_cls = " featured" if t["featured"] else ""
        badge_html = '<div class="tier-badge">Most Needed</div>' if t["featured"] else ""
        tier_cards.append(f"""
        <div class="tier-card{featured_cls}">
          {badge_html}
          <div>
            <div class="tier-amount">{t['amount']} <small style="font-size: 0.9rem; font-weight: 600; color: var(--text-muted);">CAD</small></div>
            <div class="tier-title">{t['title']}</div>
            <div class="tier-desc">{t['desc']}</div>
          </div>
          <a href="{t['link']}" target="_blank" class="btn btn-accent" style="width: 100%; font-size: 0.9rem; padding: 10px 14px;">Donate {t['amount']}</a>
        </div>
        """.strip())

    tiers_html = "\n".join(tier_cards)

    # 1. Zeffy Method Card
    qr_html = ""
    if zeffy_qr_src:
        qr_html = f"""
        <div class="qr-container">
          <img src="{zeffy_qr_src}" alt="Scan to donate via Zeffy" />
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">Scan with phone camera</p>
        </div>
        """

    zeffy_card = f"""
    <div class="method-card">
      <div>
        <h3>1. Online Credit / Debit (Zeffy)</h3>
        <p style="color: var(--text-muted); font-size: 0.95rem;">
          Donate securely with Credit Card, Apple Pay, or Google Pay through <strong>Zeffy</strong>, the only 100% free donation platform built for non-profits (<strong>0% platform fees</strong>).
        </p>
        <div style="text-align: center; margin: 24px 0 10px 0;">
          <a href="{full_zeffy_link}" target="_blank" class="btn btn-accent" style="width: 100%; font-size: 1.05rem;">
            Donate Securely via Zeffy &rarr;
          </a>
        </div>
      </div>
      {qr_html}
    </div>
    """

    # 2. Interac e-Transfer Card
    interac_email_val = interac_email or "info@kindnessforafghans.org"
    interac_card = f"""
    <div class="method-card">
      <div>
        <h3>2. Interac e-Transfer <small style="font-size: 0.85rem; color: var(--primary);">(Canada)</small></h3>
        <p style="color: var(--text-muted); font-size: 0.95rem;">
          The fastest and most direct way to donate from any Canadian bank account with <strong>0% transaction fees</strong>.
        </p>
        <div class="copy-box">
          <code>{interac_email_val}</code>
          <button id="copyBtn" class="btn-copy" onclick="copyInteracEmail()">Copy Email</button>
        </div>
        <div class="detail-row">
          <span class="detail-label">Recipient Name:</span>
          <span class="detail-value">{name}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Message / Memo:</span>
          <span class="detail-value">Donation for Relief</span>
        </div>
        <div class="detail-row" style="border-bottom: none;">
          <span class="detail-label">Auto-Deposit:</span>
          <span class="detail-value" style="color: var(--success);">Enabled (No question needed)</span>
        </div>
      </div>
      <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 15px;">
        100% of e-Transfers are deposited directly to our Canadian non-profit bank account.
      </p>
    </div>
    """

    # 3. Wire Transfer Card
    wire_card = f"""
    <div class="method-card">
      <div>
        <h3>3. International Bank Wire</h3>
        <p style="color: var(--text-muted); font-size: 0.95rem;">
          For major contributions, foundation grants, or international wire transfers from outside North America, please reach out directly to our finance team.
        </p>
        <div class="detail-row">
          <span class="detail-label">Institution:</span>
          <span class="detail-value">TD Canada Trust</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Country:</span>
          <span class="detail-value">Canada</span>
        </div>
        <div class="detail-row" style="border-bottom: none;">
          <span class="detail-label">Instructions:</span>
          <span class="detail-value">Provided via email</span>
        </div>
      </div>
      <div style="margin-top: 20px; text-align: center;">
        <a href="mailto:info@kindnessforafghans.org?subject=Wire%20Transfer%20Inquiry%20-%20Kindness%20for%20Afghans" class="btn btn-secondary" style="width: 100%;">
          Request Wire Transfer Details
        </a>
      </div>
    </div>
    """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  {head_tags}
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
{header_html}

<main class="container">
  <section class="hero" style="background: transparent; padding: 36px 0 16px;">
    <h2>Choose How You Make a Difference</h2>
    <p>100% of your contribution directly funds emergency food parcels, critical surgeries, and prescription medicines on the ground in Afghanistan.</p>
  </section>

  <!-- Giving Tiers -->
  <div class="section-header" style="text-align: center;">
    <h3 class="section-title" style="justify-content: center;">Tangible Impact Tiers</h3>
    <p class="section-subtitle">Select an amount to see what your generosity achieves on the ground.</p>
  </div>
  <div class="tiers-grid">
    {tiers_html}
  </div>

  <!-- Payment Methods Grid -->
  <div class="section-header">
    <h3 class="section-title">Payment Methods</h3>
    <p class="section-subtitle">Choose the most convenient, fee-free option for your donation.</p>
  </div>
  <div class="donation-grid">
    {zeffy_card}
    {interac_card}
    {wire_card}
  </div>

  <!-- Transparency & Charity Status Notice -->
  <div style="background: #fffbe6; padding: 22px 24px; border-radius: 10px; border: 1px solid #ffe58f; margin: 30px 0; color: #856404; line-height: 1.65;">
    <h4 style="margin: 0 0 8px 0; color: #856404; font-size: 1.05rem;">Canadian Governance & Transparency Notice</h4>
    <p style="margin: 0; font-size: 0.92rem;">
      Kindness for Afghans is incorporated as an Ontario Not-for-Profit Corporation (OCN: <strong>1001294785</strong>). We are currently operating as a non-profit while our federal registered charity application with the Canada Revenue Agency (CRA) is under processing. While this means official Canadian tax receipts cannot be issued until registration is finalized, <strong>100% of your donation is deployed directly to emergency humanitarian aid</strong> without any deductions for administrative salaries.
    </p>
  </div>

  <!-- Donor FAQ Accordion -->
  <section id="faq" class="faq-section">
    <div class="section-header">
      <h3 class="section-title">Frequently Asked Questions</h3>
      <p class="section-subtitle">Everything you need to know about our direct aid delivery and governance.</p>
    </div>

    <details class="faq-item" open>
      <summary>How do you ensure 100% of my donation reaches those in need?</summary>
      <div class="faq-content">
        Kindness for Afghans is 100% volunteer-run by professionals in Canada. We have no executive salaries or paid marketing campaigns. All field aid is executed under a formal Canada Revenue Agency (CRA) Agency Agreement with strict three-way reconciliation: every dollar is matched against itemized vendor receipts, recipient distribution lists with thumbprints, and field documentation.
      </div>
    </details>

    <details class="faq-item">
      <summary>How do funds safely reach Afghanistan under banking restrictions?</summary>
      <div class="faq-content">
        Due to international commercial banking sanctions on Afghanistan, standard Canadian bank wire transfers into Kabul are restricted. We deploy authorized remittance channels (including MoneyGram via Canadian financial counters) directly to our vetted field representative under our legal agency agreement. Full bank debit statements, MoneyGram remittance receipts, and local disbursement reports are reconciled to the penny.
      </div>
    </details>

    <details class="faq-item">
      <summary>How are beneficiary families selected?</summary>
      <div class="faq-content">
        Our on-the-ground representatives work directly within communities to identify families facing acute, life-threatening hardship—giving strict priority to widows with young children, orphan-headed households, disabled individuals, and families with zero income or breadwinners.
      </div>
    </details>

    <details class="faq-item">
      <summary>Are there any hidden platform processing fees?</summary>
      <div class="faq-content">
        None! We deliberately chose <strong>Zeffy</strong> for online credit/debit card donations because Zeffy charges <strong>0% transaction fees and 0% platform fees</strong> to non-profits (funded entirely by voluntary donor tips). For Canadian donors, Interac e-Transfer to <code>info@kindnessforafghans.org</code> is also 100% free of processing deductions.
      </div>
    </details>

    <details class="faq-item">
      <summary>Can I donate from outside Canada?</summary>
      <div class="faq-content">
        Yes! Our Zeffy online payment portal accepts international credit and debit cards from donors in the United States, Europe, Australia, and worldwide. For large wire transfers, please email us directly at <code>info@kindnessforafghans.org</code> for wire routing instructions.
      </div>
    </details>
  </section>
</main>

{COPY_INTERAC_SCRIPT}

{footer_html}
</body>
</html>
""".strip()


def build_news_html(name: str, posts: list, logo_src: str = "assets/logo.png") -> str:
    header_html = build_header(name, "news", logo_src)
    footer_html = build_footer(name)
    head_tags = build_head_tags(
        f"News & Field Reports — {name}",
        "Field activity reports, transparency disclosures, and updates on direct humanitarian relief initiatives across Afghanistan.",
        "news.html"
    )

    if not posts:
        content = '<div class="news-empty">No updates posted yet. Check back soon!</div>'
    else:
        post_items = []
        for post in posts:
            category_badge = f'<span class="news-badge">{post.get("category", "Update")}</span>'
            post_items.append(f"""
        <article class="news-card">
          <div class="news-header">
            {category_badge}
            <span class="news-date">{post['date']}</span>
          </div>
          <h2 class="news-title">{post['title']}</h2>
          <div class="news-content">{post['content']}</div>
        </article>
            """.strip())
        content = '<div class="news-list">' + "\n".join(post_items) + '</div>'

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  {head_tags}
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
{header_html}

<main class="container">
  <section class="hero" style="background: transparent; padding: 36px 0 20px;">
    <h2>Field Reports & Transparency</h2>
    <p>Read verified updates from our on-the-ground relief missions and financial accountability registers.</p>
  </section>

  {content}
</main>

{footer_html}
</body>
</html>
""".strip()


def optimize_slideshow_image(src_path: Path, dest_path: Path, max_width: int = 1280) -> bool:
    """Resizes and compresses images using Pillow for fast mobile delivery."""
    if not Image:
        shutil.copy(src_path, dest_path)
        return False

    try:
        with Image.open(src_path) as im:
            im = im.convert("RGB")
            w, h = im.size
            if w > max_width:
                new_h = int(h * (max_width / w))
                im = im.resize((max_width, new_h), Image.Resampling.LANCZOS)
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            im.save(dest_path, format="JPEG", quality=84, progressive=True, optimize=True)
            return True
    except Exception as e:
        print(f"⚠️ Image optimization fallback for {src_path.name}: {e}")
        shutil.copy(src_path, dest_path)
        return False


def generate_favicons_and_logo(logo_source: Path, assets_dir: Path) -> str:
    """Generates crisp, optimized logo.png, favicon.png (64x64), and favicon.ico from branding assets."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    dest_logo = assets_dir / "logo.png"

    if not Image or not logo_source.exists():
        if logo_source.exists() and logo_source != dest_logo:
            shutil.copy(logo_source, dest_logo)
        return "assets/logo.png"

    try:
        with Image.open(logo_source) as img:
            # 1. Optimize Web Header Logo (downscale for retina sharpness, e.g. width=600)
            orig_w, orig_h = img.size
            target_w = 600
            if orig_w > target_w:
                target_h = int(orig_h * (target_w / orig_w))
                logo_optimized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                logo_optimized.save(dest_logo, optimize=True)
            else:
                img.save(dest_logo, optimize=True)

            # 2. Extract Emblem for Favicons:
            # In 'Kindness Logo English.png' (1634x656), the emblem is in the left square (x=40..604, y=28..592)
            rgba_img = img.convert("RGBA")
            if orig_w >= 1000 and orig_h >= 500:
                emblem = rgba_img.crop((40, 28, 604, 592))
            else:
                emblem = rgba_img

            # Make background transparent if it's near-white
            try:
                import numpy as np
                arr = np.array(emblem)
                white_mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
                arr[white_mask, 3] = 0
                emblem = Image.fromarray(arr, mode="RGBA")
            except Exception:
                pass

            # Save PNG & ICO favicons
            fav_png = emblem.resize((64, 64), Image.Resampling.LANCZOS)
            fav_png.save(assets_dir / "favicon.png", format="PNG")
            emblem.save(assets_dir / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
            print("✅ Favicons generated: assets/favicon.png & assets/favicon.ico")

    except Exception as e:
        print(f"⚠️ Favicon generation error: {e}")
        if logo_source != dest_logo:
            shutil.copy(logo_source, dest_logo)

    return "assets/logo.png"


def handle_remove_readonly(func, path, exc):
    """Clear the readonly bit and reattempt the removal."""
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


def force_delete(path):
    """Robustly delete a directory or file, dealing with Windows file locks."""
    path = Path(path)
    if not path.exists():
        return

    for i in range(3):
        try:
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path, onerror=handle_remove_readonly)
            return
        except PermissionError:
            time.sleep(0.5)
        except Exception as e:
            print(f"  ... error deleting {path}: {e}")
            break

    if path.exists():
        if path.name.startswith("zzz_trash"):
            return
        try:
            new_name = path.parent / f"zzz_trash_{path.name}_{random.randint(1000,9999)}"
            path.rename(new_name)
        except Exception as e:
            print(f"❌ CRITICAL: Could not delete or move '{path}': {e}")
            raise


def run_git_automation(target_dir: Path):
    """Stages, commits, and pushes website changes to GitHub."""
    print("\n--- GitHub Automation ---")
    try:
        print("Running: git add .")
        subprocess.run(["git", "add", "."], cwd=target_dir, check=True)
        
        status = subprocess.run(["git", "status", "--porcelain"], cwd=target_dir, capture_output=True, text=True)
        if status.stdout.strip():
            print('Running: git commit -m "Update site: apply UX, SEO, speed optimizations and donation tiers"')
            subprocess.run(["git", "commit", "-m", "Update site: apply UX, SEO, speed optimizations and donation tiers"], cwd=target_dir, check=True)
            print("Running: git push origin main")
            subprocess.run(["git", "push", "origin", "main"], cwd=target_dir, check=True)
            print("✅ Successfully pushed to GitHub!")
        else:
            print("ℹ️ No changes to commit. Everything is up to date.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
    except FileNotFoundError:
        print("❌ Error: 'git' command not found. Is Git installed?")


def main():
    parser = argparse.ArgumentParser(description="Generate Kindness for Afghans Static Site")
    # General
    parser.add_argument("--name", default="Kindness for Afghans", help="Organization name")
    parser.add_argument("--out", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--logo", default="branding/Kindness Logo English.png", help="Path to custom logo image file")
    parser.add_argument("--photos", default="website_photos", help="Path to folder containing slideshow images")
    
    # Canadian / International Banking & Donation
    parser.add_argument("--interac", default="info@kindnessforafghans.org", help="Email for Interac e-Transfer")
    parser.add_argument("--zeffy", default="https://www.zeffy.com/en-CA/donation-form/donate-to-change-lives-6250", help="Zeffy Donation Link")
    parser.add_argument("--zeffy-qr", default="assets/zeffy_qr.png", help="Path to Zeffy QR Code Image")
    parser.add_argument("--bank-account", help="Bank Account Number")
    parser.add_argument("--transit", help="Bank Transit Number (5 digits)")
    parser.add_argument("--institution", help="Bank Institution Number (3 digits)")
    parser.add_argument("--swift", help="SWIFT/BIC Code (for international wire)")
    parser.add_argument("--bank-name", help="Name of the Bank")
    parser.add_argument("--wire-contact", action="store_true", default=True, help="Show 'Contact us for Wire' instead of details")
    
    # European / Other
    parser.add_argument("--iban", help="IBAN for SEPA")
    parser.add_argument("--bic", help="BIC for SEPA")
    parser.add_argument("--reference", default="Donation", help="Payment reference")
    
    # Automation & Config
    parser.add_argument("--github", action="store_true", help="Automatically git add/commit/push after generation")
    parser.add_argument("--cname", default="kindnessforafghans.org", help="Custom domain to create CNAME file")

    args = parser.parse_args()

    out = Path(args.out)
    assets = out / "assets"
    
    # Safeguard list to prevent build wiping source/governance/media/documentation files
    PROTECTED_ITEMS = {
        "legal_and_governance",
        "field_reports",
        "financial_records",
        "branding",
        "website_photos",
        "Kindness.py",
        ".gitignore",
        ".git",
        "CNAME",
        "README.md",
        "AGENTS.md",
        "DECISIONS.md",
    }

    # Create directories safely
    is_current_dir = out.resolve() == Path.cwd().resolve()
    if is_current_dir:
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
    print(f"Generating optimized site in: {out.resolve()}")

    # 1. Custom Domain CNAME
    if args.cname:
        (out / "CNAME").write_text(args.cname, encoding="utf-8")
        print(f"✅ CNAME created for: {args.cname}")

    # 2. Optimized Logo & Favicons
    logo_web_path = "assets/logo.png"
    if args.logo:
        logo_path = Path(args.logo)
        if logo_path.exists():
            logo_web_path = generate_favicons_and_logo(logo_path, assets)
            print(f"✅ Logo and favicons processed: {logo_web_path}")
        else:
            print(f"⚠️ Warning: Logo file not found at {args.logo}, checking fallback.")

    # 3. Optimized Slideshow Images
    slideshow_images = []
    if args.photos:
        photo_dir = Path(args.photos)
        if photo_dir.exists() and photo_dir.is_dir():
            slideshow_dir = assets / "slideshow"
            slideshow_dir.mkdir(exist_ok=True)
            extensions = {".jpg", ".jpeg", ".png", ".webp"}
            
            raw_size_total = 0
            opt_size_total = 0

            for f in sorted(photo_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in extensions:
                    dest = slideshow_dir / f.name
                    raw_size = f.stat().st_size
                    optimize_slideshow_image(f, dest)
                    opt_size = dest.stat().st_size
                    raw_size_total += raw_size
                    opt_size_total += opt_size
                    slideshow_images.append(f"assets/slideshow/{f.name}")
            
            savings = (1 - (opt_size_total / (raw_size_total or 1))) * 100
            print(f"✅ Slideshow: Loaded {len(slideshow_images)} images. Size reduced from {raw_size_total/1024:.0f}KB to {opt_size_total/1024:.0f}KB ({savings:.1f}% bandwidth saved).")
        else:
            print(f"⚠️ Warning: Photo directory not found: {args.photos}")

    # 4. Zeffy QR Code
    zeffy_qr_web_path = None
    if args.zeffy_qr:
        qr_path = Path(args.zeffy_qr)
        if qr_path.exists():
            dest = assets / "zeffy_qr.png"
            if qr_path.resolve() != dest.resolve():
                shutil.copy(qr_path, dest)
            zeffy_qr_web_path = "assets/zeffy_qr.png"
            print("✅ Zeffy QR code configured: zeffy_qr.png")

    today_version = int(time.time())

    # 5. Build Pages
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
            bank_account=None if args.wire_contact else args.bank_account,
            transit_number=args.transit,
            institution_number=args.institution,
            swift_bic=args.swift,
            bank_name=args.bank_name,
            wire_contact=args.wire_contact,
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

    print("✅ Optimized static site generated successfully:")
    print(f"  - {out / 'index.html'}")
    print(f"  - {out / 'donate.html'}")
    print(f"  - {out / 'news.html'}")
    print(f"  - {out / 'styles.css'}")

    # Ensure .gitignore has strict privacy quarantine rules
    gitignore_path = out / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(
            "legal_and_governance/\nfield_reports/\nfinancial_records/\n*.pdf\n*.docx\n*.xlsx\n*.mp4\nzzz_trash*\n__pycache__\n*.pyc\n",
            encoding="utf-8"
        )

    # 6. GitHub Automation
    if args.github:
        run_git_automation(out)


if __name__ == "__main__":
    main()
