# Kindness for Afghans — Official Website & Repository

[![Website](https://img.shields.io/badge/Website-kindnessforafghans.org-blue)](https://kindnessforafghans.org)
[![Status](https://img.shields.io/badge/Ontario%20Corporation-1001294785-green)](https://kindnessforafghans.org)
[![Platform](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-informational)](https://github.com/mahmadi2025/kindness)

Official static website repository and public documentation for **Kindness for Afghans**, a registered Ontario Not-for-Profit Corporation dedicated to delivering direct, transparent humanitarian relief across Afghanistan.

---

## 🌟 Mission

At **Kindness for Afghans**, our mission is to bring hope, dignity, and relief to the most vulnerable families in Afghanistan—including widows, orphans, and households without income. We provide:
- **Emergency Food Parcels:** Nutritious food staples for families facing acute food insecurity.
- **Critical Medical & Surgical Aid:** Financial support covering essential hospital operations for patients in urgent need.
- **Prescription Medicines:** Vital medications provided directly to vulnerable patients.
- **Winter & Heating Relief:** Warm clothing and heating supplies during harsh winters.

100% of public donations are deployed directly on the ground through verified agency agreements, with complete transparency, vendor receipts, and beneficiary distribution verification.

---

## 📁 Repository Structure

```
kindnessforafghans/
│
├── 🌐 Public Static Site (Deployed to GitHub Pages)
│   ├── index.html         # Homepage (Slideshow, Impact Highlights, Mission)
│   ├── donate.html        # Donation portal (Zeffy, Interac e-Transfer, Wire info)
│   ├── news.html          # Field updates & transparency reports
│   ├── styles.css         # Responsive styling
│   ├── CNAME              # Custom domain configuration (kindnessforafghans.org)
│   ├── Kindness.py        # Static site generator and automated GitHub publisher
│   ├── assets/            # Web graphics, logos, and slideshow media
│   ├── branding/          # Original logo graphics
│   └── website_photos/    # High-resolution field and stock imagery
│
├── 📚 Documentation & Governance
│   ├── AGENTS.md          # Guidelines for AI coding agents and automated pair programming
│   ├── DECISIONS.md       # Architecture & Governance Decision Records (ADRs)
│   └── README.md          # Repository overview and instructions
│
└── 🔒 Local Confidential Records (Ignored by Git for Privacy)
    ├── legal_and_governance/  # Incorporation filings, CRA application, agency contracts
    └── field_reports/         # Beneficiary sign-off sheets, thumbprints, raw receipts, videos
```

---

## 🚀 Building & Publishing the Website

This website is statically generated using Python with zero external dependencies.

### 1. Prerequisites
- Python 3.8+
- Git

### 2. Local Build
To regenerate all pages with latest content and asset paths:
```powershell
python Kindness.py
```

### 3. Build & Publish Live to GitHub Pages
To regenerate, commit, and push changes live to [kindnessforafghans.org](https://kindnessforafghans.org):
```powershell
python Kindness.py --github
```

---

## 🔒 Privacy & Compliance Directives

To protect the safety and dignity of vulnerable beneficiaries:
- **Never commit beneficiary records to Git:** Beneficiary thumbprints, individual medical details, and raw distribution records are quarantined in `field_reports/` and blocked by [`.gitignore`](.gitignore).
- **Public transparency:** The public website publishes aggregate impact figures (e.g. *"AFN 122,700 ($2,836 CAD) deployed across three missions for families and medical patients"*) while preserving recipient anonymity.

---

## 🤝 Reference Documentation

- [**AGENTS.md**](AGENTS.md): Detailed operating instructions, prompt guidelines, and safety constraints for AI agents.
- [**DECISIONS.md**](DECISIONS.md): Architectural Decision Records (ADRs) covering technology choices, CRA compliance, and donation architecture.

---

## 📬 Contact & Inquiries

- **Official Email:** [info@kindnessforafghans.org](mailto:info@kindnessforafghans.org)
- **Website:** [https://kindnessforafghans.org](https://kindnessforafghans.org)
- **Corporate Registration:** Ontario Corporation Number `1001294785`
