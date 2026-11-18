import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")

def ensure_data_store():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def load_applications() -> List[Dict[str, Any]]:
    ensure_data_store()
    try:
        with open(APPLICATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_applications(applications: List[Dict[str, Any]]):
    ensure_data_store()
    with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2)

def record_application(
    job: Dict[str, Any],
    domain: str,
    cv_path: str,
    cover_letter: str,
    screening_answers: Optional[Dict[str, Any]] = None,
    status: str = "READY_FOR_REVIEW"
) -> Dict[str, Any]:
    applications = load_applications()
    job_id = job.get("id") or f"job_{len(applications) + 1:03d}"
    
    # Check if application already exists
    existing = next((app for app in applications if app.get("id") == job_id or (app.get("url") and app.get("url") == job.get("url"))), None)
    
    now = datetime.now().isoformat()
    record = {
        "id": job_id,
        "source": job.get("source", "Unknown"),
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "domain": domain,
        "cv_path": cv_path,
        "cover_letter": cover_letter,
        "screening_answers": screening_answers or {},
        "status": status,
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

def get_pipeline_summary() -> Dict[str, Any]:
    applications = load_applications()
    summary = {
        "total": len(applications),
        "by_status": {},
        "by_domain": {}
    }
    for app in applications:
        st = app.get("status", "UNKNOWN")
        dom = app.get("domain", "UNKNOWN")
        summary["by_status"][st] = summary["by_status"].get(st, 0) + 1
        summary["by_domain"][dom] = summary["by_domain"].get(dom, 0) + 1
    return summary
