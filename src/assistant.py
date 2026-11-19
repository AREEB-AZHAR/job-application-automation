import os
import sys
import argparse
from typing import List, Dict, Any

from job_evaluator import load_profile, evaluate_job, generate_cover_letter
from tracker import (
    record_application, 
    record_scanned_job, 
    load_applications, 
    get_pipeline_summary, 
    update_status,
    is_already_applied
)

DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "candidate_profile.json")

def process_job_batch(jobs: List[Dict[str, Any]], profile_path: str = DEFAULT_PROFILE_PATH) -> List[Dict[str, Any]]:
    profile = load_profile(profile_path)
    screening = profile.get("standard_screening_answers", {})
    
    results = []
    print("=" * 80)
    print(f"JOB SEARCH ASSISTANT: Processing Batch of {len(jobs)} Opportunities")
    print(f"Candidate: {profile['personal_info']['full_name']} | Max Exp: <= 1 year")
    print("=" * 80 + "\n")

    for job in jobs:
        is_match, reason, domain, cv_path = evaluate_job(job, profile)
        
        # 1. Always record in scanned jobs ledger
        record_scanned_job(
            job=job,
            is_match=is_match,
            reason=reason,
            domain=domain,
            cv_path=cv_path
        )

        print(f"[{job.get('source', 'Job Alert')}] {job.get('title')} @ {job.get('company')} ({job.get('location')})")
        print(f" -> Assessment: {reason}")

        # Check if already applied
        dup_applied, matched_app, match_reason = is_already_applied(job)
        if dup_applied and matched_app:
            print(f" -> ⏭️ SKIPPED: {match_reason}")
            print(f" -> Existing Application ID: {matched_app.get('id')} ({matched_app.get('status')})")
            continue

        # 2. If matched, record into active applications pipeline with direct APPLIED status
        if is_match:
            cover_letter = generate_cover_letter(job, domain, profile)
            app_record = record_application(
                job=job,
                domain=domain,
                cv_path=cv_path,
                cover_letter=cover_letter,
                screening_answers=screening,
                status="APPLIED"
            )
            results.append(app_record)
            print(f" -> Status: APPLIED (Auto-dispatched with tailored CV & Cover Letter)")
            print(f" -> Selected CV: {cv_path}")
        print("-" * 80)

    print("\n" + "=" * 80)
    print(f"BATCH SUMMARY: {len(results)} / {len(jobs)} matched criteria and drafted.")
    print("=" * 80)
    return results

def display_pipeline():
    summary = get_pipeline_summary()
    applications = load_applications()

    print("\n" + "=" * 80)
    print("CURRENT APPLICATION PIPELINE")
    print("=" * 80)
    print(f"Total Scanned: {summary['total_scanned']} | Qualified: {summary['total_qualified']} ({summary['qualification_rate']}%)")
    print(f"Total Applications: {summary['total_applications']}")
    print("Status Breakdown:", summary["by_status"])
    print("Domain Breakdown:", summary["by_domain"])
    print("Disqualification Breakdown:", summary["disqualification_reasons"])
    print("-" * 80)

    if not applications:
        print("No applications recorded yet.")
        return

    for idx, app in enumerate(applications, 1):
        print(f"{idx}. [{app['status']}] {app['title']} @ {app['company']} ({app['location']})")
        print(f"   Domain: {app['domain']} | Source: {app['source']}")
        print(f"   CV: {app['cv_path']}")
        print(f"   URL: {app.get('url', 'N/A')}")
        print("-" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Job Search & Application Drafter Assistant")
    parser.add_argument("--pipeline", action="store_true", help="Display current pipeline status")
    args = parser.parse_args()

    if args.pipeline:
        display_pipeline()
    else:
        from test_run import sample_jobs
        process_job_batch(sample_jobs)
