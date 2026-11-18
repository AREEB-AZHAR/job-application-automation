# Autonomous Job Search & Application Automation

An intelligent, safety-conscious agentic automation system that scans daily job alert emails (LinkedIn, Indeed, Glassdoor), filters and scores matching opportunities against your candidate profile, prepares tailored application drafts, and tracks pipeline status.

---

## 🚀 Accomplishments & Recent Updates

- **Architecture & Implementation Plan Finalized**: Conducted online research and synthesized an account-safe, Human-in-the-Loop (HITL) automation framework based on industry best practices.
- **Repository Initialized**: Created the project workspace in `C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation` with Git version control.
- **Candidate Profile Schema Prepared**: Defined structured fields for target roles, technical skills, salary expectations, and standardized screening questions.
- **Automation Workflow Initiated**: Starting the Antigravity cron sidecar configuration flow for automated scheduled runs.

---

## 🏗️ Project Architecture & File Structure

```
job_application_automation/
├── README.md                          # Documentation and setup instructions
├── config/
│   └── candidate_profile.template.json # Resume data, target criteria, screening answers
├── src/
│   ├── email_parser.py                # Ingests and parses job alert emails
│   ├── job_matcher.py                 # LLM-based profile fit evaluator
│   └── application_tracker.py         # SQLite database management for application states
└── data/                              # Stores local sqlite database and cache
```

---

## 🛠️ Prerequisites & Environment Setup

- **Python**: Version 3.10 or higher.
- **Antigravity CLI & Extensions**:
  - Gmail Plugin (`antigravity-plugins-official/plugin/gmail`) for secure inbox querying.
- **Operating System**: Windows / macOS / Linux.

### Installation

1. Clone or navigate to the repository directory:
   ```bash
   cd C:\Users\areeb\.gemini\antigravity\scratch\job_application_automation
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install required packages (to be expanded):
   ```powershell
   pip install pydantic beautifulsoup4
   ```

---

## ⚙️ Configuration

Copy `config/candidate_profile.template.json` to `config/candidate_profile.json` and populate your personal details, target roles, experience levels, and standard screening answers.

---

## 📸 Screenshots & UI Previews

*(Screenshots are not yet available as UI and visual dashboard components are under construction)*.
> **Screenshot Request**: Once the scheduled automation dashboard and test runs are executed, please capture:
> 1. The Antigravity Automations Dashboard showing the active `Job Application Automation` sidecar.
> 2. The job digest report generated in the conversation or log file.
