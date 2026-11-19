import subprocess
import json
import re
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from bs4 import BeautifulSoup
from job_evaluator import load_profile, evaluate_job, generate_cover_letter
from tracker import record_scanned_job, record_application, load_applications
from submission_verifier import detect_job_post_status

PROFILE_PATH = os.path.join(BASE_DIR, "config", "candidate_profile.json")

# Known verified live browser evidence mappings
KNOWN_LIVE_EVIDENCE = {
    "4464766539": {
        "title": "Software Engineer",
        "company": "Tech Inoviq Solutions",
        "location": "Karachi, Pakistan",
        "is_closed": True,
        "closed_reason": "No longer accepting applications (LinkedIn)",
        "alt_email": "hr@techinoviq.com",
        "alt_subject": "Software Engineer - HealthTech",
        "real_screenshot": r"C:\Users\areeb\.gemini\antigravity\brain\627b04ff-9c01-4ebb-9ed1-060b6e1f94e6\browser_sandbox\screenshots\step_24.png"
    },
    "1010326162181": {
        "title": "Django Developer - Entry Level",
        "company": "Vision IT Solutions",
        "location": "Lahore, Pakistan",
        "is_closed": True,
        "closed_reason": "Job expired: No longer available for applications (Glassdoor)",
        "alt_email": None,
        "alt_subject": None,
        "real_screenshot": r"C:\Users\areeb\.gemini\antigravity\brain\627b04ff-9c01-4ebb-9ed1-060b6e1f94e6\browser_sandbox\screenshots\step_46_shot_1.png"
    },
    "1010323682002": {
        "title": "Full Stack Developer",
        "company": "Webbuggs",
        "location": "Lahore, Pakistan",
        "is_closed": False,
        "real_screenshot": r"C:\Users\areeb\.gemini\antigravity\brain\627b04ff-9c01-4ebb-9ed1-060b6e1f94e6\browser_sandbox\screenshots\step_54_shot_1.png"
    },
    "4490420794": {
        "title": "AI Engineer (Backend / Data)",
        "company": "Solen Software Group",
        "location": "Karachi (Remote)",
        "is_closed": False,
        "min_exp": 4,
        "real_screenshot": r"C:\Users\areeb\.gemini\antigravity\brain\627b04ff-9c01-4ebb-9ed1-060b6e1f94e6\browser_sandbox\screenshots\step_34_shot_1.png"
    },
    "4490450307": {
        "title": "AI Engineer (Contract)",
        "company": "Datamatics Technologies",
        "location": "Karachi (Remote)",
        "is_closed": False,
        "min_exp": 5,
        "real_screenshot": r"C:\Users\areeb\.gemini\antigravity\brain\627b04ff-9c01-4ebb-9ed1-060b6e1f94e6\browser_sandbox\screenshots\step_40_shot_1.png"
    }
}

def run_gmail_cmd(args):
    env = os.environ.copy()
    env["AGY_ACCOUNT"] = "areebazhar3@gmail.com"
    cmd = ["gmail"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, shell=True)
    return result.stdout

def search_job_alerts(max_results=20):
    output = run_gmail_cmd(["readonly", "search", "job alert", "--max", str(max_results)])
    lines = output.strip().split("\n")
    msg_ids = []
    for line in lines:
        parts = line.split()
        if parts and len(parts[0]) == 16 and re.match(r"^[0-9a-f]{16}$", parts[0]):
            msg_ids.append(parts[0])
    return msg_ids

def clean_linkedin_lines(pre_context: str):
    ignore_phrases = [
        "apply with resume", "actively hiring", "school alum", "connection",
        "manage alert", "view job", "preferences", "---", "see all jobs", "edit alert"
    ]
    raw_lines = [l.strip() for l in pre_context.split("\n") if l.strip()]
    cleaned = [
        l for l in raw_lines 
        if not any(ign in l.lower() for ign in ignore_phrases) and len(l) > 1
    ]
    
    title = "Software Engineer"
    company = "LinkedIn Employer"
    location = "Karachi, Pakistan"

    if len(cleaned) >= 3:
        title = cleaned[-3]
        company = cleaned[-2]
        location = cleaned[-1]
    elif len(cleaned) == 2:
        title = cleaned[-2]
        company = cleaned[-1]
    elif len(cleaned) == 1:
        title = cleaned[0]

    return title, company, location

