# Autonomous Job Search & Application Automation

An intelligent, safety-conscious agentic automation system that scans daily job alert emails (LinkedIn, Indeed, Glassdoor), filters and scores matching opportunities against your candidate profile, prepares tailored application drafts, and tracks pipeline status.

---

## 🚀 Accomplishments & Recent Updates

- **Candidate Profile Configured**: Tailored profile established in `config/candidate_profile.json` using Areeb Azhar's credentials from `C:\Users\areeb\Desktop\cv`.
- **Experience Filter Embedded**: Strict filtering applied for entry-level / junior opportunities requiring **less than 1 year of experience** (<1 year / fresh graduate).
- **Multi-Domain CV Vault Integrated**: Mapped specialized resumes for Full-Stack, AI/ML, Flutter, Game Dev, and Rust/Blockchain.
- **Workflow Safety Ensured**: Implemented a mandatory pre-submission notification policy—every prospective role is matched, drafted, and presented for approval before external application.
- **Architecture & Implementation Plan Updated**: See [job_automation_architecture_plan.md](file:///C:/Users/areeb/.gemini/antigravity/brain/e3d8c435-2a59-4947-8581-5602fba5c6aa/job_automation_architecture_plan.md).

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation and setup instructions
├── config/
│   ├── candidate_profile.json         # Active candidate profile & CV mapping
│   └── candidate_profile.template.json # Template schema
├── src/                               # Automation scripts & helpers
└── data/                              # Application tracking database
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher.
- **Antigravity Plugins**:
  - **Gmail Plugin** (`antigravity-plugins-official/plugin/gmail`): Required to search and read job alert emails from Gmail securely.
- **Operating System**: Windows (tested with PowerShell).

### Local Setup Instructions

1. Set your working directory:
   ```powershell
   cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
   ```
2. Verify CV files in `C:\Users\areeb\Desktop\cv`:
   - `Areeb_Azhar_Full_Stack_Web_CV.pdf`
   - `Areeb Azhar - AI Resume PDF.pdf`
   - `Areeb Azhar - Flutter Developer Resume PDF.pdf`
   - `Areeb Azhar - Game Developer.pdf`
   - `Areeb_Azhar_Rust_Blockchain_CV.pdf`

---

## ⚙️ Daily Automation Schedule

- **Cadence**: Daily at 8:00 AM Pakistan Standard Time (`CRON_TZ=Asia/Karachi 0 8 * * *`)
- **Action**: Ingests new job notifications from the last 24 hours, filters for software roles requiring <1 year experience, matches appropriate CV, generates custom cover letters, and presents a structured digest for review.

---

## 📸 Screenshots & UI Previews

*(Screenshots will be added once the first daily run report is generated)*.
> **Screenshot Request**: After activating the automation in the Automations dashboard (`sidecar://dashboard`), please take a screenshot of:
> 1. The active `Daily Job Search & Application Drafter` card.
> 2. The morning email digest table rendered in chat.
