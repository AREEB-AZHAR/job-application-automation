import os
import sys
import argparse
from typing import List, Dict, Any

from job_evaluator import load_profile, evaluate_job, generate_cover_letter
from tracker import record_application, load_applications, get_pipeline_summary, update_status

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
        print(f"[{job.get('source', 'Job Alert')}] {job.get('title')} @ {job.get('company')} ({job.get('location')})")
        print(f" -> Assessment: {reason}")

        if is_match:
            cover_letter = generate_cover_letter(job, domain, profile)
            app_record = record_application(
                job=job,
                domain=domain,
                cv_path=cv_path,
                cover_letter=cover_letter,
                screening_answers=screening,
                status="READY_FOR_REVIEW"
            )
            results.append(app_record)
            print(f" -> Status: READY_FOR_REVIEW")
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
    print(f"Total Tracked Applications: {summary['total']}")
    print("Status Breakdown:", summary["by_status"])
    print("Domain Breakdown:", summary["by_domain"])
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
        # Default run with sample stream if called directly
        from test_run import sample_jobs
        process_job_batch(sample_jobs)
