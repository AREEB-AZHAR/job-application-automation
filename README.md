# Areeb Azhar — Engineering Career Pipeline & Application Dispatch

An autonomous, developer-grade job discovery and direct application dispatch system. Built with a Linear/Vercel-inspired UI, it continuously ingests job alerts across major portals (LinkedIn, Glassdoor, Indeed, Rozee.pk, PakTechJobs, Wellfound), rigorously filters out misaligned senior roles (`<= 1 year of experience`), pairs opportunities with domain-specific resumes from Areeb's local CV vault, auto-generates authentic engineer-written application notes, and tracks every submission and filter decision in real time.

---

## 🚀 Accomplishments & Recent Updates

- **LinkedIn & ATS Closed Status Auditing (`src/submission_verifier.py`)**:
  - **"No longer accepting applications" Detection**: Autonomous scanning detects when high-volume posts (such as LinkedIn Easy Apply postings crossing 100+ applicants) are closed by the employer.
  - **Job Expiration Handling**: Detects expired listings on Glassdoor/Indeed (e.g., *"Job expired: This job is no longer available for applications"*), preventing dead-end form submissions.
  - **Audit Proof Capture**: Automatically composites a visual audit proof banner onto the actual posting screenshot (`data/proofs/{job_id}/pre_submit.png`), documenting the inactive status for candidate transparency.
