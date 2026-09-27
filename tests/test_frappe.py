import sys
import types
import unittest
from unittest.mock import patch
from frappe_jev.jobs import queue_lead, evaluate_lead
class Lead(dict):
    name = "LEAD-1"
    def get(self, field): return super().get(field)
    def add_comment(self, kind, text): self["comment"] = text
class FrappeTests(unittest.TestCase):
    def test_queue_and_decision(self):
        lead = Lead(jev_request_text="Please quote 20 licenses")
        calls=[]
        sys.modules["frappe"] = types.SimpleNamespace(enqueue=lambda *a,**k:calls.append((a,k)),get_doc=lambda *a:lead)
        try:
            queue_lead(lead)
            self.assertEqual(calls[0][1]["lead_name"],"LEAD-1")
            import os
            old=os.environ.get("TYPESAFE_API_KEY");os.environ["TYPESAFE_API_KEY"]="test"
            try: result=evaluate_lead("LEAD-1",evaluate=lambda text,policy,key:{"outcome":"sales","probability":0.95,"policyVersion":"0.1.0","inputSha256":"abc123456789"})
            finally:
                if old is None: os.environ.pop("TYPESAFE_API_KEY",None)
                else: os.environ["TYPESAFE_API_KEY"]=old
            self.assertEqual(result["outcome"],"sales")
            self.assertIn("Jev intent",lead["comment"])
        finally: sys.modules.pop("frappe",None)

    def test_erpnext_notes_table(self):
        from frappe_jev.jobs import evaluate_lead
        lead=Lead(notes=[{"note":"Please quote 20 licenses"}])
        sys.modules["frappe"]=types.SimpleNamespace(get_doc=lambda *a:lead)
        try:
            import os
            with patch.dict(os.environ,{"TYPESAFE_API_KEY":"test"}):
                result=evaluate_lead("LEAD-1",evaluate=lambda text,policy,key:{"outcome":"sales","probability":0.95,"policyVersion":"0.1.0","inputSha256":"abc123456789"})
            self.assertEqual(result["outcome"],"sales")
        finally: sys.modules.pop("frappe",None)
