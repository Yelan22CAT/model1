# Bridge-0 Stage9 RFC: Declared-Conflict Triage (Public-Safe)

**Status:** Experimental / Draft for Human Review / Not Production Ready / Training Hold.

**Relationship:** Optional read-only advisory extension of the Stage8 multiple-claim review interface. No change to official Bridge grammar, IR, live tool authorization, permission ownership, or protected Model 1 core. Full-Push of the reusable *method* does not promote the implementation.

## Problem

A conservative multi-claim audit can safely refuse to execute while still not detecting textual contradictions. It is important to separate (a) preventing unauthorized action, (b) detecting declared inconsistency, (c) proving source truth or textual entailment, and (d) establishing effect authority. These are not interchangeable assurances.

## Proposed advisory interface

An external, explicitly **untrusted** declaration may bind a claim ID to a subject, scope, predicate, Boolean value, and half-open time interval. A sidecar emits **review-only** statuses:

- `HOLD_DECLARED_CONTRADICTION`: equal subject/scope/predicate with opposing declared values within overlapping intervals.
- `HOLD_SEMANTIC_BINDING`: declaration/claim ID or explicit scope binding invalid.
- `HOLD_SHARED_PROVENANCE_REVIEW`: same opaque evidence ID appears in more than one claim. This does not by itself indicate manipulation.
- `HOLD_TIME_SCOPE`: declared support does not overlap the requested interval.
- `HOLD_UNRESOLVED_SEMANTICS`: declarations unavailable or invalid.
- `REVIEW_ONLY_NO_ENTAILMENT_PROOF`: syntactic declaration checks did not find a hold; this is **not** a verified claim.

Any underlying rejection, contextual hold or attestation requirement is preserved. None of the statuses grants execution, verifies goal completion or attests truth. The experiment also has bounded inputs and synthetic-time semantics.

## Evidence and limitations

Local author-written candidate tests, including directed regression, deterministic synthetic inputs and mutation probes, have been run; this is **not** an independent benchmark, remote proof or production-grade evaluation. Tests can distinguish selected intentionally broken guard branches but cannot demonstrate sound reasoning over arbitrary natural language.

A caller can supply misleading structured declarations. The design **does not** prove those declarations follow from original language or from trusted observations. Distinct evidence IDs are not evidence independence. Open cross-stage blockers include privileged mock witness/receipt forgery and the need for externally anchored trust, independent evidence provenance, policy authority, and replay/rollback controls. These are design and validation gaps, not claims of observed production compromise.

## Future review gates

1. Define authenticated provenance and independent trust roots before promotion.
2. Prove or independently review text-to-atom alignment; treat disagreement and ambiguity as a hold.
3. Preserve negative tests with falsified, correlated and stale evidence.
4. Keep human approval, limited authority and reversible effects separate from candidate reasoning outputs.

**Do not merge or deploy based on this RFC.** Stacked draft review should remain separate from the Stage8 candidate and must not rewrite historical verified high-water claims.