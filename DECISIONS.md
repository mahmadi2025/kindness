# Architecture & Governance Decision Records (ADR)

This document captures the rationale, context, and implications of key structural, technical, and compliance decisions made for **Kindness for Afghans**.

---

## ADR 001: Separation of Public Static Site and Private Governance/Beneficiary Records

- **Status:** Accepted & Implemented
- **Date:** 2026-11-08

### Context
Originally, official corporate filings (Ontario Articles of Incorporation), CRA charity application documents, overseas agency agreements, field financial reports, raw receipt images, beneficiary sign-off sheets with thumbprints, and heavy field videos (50MB MP4) were mixed in a single flat directory alongside website HTML and script files. This posed a major privacy risk: committing the directory to a public GitHub repository would expose sensitive beneficiary personal information and confidential corporate records.

### Decision
Segregate the workspace into distinct functional boundaries:
1. `legal_and_governance/`: For official legal, corporate, and CRA correspondence (strictly private).
2. `field_reports/<period>_<name>/`: For on-the-ground project financial reports, receipts, beneficiary records, and field media (strictly private).
3. Root & `assets/`: For the public static website code and assets.
4. Rigid [`.gitignore`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/.gitignore) rules blocking `legal_and_governance/`, `field_reports/`, `*.pdf`, `*.docx`, and video formats from Git.

### Consequences
- Beneficiary dignity, thumbprint data, and medical details are safely quarantined from public web repositories.
- The public GitHub repository remains lightweight, secure, and clean.

---

## ADR 002: CRA International Compliance via Agency Agreement Model

- **Status:** Accepted & Implemented
- **Date:** 2026-05-23 / 2026-11-08

### Context
Under Canada Revenue Agency (CRA) regulations, Canadian charities and non-profits carrying out charitable activities outside Canada without qualified donees must maintain "direction and control" over their resources. Disbursing funds without a structured intermediary agreement risks non-compliance during CRA audits.

### Decision
Adopt the **International Agency Agreement** model:
- Maintain the executed International Agency Agreement with local representative Mr. Farzam (`legal_and_governance/International_Agency_Agreement_Farzam.pdf`).
- Require the field representative to produce structured periodic `Financial and Activity Reports` accounting for 100% of disbursed funds.
- Maintain a standardized 7-part attachment verification trail (vendor receipts, recipient sign-offs with thumbprints, and distribution videos).

### Consequences
- Full audit readiness for Canadian registered charity operations and annual CRA T3010 reporting.
- Standardized legal identity across all project reports: **Kindness for Afghans (Ontario Corporation No. 1001294785)**.

---

## ADR 003: Zero-Cost, Lightweight Python Static Site Generator (`Kindness.py`)

- **Status:** Accepted & Implemented
- **Date:** 2025-12-27 (Hardened 2026-11-08)

### Context
The organization needed a reliable, fast, zero-cost, and maintenance-free web presence for [kindnessforafghans.org](https://kindnessforafghans.org). Heavy CMS platforms (WordPress) require database maintenance, vulnerability patching, and ongoing hosting fees. Modern JavaScript frameworks (Next.js, Gatsby) require Node.js runtimes, package updates, and complex build steps.

### Decision
Use a lightweight, standalone Python static site generator ([`Kindness.py`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/Kindness.py)) that:
- Emits clean, dependency-free HTML and CSS.
- Adds timestamp-based cache busting for CSS (`styles.css?v=<timestamp>`).
- Provides 1-command build and automated Git deployment (`python Kindness.py --github`).
- Contains a built-in safety list (`PROTECTED_ITEMS`) to guarantee that building in the root directory never deletes legal or configuration files.

### Consequences
- Zero hosting costs (hosted on GitHub Pages).
- Maximum speed and accessibility worldwide, including on low-bandwidth mobile connections.
- Easily maintained by anyone with Python 3 installed.

---

## ADR 004: Zero-Platform-Fee Donation Architecture (Zeffy + Interac e-Transfer)

- **Status:** Accepted & Implemented
- **Date:** 2025-12-27 (Refined 2026-11-08)

### Context
Standard payment processors (Stripe, PayPal, CanadaHelps) deduct between 2.9% and 4% + fixed fees from every donation. For a small non-profit operating on direct relief, fees directly reduce the volume of food and medicine delivered.

### Decision
Adopt a dual zero-fee donation model on [`donate.html`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/donate.html):
1. **Zeffy (Online Credit Card / Debit):** 100% free platform specifically built for non-profits (funded by voluntary donor tips, charging 0% transaction and platform fees to the charity).
2. **Interac e-Transfer (Direct Canadian Banking):** Direct bank-to-bank transfers to `info@kindnessforafghans.org` with 0% processing fees.
3. **Direct Contact for Wire Transfers:** Display an email contact option for large international wires rather than exposing sensitive full wire routing information publicly.

### Consequences
- 100% of donor contributions go directly to humanitarian aid without third-party commission deductions.

---

## ADR 005: Standardized Field Attachment Audit Register

- **Status:** Accepted & Implemented
- **Date:** 2026-11-08

### Context
Field reports often reference multiple supporting attachments (receipts, sign-off sheets, photos, videos). Irregular naming conventions or unrecorded missing files complicate future financial audits.

### Decision
- Standardize all attachment file naming into `Attachment <N> <Description>.<ext>`.
- In each distribution folder, maintain an [`AUDIT_CHECKLIST.md`](file:///c:/Users/mahmadi/OneDrive%20-%20purdue.edu/kindnessforafghans/field_reports/2026-07_distribution/AUDIT_CHECKLIST.md) mapping expenditures, supporting attachments, verification status, and pending items.

### Consequences
- Immediate visibility on missing documentation.
- Streamlined handoff to accountants, legal advisors, and board members.

---

## ADR 006: GitHub Pages Deployment Pipeline with Custom Domain

- **Status:** Accepted & Implemented
- **Date:** 2025-12-27 (Re-verified 2026-11-08)

### Context
The custom domain `kindnessforafghans.org` needed DNS and SSL integration with GitHub Pages without vendor lock-in.

### Decision
- Host repository on GitHub: `mahmadi2025/kindness` (branch `main`).
- Maintain a root `CNAME` file pointing to `kindnessforafghans.org`.
- Configure DNS A records pointing to GitHub Pages IP addresses (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) with automatic HTTPS certificate provisioning.

### Consequences
- Highly available worldwide CDN delivery backed by GitHub and Fastly.
- Automatic HTTPS renewal at zero cost.
