import os
import sys
import json
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")
WEB_DIR = os.path.join(BASE_DIR, "web")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from tracker import load_applications, load_scanned_jobs, get_full_metrics
from job_evaluator import load_profile

PROFILE_PATH = os.path.join(BASE_DIR, "config", "candidate_profile.json")

def export_static_assets():
    print("Exporting static web assets for GitHub Pages deployment...")
    
    # 1. Generate full data payload
    metrics = get_full_metrics()
    apps = load_applications()
    scanned = load_scanned_jobs()
    profile = load_profile(PROFILE_PATH)

    payload = {
        "metrics": metrics,
        "applications": apps,
        "scanned": scanned,
        "candidate": profile
    }

    # Save to web/data.json
    data_json_path = os.path.join(WEB_DIR, "data.json")
    with open(data_json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f" -> Generated {data_json_path} ({len(apps)} apps, {len(scanned)} scanned)")

    # Save to web/api/data.json
    api_dir = os.path.join(WEB_DIR, "api")
    os.makedirs(api_dir, exist_ok=True)
    api_data_path = os.path.join(api_dir, "data.json")
    with open(api_data_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f" -> Generated {api_data_path}")

    # 2. Copy proofs directory to web/proofs
    src_proofs = os.path.join(DATA_DIR, "proofs")
    dest_proofs = os.path.join(WEB_DIR, "proofs")
    if os.path.exists(src_proofs):
        if os.path.exists(dest_proofs):
            shutil.rmtree(dest_proofs)
        shutil.copytree(src_proofs, dest_proofs)
        print(f" -> Synced visual proofs from {src_proofs} to {dest_proofs}")

    # 3. Create .nojekyll in web/
    nojekyll_path = os.path.join(WEB_DIR, ".nojekyll")
    with open(nojekyll_path, "w", encoding="utf-8") as f:
        f.write("")
    print(f" -> Created {nojekyll_path}")

    print("Static bundle export complete!")

if __name__ == "__main__":
    export_static_assets()
