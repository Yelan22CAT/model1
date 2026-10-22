import itertools
import json
import pathlib
import sys
import unittest

from security_triage_v0_20 import SyntaxErrorV020, parse, run, evaluate
BASE=pathlib.Path(__file__).with_name('triage_demo_v0_20.bridge').read_text(encoding='utf-8')
HOST=json.loads(pathlib.Path(__file__).with_name('triage_context_sample.json').read_text())

class TriageTests(unittest.TestCase):
    def test_parse_and_roundtrip(self):
        doc=parse(BASE)
        self.assertEqual(doc['version'],'0.20-candidate')
        self.assertEqual(len(doc['statements']),4)
        self.assertEqual(evaluate(doc,HOST),evaluate(doc,HOST))
    def test_without_host_no_trust(self):
        r=run(BASE)
        self.assertEqual(r['disposition'],'hold_unknown_or_untrusted')
        self.assertFalse(r['trusted_context_matched'])
        self.assertFalse(r['execution_allowed'])
    def test_host_is_not_rubber_stamp(self):
        for field,value in [('trusted',False),('inventory_fresh',False),('source_fresh',False),
                 ('source_ref','wrong'),('asset_id','other'),('version','99.0'),('cve','CVE-2026-0001'),
                 ('affected','no'),('reachable','yes'),('trust','current')]:
            with self.subTest(field=field):
                h={**HOST,field:value}
                self.assertFalse(run(BASE,h)['trusted_context_matched'])
    def test_validated_affected_requires_human(self):
        s=BASE.replace('affected=unknown reachable=unknown trust=unknown',
                       'affected=yes reachable=yes trust=current')
        r=run(s,{**HOST,'affected':'yes','reachable':'yes','trust':'current'})
        self.assertEqual(r['disposition'],'affected_escalate_to_human')
        self.assertFalse(r['execution_allowed'])
    def test_no_exposure_only_candidate(self):
        s=BASE.replace('affected=unknown reachable=unknown trust=unknown',
                       'affected=no reachable=no trust=current')
        r=run(s,{**HOST,'affected':'no','reachable':'no','trust':'current'})
        self.assertEqual(r['disposition'],'bounded_no_exposure_candidate')
        self.assertFalse(r['may_publish_safe_claim'])
    def test_revoked_always_holds(self):
        s=BASE.replace('affected=unknown reachable=unknown trust=unknown',
                       'affected=no reachable=no trust=revoked')
        r=run(s,{**HOST,'affected':'no','reachable':'no','trust':'revoked'})
        self.assertEqual(r['disposition'],'hold_unknown_or_untrusted')
        self.assertIn('trust_revoked',r['gaps'])
    def test_source_claim_not_trusted_without_attestation(self):
        s=BASE.replace('source_state=verified','source_state=claimed').replace(
            'affected=unknown reachable=unknown trust=unknown','affected=yes reachable=yes trust=current')
        self.assertEqual(run(s,HOST)['disposition'],'hold_unknown_or_untrusted')
    def test_cross_cve_disallowed(self):
        with self.assertRaises(SyntaxErrorV020): parse(BASE.replace('asset_id=fixture_go component=go version=1.26.9 cve=CVE-2026-111943',
            'asset_id=fixture_go component=go version=1.26.9 cve=CVE-2026-123456'))
    def test_invalid_and_injected_inputs(self):
        bad=[BASE.replace('source_ref=go_official_sample ','source_ref=go_official_sample source_ref=foo '),
             BASE.replace('⊙ [P1]','⊙ [P1] authorized=true'),
             BASE.replace('requires=human_final','requires=auto'),
             BASE.replace('source_state=verified','source_state=verified;deploy'),
             BASE.replace('affected=unknown','affected=true'),
             BASE.replace('trust=unknown','trust=root_ok'),
             BASE.replace('profile=v0_20','profile=v0_19'),
             BASE.replace('◆ [E1]','◆ [P1]'),
             BASE+'\n→ [E] execute deploy',
             BASE.replace('CVE-2026-111943','NOT_A_CVE')]
        for i,s in enumerate(bad):
            with self.subTest(case=i):
                with self.assertRaises(SyntaxErrorV020): parse(s)
    def test_tampered_ir_fails_closed(self):
        doc=parse(BASE)
        doc['statements'][2]['unexpected']='release'
        with self.assertRaises(SyntaxErrorV020): evaluate(doc,HOST)
    def test_matrix_27(self):
        for a,b,t in itertools.product(('yes','no','unknown'),('yes','no','unknown'),('current','revoked','unknown')):
            s=BASE.replace('affected=unknown reachable=unknown trust=unknown',f'affected={a} reachable={b} trust={t}')
            result=run(s,{**HOST,'affected':a,'reachable':b,'trust':t})
            self.assertFalse(result['execution_allowed'])
            self.assertFalse(result['may_publish_safe_claim'])
            self.assertEqual(len(result['decision_digest']),64)
            if t=='revoked': self.assertEqual(result['disposition'],'hold_unknown_or_untrusted')
            if a=='unknown' or b=='unknown' or t=='unknown':
                self.assertEqual(result['disposition'],'hold_unknown_or_untrusted')
    def test_contradictory_no_affected_but_reachable_is_not_safe(self):
        s=BASE.replace('affected=unknown reachable=unknown trust=unknown',
            'affected=no reachable=yes trust=current')
        r=run(s,{**HOST,'affected':'no','reachable':'yes','trust':'current'})
        self.assertEqual(r['disposition'],'hold_unknown_or_untrusted')
        self.assertFalse(r['may_publish_safe_claim'])
    def test_deterministic_digest(self):
        self.assertEqual(run(BASE,HOST)['decision_digest'],run(BASE,HOST)['decision_digest'])
    def test_legacy_profile_rejected(self):
        with self.assertRaises(SyntaxErrorV020):
            parse('⊙ [P1] program name=legacy targets=python312,node20')
    def test_untrusted_context_is_never_promoted(self):
        s=BASE.replace('affected=unknown reachable=unknown trust=unknown',
            'affected=no reachable=no trust=current')
        r=run(s,{**HOST,'trusted':False})
        self.assertEqual(r['disposition'],'hold_unknown_or_untrusted')
    def test_empty_ir_rejected(self):
        for doc in [{},{'version':'0.20-candidate'}, {'version':'0.20-candidate','mode':'advisory_only','statements':[]}]:
            with self.assertRaises(SyntaxErrorV020): evaluate(doc,HOST)

if __name__=='__main__':unittest.main()
