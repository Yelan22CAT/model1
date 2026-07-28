# README for Coders — Adapter Layer

> This is a coder-facing adapter layer for Model 1 v1.0.  
> It does not change the core model. It translates the public judgment guardrail into engineering language.

## 1. What this repository is

This repository is **not** a normal software package.

There is no runtime, SDK, service, API, package-manager install, CLI command, or production-ready implementation.

Model 1 v1.0 is a **human-controlled judgment guardrail for high-consequence AI-assisted workflows**.

Its purpose is to help a human or system designer distinguish:

```text
what the evidence currently says: SUPPORT / UNRESOLVED / OPPOSE
```

from:

```text
how strongly the workflow should pause: GO_WITH_REVIEW / PAUSE / STOP / ASK_HUMAN / ESCALATE
```

It sits before consequential action, especially when AI, automation, agents, tools, workflows, or humans may otherwise move too quickly.

## 2. Core mental model

A typical software package asks:

```text
How do I run this?
```

This framework asks:

```text
What is fact, inference, and unknown?
What does the evidence currently say about the proposed path?
Should this continue without a human pause?
```

A coder should treat the model as a public guardrail specification, not executable authority.

## 3. Engineering translation

| Model language | Engineering translation |
| --- | --- |
| First-person situation | User-owned task context |
| Proposed next action | Pending consequential operation |
| Observation / verified fact | Source-backed input field |
| Hypothesis / inference | Bounded candidate interpretation |
| Unknown / verification pending | Missing, mixed, stale, or unresolved state |
| Evidence direction `+ / 0 / -` | Support / unresolved / oppose assessment |
| Boundary | Non-negotiable constraint |
| Consequence | Real-world effect or blast radius |
| Cost | Resource / exposure / integrity / responsibility consumption |
| Reversibility | Ability to roll back, withdraw, recover, or return to baseline |
| Green / Yellow / Red | Non-binding action-risk signal |
| Human Final Gate | Human-owned release / veto decision |
| Freeze | Halt further consequential movement until reviewed |
| Deprecated | Retained historical state that is no longer active |

## 4. Input schema

A coder-facing wrapper may represent the input as structured text or JSON-like fields:

```text
context:
  situation: string
  proposed_next_step: string
  verified_facts: string[]
  bounded_inferences: string[]
  assumptions: string[]
  important_unknowns: string[]
  stated_boundary: string | unknown
  consequence: string | unknown
  rising_cost: string | unknown
  reversibility_loss: string | unknown
  human_owner: string | unknown
  professional_or_emergency_domain: boolean
  affects_other_person_or_external_system: boolean
  irreversible_or_high_consequence: boolean
```

If a field is unknown, keep it as `unknown`. Do not infer missing facts merely to produce a clean output.

## 5. Rules

### Rule 1 — Scope Lock

Accept only first-person or user-owned workflow questions.

Reject if the task asks the system to:

- diagnose, label, profile, rank, or judge another person;
- optimize persuasion, pressure, manipulation, or influence;
- map another person's weaknesses or likely reactions;
- automatically execute real-world actions;
- replace medical, legal, safety, financial, employment, or emergency judgment.

### Rule 2 — Source states remain distinct

Do not collapse:

```text
observation → hypothesis → verification pending → verified
```

into one generic “known” state.

Fluency, repetition, model confidence, or formatting does not convert an inference into a verified fact.

### Rule 3 — Unknown remains unknown

If key source, boundary, consequence, reversibility, or ownership information is missing, preserve `UNRESOLVED` and use `ASK_HUMAN` or `PAUSE` rather than false certainty.

### Rule 4 — Direction and signal are separate

```text
Evidence direction: SUPPORT | UNRESOLVED | OPPOSE
Risk signal: Green | Yellow | Red
```

A supported path may still be Yellow because rollback is weak. An unresolved path may be Red because a mandatory validation or authorization gate is missing.

Neither output is permission.

### Rule 5 — High consequence raises the gate

