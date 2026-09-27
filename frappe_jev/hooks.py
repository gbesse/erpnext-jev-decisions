app_name = "frappe_jev"
app_title = "Jev Decisions"
app_publisher = "gbesse"
app_description = "Reviewable Jev lead intent for ERPNext"
app_email = ""
app_license = "MIT"
required_apps = ["erpnext"]
doc_events = {"Lead": {"after_insert": "frappe_jev.jobs.queue_lead"}}
