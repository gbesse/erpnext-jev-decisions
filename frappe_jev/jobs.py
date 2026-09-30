"""Frappe background job; writes an auditable comment, never changes lead status."""
import hashlib
import json
import os
from pathlib import Path
from jev_core import decide

POLICY = json.loads((Path(__file__).with_name("policy.json")).read_text())

def queue_lead(doc, method=None):
    import frappe
    frappe.enqueue("frappe_jev.jobs.evaluate_lead", queue="short", enqueue_after_commit=True, lead_name=doc.name)

def evaluate_lead(lead_name, *, evaluate=decide):
    import frappe
    doc = frappe.get_doc("Lead", lead_name)
    text = doc.get("jev_request_text") or doc.get("description")
    if not isinstance(text, str) or not text.strip():
        notes = doc.get("notes") or []
        text = "\n".join(value for row in notes if isinstance(value := (row.get("note") if hasattr(row, "get") else getattr(row, "note", None)), str))
    if not isinstance(text, str) or not text.strip(): return None
    digest = hashlib.sha256(text.encode()).hexdigest()
    marker = f"jev-review:{POLICY['version']}:{digest}"
    if frappe.db.exists("Comment", {
        "reference_doctype": "Lead",
        "reference_name": lead_name,
        "comment_type": "Comment",
        "content": ["like", f"%{marker}%"],
    }):
        return {"skipped": "already reviewed"}
    result = evaluate(text, POLICY, os.environ["TYPESAFE_API_KEY"])
    doc.add_comment("Comment", f"Jev intent: {result['outcome']} (p={result['probability']:.3f}; policy={result['policyVersion']}; input={result['inputSha256'][:12]}) [{marker}]")
    return result
