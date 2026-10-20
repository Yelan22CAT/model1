#!/usr/bin/env python3
"""SPCSG candidate policy-claim evidence admission profile for Bridge-0.

No network, no signature verification, no side effects. A profile for *claims*
only, not a normative Bridge-0 specification or an official legal decision.
The profile cannot determine whether any real-world source is truthful.
"""

KINDS = frozenset({'legal_scope', 'stated_risk', 'economic_effect', 'decision_motive'})
STATES = frozenset({'verified', 'candidate', 'unknown', 'refuted', 'conflict'})
EVIDENCE = frozenset({'primary_text', 'government_assertion', 'measured_outcome',
                     'decision_record', 'secondary_commentary'})


def audit_claim(record):
    """Return (accepted, reason). Fail closed on malformed records and invalid upgrades."""
    if not isinstance(record, dict):
        return False, 'RECORD_TYPE'
    required = {'kind', 'state', 'evidence', 'claim_id', 'source_scope'}
    if not required <= record.keys():
        return False, 'REQUIRED_FIELDS'
    kind, state, evidence = record['kind'], record['state'], record['evidence']
    if kind not in KINDS or state not in STATES or evidence not in EVIDENCE:
        return False, 'UNKNOWN_ENUM'
    if not isinstance(record['claim_id'], str) or not record['claim_id'].strip():
        return False, 'CLAIM_ID'
    if not isinstance(record['source_scope'], str) or not record['source_scope'].strip():
        return False, 'SOURCE_SCOPE'
    if record.get('market_impact') is not None and kind != 'economic_effect':
        return False, 'CROSS_KIND_VALUE'
    if state != 'verified':
        return True, 'UNPROMOTED'
    # Context-bound profile gates, not a real-world evidence authenticity check.
    if kind == 'legal_scope' and evidence != 'primary_text':
        return False, 'SCOPE_NEEDS_PRIMARY_TEXT'
    if kind == 'stated_risk' and evidence not in {'primary_text', 'government_assertion'}:
        return False, 'ASSERTION_NEEDS_SOURCE'
    if kind == 'economic_effect' and evidence != 'measured_outcome':
        return False, 'EFFECT_NEEDS_MEASUREMENT'
    if kind == 'decision_motive' and evidence != 'decision_record':
        return False, 'MOTIVE_NEEDS_DECISION_RECORD'
    # A primary government assertion verifies *that the agency asserted it*,
    # not that the underlying technical danger actually occurred.
    if kind == 'stated_risk' and record.get('assertion_is_proven_incident') is True:
        return False, 'ASSERTION_NOT_INCIDENT_PROOF'
    if kind == 'decision_motive' and record.get('inferred_from_effect') is True:
        return False, 'EFFECT_NOT_MOTIVE_PROOF'
    return True, 'PROFILE_ADMITTED_NOT_WORLD_TRUTH'