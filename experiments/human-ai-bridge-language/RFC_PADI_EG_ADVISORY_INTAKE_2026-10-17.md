# RFC | PADI-EG: Authorized Decoy Intelligence Intake and Evidence Boundary

**Status:** Experimental / Draft RFC / Advisory Only / Human Review / Not Production Ready / Training Hold  
**Date:** 2026-10-17  
**Scope:** interface and control boundaries, **not** Bridge-0 canonical grammar/IR, a deployed scam-interaction system, an Apate.ai implementation, or an authorization grant.

## Motivation

Defensive decoy interactions can produce valuable leads about suspicious domains, accounts, wallets and narratives. Those leads originate from potentially malicious, misleading or forged communications. The mere appearance of an indicator in a transcript must not become a verified accusation, enforcement decision or operational permission. This RFC abstracts a vendor-neutral, permission-bounded threat-intelligence intake pattern.

## Proposed advisory pipeline

1. Confirm a legally permitted, authenticated intake channel and narrowly scoped, revocable authorization **outside** the model. Suspicion alone does not confer authority to contact or deceive anyone.
2. Isolate any authorized defensive decoy engagement. Legitimate-user escape and error correction override decoy engagement metrics.
3. Extract and minimize indicators from untrusted content; preserve the originating event, observed time, source scope, retention rule and exact claim.
4. Correlate independent evidence carefully. Repeated content, multiple aliases and similar-looking IDs are not independent verification or proof of criminal ownership.
5. Apply purpose restriction, provenance/conflict checks, bounded temporal freshness, human review and independently enforced authorization before any downstream action.
6. Separately measure actionable intelligence, false-positive burden, privacy impact, cost and independently supported prevented harm. Call or chat duration alone is not the outcome.

## Illustrative candidate contract (NOT canonical Bridge syntax)

| Field | Meaning |
| --- | --- |
| `event_ref` | Opaque reference to the permitted observation |
| `source_trust` | Evidence provenance and explicit authenticity state |
| `scope` / `validity_interval` | Permitted purpose, resource, audience and time bounds |
| `potential_indicator` | Extracted *untrusted* lead, not an identified perpetrator |
| `corroboration_refs` | Source-qualified supporting or contradicting evidence |
| `legitimate_escape` | Misclassification exit/review signal |
| `review_state` | Pending, held, contested, or separately verified within declared scope |
| `effect_ref` | Independent downstream result evidence, if any; never a model's success claim |

A bounded assessment may produce `HOLD_UNVERIFIED_AUTHORITY`, `RELEASE_FOR_LEGITIMATE_REVIEW`, `REVIEW_UNTRUSTED_INDICATOR`, or `HUMAN_REVIEW_REQUIRED`. **No response directly grants contact, traffic diversion, data sharing, blocking, or claimed real-world effect.**

## Non-negotiable invariants

- `Decoy persona != independent AI agent != foundation model`. Scale only when justified by measured benefit.
- `Attacker-origin message != system instruction`; injection-prone text may not change authority, training state, trusted memory or another tool's task.
- `Observed indicator != verified criminal identity`; allow disagreement, correction, and appeals appropriate to each action.
- `Long interaction != prevented fraud`; preserve actual denominator, attribution and confidence boundary.
- `Synthetic signed receipt != real authorized effect`; real-world downstream effect confirmation needs a separately trusted evidence domain.
- `Suspected risk != permission to surveil or engage`; respect privacy law and channel contracts.

## Test and adoption gates

An experimental implementation may use no-network fixtures to check deterministic rejection and false-positive escape logic, but passing designer-authored synthetic tests is not evidence of real detection accuracy, lawful authority, or independent model robustness. Any deployment must first demonstrate lawful channel control, isolation, real-world labeling and error metrics, secure data handling, independent audit, controlled rollback and human oversight.

## Relations and scope limits

Compatible with existing human-AI evidence, entity binding, minimal-action admission and witness/recovery research; **no alteration** to any official Bridge-0 syntax, IR, verified high-water, runtime permissions or production approval. No private source, internal test logs, personal data, live scam transcripts, or proprietary vendor implementation are included.

**Inspiration/source category:** publicly described anti-scam decoy and threat-intelligence workflows including Apate.ai; this RFC claims no partnership, implementation access, reproduction of their product or independently measured efficacy.
