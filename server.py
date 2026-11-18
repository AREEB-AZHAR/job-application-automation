import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# Ensure parent directory and src are on sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from tracker import (
    load_applications, 
    load_scanned_jobs, 
    get_full_metrics, 
    update_status, 
    record_scanned_job, 
    record_application
)
from job_evaluator import load_profile, evaluate_job, generate_cover_letter

PROFILE_PATH = os.path.join(BASE_DIR, "config", "candidate_profile.json")
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

class JobShowcaseHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/data":
            self.handle_api_data()
        elif path == "/" or path == "/index.html":
            self.serve_file(os.path.join(WEB_DIR, "index.html"), "text/html; charset=utf-8")
        elif path == "/styles.css":
            self.serve_file(os.path.join(WEB_DIR, "styles.css"), "text/css; charset=utf-8")
        elif path == "/app.js":
            self.serve_file(os.path.join(WEB_DIR, "app.js"), "application/javascript; charset=utf-8")
        elif path.startswith("/proofs/"):
            rel_path = path[len("/proofs/"):].replace("/", os.sep)
            proof_file = os.path.join(BASE_DIR, "data", "proofs", rel_path)
            self.serve_file(proof_file, "image/png")
        elif path.startswith("/screenshots/"):
            rel_path = path[len("/screenshots/"):].replace("/", os.sep)
            screenshot_file = os.path.join(WEB_DIR, "screenshots", rel_path)
            self.serve_file(screenshot_file, "image/png")
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/status":
            self.handle_api_status(payload)
        elif path == "/api/evaluate":
            self.handle_api_evaluate(payload)
        else:
            self.send_error(404, "Endpoint not found")

    def serve_file(self, filepath: str, content_type: str):
        if not os.path.exists(filepath):
            self.send_error(404, "File not found")
            return
        with open(filepath, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def handle_api_data(self):
        metrics = get_full_metrics()
        applications = load_applications()
        scanned = load_scanned_jobs()
        profile = load_profile(PROFILE_PATH)

        response_data = {
            "metrics": metrics,
            "applications": applications,
            "scanned": scanned,
            "candidate": {
                "name": profile.get("personal_info", {}).get("full_name", "Areeb Azhar"),
                "email": profile.get("personal_info", {}).get("email", ""),
                "phone": profile.get("personal_info", {}).get("phone", ""),
                "education": profile.get("standard_screening_answers", {}).get("education", ""),
                "github": profile.get("personal_info", {}).get("github_url", ""),
                "criteria": profile.get("job_search_criteria", {})
            }
        }
        self.send_json(response_data)

    def handle_api_status(self, payload: dict):
        job_id = payload.get("id")
        new_status = payload.get("status")

        if not job_id or not new_status:
            self.send_json({"error": "Missing id or status"}, status=400)
            return

        success = update_status(job_id, new_status)
        if success:
            self.send_json({"success": True, "id": job_id, "new_status": new_status})
        else:
            self.send_json({"error": "Application not found"}, status=404)

    def handle_api_evaluate(self, payload: dict):
        profile = load_profile(PROFILE_PATH)
        screening = profile.get("standard_screening_answers", {})

        is_match, reason, domain, cv_path = evaluate_job(payload, profile)

        # Record into scanned log
        scan_record = record_scanned_job(
            job=payload,
            is_match=is_match,
            reason=reason,
            domain=domain,
            cv_path=cv_path
        )

        app_record = None
        if is_match:
            cover_letter = generate_cover_letter(payload, domain, profile)
            app_record = record_application(
                job=payload,
                domain=domain,
                cv_path=cv_path,
                cover_letter=cover_letter,
                screening_answers=screening,
                status="APPLIED"
            )

        self.send_json({
            "success": True,
            "is_match": is_match,
            "reason": reason,
            "domain": domain,
            "cv_path": cv_path,
            "scan_record": scan_record,
            "app_record": app_record
        })

    def send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

def run_server(port: int = 5000):
    handler = JobShowcaseHTTPHandler
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    current_port = port
    max_tries = 5
    for attempt in range(max_tries):
        try:
            with socketserver.TCPServer(("", current_port), handler) as httpd:
                print(f"============================================================")
                print(f"🌐 Job Showcase & Audit Website running at:")
                print(f"   http://localhost:{current_port}")
                print(f"============================================================")
                print(f"Serving data from: {BASE_DIR}/data")
                print("Press Ctrl+C to stop the server.")
                httpd.serve_forever()
                break
        except OSError as e:
            if attempt < max_tries - 1:
                current_port += 1
            else:
                raise e

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
