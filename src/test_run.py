import json
from job_evaluator import load_profile, evaluate_job, generate_cover_letter

def run_test():
    profile_path = "C:/Users/areeb/.gemini/antigravity/scratch/job_application_automation/config/candidate_profile.json"
    profile = load_profile(profile_path)

    # Sample batch of alert emails (e.g. from LinkedIn, Indeed, Glassdoor)
    sample_jobs = [
        {
            "id": "job_001",
            "source": "LinkedIn Alerts",
            "title": "Junior Full Stack Developer",
            "company": "Apex Technologies",
            "location": "Lahore (Hybrid)",
            "description": "Seeking an entry level or junior developer with React, Node.js, and TypeScript skills. 0-1 years of experience or fresh graduates welcome.",
            "url": "https://linkedin.com/jobs/view/1001"
        },
        {
            "id": "job_002",
            "source": "Indeed Daily Alert",
            "title": "Senior Frontend Engineer",
            "company": "Global Cloud Corp",
            "location": "Remote",
            "description": "Requires at least 5+ years of experience with React, Next.js, and cloud deployments.",
            "url": "https://indeed.com/viewjob?jk=2002"
        },
        {
            "id": "job_003",
            "source": "LinkedIn Alerts",
            "title": "Associate Flutter Developer",
            "company": "MobileCraft Studios",
            "location": "Karachi (On-site)",
            "description": "Looking for a fresh graduate or associate developer with Flutter and Dart knowledge. Less than 1 year experience required.",
            "url": "https://linkedin.com/jobs/view/3003"
        },
        {
            "id": "job_004",
            "source": "Glassdoor Alert",
            "title": "Mid-Level Python Developer",
            "company": "FinData Systems",
            "location": "Islamabad",
            "description": "Must have 3 years of experience in Python and PostgreSQL.",
            "url": "https://glassdoor.com/job-listing/4004"
        },
        {
            "id": "job_005",
            "source": "Direct Company Alert",
            "title": "Junior Blockchain / Rust Engineer",
            "company": "ChainPulse Labs",
            "location": "Remote",
            "description": "Entry-level position for engineers interested in Rust, smart contracts, and distributed ledgers. Fresh graduates encouraged to apply.",
            "url": "https://chainpulse.io/careers/junior-rust"
        }
    ]

    print("================================================================================")
    print("STARTING TEST RUN: Daily Job Search & Application Drafter")
    print(f"Candidate: {profile['personal_info']['full_name']} | Max Experience: <= 1 year")
    print("================================================================================\n")

    matched_jobs = []

    for job in sample_jobs:
        is_match, reason, domain, cv_path = evaluate_job(job, profile)
        print(f"[{job['source']}] {job['title']} @ {job['company']} ({job['location']})")
        print(f" -> Result: {reason}")
        if is_match:
            cover_letter = generate_cover_letter(job, domain, profile)
            matched_jobs.append({
                "job": job,
                "domain": domain,
                "cv_path": cv_path,
                "cover_letter": cover_letter
            })
            print(f" -> Selected CV: {cv_path}")
        print("-" * 80)

    print("\n================================================================================")
    print(f"TEST RUN COMPLETE: {len(matched_jobs)} / {len(sample_jobs)} Jobs Qualified for Approval")
    print("================================================================================\n")

    return matched_jobs

if __name__ == "__main__":
    run_test()
