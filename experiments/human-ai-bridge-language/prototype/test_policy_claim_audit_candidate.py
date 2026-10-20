#!/usr/bin/env python3
"""SPCSG candidate profile tests, including Bridge-0 v0.2 parser integration.

When installed in Bridge-0/prototype, imports its actual parser and validator.
The optional SKIP is only for offline profile-only smoke testing.
"""
import unittest
from policy_claim_audit_candidate import audit_claim
try:
    from parser_v0_2 import parse_document, BridgeParseError
    from validator_v0_2 import validate_document
except ImportError:
    parse_document = None
    BridgeParseError = ValueError
    validate_document = None

BASE = dict(claim_id='C1', source_scope='federal_civilian_it')

class SPCSGProfileTests(unittest.TestCase):
    def check(self, kind, state, evidence, expected, **kw):
        item = dict(BASE, kind=kind, state=state, evidence=evidence, **kw)
        self.assertEqual(audit_claim(item)[0], expected, item)

    def test_scope_primary_accepted(self): self.check('legal_scope','verified','primary_text',True)
    def test_scope_commentary_rejected(self): self.check('legal_scope','verified','secondary_commentary',False)
    def test_risk_as_statement_accepted(self): self.check('stated_risk','verified','government_assertion',True)
    def test_asserted_risk_not_incident(self): self.check('stated_risk','verified','government_assertion',False,assertion_is_proven_incident=True)
    def test_economic_effect_measured(self): self.check('economic_effect','verified','measured_outcome',True)
    def test_effect_no_measured_data(self): self.check('economic_effect','verified','primary_text',False)
    def test_competition_effect_not_motive(self): self.check('decision_motive','verified','measured_outcome',False,inferred_from_effect=True)
    def test_motive_direct_record_profile(self): self.check('decision_motive','verified','decision_record',True)
    def test_motive_guess_retained(self): self.check('decision_motive','candidate','secondary_commentary',True)
    def test_unknown_retained(self): self.check('economic_effect','unknown','secondary_commentary',True)
    def test_missing_scope(self): self.assertFalse(audit_claim(dict(BASE,kind='legal_scope',state='verified',evidence='primary_text',source_scope=''))[0])
    def test_missing_type(self): self.assertFalse(audit_claim(dict(BASE,kind='political_truth',state='verified',evidence='primary_text'))[0])
    def test_nonrecord(self): self.assertFalse(audit_claim('policy')[0])
    def test_nonstring_claim_id(self): self.assertFalse(audit_claim(dict(BASE,kind='legal_scope',state='verified',evidence='primary_text',claim_id=42))[0])
    def test_cross_kind_field(self): self.check('decision_motive','candidate','decision_record',False,market_impact=12)
    def test_contradictory_motive_record(self): self.check('decision_motive','verified','decision_record',False,inferred_from_effect=True)

@unittest.skipIf(parse_document is None,'Bridge-0 parser files not locally installed: requires actual repo checkout')
class BridgeParserIntegrationTests(unittest.TestCase):
    def test_four_claim_domains_and_hypothesis_preserved(self):
        source = ('■ [C1] policy.scope = federal_civilian_it\n'
                  '■ [C2] agency.rationale = stated_security\n'
                  '△ [C3] policy.motive = domestic_industry_support\n'
                  '△ [C4] policy contributes_to procurement_reallocation\n'
                  '◆ [V1] official_notice supports [C1]\n'
                  '◆ [V2] agency_statement supports [C2]\n')
        doc = parse_document(source)
        self.assertTrue(validate_document(doc)['valid'])
        self.assertEqual([c['epistemic_state'] for c in doc['statements'] if c['kind']=='claim'],
                         ['fact','fact','hypothesis','hypothesis'])
    def test_asserted_motive_stays_hypothesis(self):
        doc = parse_document('△ [C1] policy.motive = market_protection\n■ [C2] commentator asserted [C1]\n')
        validation = validate_document(doc)
        self.assertTrue(validation['valid'])
        self.assertEqual(doc['statements'][0]['epistemic_state'],'hypothesis')
        self.assertIn('V006',[w['rule'] for w in validation['warnings']])
    def test_causal_and_associative_relations_stay_distinct(self):
        doc = parse_document('△ [C1] procurement associated_with market_change\n△ [C2] procurement causes market_change\n')
        self.assertTrue(validate_document(doc)['valid'])
        self.assertEqual([c['relation_class'] for c in doc['statements']], ['descriptive','causal'])
    def test_reject_unsupported_direct_promotion_syntax(self):
        with self.assertRaises(BridgeParseError):
            parse_document('■ [C1] outcome = ?')
    def test_no_fact_by_source_assertion(self):
        doc = parse_document('△ [C1] market_effect = benefit_domestic\n■ [C2] report asserted [C1]\n')
        self.assertEqual(doc['statements'][0]['epistemic_state'],'hypothesis')
        self.assertTrue(validate_document(doc)['valid'])

if __name__ == '__main__': unittest.main()