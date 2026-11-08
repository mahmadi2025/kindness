# AGENTS.md — AI Agent Guidance for Kindness for Afghans

> **Purpose:** This document provides context, behavioral guidelines, and operational procedures for AI assistants and automated coding tools working within this workspace.

---

## 1. Project Overview & Organization Identity

- **Organization Name:** Kindness for Afghans
- **Entity Type:** Registered Ontario Not-for-Profit Corporation
- **Ontario Corporation Number (OCN):** `1001294785` (Incorporated July 11, 2025)
- **Primary Domain:** [kindnessforafghans.org](https://kindnessforafghans.org)
- **Official Contact Email:** `info@kindnessforafghans.org` / `mjahmadi@gmail.com`
- **Head Office:** 9 Seedland Crescent, Brampton, Ontario, L6R 0Z6, Canada
- **Mission:** Providing direct emergency relief (food parcels, emergency surgeries, prescription medicines, and heating supplies) directly to the most vulnerable families, widows, and orphans across Afghanistan.

---

## 2. Critical Safety & Privacy Directives (NON-NEGOTIABLE)

> [!CAUTION]
> **Vulnerable Beneficiary Privacy & Data Security**
> This repository contains sensitive humanitarian records. Agents must strictly adhere to the following rules at all times:

1. **NEVER Stage or Commit Private Folders to Git**:
   - `legal_and_governance/`: Contains confidential corporate filings, CRA correspondence, and agency contracts.
   - `field_reports/`: Contains on-the-ground beneficiary sign-off sheets with thumbprints, individual names, sensitive medical procedures, and raw distribution videos.
2. **Preserve [`.gitignore`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/.gitignore)**:
   - Ensure `legal_and_governance/`, `field_reports/`, `*.pdf`, `*.docx`, and video formats (`*.mp4`, etc.) remain actively ignored.
3. **Public Transparency vs. Beneficiary Anonymity**:
   - When generating website updates (`news.html`, `index.html`), publish only aggregated impact metrics (e.g., "6 vulnerable families", "female patient surgical assistance", "AFN 41,200 deployed").
   - **Never** publish beneficiary full names, hospital patient IDs, or legible thumbprints on the public website.

---

## 3. Workspace Architecture

```
kindnessforafghans/
│
├── 🌐 Public Static Site (Tracked by Git / Deployed to GitHub Pages)
│   ├── index.html         # Homepage (Slideshow, Hero, Latest Impact, Mission)
│   ├── donate.html        # Donation portal (Zeffy 0% fees, Interac e-Transfer, Wire)
│   ├── news.html          # Field reports and transparency updates
│   ├── styles.css         # Responsive minimal CSS styling
│   ├── CNAME              # Custom domain configuration (kindnessforafghans.org)
│   ├── Kindness.py        # Python static site builder and deployment pipeline
│   ├── assets/            # Deployed web assets (logo.png, zeffy_qr.png, slideshow/)
│   ├── branding/          # High-resolution logos and graphic assets
│   └── website_photos/    # Source slideshow and activity photographs
│
├── 🔒 Confidential Governance & Legal (Local Only - Ignored by Git)
│   └── legal_and_governance/
│       ├── Articles_of_Incorporation_EN.pdf
│       ├── Certificate_of_Incorporation.pdf
│       ├── Charity Application.pdf (CRA T2050 Application)
│       ├── International_Agency_Agreement_Farzam.pdf (CRA overseas intermediary agreement)
│       └── ...
│
├── 🔒 Confidential Field Reports & Audit Records (Local Only - Ignored by Git)
│   └── field_reports/
│       └── 2026-07_distribution/
│           ├── Financial and Activity Report.docx   # Master report for AFN 41,200
│           ├── AUDIT_CHECKLIST.md                  # Status of all 7 supporting attachments
│           ├── Attachment 2 Food Purchase Receipt...jpeg
│           ├── Attachment 3 Food Distribution List with Beneficiary Thumbprints.jpeg
│           ├── Attachment 4 Food Distribution Video.mp4
│           └── Attachment 5 Pharmacy Receipts...docx
│
└── 📚 Operational Documentation
    ├── AGENTS.md          # This file (guidelines for AI agents)
    ├── DECISIONS.md       # Architecture & Governance Decision Records (ADRs)
    ├── README.md          # Repository overview and setup guide
    └── .gitignore         # Strict exclusion rules for private assets
```

---

## 4. Technical Architecture: Static Site Generator (`Kindness.py`)

The website does **not** use a heavy framework (React, Next.js, or WordPress). It is powered by a zero-dependency Python script (`Kindness.py`) that generates static HTML and CSS.

### Key Generator Characteristics:
- **Fast & Zero Overhead:** Runs on standard Python 3 with built-in standard libraries (`argparse`, `pathlib`, `shutil`, `subprocess`, `time`).
- **Cache Busting:** Generates timestamped CSS version queries (`styles.css?v=<timestamp>`) on each build to prevent browser caching stale styles.
- **Direct GitHub Push:** Includes an automated `--github` flag that verifies git porcelain status, commits changes, and pushes to `origin main`.
- **Directory Protection:** Contains a built-in `PROTECTED_ITEMS` safeguard to ensure running builds in the root directory never deletes governance files, media folders, or configuration files.

### Common Build Commands:

```powershell
# 1. Regenerate static site locally
python Kindness.py

# 2. Regenerate and publish directly to GitHub Pages
python Kindness.py --github

# 3. View CLI parameters and overrides
python Kindness.py --help
```

---

## 5. Agent Instructions for Common Tasks

### Task A: Adding a New Field Report or News Post
1. Open [`Kindness.py`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/Kindness.py).
2. Locate the `NEWS_POSTS` list near line 30.
3. Prepend a new dictionary with:
   - `date`: `YYYY-MM-DD`
   - `title`: Concise, impact-driven headline.
   - `content`: Clean HTML paragraphs (`<p>...</p>`) and lists (`<ul><li>...</li></ul>`) highlighting expenditure breakdown, families helped, and transparency verification.
4. If the milestone is significant, update the "Latest Direct Impact" section in `build_home_html`.
5. Run `python Kindness.py --github` to build and deploy.

### Task B: Updating Donation Information
- Online donation is routed through **Zeffy** (`https://www.zeffy.com/en-CA/donation-form/donate-to-change-lives-6250`), which offers 100% free processing for non-profits.
- Canadian bank donations are routed through Interac e-Transfer to `info@kindnessforafghans.org`.
- All donation parameters have smart defaults in `Kindness.py` and can be customized via command-line arguments.

### Task C: CRA & Field Audit Documentation
- When new field documentation arrives from overseas representatives:
  1. Save them in `field_reports/<YYYY-MM>_<event_name>/`.
  2. Standardize filenames matching `Attachment <N> <Description>.<ext>`.
  3. Update or create the `AUDIT_CHECKLIST.md` in that folder.
  4. Ensure the legal entity name is always recorded as **"Kindness for Afghans" (Ontario Corporation No. 1001294785)**.

### Task D: Bank Reconciliation & Financial Ledger Maintenance
- Internal accounting and bank reconciliation are tracked in `financial_records/Kindness_for_Afghans_Financial_Ledger.xlsx`.
- **Shoppers Drug Mart Transactions:** Withdrawals labeled `SHOPPERS DRUG M` represent **MoneyGram remittances sent directly to Kabul** for emergency relief.
- **Zeffy Deposits:** Bank deposits labeled `Zeffy-9355-0861 MSP` represent payouts from online donor contributions (0% platform fee).
- Always ensure `financial_records/` and `*.xlsx` remain strictly excluded from Git.