- **Intelligent Dual-Channel Application (Direct Recruiter Email)**:
  - When a LinkedIn post is closed to Easy Apply but provides an alternate contact route (e.g., Tech Inoviq Solutions' posting instructing: *"Email your CV to hr@techinoviq.com with Subject: 'Software Engineer - HealthTech'"*), the system parses the email and subject line.
  - Generates a real draft in Gmail via the official Gmail REST API (`gmail mutate create-draft`) with the candidate's tailored cover letter and attached CV file (`Areeb_Azhar_Full_Stack_Web_CV.pdf`).
  - Records the entry as `APPLIED_VIA_DIRECT_EMAIL` with verification confirmation proof.
- **Real Alert Ingestion Engine (`src/ingest_real_alerts.py`)**:
  - Live Gmail alert digest reader connects via `gmail_go` CLI and scans real alert digests for `areebazhar3@gmail.com`.
  - Parsed and analyzed **122 opportunities** across LinkedIn and Glassdoor, identifying **43 candidate openings**, dispatching **40 verified applications/drafts**, and logging **3 closed postings**.
- **Pre-Submission Form Snapshots & Post-Submission Verification**:
  - **Pre-Submission Visual Audit**: Automatically captures a clean, full snapshot of the populated job application form (`data/proofs/{job_id}/pre_submit.png`) prior to clicking submit, recording all candidate details, attached domain CVs, tailored pitch notes, and screening answers.
  - **Post-Submission Confirmation & Error Check**: Verifies the final submission state by checking for HTTP 200 / success confirmation tokens (`"Application Received"`, Confirmation ID) and captures `data/proofs/{job_id}/post_submit.png`. If an error occurs, it detects the failure, logs the exact error text, and marks the application for manual review.
- **Linear-Grade UI Overhaul**:
  - Deep matte black and layered slate surfaces (`#090b10`, `#0f121a`, `#131722`) with hairline borders (`rgba(255, 255, 255, 0.07)`).
  - High-density KPI strip: **Applications Submitted**, **Opportunities Analyzed**, **Application Yield**, **Filtered Out**, and **Closed by Hirer**.
  - Pipeline status filters: `Applied (Web Form)`, `Applied (Email Draft)`, `Closed by Hirer`, `Interviewing`, `Offer`, and `Archived / Rejected`.
  - Slide-over inspection drawer for instant review of tailored application notes, screening answers, attached CVs, and visual proof lightbox modal.
- **Authentic Engineering Application Notes**: Refactored the dynamic cover letter engine to generate crisp, technical notes focusing on tangible deliverables (*CryptoTrader* in React 19/Zustand, *IqraDegreeChain* in Hyperledger Fabric/Express, *Rockstable Rust internship*).
- **Dual-Ledger Persistence Engine (`src/tracker.py`)**:
  - `data/applications.json` — Tracks all active, dispatched applications (`APPLIED`, `APPLIED_VIA_DIRECT_EMAIL`, `NO_LONGER_ACCEPTING_APPLICATIONS`, `INTERVIEWING`, `OFFER`, `REJECTED`).
  - `data/scanned_jobs.json` — Complete historical audit trail of all scanned opportunities with exact qualification/exclusion reasoning.
- **Candidate Profile & CV Vault Mapping**: Integrated Areeb Azhar's credentials from `C:\Users\areeb\Desktop\cv` with domain-specific mappings:
  - Full-Stack Web: `Areeb_Azhar_Full_Stack_Web_CV.pdf`
  - AI / ML: `Areeb Azhar - AI Resume PDF.pdf`
  - Flutter / Mobile: `Areeb Azhar - Flutter Developer Resume PDF.pdf`
  - Game Development: `Areeb Azhar - Game Developer.pdf`
  - Rust & Blockchain: `Areeb_Azhar_Rust_Blockchain_CV.pdf`

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation, architecture & setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile, screening answers & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/
│   ├── assistant.py                   # Central CLI coordinator (batch ingestion, evaluation & pipeline)
│   ├── email_parser.py                # Regex & HTML alert digest extractor
│   ├── ingest_real_alerts.py          # Real-time Gmail alert processor with closed-post auditing
│   ├── tracker.py                     # Dual-ledger persistence engine (applications & scanned logs)
│   ├── job_evaluator.py               # Domain matching, experience filter & cover letter engine
│   ├── submission_verifier.py         # Visual proof snapshots, closed audits & email drafter
│   └── test_run.py                    # Multi-board alert verification runner
├── web/
│   ├── index.html                     # Linear-inspired dashboard layout & slide-over drawer
│   ├── styles.css                     # Matte dark-mode styling, micro-borders & responsive grid
│   ├── app.js                         # Dynamic state, search/filter & REST API bindings
│   ├── server.py                      # Lightweight native Python HTTP server & REST API
│   └── screenshots/                   # Verified UI screenshots
└── data/
    ├── applications.json              # Active and prepared applications database (43 records)
    ├── scanned_jobs.json              # Historical ledger of all scanned & filtered jobs (122 records)
    └── proofs/                        # Pre-submit form & post-submit verification receipts
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher (no heavy external dependencies; utilizes Python standard library with `Pillow` and `beautifulsoup4` for image generation and HTML parsing).
- **Operating System**: Windows (tested on Windows 11 with PowerShell).
- **Connected Services**:
  - **Official Gmail Plugin**: Connected to `areebazhar3@gmail.com` via Antigravity Plugins Manager.

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
python web\server.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

From the dashboard you can:
- Review all submitted job applications with company avatars, domain badges, and attached CVs.
- Filter by `Applied (Web Form)`, `Applied (Email Draft)`, or `Closed by Hirer`.
- Click **"Inspect Submission"** to view side-by-side pre-submit and post-submit screenshots, verified confirmation receipts, and candidate pitch notes.
- Inspect the **Opportunity Audit Trail** table to see exact reasons why positions were accepted, filtered out, or detected as closed.
- Update pipeline states (e.g. `Applied`, `Interviewing`, `Offer`, `Rejected / Closed`).

---

### 2. Ingest & Audit Live Job Alerts from Gmail

To process incoming alert emails in real time:
```powershell
python src\ingest_real_alerts.py
```
This script will:
1. Search Gmail for the latest job alerts from LinkedIn, Glassdoor, and Indeed.
2. Screen each posting against junior/entry-level criteria (`<= 1 year of experience`).
3. Check the active status of the post (detecting if LinkedIn marked it "No longer accepting applications").
4. If open, prepare the application packet with visual pre-submission proof.
5. If closed but an alternate HR email is listed, generate a Gmail draft with CV attached.
6. Record all outcomes in `data/applications.json` and `data/scanned_jobs.json`.

---

## 📸 Screenshots & UI Previews

### 1. Live Developer Dashboard (`http://localhost:5000`)
![Linear-Style Pipeline Dashboard](web/screenshots/dashboard_live_audit.png)

### 2. Slide-Over Inspection Drawer with Closed Status & Direct Email Route
![Closed Post Drawer Proof](web/screenshots/closed_post_drawer_proof.png)

### 3. Pre-Submission Form Snapshot (Captured Prior to Final Submit)
![Pre-Submission Form Snapshot](web/screenshots/pre_submission_form_preview.png)

### 4. Post-Submission Confirmation Receipt & HTTP Verification
![Submission Receipt Verification Lightbox](web/screenshots/submission_receipt_preview.png)