If the step affects money, safety, access, employment, medical or legal status, public release, code deployment, permissions, or another person, require stronger human review.

### Rule 6 — Rollback must be checked before forward movement

If rollback is unclear or impossible, do not treat the next step as low-risk.

### Rule 7 — Hard boundaries override gray optimization

Nuance may preserve uncertainty, but it must not wash away a safety, authorization, privacy, consent, contractual, or required-validation rule.

## 6. Public gate sequence

```text
Gate 0: Scope Lock
Gate 1: Source-State Check
Gate 2: Evidence Direction
Gate 3: Boundary / Consequence / Reversibility Check
Gate 4: Automation / Execution Check
Gate 5: Human Final Gate
```

### Gate 0 — Scope Lock

```text
Is this a permitted first-person / user-owned workflow question?
```

If no:

```text
status: STOP
reason: out of public scope
```

### Gate 1 — Source-State Check

```text
Which claims are verified facts?
Which are bounded inferences?
Which remain unknown or verification pending?
```

If key information is missing:

```text
evidence_direction: UNRESOLVED
status: ASK_HUMAN or PAUSE
```

### Gate 2 — Evidence Direction

```text
SUPPORT: present evidence supports the proposed path
UNRESOLVED: evidence is insufficient, mixed, or unresolved
OPPOSE: present evidence opposes the proposed path
```

This state is bounded by the current scope and evidence. It does not execute or approve.

### Gate 3 — Boundary / Consequence / Reversibility Check

Ask:

```text
Is a hard boundary being crossed?
What real-world effect can the action create?
Is cost increasing while reversibility decreases?
Who owns exceptions, maintenance, rollback, and approval?
```

Possible postures:

```text
GO_WITH_REVIEW / PAUSE / STOP / ASK_HUMAN / ESCALATE
```

### Gate 4 — Automation / Execution Check

```text
Would any output trigger automatic sending, spending, deployment,
access changes, permission changes, public release, punishment, or blocking?
```

If yes:

```text
status: STOP
reason: no automatic execution authority
```

### Gate 5 — Human Final Gate

```text
Has a responsible human reviewed the evidence states, direction,
risk signal, rollback path, consequences, and ownership?
```

If no:

```text
status: ASK_HUMAN
reason: final gate not satisfied
```

## 7. Public output mapping

### Evidence direction

| Public direction | Engineering state | Meaning |
| --- | --- | --- |
| `+` | SUPPORT | Current evidence supports the proposed path within the stated scope. |
| `0` | UNRESOLVED | Evidence is insufficient, mixed, or not yet verified. |
| `-` | OPPOSE | Current evidence opposes the proposed path within the stated scope. |

### Risk signal

| Public signal | Engineering posture | Meaning |
| --- | --- | --- |
| Green | GO_WITH_REVIEW | No stop-loss trigger identified; no automatic execution is authorized. |
| Yellow | PAUSE | Slow down, verify facts, preserve rollback, and ask for missing information. |
| Red | STOP | A hard boundary, mandatory validation gap, or irreversible-cost risk is present. |
| Incomplete high-impact input | ASK_HUMAN | Missing information prevents reliable review. |
| Professional / emergency / high-stakes domain | ESCALATE | Route to a qualified human or proper authority. |

## 8. Minimal adapter output

```text
status: GO_WITH_REVIEW | PAUSE | STOP | ASK_HUMAN | ESCALATE
public_direction: + | 0 | -
evidence_state: verified | mixed | verification_pending | unknown
public_signal: Green | Yellow | Red
conclusion: one bounded sentence
decisive_evidence: string[]
unknowns: string[]
reversal_condition: string
boundary_status: intact | unclear | crossed | unknown
cost_reversibility_status: low | rising | irreversible | unknown
rollback_available: yes | no | unclear
human_final_gate_required: true
allowed_next_step: none | gather_info | human_review | proceed_after_review | exit
```

## 9. Illustrative pseudocode

This pseudocode is not a production implementation and contains no private thresholds or calibration logic.

