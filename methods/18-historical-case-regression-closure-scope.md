# 18 — Historical-Case Regression and Closure-Scope Gate

**Method:** Full-Push / Not Frozen (2026-10-23). **Code:** archived Bridge candidates, local-only replay; no production promotion.

## Prefer historical evidence to unnecessary novelty

When an archived parser, tests, known weaknesses and previously adjudicated cases exist, reproduce them before claiming a new concept or stronger capability:

`Immutable Archived Source → Hash Check → Closed-Scope Case Selection → Typed Fixture → Existing Test Runner → Negative Cases → Report What Passed AND What Failed`.

The critical difference is between *closing a decision* and *verifying every downstream effect*. A past decision to reject a candidate after inspection can be closed, while performance of an unpurchased alternative remains untested. An itinerary prepared before travel is not a completed trip. A safety stop does not itself demonstrate that the underlying engineering defect has been repaired.

### Scoping table

| Evidence | Permitted claim | Not permitted |
|---|---|---|
| Firsthand inspection plus explicit rejection | Decision closed, user-reported | Product class universally defective |
| Prepared plan and booking data | Planning/intent recorded | Travel/operational effect completed |
| Detected equipment inconsistency and stopped work | Local containment reported | Repair and all downstream effects verified |
| Synthetic Bridge parser/validator pass | Scoped test expectations matched | Verified real-world task or security assurance |
| Demonstrated security exploit | Blocking negative finding | Calling expected test exit 0 a secure outcome |

## Re-execution record (2026-10-23)

Archived Stage3/Stage8/Stage9 Conflict Triage sources were recovered and checksum verified. Fresh isolated replay reported:
- Directed regressions **41/41**, **44/44**, **32/32**, respectively (117 test assertions/methods; avoid double-counting shared sources).
- Stage8: 16,000 fixed-seed synthetic cases, zero unexpected outcomes.
- Stage9: 16,000 fixed-seed synthetic cases, zero unexpected outcomes.
- 13 typed, historical-case scenarios matched their authored read-only/hold/reject expectations. These fixtures do **not** independently attest real outcomes or verify natural-language-to-IR extraction.
- **Blocking negative finding persists:** an old Stage3 mocked effect-store forged receipt was accepted. Thus **Production: FAIL/HOLD** and **Training Hold** stay in force.

The replay did **not** exercise remote verified targets, independent trusted effect witness, deployed agent operations or the full frozen Bridge-0 governance suite. Original source archives and fresh logs were kept separate. Private case details and raw bundles remain outside this public repository.

## Rule

`Local Test PASS != External Effect Verified != Production Approved`.

Reuse original versions and concrete cases, keep their evidence grade and identity intact, expose contradictions, and never promote a candidate only because the replay exits successfully.
