# 33 — Automation Irony & Human Takeover Readiness
**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-17). Public-safe governance method, **not** a deployed control system, production Bridge grammar, operator certification, or foundation-weight update.

## Source and problem
Lisanne Bainbridge, *Ironies of Automation*, *Automatica* 19(6):775–779 (1983), DOI: [10.1016/0005-1098(83)90046-8](https://doi.org/10.1016/0005-1098(83)90046-8). The original concerns industrial process control and human factors, not modern LLMs; applying it to AI agents is a **methodological transfer**.

Highly automated workflows can leave humans monitoring routine success while demanding difficult diagnosis and recovery during rare failures. Long periods without manual operation can reduce relevant practice; missing operating history can make emergency takeover ineffective.

## Method: AITR-G (human takeover readiness)
`Human Final != Human Ready != Safe Takeover`.

Before asking a person to take over consequential automation, distinguish:
1. **Permission** to decide from demonstrated understanding and operating skill.
2. **Fresh, independent state** from the AI model's own narrative.
3. **Completed action/effect receipts** from unverified summaries.
4. **Exception detection**, diagnosis, stabilization and recovery as different tasks.
5. **Measured response time** from a vague claim that a human is available.
6. **Authorized pretested safe-state response** from unrestricted automation.
7. **An observable acceptance test** from a plan, instruction sheet or simulation.

### Advisory-only handoff packet
Record `TASK`, `STATE` (source/time), `HISTORY` (effects/receipts), `ANOMALY`, `TIMING`, `HUMAN` (role and recent practice), `CHOICES`, `NEXT STEP` (owner, tools, success signal, stop condition), and scoped `SIGNOFF`.

Each missing independent source, stale state, invalid time, incomplete action history, insufficient human skill or absent permission must **hold**, not default to an optimistic ready state. Numeric timing inputs must be finite and nonnegative; a `NaN` cannot count as safety margin. "Advisory ready" is never an authority token.

## Local assurance evidence (strictly bounded)
A private archived Bridge-0 test exercise (2026-11-17) found that an earlier educational AITR prototype incorrectly labeled **4 of 6** additional invalid-input scenarios as `ADVISORY_READY`, including absent explicit attestations and `NaN` timing values. It continued to set `may_act=false`, but the misleading status remains a material candidate defect.

A revised advisory-only candidate explicitly requires every input and rejects malformed booleans, missing values, nonfinite timing and overflow. On 2026-11-17, **29/29 self-authored directed tests** passed, including **1,500 deterministic randomized vectors** checking that the evaluator never authorizes execution. A separately versioned `BRIDGE-HANDOFF/0.2-CANDIDATE` syntax prototype passed **17/17** local syntax tests with **2,500** deterministic round trips. These are scoped synthetic tests, **not independent proof of safety, true human competence or reliable authentication**.

## Non-negotiable boundaries
- Previous Bridge witness forgery, signer-independence and repeatability problems remain **OPEN / Production HOLD**.
- A formal candidate grammar document is not a released or backward-compatible production Bridge grammar.
- No external actuation, model-weight training, user-identity profiling, automatic approval or claimed field validation.
- Public content omits private scripts, raw exploits, user cases, credentials, proprietary data and hidden thresholds.

**Integration:** Existing Human Catch-up Gate / Human Final, task-authentic testing, SREG/HCRS-G, LCR/MISA, TAPEG, historical regression and PERV-G / Reality Gate. No competing governance stack.
