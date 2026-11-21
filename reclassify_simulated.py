import json

app_file = 'C:/Users/areeb/.gemini/antigravity/scratch/job_application_automation/data/applications.json'
apps = json.load(open(app_file, 'r', encoding='utf-8'))

simulated_ids = [
    'job_009', 'job_010', 'job_018', 'job_021', 'job_024', 'job_025', 'job_026', 
    'job_038', 'job_048', 'job_049', 'job_050', 'job_051', 'job_052', 'job_053', 
    'job_054', 'job_055', 'job_056', 'job_057', 'job_058', 'job_059', 'job_060', 
    'job_061', 'job_062'
]

reclassified_count = 0
for a in apps:
    if a.get('id') in simulated_ids:
        a['status'] = 'UNSUBMITTED_TEST_MOCK'
        a['is_test'] = True
        a['verification_status'] = 'UNSUBMITTED_SIMULATION'
        a['verification_details'] = 'Recorded as simulation during early testing run; not actually submitted to portal.'
        a['confirmation_id'] = 'TEST-SIMULATED-' + str(a.get('id'))
        reclassified_count += 1

with open(app_file, 'w', encoding='utf-8') as f:
    json.dump(apps, f, indent=2)

print(f"Reclassified {reclassified_count} simulated records to UNSUBMITTED_TEST_MOCK (is_test=True).")