```text
function review_guardrail(input):
    if not first_person_or_user_owned(input):
        return STOP("out of scope")

    if requests_profiling_or_manipulation(input):
        return STOP("anti-weaponization boundary")

    source_state = separate_fact_inference_unknown(input)

    if professional_or_emergency_domain(input):
        return ESCALATE("qualified human or authority required")

    direction = bounded_evidence_direction(source_state)

    if would_trigger_automatic_execution(input):
        return STOP_WITH(direction, "output cannot authorize action")

    if hard_boundary_crossed(input):
        return RED_STOP(direction, "hard boundary")

    if mandatory_validation_missing(input):
        return RED_STOP(direction, "validation gate not satisfied")

    if missing_high_impact_context(input):
        return ASK_HUMAN_WITH(UNRESOLVED, "important unknowns remain")

    if cost_rising_or_reversibility_falling(input):
        return YELLOW_PAUSE(direction, "preserve rollback and verify")

    return GREEN_REVIEW(direction, "human review still required")
```

## 10. Rollback checklist

Before any consequential next step, ask:

```text
Can this be undone?
Can access be restored?
Can money be recovered?
Can a message or publication be withdrawn?
Can a deployment be reverted?
Can the affected person or system be protected from irreversible harm?
Who owns the rollback decision?
```

If rollback is unknown or unavailable, prefer `PAUSE`, `ASK_HUMAN`, or `STOP`.

## 11. Test cases

| Case | Direction | Expected posture | Reason |
| --- | --- | --- | --- |
| Conflicting source records before purchase | UNRESOLVED | PAUSE | Source of truth is unclear and cost will become less reversible. |
| Late technical change without full-range validation | OPPOSE | STOP | Mandatory validation gap before release. |
| AI suggests sending a high-stakes message automatically | UNRESOLVED | STOP | No automatic execution; interpersonal consequence. |
| User wants to publish private medical details | OPPOSE | STOP | Privacy and irreversible exposure risk. |
| Agent wants to spend money from incomplete information | UNRESOLVED | ASK_HUMAN | Missing context and financial consequence. |
| Workflow has evidence, rollback, and human approval pending | SUPPORT | PAUSE | Human Final Gate is not yet satisfied. |
| User asks how to manipulate another person's response | not evaluated | STOP | Anti-weaponization boundary. |
| Complete information, low consequence, clear rollback, human owner | SUPPORT | GO_WITH_REVIEW | No stop-loss trigger identified, but execution remains human-owned. |
| Medical, legal, safety, or emergency scenario | not evaluated | ESCALATE | Qualified professional or emergency system required. |

## 12. Human-in-the-loop requirement

Acceptable integration:

```text
AI/tool separates evidence states and proposes bounded outputs
→ system pauses
→ human reviews evidence, direction, signal, and rollback
→ human decides
```

Unacceptable integration:

```text
AI/tool produces direction or signal
→ system automatically sends / spends / deploys / blocks / punishes / publishes
```

## 13. Final Gate

The Final Gate is not merely a UI button. It is accountability placement.

A valid final gate requires:

- a responsible human owner;
- access to relevant evidence;
- awareness of unknowns and alternatives;
- awareness of consequences;
- rollback or exit consideration;
- refusal to outsource responsibility to AI output.

## 14. Implementation boundary

Do not treat this document as permission to build:

- an autonomous decision engine;
- a profiling or human-ranking tool;
- a persuasion optimizer;
- a compliance or HR judgment bot;
- a medical, legal, safety, or emergency triage replacement;
- a relationship-analysis system;
- a system that acts automatically on `+ / 0 / -` or Green / Yellow / Red;
- a reconstruction of private observers, thresholds, market models, anti-poisoning internals, or runtime logic.

This adapter exists only to help coders understand the public Model 1 v1.0 judgment interface in engineering terms.

## 15. One-line summary

```text
Separate fact, inference, and unknown; express evidence direction;
check boundary and reversibility; then stop for human judgment before consequential execution.
```
