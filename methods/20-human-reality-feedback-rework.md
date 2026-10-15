# Human-Reviewed Reality Feedback & Rework Gate (HRRFG)

**Public method note | 2026-10-14 | Full-Push method proposal; NOT production-validated**

## Purpose

A model-generated artifact, a human-authored design and a physical component can all pass a local check while failing their **real intended use**. HRRFG offers a reusable, bounded feedback-and-rework procedure to find that gap. It is a method **for checking outputs**, not a new model, an always-on agent, or a claim that AI is unable to do the underlying work without personal memory.

**Core loop:**

```text
Specify outcome and risk
        ↓
Create a versioned candidate
        ↓
Check against independent acceptance criteria
        ↓
Human / qualified reviewer decides
        ↓
  [Accept]  [Rework]  [Hold/Escalate]  [Reject]
                ↓
          New revision + affected regression checks
                ↺ to review
        ↓
Release ONLY under appropriate authority
        ↓
Observe actual effect and re-open on contradictions
```

### Different risk, different validation

| Example | Candidate | Concrete gap | Appropriate closure |
| --- | --- | --- | --- |
| Illustrated instructional booklet | A consistent multi-page visual artifact | Two pages miss necessary diagrams or later edits introduce contradictory quantities | Revise affected pages; check the whole booklet; specialist verifies the actual procedure if it purports to teach a physical craft |
| Safety-relevant mechanical component | Designed/manufactured part with a lab pass | Credible in-service failure despite another, differently conditioned test passing | Contain risk, preserve failed samples, conduct qualified independent failure analysis; version-specific system and field validation before authorization |

**Same process structure does not mean equivalent risk.** Human reviewers may request a visual re-render, but cannot approve away a safety-critical physical failure by opinion alone.

## Minimum validation contract

Record for each candidate:
- artifact ID, revision, exact source inputs and declared constraints;
- risk tier, review owner, authorized actions and independent verifier if required;
- acceptance check ID, evidence source, test environment, exact tested revision;
- defect description, severity, possible explanations and uncertain facts;
- review decision: accept, bounded rework, reject, hold / escalate;
- what changed, impacted previous checks and new regression results;
- release decision and independently observed downstream effect when available.

**Invariants**

1. `Generated != Reviewed != Verified != Released != Proven Effective`.
2. `Attractive Graphics != Correct Instructions != Physically Reproduced Outcome`.
3. `Lab Pass != All Foreseeable Field Conditions`; `Observed Failure != Proven Root Cause`.
4. `Review Feedback != Independent Evidence`, especially when the reviewer generated the output.
5. `Fix Proposed != Fix Validated`; `Tested Revision A != Revised Artifact B`.
6. `Rework != Rollback != Field Remediation`.
7. `More Iterations != Better Results`; stop with a supported decision or explicit unresolved status.

## Safe implementation outline

1. Fix the goal, constraints and acceptance matrix **before** generation.
2. Produce a traceable artifact and save prior revisions.
3. Evaluate locally and across interdependent pages/modules/assemblies.
4. Classify failures as missing coverage, visual inconsistency, semantic error, wrong source, physical incompatibility, missing evidence, or unapproved action.
5. Human reviewers select a minimal sufficient correction, test plan, rejection or escalation. Critical physical systems require competent engineering and formal safety authority.
6. Retest the exact new revision **and all impacted prior-pass cases**. Preserve contradictory evidence and failures.
7. Release only when the relevant authority approves; observe actual user/field effects separately from the approval event.

## What the example does *not* establish

- A base GPT equipped with the same image tools and reference examples may create a similar multi-page visual guide. Adding a persistent review manifest is a workflow feature, not new model weights.
- A photorealistic craft diagram or a passing numerical check does not prove a physical item was successfully made.
- Passing a component test does not justify ignoring a credible field failure, but a field anecdote does not prove a universal root cause.
- No claimed quantitative improvement of this process exists without a fair benchmark against an ordinary-GPT baseline.

## Suggested validation exercises (design only; NOT RUN)

Check missing illustrated pages, page numbering gaps, numeric inconsistencies, regenerated-page style drift, false review receipts, stale evidence on a new revision, unbounded iteration, test/field contradiction, and unauthorized safety-critical release. Test effectiveness and human review cost in controlled studies.

**Boundary:** This public description deliberately excludes private individual information, original images, unpublished artifacts, internal implementation and third-party allegations. Existing human final authority, copyright/usage controls and test evidence requirements remain in force. No deployment, merge, model fine-tuning or safety certification is implied.