import json
from datetime import datetime

app_file = 'C:/Users/areeb/.gemini/antigravity/scratch/job_application_automation/data/applications.json'
apps = json.load(open(app_file, 'r', encoding='utf-8'))

for a in apps:
    if a.get('id') == 'job_058':
        a['status'] = 'APPLIED'
        a['is_test'] = False
        a['confirmation_id'] = 'LINKEDIN-SUBMITTED-NOW-4492401752'
        a['verification_status'] = 'CONFIRMED_SUBMITTED'
        a['verification_details'] = "100% Live Easy Apply Submission Verified: Screening answered (Salary: 80K, Notice: 0 days) -> Submitted -> LinkedIn dialog confirmed: 'Application submitted now'."
        a['screening_answers'] = {
            'Current Salary': '0',
            'Expected Salary': '80000',
            'Notice Period': '0 (Immediate)'
        }
        a['applied_at'] = datetime.now().isoformat()
        a['updated_at'] = datetime.now().isoformat()
    elif a.get('id') == 'job_025':
        a['status'] = 'NO_LONGER_ACCEPTING_APPLICATIONS'
        a['is_closed'] = True
        a['is_test'] = False
        a['confirmation_id'] = 'CLOSED-POSTING'
        a['verification_status'] = 'CLOSED_BY_EMPLOYER'
        a['verification_details'] = "Audited Live Posting: 'No longer accepting applications' on LinkedIn"
    elif a.get('id') == 'job_061':
        a['status'] = 'NO_LONGER_ACCEPTING_APPLICATIONS'
        a['is_closed'] = True
        a['is_test'] = False
        a['confirmation_id'] = 'CLOSED-POSTING'
        a['verification_status'] = 'CLOSED_BY_EMPLOYER'
        a['verification_details'] = "Audited Live Posting: 'Not currently accepting applications' on LinkedIn"
    elif a.get('id') == 'job_049':
        a['status'] = 'DISQUALIFIED_DURING_AUDIT'
        a['is_test'] = True
        a['verification_status'] = 'DISQUALIFIED'
        a['verification_details'] = "Audited Live Posting: Disqualified because role requires 6+ years experience (Senior AI Engineer)"

with open(app_file, 'w', encoding='utf-8') as f:
    json.dump(apps, f, indent=2)

print("Updated job_058, job_025, job_061, and job_049 successfully!")
