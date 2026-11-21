import json

app_file = 'C:/Users/areeb/.gemini/antigravity/scratch/job_application_automation/data/applications.json'
apps = json.load(open(app_file, 'r', encoding='utf-8'))

print(f"Total records in applications.json: {len(apps)}\n")

real_submissions = []
simulated_submissions = []
test_records = []
closed_audits = []

for a in apps:
    app_id = a.get('id')
    company = a.get('company')
    title = a.get('title')
    status = a.get('status')
    conf_id = a.get('confirmation_id', '')
    source = a.get('source', '')
    is_test = a.get('is_test', False)
    
    if 'LINKEDIN-SUBMITTED-NOW' in conf_id or 'GMAIL-MSG' in conf_id:
        real_submissions.append(a)
    elif status == 'NO_LONGER_ACCEPTING_APPLICATIONS' or a.get('is_closed'):
        closed_audits.append(a)
    elif is_test or status in ['TEST_RECORD', 'DISQUALIFIED_DURING_AUDIT', 'TEST_DUPLICATE_PRUNED']:
        test_records.append(a)
    else:
        simulated_submissions.append(a)

print(f"=== 1. GENUINELY APPLIED (Real Live Submissions) ({len(real_submissions)}) ===")
for a in real_submissions:
    print(f"  [REAL] {a['id']}: {a['title']} @ {a['company']} | {a.get('confirmation_id')}")

print(f"\n=== 2. NOT ACTUALLY APPLIED / SIMULATED (The Mess-Ups) ({len(simulated_submissions)}) ===")
for a in simulated_submissions:
    print(f"  [SIMULATED] {a['id']}: {a['title']} @ {a['company']} | Conf: {a.get('confirmation_id')} | URL: {a.get('url')}")

print(f"\n=== 3. CLOSED AUDITS ({len(closed_audits)}) ===")
for a in closed_audits:
    print(f"  [CLOSED] {a['id']}: {a['title']} @ {a['company']}")

print(f"\n=== 4. TEST RECORDS ({len(test_records)}) ===")
print(f"  Total test/scaffold records: {len(test_records)}")
