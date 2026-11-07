# 23 — Claim–Evidence–Effect–Deployment Gate (CEED-G)

**Status:** Public-safe method-level Full-Push / Not Frozen (2026-11-08). **Implementation:** Not deployed or independently security-tested.

## Purpose

An AI governance interface may report “configured,” “cleared,” or “100%” even while runtime coverage and residual risk remain unresolved. Separate four questions: **what was asserted; what evidence supports it; what changed in actual behavior; and which version/environment was deployed**.

## Minimal review sequence

`Objective and risk scope → discover active agent topology → claim/source register → authorized proposed minimal change → scoped implementation → malicious and legitimate request replays → independent effect evidence → deployment revision check → residual-risk register → accountable GO/HOLD/ROLLBACK`.

| Boundary | Practical test |
| --- | --- |
| Catalog entry versus identity | Confirm the runtime actor, owner, service identity and least-privilege access independently. |
| Gateway configuration versus coverage | Recheck effective routing; sample protected *and unprotected* agents and paths. |
| Inbound screening versus failure handling | Exercise the screen's timeout/unavailable behavior; **fail-open is a distinct risk**, not a blocked attack. |
| Security test versus service quality | Test adversarial instructions *and* legitimate user tasks; measure false blocks and misses. |
| Judge score versus ground truth | Retain scenario-by-scenario reasons, independent labels, denominator, failures and uncertainty. |
| Local copy versus live deployment | Record exact revision, environment, approvals, observations and external-effect receipts. |
| Tutorial or dashboard success versus assurance | Badges and progress counts are not estate-wide security certification. |

## Plain-language human review

Who is running? What can it read/write/send? Which paths are checked? What happens if checking fails? What changed and where? Which good and bad requests were retested? What is still unsafe, and who can stop or reverse it?

## Example and evidence boundary

A 2026 developer-event teaching scenario described an agent registry, identity/IAM, caller restrictions, inbound content scanning, local-copy evaluation and wrap-up. It also presented uncovered agents, broad permissions, a possible fail-open screen and a local fix **not yet deployed**. These are **presentation-observed teaching claims**, not independently verified cloud state or end-to-end effectiveness.

This method extends existing human-final authority, task-authentic evaluation, risk-proportional validation, and effect-receipt requirements. It does not authorize new agent behavior or clear any inherited production hold.

**Not released:** credentials, user identities, raw event photos, private cloud data, runtime guards, deployment manifests or validation artifacts.