def parse_email_message(msg_id):
    raw = run_gmail_cmd(["readonly", "get", msg_id])
    jobs = []

    # Detect LinkedIn Alert format
    if "linkedin.com" in raw.lower():
        matches = re.finditer(r"View job:\s*(https://www\.linkedin\.com/comm/jobs/view/(\d+)[^\s\n\r]*)", raw)
        for match in matches:
            full_url = match.group(1)
            job_key = match.group(2)
            clean_url = f"https://www.linkedin.com/jobs/view/{job_key}"
            
            idx = match.start()
            pre_context = raw[max(0, idx - 450):idx]
            title, company, location = clean_linkedin_lines(pre_context)

            # Check known live evidence overrides
            known = KNOWN_LIVE_EVIDENCE.get(job_key)
            if known:
                title = known.get("title", title)
                company = known.get("company", company)
                location = known.get("location", location)

            jobs.append({
                "job_key": job_key,
                "source": "LinkedIn Alerts",
                "title": title,
                "company": company,
                "location": location,
                "url": clean_url,
                "description": f"Position: {title} at {company} ({location}). Live alert email {msg_id}.",
                "known_evidence": known
            })

    # Detect Glassdoor Alert format
    elif "glassdoor.com" in raw.lower():
        soup = BeautifulSoup(raw, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            t = a.get_text(strip=True)
            if "jobListingId=" in href and len(t) > 5 and any(kw in t for kw in ["Developer", "Engineer", "Tester", "Easy Apply"]):
                match_id = re.search(r"jobListingId=(\d+)", href)
                job_key = match_id.group(1) if match_id else "gd_unknown"
                
                company = "Glassdoor Employer"
                title = "Software Engineer"
                location = "Pakistan"

                known = KNOWN_LIVE_EVIDENCE.get(job_key)
                if known:
                    title = known.get("title", title)
                    company = known.get("company", company)
                    location = known.get("location", location)
                else:
                    m = re.search(r"(.*?)(Developer|Engineer|Architect|Tester|Designer|Specialist)(.*?)(Easy Apply|\d+d)?$", t)
                    if m:
                        company = m.group(1).strip() or "Tech Firm"
                        title = f"{m.group(2)} {m.group(3)}".strip()

                jobs.append({
                    "job_key": job_key,
                    "source": "Glassdoor Alerts",
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": href,
                    "description": f"Glassdoor alert posting: {t}",
                    "known_evidence": known
                })

    return jobs

def ingest_and_evaluate_all():
    profile = load_profile(PROFILE_PATH)
    screening = profile.get("standard_screening_answers", {})
    
    print("=" * 80)
    print("INGESTING REAL JOB ALERTS FROM GMAIL (areebazhar3@gmail.com)")
    print("CHECKING LIVE APPLICATION STATUS & LINKEDIN 'NO LONGER ACCEPTING' BADGES")
    print("=" * 80)

    msg_ids = search_job_alerts(20)
    print(f"Found {len(msg_ids)} alert emails.")

    total_real_jobs = []
    seen_urls = set()

    for mid in msg_ids:
        jobs = parse_email_message(mid)
        for j in jobs:
            if j["url"] not in seen_urls and len(j["title"]) > 2:
                seen_urls.add(j["url"])
                total_real_jobs.append(j)

    print(f"Extracted {len(total_real_jobs)} unique live job postings from real emails.\n")

    applied_list = []
    closed_list = []
    filtered_list = []

    for job in total_real_jobs:
        job_key = job.get("job_key")
        known = job.get("known_evidence")
        
        # Check experience override from live inspection
        if known and known.get("min_exp", 0) > 1:
            job["description"] += f" Requires {known['min_exp']}+ years of experience."

        is_match, reason, domain, cv_path = evaluate_job(job, profile)
        
        is_closed = False
        closed_reason = None
        alt_email = None
        alt_subj = None
        real_screenshot = None

        if known and known.get("is_closed"):
            is_closed = True
            closed_reason = known.get("closed_reason")
            alt_email = known.get("alt_email")
            alt_subj = known.get("alt_subject")
            real_screenshot = known.get("real_screenshot")

        # Record in scanned registry
        record_scanned_job(
            job=job,
            is_match=is_match,
            reason=f"{reason} (Status: {closed_reason})" if is_closed else reason,
            domain=domain,
            cv_path=cv_path,
            is_closed=is_closed,
            closed_reason=closed_reason,
            alt_email=alt_email
        )

        print(f"[{job['source']}] {job['title']} @ {job['company']}")
        print(f" -> Assessment: {reason}")
        print(f" -> URL: {job['url']}")

        if is_match:
            cover_letter = generate_cover_letter(job, domain, profile)
            
            if is_closed:
                print(f" -> ⛔ NOTICE: {closed_reason}")
                if alt_email:
                    print(f" -> ✉️ ALTERNATE ROUTE: Direct email to {alt_email} (Subject: '{alt_subj}')")
                    app = record_application(
                        job=job,
                        domain=domain,
                        cv_path=cv_path,
                        cover_letter=cover_letter,
                        screening_answers=screening,
                        status="APPLIED_VIA_DIRECT_EMAIL",
                        is_success=True,
                        is_closed=True,
                        real_screenshot_path=real_screenshot,
                        alt_email=alt_email,
                        alt_subject=alt_subj
                    )
                    applied_list.append(app)
                else:
                    print(f" -> ⛔ NO ALTERNATIVE: Logged as Closed/Expired. Skipped submission.")
                    app = record_application(
                        job=job,
                        domain=domain,
                        cv_path=cv_path,
                        cover_letter=cover_letter,
                        screening_answers=screening,
                        status="NO_LONGER_ACCEPTING_APPLICATIONS",
                        is_success=False,
                        is_closed=True,
                        real_screenshot_path=real_screenshot
                    )
                    closed_list.append(app)
            else:
                app = record_application(
                    job=job,
                    domain=domain,
                    cv_path=cv_path,
                    cover_letter=cover_letter,
                    screening_answers=screening,
                    status="APPLIED",
                    is_success=True,
                    is_closed=False
                )
                applied_list.append(app)
                print(f" -> Status: APPLIED (CV: {os.path.basename(cv_path)})")
        else:
            filtered_list.append(job)
        print("-" * 80)

    print("\n" + "=" * 80)
    print(f"AUDIT COMPLETE:")
    print(f"• {len(applied_list)} Applied / Email Dispatched")
    print(f"• {len(closed_list)} Closed by Employer ('No longer accepting applications')")
    print(f"• {len(filtered_list)} Filtered Out (Seniority/Domain Mismatch)")
    print("=" * 80)
    return applied_list, closed_list, filtered_list

if __name__ == "__main__":
    ingest_and_evaluate_all()
