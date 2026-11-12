# 16 — Human Comprehension Review Gate (HCRG)

**Purpose:** one additional, risk-adaptive human comprehension review between AI-generated/tested change and material approval. **Method status:** Full-Push / Not Frozen in private Model Root by explicit user instruction, 2026-10-21. **GitHub document:** Draft PR candidate until reviewed and merged. **Implementation status:** proposed method, not deployed enforcement.

## Problem and minimum change

AI code-generation speed can outrun the human owner's ability to understand, verify, own, and stop material behavior. Do not replace the original Model 1 Pre-Stop or Human Final with a new agent, a mandatory exam for trivial edits, or automatic approvals.

```text
Human reality observation + provisional view
 -> define desired behavior and hard boundaries
 -> AI prepares candidate change + ordinary-language explanation
 -> relevant automated positive/negative/regression checks
 -> HUMAN COMPREHENSION REVIEW  (the single added stage)
 -> accountable human decides: HOLD / bounded experiment / expert review / scoped approval
 -> separately authorized merge or deployment, if appropriate
 -> reality feedback / correction
```

## Three questions answered by the human

The assistant may explain and ask, but must **not** generate the human's supposed answer or certify comprehension by self-review:

1. **Purpose:** What real-world problem does the change solve, and what fails if we omit it?
2. **Failure:** Under what conditions could the change be wrong, unsafe, or misleading?
3. **Control:** Who can stop it, and what must be true for a safe recovery/rollback?

Unknown, disagreement, and **NOT YET REVIEWED** are legitimate results. A person cannot sign off on a safety-critical change simply by repeating an AI's explanation.

## Proportional application

| Tier | Examples | Minimum before material promotion |
| --- | --- | --- |
| L0 | Typo, non-semantic reversible cleanup | Automated check and selective sampling; no mandatory quiz |
| L1 | Routine code/behavior modification | Explanation + revision-bound tests + human's own responses |
| L2 | Permission, privacy, money, external effect, trust, freeze/resume, safety, normative grammar, irreversible action | Candidate/HOLD pending competent independent review, negative cases, explicit exact-scope human approval and existing external gates |

Classification follows effects, not filename: a prose edit that changes normative authority may be L2. Independent assurance is not identical to another prompt to the same generating model.

## Evidence record

For a material change, preserve: real problem, baseline expectation, changed behavior, exact revision/PR, risk tier, tests actually run and gaps, negative cases, human response or pending, owner/authority, stop/rollback limitations and an explicit disposition.

Statuses remain distinct: **Method Full-Push != Code Approved != Human Understood != Independent Assurance != Production Ready.** A green CI result does not authorize a release.

## Synthetic counterexample (not executed)

A hypothetical assembly drawing requires a mounting plate. The BOM and a fictional kit do not agree. The candidate aid must preserve **CONFLICT/UNKNOWN**, and must not turn an unverified missing item into permission for physical installation. **Case status: Candidate / Evidence Pending / Human Comprehension Review Pending**. No actual customer, employer, installation, or field test is asserted.

## Compatibility and scope

This is a lightweight operational link to existing [human-first learning](09-human-first-learning-review.md), [Human Catch-up Gate](../safety/HUMAN_CATCHUP_GATE.md) and [selective intervention](14-selective-intervention-autonomy-governance.md). Original [Model 1 minimal core](../MODEL1_MINIMAL_CORE.md) remains a **first-person stop-loss guardrail**, not an execution system. Bridge-0 remains experimental; no normative syntax, freeze status, or stop/resume authority is modified. Human Final retains accountable decision power, with independent technical review required when risk warrants.

**Core invariant:** AI-generated != machine-tested != human-understood != independently-audited != release-authorized.
