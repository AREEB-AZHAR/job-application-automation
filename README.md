# Autonomous Job Search & Application Automation

An intelligent, safety-conscious agentic automation system that scans daily job alert emails (LinkedIn, Indeed, Glassdoor), filters and scores matching opportunities against your candidate profile, prepares tailored application drafts, and tracks pipeline status.

---

## 🚀 Accomplishments & Recent Updates

- **Architecture & Implementation Plan Finalized**: Detailed plan documented in [job_automation_architecture_plan.md](file:///C:/Users/areeb/.gemini/antigravity/brain/e3d8c435-2a59-4947-8581-5602fba5c6aa/job_automation_architecture_plan.md).
- **Candidate Profile & CV Vault Mapping**: Integrated Areeb Azhar's credentials from `C:\Users\areeb\Desktop\cv` with domain-specific mappings:
  - Full-Stack Web: `Areeb_Azhar_Full_Stack_Web_CV.pdf`
  - AI / ML: `Areeb Azhar - AI Resume PDF.pdf`
  - Flutter / Mobile: `Areeb Azhar - Flutter Developer Resume PDF.pdf`
  - Game Development: `Areeb Azhar - Game Developer.pdf`
  - Rust & Blockchain: `Areeb_Azhar_Rust_Blockchain_CV.pdf`
- **Filtering Logic Verified**: Tested and verified strict `< 1 year of experience` qualification logic, rejecting senior roles (e.g., 3+ or 5+ years) and auto-routing entry-level/associate roles.
- **Tailored Cover Letter Generator**: Programmed dynamic cover letter drafting highlighting actual projects (CryptoTrader, IqraDegreeChain, Bunetto, Rust internship).
- **Sidecar Automation Configured**: Created `Daily Job Search & Application Drafter` sidecar configured for daily execution at 8:00 AM Pakistan Standard Time (`CRON_TZ=Asia/Karachi 0 8 * * *`).

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation and setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/
│   ├── job_evaluator.py               # Domain matching, experience filter & cover letter engine
│   └── test_run.py                    # Verification script testing multi-board alert batches
└── data/                              # Application tracking database
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher.
- **Antigravity Plugins**:
  - **Gmail Plugin** (`antigravity-plugins-official/plugin/gmail`): Recommended to read incoming job alerts directly from your Gmail inbox.
- **Operating System**: Windows (tested on Windows PowerShell).

### Local Execution Instructions

1. Navigate to the project directory:
   ```powershell
   cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
   ```
2. Execute the verification suite:
   ```powershell
   python src\test_run.py
   ```
   **Test Output Example:**
   ```
   [LinkedIn Alerts] Junior Full Stack Developer @ Apex Technologies (Lahore (Hybrid))
    -> Result: Accepted: Matches domain and experience criteria (< 1 year)
    -> Selected CV: C:\Users\areeb\Desktop\cv\Areeb_Azhar_Full_Stack_Web_CV.pdf

   [Indeed Daily Alert] Senior Frontend Engineer @ Global Cloud Corp (Remote)
    -> Result: Disqualified: Title contains senior keyword 'senior'

   [LinkedIn Alerts] Associate Flutter Developer @ MobileCraft Studios (Karachi (On-site))
    -> Result: Accepted: Matches domain and experience criteria (< 1 year)
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
