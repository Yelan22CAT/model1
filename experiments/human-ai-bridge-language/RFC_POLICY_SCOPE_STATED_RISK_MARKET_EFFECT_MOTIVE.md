# RFC — Policy Claim Scope and Attribution Profile (SPCSG)

**Date:** 2026-10-20  
**Status:** Candidate method / experimental Bridge-0 domain validation; not RC1 grammar or core validator revision; not a production legal assessment.  
**User authorization:** amend private/public repositories and Bridge implementation as required, subject to actual tests and compatibility evidence.

## Motivation

A policy text may certify that an agency *asserted* a cybersecurity risk. This does not certify that a technical incident occurred, that certain firms profited, or that the agency had a particular political/economic motive. A market-access rule can have an economic effect without proving a specific intent. Safety review and economic-impact analysis are both relevant, but they ask distinct questions.

## Four typed assertion domains (profile-level, not new grammar symbols)

1. `legal_scope`: what a primary order actually covers, its date and exceptions.
2. `stated_risk`: what the issuing agency asserts as a risk; assertion ≠ externally verified incident.
3. `economic_effect`: market-access or procurement effects, measured independently where an empirical claim is asserted.
4. `decision_motive`: why decision-makers issued the policy; not inferred solely from side effects or product price.

All include `claim_id`, `source_scope`, epistemic `state`, and an evidence-kind **label**. These labels are inputs to the experimental domain gate, **not proof authenticity**.

## Existing Bridge-0 v0.2 surface encoding (no new lexemes needed)

```bridge
■ [C1] policy.scope = federal_civilian_it
■ [C2] agency.rationale = stated_security
△ [C3] policy.motive = domestic_industry_support
△ [C4] policy contributes_to procurement_reallocation
◆ [V1] official_notice supports [C1]
◆ [V2] agency_statement supports [C2]
```

`■ [C2]` records the agency's stated rationale, **not proof that danger occurred**. `△ [C3]` remains hypothetical. `△ [C4]` denotes a possible *consequence*, not established motive.

```bridge
△ [C1] policy.motive = domestic_industry_support
■ [C2] commentator asserted [C1]
```

The second fact is **about the assertion**. The first claim remains a hypothesis; a meta-claim is not a promotion instruction.

## Separate claim-admission profile

Reference prototype: `prototype/policy_claim_audit_candidate.py`. It rejects promotion of `legal_scope` without primary-text evidence class; `stated_risk` without government assertion provenance; `economic_effect` without measured-outcome evidence; and `decision_motive` without decision records. No source is independently authenticated by this program. `verified` means a **profile admission**, not empirical truth.

## Tests and negative controls

`python -m unittest -v test_policy_claim_audit_candidate.py` in `prototype/`. Includes v0.2 Bridge parser/validator semantic separation, statement/motive preservation, causal vs descriptive distinction and unknown rejection. Works alongside, not in place of, the frozen RC1 public-reproduction suite. Test execution claims must identify runner, commit and skips.

## RC1 freeze and proposed disposition

**No RC1 grammar change proposed today**. The existing `■ △ ◆ ✓ ?` markers and `asserted / associated_with / causes` relations can express all four domains. New language primitives would introduce compatibility and migration obligations without an observed representational gap. The owner now authorizes review of future normative changes; actual freeze alteration, anchored corpus/digest regeneration and third-party qualification remain separate gated actions. A green candidate profile test does not certify protected RC1 semantics.

## Reference / privacy

- DHS Federal Register FR Doc. 2026-21447: https://public-inspection.federalregister.gov/2026-21447.pdf
- NIST/CAISI May 2026 DeepSeek V4 Pro evaluation: https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro
- No user screenshots, private capture files, private narratives or unverified social-media statistics are reproduced.