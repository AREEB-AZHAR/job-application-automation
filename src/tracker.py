import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")
SCANNED_FILE = os.path.join(DATA_DIR, "scanned_jobs.json")

def ensure_data_store():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
    if not os.path.exists(SCANNED_FILE):
        with open(SCANNED_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def load_applications() -> List[Dict[str, Any]]:
    ensure_data_store()
    try:
        with open(APPLICATIONS_FILE, "r", encoding="utf-8") as f:
            apps = json.load(f)
            # Automatic migration: promote READY_FOR_REVIEW to APPLIED
            changed = False
            for app in apps:
                if app.get("status") == "READY_FOR_REVIEW":
                    app["status"] = "APPLIED"
                    changed = True
            if changed:
                save_applications(apps)
            return apps
    except Exception:
        return []

def save_applications(applications: List[Dict[str, Any]]):
    ensure_data_store()
    with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2)

def load_scanned_jobs() -> List[Dict[str, Any]]:
    ensure_data_store()
    try:
        with open(SCANNED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_scanned_jobs(jobs: List[Dict[str, Any]]):
    ensure_data_store()
    with open(SCANNED_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

def record_scanned_job(
    job: Dict[str, Any],
    is_match: bool,
    reason: str,
    domain: Optional[str] = None,
    cv_path: Optional[str] = None
) -> Dict[str, Any]:
    scanned_list = load_scanned_jobs()
    job_id = job.get("id") or f"scan_{len(scanned_list) + 1:04d}"
    
    existing = next((s for s in scanned_list if s.get("id") == job_id or (s.get("url") and s.get("url") == job.get("url"))), None)
    now = datetime.now().isoformat()
    record = {
        "id": job_id,
        "source": job.get("source", "Direct"),
        "title": job.get("title", "Untitled Role"),
        "company": job.get("company", "Company"),
        "location": job.get("location", "Location"),
        "url": job.get("url", ""),
        "description": job.get("description", ""),
        "is_match": is_match,
        "reason": reason,
        "domain": domain,
        "cv_path": cv_path,
        "scanned_at": now
    }

    if existing:
        existing.update(record)
    else:
        scanned_list.insert(0, record)

    save_scanned_jobs(scanned_list)
    return record

def record_application(
    job: Dict[str, Any],
    domain: str,
    cv_path: str,
    cover_letter: str,
    screening_answers: Optional[Dict[str, Any]] = None,
    status: str = "APPLIED"
) -> Dict[str, Any]:
    applications = load_applications()
    job_id = job.get("id") or f"job_{len(applications) + 1:03d}"
    
    existing = next((app for app in applications if app.get("id") == job_id or (app.get("url") and app.get("url") == job.get("url"))), None)
    
    now = datetime.now().isoformat()
    record = {
        "id": job_id,
        "source": job.get("source", "Direct"),
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "description": job.get("description", ""),
        "domain": domain,
        "cv_path": cv_path,
        "cover_letter": cover_letter,
        "screening_answers": screening_answers or {},
        "status": status,
        "applied_at": now,
        "updated_at": now
    }

    if existing:
        existing.update(record)
    else:
        record["created_at"] = now
        applications.append(record)

    save_applications(applications)
    return record

def update_status(job_id: str, new_status: str) -> bool:
    applications = load_applications()
    for app in applications:
        if app.get("id") == job_id:
            app["status"] = new_status
            app["updated_at"] = datetime.now().isoformat()
            save_applications(applications)
            return True
    return False

def get_full_metrics() -> Dict[str, Any]:
    applications = load_applications()
    scanned_list = load_scanned_jobs()

    total_scanned = len(scanned_list)
    total_qualified = sum(1 for s in scanned_list if s.get("is_match"))
    total_disqualified = total_scanned - total_qualified

    by_status = {}
    for app in applications:
        st = app.get("status", "UNKNOWN")
        by_status[st] = by_status.get(st, 0) + 1

    total_applied = by_status.get("APPLIED", 0) + by_status.get("SUBMITTED", 0)

    by_domain = {}
    for app in applications:
        dom = app.get("domain", "other")
        by_domain[dom] = by_domain.get(dom, 0) + 1

    disqualification_reasons = {}
    for s in scanned_list:
        if not s.get("is_match"):
            r = s.get("reason", "Filtered")
            if "experience" in r.lower():
                category = "Requires > 1 yr exp"
            elif "senior" in r.lower() or "lead" in r.lower() or "principal" in r.lower():
                category = "Senior/Lead role"
            elif "tech stack" in r.lower() or "domain" in r.lower():
                category = "Stack mismatch"
            else:
                category = "Out of scope"
            disqualification_reasons[category] = disqualification_reasons.get(category, 0) + 1

    return {
        "total_scanned": total_scanned,
        "total_qualified": total_qualified,
        "total_disqualified": total_disqualified,
        "total_applications": len(applications),
        "total_applied": total_applied,
        "application_rate": round((total_qualified / total_scanned * 100) if total_scanned else 0, 1),
        "by_status": by_status,
        "by_domain": by_domain,
        "disqualification_reasons": disqualification_reasons
    }

def get_pipeline_summary() -> Dict[str, Any]:
    return get_full_metrics()
