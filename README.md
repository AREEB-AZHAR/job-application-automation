# Autonomous Job Search & Application Automation

An intelligent, safety-conscious agentic automation system that scans daily job alert emails (LinkedIn, Indeed, Glassdoor, Rozee, PakTechJobs), filters and scores matching opportunities against Areeb Azhar's candidate profile, prepares tailored application drafts with domain-specific CV routing, and tracks pipeline status in a persistent database.

---

## 🚀 Accomplishments & Recent Updates

- **Autonomous Assistant Initialization & Operational Master Plan**: Comprehensive roadmap finalized in [job_search_assistant_plan.md](file:///C:/Users/areeb/.gemini/antigravity/brain/afc4de98-f6c8-4d9c-b23a-d789716be675/job_search_assistant_plan.md).
- **Persistent Pipeline Tracker (`src/tracker.py`)**: Implemented full application lifecycle tracking in `data/applications.json` supporting statuses (`READY_FOR_REVIEW`, `SUBMITTED`, `INTERVIEWING`, `REJECTED`, `OFFER`).
- **Interactive Assistant CLI (`src/assistant.py`)**: Built command-line coordinator with `--pipeline` visualizer and automated batch assessment engine.
- **Candidate Profile & CV Vault Mapping**: Integrated Areeb Azhar's credentials from `C:\Users\areeb\Desktop\cv` with domain-specific mappings:
  - Full-Stack Web: `Areeb_Azhar_Full_Stack_Web_CV.pdf`
  - AI / ML: `Areeb Azhar - AI Resume PDF.pdf`
  - Flutter / Mobile: `Areeb Azhar - Flutter Developer Resume PDF.pdf`
  - Game Development: `Areeb Azhar - Game Developer.pdf`
  - Rust & Blockchain: `Areeb_Azhar_Rust_Blockchain_CV.pdf`
- **Filtering Logic Verified**: Tested and verified strict `< 1 year of experience` qualification logic, rejecting senior roles (e.g., 3+ or 5+ years) and auto-routing entry-level/associate roles.
- **Tailored Cover Letter Generator**: Programmed dynamic cover letter drafting highlighting actual projects (CryptoTrader, IqraDegreeChain, Bunetto, Rockstable x Hazara Rust internship).
- **Sidecar Automation Configured**: Registered `Daily Job Search & Application Drafter` configured for daily execution at 8:00 AM Pakistan Standard Time (`CRON_TZ=Asia/Karachi 0 8 * * *`).

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation and setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile, screening answers & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/
│   ├── assistant.py                   # Central CLI coordinator (batch ingestion, evaluation & pipeline)
│   ├── tracker.py                     # Application tracking store and status lifecycle engine
│   ├── job_evaluator.py               # Domain matching, experience filter & cover letter engine
│   └── test_run.py                    # Verification script testing multi-board alert batches
└── data/
    └── applications.json              # Local persistent application tracking database
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher.
- **Git**: Configured with local repository.
- **Recommended Plugins**:
  - **Gmail Plugin** (`antigravity-plugins-official/plugin/gmail`): To read incoming job alert emails directly.
- **Operating System**: Windows (tested with Windows PowerShell).

### Local Execution Instructions

1. Navigate to the project directory:
   ```powershell
   cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
   ```

2. Process a new batch of job opportunities:
   ```powershell
   python src\assistant.py
   ```

3. View current application pipeline & tracking status:
   ```powershell
   python src\assistant.py --pipeline
   ```

4. Run the standalone unit and evaluation tests:
   ```powershell
   python src\test_run.py
   ```

   **Test Output Example:**
   ```
   [LinkedIn Alerts] Junior Full Stack Developer @ Apex Technologies (Lahore (Hybrid))
    -> Assessment: Accepted: Matches domain and experience criteria (< 1 year)
    -> Status: READY_FOR_REVIEW
    -> Selected CV: C:\Users\areeb\Desktop\cv\Areeb_Azhar_Full_Stack_Web_CV.pdf

   [Indeed Daily Alert] Senior Frontend Engineer @ Global Cloud Corp (Remote)
    -> Assessment: Disqualified: Title contains senior keyword 'senior'

   [LinkedIn Alerts] Associate Flutter Developer @ MobileCraft Studios (Karachi (On-site))
    -> Assessment: Accepted: Matches domain and experience criteria (< 1 year)
    -> Status: READY_FOR_REVIEW
    -> Selected CV: C:\Users\areeb\Desktop\cv\Areeb Azhar - Flutter Developer Resume PDF.pdf
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

*(Screenshots will be added once captured from the active dashboard)*.
> **Screenshot Request**: After activating the automation in the Automations dashboard (`sidecar://dashboard`), please take a screenshot of:
> 1. The active `Daily Job Search & Application Drafter` sidecar card in the Automations Dashboard.
> 2. The morning digest summary card rendered in your conversation feed.
