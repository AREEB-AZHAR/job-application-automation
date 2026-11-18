# Autonomous Job Search & Application Automation

An intelligent, safety-conscious agentic automation system and interactive web dashboard that scans daily job alerts (LinkedIn, Indeed, Glassdoor, Rozee.pk, PakTechJobs, Wellfound), filters and scores matching opportunities against Areeb Azhar's candidate profile, prepares tailored application drafts with domain-specific CV routing, and tracks the entire scanning & application lifecycle with an audit command center.

---

## 🚀 Accomplishments & Recent Updates

- **Interactive Showcase & Audit Website (`web/`)**: Built a full-stack dashboard served via a lightweight native Python server (`web/server.py`) and modern dark-mode single-page application (`web/index.html`, `web/styles.css`, `web/app.js`):
  - **Applied & Ready for Review View**: Interactive cards for all qualified jobs, showcasing company meta, matched domain, status badges, attached CVs, direct job links, and a modal inspector with 1-click tailored cover letter copying.
  - **All Scanned & Filtered Audit Trail**: Complete historical ledger of every evaluated opportunity with color-coded qualification pills (`QUALIFIED` vs `DISQUALIFIED`), detailed rejection reasons (e.g., senior keyword in title, experience > 1 yr, stack mismatch), source platforms, and timestamps.
  - **Filter Analytics & Intelligence**: Live breakdown charts of rejection root causes and domain distribution across target verticals.
  - **On-the-Fly Opportunity Evaluator**: Built-in modal allowing users to paste any job description to test filtering and draft a tailored packet instantly.
  - **REST API Endpoints**: `/api/data` (metrics & records), `/api/status` (inline status updates), `/api/evaluate` (live scan).
- **Audit Logging Engine (`src/tracker.py`)**: Dual-ledger persistence:
  - `data/applications.json` — Tracks active and prepared application packets (`READY_FOR_REVIEW`, `SUBMITTED`, `INTERVIEWING`, `REJECTED`, `OFFER`).
  - `data/scanned_jobs.json` — Complete historical audit trail of all scanned opportunities.
- **Candidate Profile & CV Vault Mapping**: Integrated Areeb Azhar's credentials from `C:\Users\areeb\Desktop\cv` with domain-specific mappings:
  - Full-Stack Web: `Areeb_Azhar_Full_Stack_Web_CV.pdf`
  - AI / ML: `Areeb Azhar - AI Resume PDF.pdf`
  - Flutter / Mobile: `Areeb Azhar - Flutter Developer Resume PDF.pdf`
  - Game Development: `Areeb Azhar - Game Developer.pdf`
  - Rust & Blockchain: `Areeb_Azhar_Rust_Blockchain_CV.pdf`
- **Filtering Logic Verified**: Tested and verified strict `< 1 year of experience` qualification logic, rejecting senior roles (e.g., 3+ or 5+ years) and auto-routing entry-level/associate roles.
- **Tailored Cover Letter Generator**: Programmed dynamic cover letter drafting highlighting actual projects (*CryptoTrader*, *IqraDegreeChain*, *Bunetto*, *Rockstable x Hazara Rust internship*).
- **Daily Sidecar Automation**: Registered `Daily Job Search & Application Drafter` configured for daily execution at 8:00 AM Pakistan Standard Time (`CRON_TZ=Asia/Karachi 0 8 * * *`).

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
│   ├── tracker.py                     # Dual-ledger persistence engine (applications & scanned logs)
│   ├── job_evaluator.py               # Domain matching, experience filter & cover letter engine
│   └── test_run.py                    # Multi-board alert verification runner
├── web/
│   ├── index.html                     # Showcase dashboard layout & modal inspector
│   ├── styles.css                     # Dark-mode styling, glassmorphism & responsive grid
│   ├── app.js                         # Dynamic state, search/filter & REST API bindings
│   └── server.py                      # Lightweight native Python HTTP server & REST API
└── data/
    ├── applications.json              # Active and prepared applications database
    └── scanned_jobs.json              # Historical ledger of all scanned & filtered jobs
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher (no heavy external dependencies required; uses Python standard library `http.server`, `json`, `socketserver`).
- **Operating System**: Windows (tested with Windows PowerShell).
- **Recommended Plugins**:
  - **Gmail Plugin** (`antigravity-plugins-official/plugin/gmail`): To read incoming job alert emails directly.

---

## 🖥️ Local Execution & Running the Website

### 1. Launch the Job Showcase & Audit Website

Navigate to the project directory and start the local web server:
```powershell
cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
python web\server.py
```

Open your browser and navigate to:
👉 **`http://localhost:5000`**

From the dashboard you can:
- Review all prepared job applications and their tailored cover letters.
- Inspect the **Scanned & Filtered Log** to see why jobs were accepted or disqualified.
- Update pipeline statuses (e.g., mark as `SUBMITTED`, `INTERVIEWING`).
- Click **"+ Evaluate New Job"** to test any job post on the fly.

---

### 2. Run the CLI Assistant & Verification Suite

- **Process a batch of alert leads**:
  ```powershell
  python src\assistant.py
  ```
- **View current pipeline CLI metrics**:
  ```powershell
  python src\assistant.py --pipeline
  ```
- **Execute the test suite**:
  ```powershell
  python src\test_run.py
  ```

---

## ⚙️ Daily Automation Schedule & Enabling Instructions

The background sidecar is registered under:
- **Automation Display Name**: `Daily Job Search & Application Drafter`
- **Schedule**: Daily at 8:00 AM (Asia/Karachi)
- **Permissions**: Scoped read access to `C:\Users\areeb\Desktop\cv` and workspace files.

To enable the automation:
1. Open the Automations dashboard: [Open Automations Dashboard](sidecar://dashboard).
2. Locate **Daily Job Search & Application Drafter**.
3. Toggle it to **Enabled**.

---

## 📸 Screenshots & UI Previews

### Live Web Dashboard (`http://localhost:5000`)
![AutoJobBot Live Dashboard](web/screenshots/dashboard_preview.png)

> **Screenshot Request**: After launching the dashboard and applying to opportunities, please also capture:
> 1. The **All Scanned & Filtered Log** tab showing detailed disqualification root causes.
> 2. The **Inspect Application Packet** modal displaying the tailored cover letter and attached CV.
