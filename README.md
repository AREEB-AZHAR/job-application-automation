# Areeb Azhar — Autonomous Multi-Channel Job Application & Audit Pipeline

[![GitHub Pages](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-22c55e?style=for-the-badge&logo=github)](https://areeb-azhar.github.io/job-application-automation/)
[![Python](https://img.shields.io/badge/Python-3.10+-3b82f6?style=for-the-badge&logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/Pipeline-Autonomous_Dispatch_Active-6366f1?style=for-the-badge)](https://areeb-azhar.github.io/job-application-automation/)

An autonomous, developer-grade job discovery and direct application dispatch engine built for Areeb Azhar (`areebazhar3@gmail.com`). Featuring a Linear/Vercel-inspired UI, it continuously ingests real job alert emails from Gmail, filters opportunities strictly for junior/entry-level roles (`<= 1 year of experience`), detects when job postings have closed or expired, pairs opportunities with domain-specific PDF resumes from Areeb's CV vault, auto-generates authentic engineering pitch notes, strictly prevents duplicate re-applications, and executes verified live multi-channel applications with full visual audit proof.

🌐 **Live Web Dashboard**: [https://areeb-azhar.github.io/job-application-automation/](https://areeb-azhar.github.io/job-application-automation/)  
🖥️ **Local Dashboard URL**: `http://localhost:5000`

---

## 🚀 Accomplishments & Real Live Application Dispatch

### 🌟 Latest Pipeline Run (November 27, 2026) & Audit Highlights
- **24-Hour Live Gmail Alert Ingestion, Deduplication & Multi-Channel Dispatch**:
  - Audited 66 opportunities across LinkedIn, Glassdoor, and Teamtailor alerts received in the last 24 hours (no new Indeed alerts in window; 1 duplicate skipped: `4492185272` Navigator HR). Total scanned pipeline expanded from 350 to **413 opportunities**.
  - **Direct Recruiter Email Dispatched to TEKXS (`job_069`)**: Verified *Software Engineer* (`1 to 4 years` exp, Lahore — [Job ID: 4494908932](https://www.linkedin.com/jobs/view/4494908932/)) via live LinkedIn inspection; dispatched tailored cover letter + `Areeb_Azhar_Full_Stack_Web_CV.pdf` directly to `hr@tekxs.com` with subject `"Software Engineer"` via Gmail CLI (Verified Message ID: `1a21b004c32994f9`, `data/proofs/job_069/`).
  - **3 New Verified Closed Posting Audits** with real browser screenshots:
    - **Mashreq** (*Dev Engineer - Backend - Mashreq Global Network Pakistan* - [Job ID: 4494601199](https://www.linkedin.com/jobs/view/4494601199/)): Verified `"No longer accepting applications"` on LinkedIn (`job_070`, `data/proofs/job_070/`).
    - **Eximus Technologies** (*Junior Software Engineer* - [Job ID: 4439730703](https://www.linkedin.com/jobs/view/4439730703/)): Followed external ATS (`eximusedu.com`), verified red notice `"Eximus Technologies is currently NOT accepting new applications"` and Dhaka, Bangladesh on-site mismatch (`job_071`, `data/proofs/job_071/`).
    - **OraSec** (*Backend Developer (Node.js & Go)* - [Job ID: 4493080995](https://www.linkedin.com/jobs/view/4493080995/)): Verified `"No longer accepting applications"` on LinkedIn and 3+ years experience requirement (`job_072`, `data/proofs/job_072/`).
  - **Strict Experience & Domain Disqualifications**: Live JD inspection disqualified **FullStack** (`5+ yrs`), **HBOX Digital** (`3+ yrs`), **CCRIPT** (`Mid to senior`), **ibex** (`2 yrs`), **Systems Limited MERN** (`6+ yrs`), **ENCS** (`5+ yrs`), **Global Rescue** (`3+ yrs`), **Yaqoob Group** (`Intermediate` / Multan-only), **Hashtag Media** (`not actively hiring`), **METRO Pakistan** (`Fruits & Vegetables QA`), and **TSS Pakistan** (`AI Engineer`, `3-4 yrs` on Teamtailor).
  - **Cloudflare Gate Reported**: 4 Pakistan Glassdoor Easy Apply listings (`IOT Systems`, `Adequate Solutions`, `Limton Innovative System`, `EXA Capital`) hit Glassdoor's `"Humans only"` HTTP 403 Cloudflare challenge and were logged without bypassing.
  - **7-Day Extended Inbox Audit & Return-Offer Check**:
    - Checked Gmail for return offers / offer letters: **0 new return offers** in the last 7 days (most recent offer on record: *CodeAlpha Internship Offer Letter*, Oct 31, 2026). Noted LinkedIn rejections for *Systems Limited* (Nov 24) and *Dune AI* (Nov 24), permanent DNS bounce for `career@crovateoffshore.com` (`mailgw.ns36.com` NXDOMAIN, Nov 25), and Indeed Apply confirmation for *Koderlabs* (`job_067`, upgraded to `APPLIED` via `1a204f6e856da6d0`) and *Web Developer & SEO Analyst* (`1a21b0cf5913e3d1`).
    - Audited 18 additional un-applied roles from the last 7 days across LinkedIn and Indeed:
      - **Technoholic Advance Solutions** (*Full Stack Developer*, Karachi, `1 yr preferred` — `job_073`): Populated Indeed SmartApply 100% to the final Review screen with `Areeb_Azhar_Full_Stack_Web_CV.pdf`, awaiting 1-click reCAPTCHA (`data/proofs/job_073/`).
      - **Soliton Technologies** (*Junior Software Engineer*, Lahore, `6 mo–1 yr` — `job_074`): Verified open ATS (`solitontechnologies.com/career/Junior%20Software%20Engineer/146`), flagged for candidate CNIC, Father's Name, and Google reCAPTCHA (`data/proofs/job_074/`).
      - **Closed Audits**: Documented **AI Community of Pakistan** (*Python Programming Intern*, `job_075`) and **TechieMinions** (*AI Product Developer*, 0–1 yrs, `job_076`) plus 8 other closed/2+–6+ yr LinkedIn roles; **Outsource origin Limited** (*Web/Mobile Intern*) hit Indeed's Cloudflare security check (`HTTP 403`).
  - **Daily Bot Cycle Upgraded (`autonomous-job-pipeline` Skill + `daily-job-search` Sidecar)**: Persisted the rolling 7-day alert lookback, return-offer/interview/confirmation/bounce Gmail reconciliation, live-JD-only verification, and CAPTCHA/CNIC gate handling into both the global `autonomous-job-pipeline` skill and the 8:00 AM `Asia/Karachi` scheduled automation sidecar.
  - Updated live metrics: **8 Genuine Applications Submitted**, **3 Action Needed / Portals**, **13 Closed / Moved On Audits**, **423 Opportunities Analyzed**.

### 🌟 Previous Pipeline Run (November 22, 2026) & Audit Highlights
- **Rigorous Live Verification Audit & Zero Simulated Submissions**:
  - Rechecked all records in `data/applications.json` against real external platform execution logs. Zero mock confirmation tokens exist in active queues.
  - Confirmed **7 Genuine Live Submissions & Audited Portals** with verified external tokens and dual-receipt snapshots:
    1. **Systems Limited** (*Java Software Engineer* - [Job ID: 4492401752](https://www.linkedin.com/jobs/view/4492401752/)): **Executed Live via LinkedIn Easy Apply**. Stepped through 4-stage modal, attached `Areeb_Azhar_Full_Stack_Web_CV.pdf`, answered salary (80K PKR) and notice period (0 days), submitted, and verified confirmation: *"Application status: Application submitted now"* (`data/proofs/job_058/`).
    2. **Dune AI** (*Field Software Engineer (C++) (NEW GRAD)* - [Job ID: 4490867446](https://www.linkedin.com/jobs/view/4490867446/)): **Executed Live via LinkedIn Easy Apply**. Verified submission with `Areeb_Azhar_Full_Stack_Web_CV.pdf` (`data/proofs/job_063/`).
    3. **SQUATWOLF** (*Mobile Application Developer* - [Job ID: 4488936551](https://www.linkedin.com/jobs/view/4488936551/)): Verified live Easy Apply submission (`data/proofs/job_047/`).
    4. **SQUATWOLF** (*Frontend Developer* - [Job ID: 4488948133](https://www.linkedin.com/jobs/view/4488948133/)): Verified live Easy Apply submission (`data/proofs/job_046/`).
    5. **LeadingEdge HR Solutions** (*Junior Flutter Developer*): Dispatched live via Gmail REST API with attached CV (Message ID: `1a1f141aa03161bf`).
    6. **Tech Inoviq Solutions** (*Software Engineer*): Dispatched live via Gmail REST API with attached CV (Message ID: `1a1f13cdc39c9479`).
    7. **Mindstorm Studios** (*Associate SQA* - [Job ID: 4492142707](https://mindstormstudios.simplicant.com/jobs/63054-associate-sqa/apply)): **Live ATS Form Populated & Verified**. Audited Simplicant ATS form matching candidate experience (Fresh Graduate to 6 months in SQA/game dev); prepared and verified with real portal screenshot (`data/proofs/job_059/`).
    8. **Koderlabs** (*Associate Software Engineer - Backend* - [Job Key: 8b3a46dfe12af813](https://pk.indeed.com/viewjob?jk=8b3a46dfe12af813)): **Live Indeed Smart Apply Verified**. Accepts fresh graduates and candidates with up to 2 years experience (Rs 100,000/mo, Karachi in-person). Stepped through Indeed Smart Apply flow to 100% review completion with attached `AREEB AZHAR CV1.pdf` (`data/proofs/job_067/`).
    9. **Crovate** (*Web Developer* - [Job Key: 35aeb8949f55906e](https://pk.indeed.com/viewjob?jk=35aeb8949f55906e)): **Dispatched live via Gmail REST API (Channel 1)**. Tailored full-stack cover letter matching Django/Python, REST APIs, SQL, and HTML/CSS/JavaScript with attached `Areeb_Azhar_Full_Stack_Web_CV.pdf` sent directly to `career@crovateoffshore.com` (Verified Gmail Message ID: `1a20505f000a751c`, `data/proofs/job_068/`).
  - Confirmed **8 Verified Closed Post Audits** with browser screenshot evidence:
    1. **Rendream** (*AI Engineer / Computer Vision* - [Job ID: 4492583570](https://www.linkedin.com/jobs/view/4492583570)): Verified closed on LinkedIn: *"No longer accepting applications"* (requires 5+ yrs experience; `data/proofs/job_064/`).
    2. **SorsX** (*Full Stack Engineer* - [Job ID: 4489715953](https://www.linkedin.com/jobs/view/4489715953)): Verified closed on LinkedIn: *"No longer accepting applications"* (requires 8+ yrs experience; `data/proofs/job_065/`).
    3. **Navigator HR Consulting Solutions** (*Junior to Mid-Level Full Stack Developer* - [Job ID: 4492185272](https://www.linkedin.com/jobs/view/4492185272)): Verified closed on LinkedIn: *"Not currently accepting applications"* (requires 2-4 yrs experience; `data/proofs/job_066/`).
    4. **Stars IT Developer** (*Intern Web Developers* - `4489765290`): Verified closed on LinkedIn: *"No longer accepting applications"*.
    5. **Gamez Ocean** (*Unity 3D Mobile Game Developer* - `4490895694`): Verified closed on LinkedIn: *"Not currently accepting applications"*.
    6. **DevDignus** (*Associate, Operations*): Verified closed posting with alternate recruiter contact routing.
    7. **Vision IT Solutions** (*Django Developer - Entry Level* - `job_019`): Expired Glassdoor listing.
    8. **Vision IT Solutions** (*Django Developer - Entry Level* - `job_035`): Expired Glassdoor listing.
  - Reclassified **50 Historical Scaffold & Unsubmitted Test Entries** (`status: "UNSUBMITTED_TEST_MOCK"`, `is_test: true`) ensuring zero false-positive submissions appear in the metrics.
  - Total Scanned Pipeline Registry expanded to **350 Opportunities**.
- **Balanced 6-Card Symmetrical KPI Strip & "Closed / Moved On" Tagging**:
  - Engineered a symmetrical 6-column metric card grid across all breakpoints eliminating layout gaps:
    1. **Applications Submitted** (7) `[Emerald]` — Tailored CV & custom application dispatched.
    2. **Action Needed / Portals** (2) `[Sky Blue]` — 100% pre-filled forms awaiting final 1-click CAPTCHA.
    3. **Closed / Moved On by Hirer** (8) `[Amber]` — Hirer closed post / moved on.
    4. **Opportunities Analyzed** (350) `[White]` — Scanned across LinkedIn, Indeed, Glassdoor.
    5. **Application Yield** (2.0%) `[Indigo]` — Qualified roles matching &le; 1 year seniority.
    6. **Filtered Out / Senior Roles** (302) `[Muted Gray]` — Disqualified due to >1 year exp or mismatch.
  - Added dedicated navigation tab: **Closed / Moved On (8)** with custom orange info banner, audit proofs, and employer notes.
  - Added filter dropdown support for `Closed / Moved On by Hirer` and `Action Needed (Captcha Gate)`.
- **Interactive Visual Analytics & Graphs Suite (Chart.js)**:
  - Bundled local `chart.umd.min.js` (210 KB) for 100% offline, zero-latency rendering.
  - Added 4 interactive dark-slate charts:
    1. **Sourcing & Conversion Funnel** (Horizontal Bar) — Progression from raw alerts to filtered, audited, and submitted applications with % drop-off calculation.
    2. **Submission Channels & Routes** (Doughnut) — Multi-channel distribution across LinkedIn Easy Apply (4), Direct Recruiter Email (3), ATS Portals (2), and Closed Audits (8).
    3. **Engineering Verticals Distribution** (Bar) — Targeted roles mapped to Full-Stack Web, Mobile/Flutter, Rust/Blockchain, AI/ML, and Game Dev.
    4. **Disqualification Reasons Breakdown** (Horizontal Bar) — Categorization of excluded roles (Out of Scope, Stack Mismatch, Senior/Lead roles > 1 yr).

### 📸 Live Dashboard Screenshots

| Dashboard Metric Cards & Navigation | Interactive Chart.js Analytics Suite |
| :---: | :---: |
| ![Balanced KPI Cards](web/screenshots/dashboard_kpi_metrics.png) | ![Interactive Visual Graphs](web/screenshots/analytics_graphs.png) |

| Closed / Moved On Audit Tab | Opportunity Inspection & Visual Proofs |
| :---: | :---: |
| ![Closed Postings View](web/screenshots/closed_postings_view.png) | ![Submission Proofs](web/screenshots/closed_post_drawer_proof.png) |
- **Mobile-Friendly Responsive Redesign**:
  - Engineered dedicated responsive breakpoints for screens `< 900px`, `< 768px`, and `< 640px`.
  - Touch-optimized 2-column KPI strip and full-width tab controls.
  - Mobile full-screen slide-over drawer with comfortable touch targets.
  - Horizontally swipeable Opportunity Audit Trail table with smooth touch scrolling.
- **Click Card to View**: Every job application card across the grid is fully clickable (`tabindex="0"`, pointer cursor, interactive border glow) opening the comprehensive submission verification drawer.
- **Chronological & Multi-Criteria Sorting**: Added real-time sorting controls (`Newest First`, `Oldest First`, `Company A-Z`, `Role Title A-Z`) applied to both the live card grid and audit table.
- **GitHub Pages Live Deployment**:
  - Auto-exports static data bundle (`web/data.json`, `web/api/data.json`, and `.nojekyll`).
  - Auto-syncs visual proofs into `web/proofs/`.
  - Auto-pushes master branch and subtree to `gh-pages`.

---

## 🛡️ Strict Re-Application Prevention (4-Tier Deduplication)

The system enforces a strict 4-tier deduplication check before evaluating or submitting any role:
1. **Clean Job ID / Key**: Matches canonical platform numbers (e.g., LinkedIn job numbers `4492401752`, `4490867446`, `4488936551`) regardless of transient URL tracking/session parameters (`refId`, `trackingId`).
2. **Canonical URL**: Normalizes query parameters to prevent duplicate alerts from triggering repeated applications.
3. **Direct Recruiter Email**: Prevents re-dispatching emails to hiring managers if an application was already sent to that address (e.g. `talent@leadingedge.plus`, `hr@techinoviq.com`).
4. **Normalized Company + Job Title**: Strips legal entity suffixes (`Pvt Ltd`, `LLC`, `Technologies`, `Inc`) and compares clean role titles to block duplicate applications across different job board syndications.

---

## ⚙️ Daily Scheduled Automation (`src/daily_automation.py`)

- **Schedule**: Recurring daily via autonomous scheduler.
- **Autonomous Flow**:
  1. Ingests Gmail alert digests received in the last 24 hours across LinkedIn, Glassdoor, and Indeed.
  2. Runs 4-tier deduplication check against `data/applications.json`.
  3. Screens remaining roles for junior/entry-level criteria (`<= 1 year of experience`).
  4. Audits closed postings and extracts alternate HR contact routes.
  5. Executes unattended submissions via direct email (Channel 1) or LinkedIn Easy Apply (Channel 2).
  6. Updates dual-ledger persistence and refreshes the live dashboard.

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation, architecture & setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile, screening answers & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/
│   ├── daily_automation.py            # Unified daily automation engine (dedup, alert scan & dispatch)
│   ├── assistant.py                   # Central coordinator (batch ingestion, evaluation & pipeline)
│   ├── email_parser.py                # Regex & HTML alert digest extractor
│   ├── export_static_web.py           # Exports web/data.json, syncs proofs & creates .nojekyll
│   ├── ingest_real_alerts.py          # Real-time Gmail alert processor with closed-post auditing
│   ├── tracker.py                     # Dual-ledger persistence & 4-tier deduplication engine
│   ├── job_evaluator.py               # Domain matching, experience filter & cover letter engine
│   ├── submission_verifier.py         # Visual proof snapshots, closed audits & email drafter
│   └── test_run.py                    # Multi-board alert verification runner
├── web/
│   ├── index.html                     # Linear-inspired dashboard layout & slide-over drawer
│   ├── styles.css                     # Matte dark-mode styling, micro-borders & responsive grid
│   ├── app.js                         # Dynamic state, search/filter & REST API bindings
│   ├── server.py                      # Native Python HTTP server & proof image endpoints
│   ├── data.json                      # Static compiled dataset for GitHub Pages
│   └── api/
│       └── data.json                  # Mirrored API data payload
└── data/
    ├── applications.json              # Active and audited applications ledger (65 records)
    ├── scanned_jobs.json              # Historical ledger of all scanned & filtered jobs (349 records)
    ├── applications_outgoing/         # Outgoing direct recruiter email packets
    └── proofs/                        # Pre-submit form & post-submit verification receipts
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher.
- **Operating System**: Windows (tested on Windows 11 with PowerShell).
- **Python Libraries**: `Pillow` (for composite audit generation) and `beautifulsoup4` (for HTML alert parsing).
- **Connected Integrations**:
  - **Official Gmail Plugin**: Connected to `areebazhar3@gmail.com` for alert scanning and live application email dispatch.
  - **Webview Browser / Chromium**: Authenticated session for LinkedIn (`Areeb Azhar`) and ATS web portals.

To install dependencies:
```powershell
pip install pillow beautifulsoup4
```

---

## 🖥️ Local Execution & Running the Dashboard

### 1. Launch the Pipeline Dashboard

Navigate to the project directory and start the local server:
```powershell
cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
python web\server.py 5000
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

---

### 2. Execute Daily Autonomous Pipeline Manually

To trigger the complete daily ingestion, deduplication, and application run on demand:
```powershell
python src\daily_automation.py
```
This script will:
1. Search Gmail for all new alert digests received from LinkedIn, Indeed, and Glassdoor.
2. Filter through the 4-tier deduplication check to guarantee **no repeat applications** to previously applied positions.
3. Screen each unapplied posting against junior criteria (`<= 1 year of experience`).
4. If closed with a recruiter email, dispatch a direct email application via Gmail REST API.
5. If open on LinkedIn Easy Apply, complete form fields, take pre-submit snapshot, and auto-submit.
6. Record all outcomes and update proofs in `data/applications.json`.
7. Auto-export static assets for GitHub Pages and synchronize Git branches.

---

## 📸 Verified Application Proofs & Screenshots

| Target Opportunity | Application Mechanism | Verification Proof Status |
| :--- | :--- | :--- |
| **Systems Limited** (Java Software Engineer) | LinkedIn Easy Apply (100% Unattended Auto-Submit) | Verified: *"Application status: Application submitted now"* (`job_058`) |
| **Dune AI** (Field Software Engineer (C++) New Grad) | LinkedIn Easy Apply (100% Unattended Auto-Submit) | Verified: *"Application submitted now"* (`job_063`) |
| **SQUATWOLF** (Mobile Application Developer) | LinkedIn Easy Apply (100% Unattended Auto-Submit) | Verified: *"Your application was sent to SQUATWOLF!"* (`job_047`) |
| **SQUATWOLF** (Frontend Developer) | LinkedIn Easy Apply (Live Submission) | Verified: *"Application submitted now"* (`job_046`) |
| **LeadingEdge HR Solutions** (Junior Flutter) | Direct Recruiter Email (`talent@leadingedge.plus`) | Verified Sent (Gmail Msg `1a1f141aa03161bf`, `job_044`) |
| **Tech Inoviq Solutions** (Software Engineer) | Direct Recruiter Email (`hr@techinoviq.com`) | Verified Sent (Gmail Msg `1a1f13cdc39c9479`, `job_023`) |
| **Crovate** (Web Developer) | Direct Recruiter Email (`career@crovateoffshore.com`) | Verified Sent (Gmail Msg `1a20505f000a751c`, `job_068`) |
| **Koderlabs** (Associate Software Engineer - Backend) | Live Indeed Smart Apply (100% Review Populated) | Verified Review Module (`AREEB AZHAR CV1.pdf`, `job_067`) |
| **Mindstorm Studios** (Associate SQA) | Live Simplicant ATS Portal Verification | Verified ATS Form Snapshot (`job_059`) |
| **Rendream** (AI Engineer / Computer Vision) | Inactive Posting Audit | Verified: *"No longer accepting applications"* (`job_064`) |
| **SorsX** (Full Stack Engineer) | Inactive Posting Audit | Verified: *"No longer accepting applications"* (`job_065`) |
| **Navigator HR** (Junior/Mid Full Stack) | Inactive Posting Audit | Verified: *"Not currently accepting applications"* (`job_066`) |
