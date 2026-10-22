"""Bounded smoke checks for the public experimental CVE triage profile."""
import json
import pathlib
import unittest
from security_triage_v0_20 import parse, run

ROOT=pathlib.Path(__file__).resolve().parent
BASE=(ROOT/'triage_demo_v0_20.bridge').read_text(encoding='utf-8')
HOST=json.loads((ROOT/'triage_context_sample.json').read_text())

class BoundedTriageChecks(unittest.TestCase):
    def test_parse_profile(self):
        self.assertEqual(parse(BASE)['version'],'0.20-candidate')
    def test_unknown_remains_hold(self):
        self.assertEqual(run(BASE,HOST)['disposition'],'hold_unknown_or_untrusted')
    def test_no_external_inventory_is_untrusted(self):
        self.assertFalse(run(BASE)['trusted_context_matched'])
    def test_revoked_trust_blocks_positive_disposition(self):
        s=BASE.replace('trust=unknown','trust=revoked')
        self.assertIn('trust_revoked',run(s,HOST)['gaps'])
    def test_no_execution_authority(self):
        self.assertFalse(run(BASE,HOST)['execution_allowed'])
        self.assertFalse(run(BASE,HOST)['may_publish_safe_claim'])

if __name__=='__main__': unittest.main()
