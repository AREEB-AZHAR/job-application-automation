# Areeb Azhar — Autonomous Multi-Channel Job Application & Audit Pipeline

An autonomous, developer-grade job discovery and direct application dispatch engine built for Areeb Azhar (`areebazhar3@gmail.com`). Featuring a Linear/Vercel-inspired UI, it continuously ingests real job alert emails from Gmail, filters opportunities strictly for junior/entry-level roles (`<= 1 year of experience`), detects when job postings have closed or expired, pairs opportunities with domain-specific PDF resumes from Areeb's CV vault, auto-generates authentic engineering pitch notes, and executes verified live multi-channel applications with full visual audit proof.

---

## 🚀 Accomplishments & Real Live Application Dispatch

### 1. Channel 1: Authenticated LinkedIn Easy Apply (100% Unattended Auto-Submit)
- **Live Authentication**: Operates through the candidate's active LinkedIn session (`Areeb Azhar`, Iqra University alumni).
- **Search & Screening**: Discovers live junior roles in Pakistan filtered by `f_AL=true` (Easy Apply).
- **Autonomous End-to-End Execution**: Steps through candidate contact information, attached domain CV, and screening questionnaires, captures the pre-submission review snapshot, **automatically triggers submission without waiting for oversight**, and verifies the post-submission confirmation receipt.
- **Verified Submissions**:
  1. **Mobile Application Developer @ SQUATWOLF** ([Job ID: 4488936551](https://www.linkedin.com/jobs/view/4488936551/)):
     - **Stack & Focus**: React Native, iOS, Swift, cross-platform mobile development (Karachi on-site).
     - **Execution**: 100% unattended auto-submit.
     - **Pre-Submit Snapshot**: `data/proofs/job_047/pre_submit.png`
     - **Post-Submit Confirmation**: Verified dialog: *"Your application was sent to SQUATWOLF!"* (`data/proofs/job_047/post_submit.png`).
  2. **Frontend Developer @ SQUATWOLF** ([Job ID: 4488948133](https://www.linkedin.com/jobs/view/4488948133/)):
     - **Stack & Focus**: React, Next.js, TypeScript, Tailwind CSS (Karachi on-site).
     - **Pre-Submit Snapshot**: `data/proofs/job_046/pre_submit.png`
     - **Post-Submit Confirmation**: Verified status: *"Application status: Application submitted now"* (`data/proofs/job_046/post_submit.png`).

### 2. Channel 2: Direct Recruiter Email Dispatch (Gmail REST API)
- When LinkedIn posts or external listings are closed to Easy Apply but specify direct hiring manager/recruiter contact details in the job body:
  - **Tech Inoviq Solutions** (`hr@techinoviq.com`): Dispatched live application for *Software Engineer - HealthTech* with attached `Areeb_Azhar_Full_Stack_Web_CV.pdf` (Verified Gmail Message ID: `1a1f13cdc39c9479`).
  - **LeadingEdge HR Solutions** (`talent@leadingedge.plus`): Dispatched live application for *Junior Flutter Developer* with attached `Areeb Azhar - Flutter Developer Resume PDF.pdf` (Verified Gmail Message ID: `1a1f141aa03161bf`).
  - **DevDignus** (`hr@devdignus.com`): Extracted direct recruiter contact route from closed LinkedIn posting.

### 3. Channel 3: Public ATS Form Inspection & Automation
- Discovers and resolves off-LinkedIn application portals (e.g. Manatal ATS on `careers-page.com`, Greenhouse, Lever).
- Inspects mandatory vs optional fields, stages domain CVs for file input upload (`setInputFiles()`), and prepares form entries.

### 4. Closed Post Detection & Visual Audit Engine (`src/submission_verifier.py`)
- **"No longer accepting applications" Detection**: Autonomous scanning identifies when high-volume posts (100+ applicants) are closed by the hirer.
- **Job Expiration Handling**: Audits expired listings on Glassdoor/Indeed (e.g., *Vision IT Solutions* Django Developer - Entry Level), preventing failed submissions.
- **Composite Audit Snapshots**: Binds an audit verification banner onto real browser screenshots (`data/proofs/{job_id}/pre_submit.png`) documenting post status and alternate contact details.

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation, architecture & setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile, screening answers & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/
│   ├── assistant.py                   # Central coordinator (batch ingestion, evaluation & pipeline)
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
│   ├── server.py                      # Native Python HTTP server & proof image endpoints
│   └── screenshots/                   # Verified UI screenshots
└── data/
    ├── applications.json              # Active and prepared applications database (47 records)
    ├── scanned_jobs.json              # Historical ledger of all scanned & filtered jobs (122 records)
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
python web\server.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

From the dashboard you can:
- Review all submitted and audited job applications with company avatars, domain badges, and attached CVs.
- Filter by `Applied (Web Form)`, `Applied (Email Dispatched)`, or `Closed by Hirer`.
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
5. If closed but an alternate HR email is listed, dispatch or stage an email application with CV attached.
6. Record all outcomes in `data/applications.json` and `data/scanned_jobs.json`.

---

## 📸 Verified Application Proofs & Screenshots

| Target Opportunity | Application Mechanism | Verification Proof Status |
| :--- | :--- | :--- |
| **SQUATWOLF** (Mobile Application Developer) | LinkedIn Easy Apply (100% Unattended Auto-Submit) | Verified: *"Your application was sent to SQUATWOLF!"* (`job_047`) |
| **SQUATWOLF** (Frontend Developer) | LinkedIn Easy Apply (Live Submission) | Verified: *"Application submitted now"* (`job_046`) |
| **LeadingEdge HR Solutions** (Junior Flutter) | Direct Recruiter Email (`talent@leadingedge.plus`) + Manatal ATS | Verified Sent (Gmail Msg `1a1f141aa03161bf`) + ATS Form Proofs (`job_044`) |
| **Tech Inoviq Solutions** (Software Engineer) | Direct Recruiter Email (`hr@techinoviq.com`) | Verified Sent (Gmail Msg `1a1f13cdc39c9479`) + Inactive LinkedIn Audit (`job_023`) |
| **DevDignus** (Associate Operations) | Direct Recruiter Email (`hr@devdignus.com`) | Closed post audit proof + alternate route identified (`job_045`) |
| **Vision IT Solutions** (Django Developer) | Public Board Inspection | Glassdoor Inactive/Expired Audit (`data/proofs/job_019/pre_submit.png`) |

### Dashboard Live UI Preview
![Linear-Style Pipeline Dashboard](web/screenshots/dashboard_live_audit.png)
