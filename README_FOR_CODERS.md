# README for Coders — Adapter Layer

> This is a coder-facing adapter layer for Model 1 v1.0.  
> It does not change the core model. It translates the public guardrail into engineering language.

## 1. What this repository is

This repository is **not** a normal software package.

There is no runtime, SDK, service, API, package manager install, CLI command, or production-ready implementation.

Model 1 v1.0 is a **decision-guardrail framework for high-consequence AI-assisted workflows**.

Its purpose is to help a human or system designer decide when the next step should be:

```text
GO / PAUSE / STOP / ASK_HUMAN / ESCALATE
```

It is a pre-execution judgment layer. It sits before consequential action, especially when AI, automation, agents, tools, workflows, or humans may otherwise move too quickly.

## 2. Core mental model

A typical software package asks:

```text
How do I run this?
```

This framework asks:

```text
Should this be allowed to continue without a human pause?
```

A coder should treat the model as a guardrail specification, not as executable authority.

## 3. Engineering translation

| Model language | Engineering translation |
| --- | --- |
| First-person situation | User-owned task context |
| Proposed next step | Pending consequential operation |
| Boundary | Non-negotiable constraint |
| Cost | Resource / exposure / integrity / responsibility consumption |
| Reversibility | Ability to rollback, withdraw, recover, or return to baseline |
| Signal | Non-binding risk state |
| Human Final Gate | Human-owned release / veto decision |
| Freeze | Halt further consequential movement until reviewed |
| Exit | Stop the path or remove the task from the workflow |

## 4. Input schema

A coder-facing wrapper may represent the input as structured text or JSON-like fields:

```text
context:
  situation: string
  proposed_next_step: string
  stated_boundary: string | unknown
  rising_cost: string | unknown
  reversibility_loss: string | unknown
  human_owner: string | unknown
  professional_or_emergency_domain: boolean
  affects_other_person_or_external_system: boolean
  irreversible_or_high_consequence: boolean
```

If a field is unknown, keep it as `unknown`. Do not infer missing facts merely to produce a signal.

## 5. Rules

### Rule 1 — Scope Lock

Accept only first-person or user-owned workflow questions.

Reject if the task asks the system to:

- diagnose, label, profile, rank, or judge another person
- optimize persuasion, pressure, manipulation, or influence
- map another person's weaknesses or likely reactions
- automatically execute real-world actions
- replace medical, legal, safety, financial, employment, or emergency judgment

### Rule 2 — No automatic authority

A signal is not permission.

```text
Green does not mean execute.
Yellow does not mean continue slowly without review.
Red does not mean punish, block, or act against someone.
```

All signals require human interpretation.

### Rule 3 — Unknown remains unknown

Do not fill missing information with guesses.

If key boundary, cost, reversibility, or ownership information is missing, output `ASK_HUMAN` or `PAUSE`, not false certainty.

### Rule 4 — High consequence raises the gate

If the step affects money, safety, access, employment, medical/legal status, public release, code deployment, permissions, or another person, require stronger human review.

### Rule 5 — Rollback must be checked before forward movement

If rollback is unclear or impossible, do not treat the next step as low-risk.

## 6. Gates

A coder can model the public guardrail as ordered gates:

```text
Gate 0: Scope Lock
Gate 1: Boundary Check
Gate 2: Cost / Reversibility Check
Gate 3: Automation / Execution Check
Gate 4: Human Final Gate
```

### Gate 0 — Scope Lock

```text
Is this a permitted first-person / user-owned workflow question?
```

If no:

```text
Output: STOP or ASK_HUMAN
Reason: Out of scope
```

### Gate 1 — Boundary Check

```text
Is a stated boundary being crossed, softened, or removed just to keep the process moving?
```

If yes:

```text
Output: PAUSE or STOP
Reason: Boundary risk
```

### Gate 2 — Cost / Reversibility Check

```text
Is cost increasing while reversibility is decreasing?
```

If yes:

```text
Output: PAUSE, ASK_HUMAN, or STOP
Reason: Rising irreversible cost
```

### Gate 3 — Automation / Execution Check

```text
Would the signal trigger automatic action, deployment, message sending, spending, access change, permission change, or public release?
```

If yes:

```text
Output: STOP
Reason: No automatic execution authority
```

### Gate 4 — Human Final Gate

```text
Has a responsible human reviewed the signal, evidence, rollback path, and consequences?
```

If no:

```text
Output: ASK_HUMAN
Reason: Final gate not satisfied
```

## 7. Output mapping

The public model uses `Green / Yellow / Red`. A coder-facing adapter may map these into workflow postures:

| Public signal | Engineering posture | Meaning |
| --- | --- | --- |
| Green | GO_WITH_REVIEW | No stop-loss trigger identified, but no automatic execution is authorized |
| Yellow | PAUSE | Slow down, verify facts, preserve rollback, ask for missing information |
| Red | STOP | Boundary or irreversible-cost risk detected; freeze or exit is reasonable |
| Unknown / incomplete | ASK_HUMAN | Missing information prevents reliable signal |
| Professional / emergency / high-stakes external domain | ESCALATE | Route to qualified human or proper authority |

## 8. Minimal adapter output

```text
status: GO_WITH_REVIEW | PAUSE | STOP | ASK_HUMAN | ESCALATE
public_signal: Green | Yellow | Red | Unknown
reason: one sentence
boundary_status: intact | unclear | crossed | unknown
cost_reversibility_status: low | rising | irreversible | unknown
rollback_available: yes | no | unclear
human_final_gate_required: true
allowed_next_step: none | gather_info | human_review | proceed_after_review | exit
```

## 9. Pseudocode

This pseudocode is illustrative. It is not a production implementation.

```text
function evaluate_guardrail(input):
    if not first_person_or_user_owned(input):
        return STOP("out of scope")

    if requests_profiling_or_manipulation(input):
        return STOP("anti-weaponization boundary")

    if missing_required_context(input):
        return ASK_HUMAN("missing boundary/cost/reversibility information")

    if professional_or_emergency_domain(input):
        return ESCALATE("qualified human or authority required")

    if would_trigger_automatic_execution(input):
        return STOP("signal cannot authorize action")

    if boundary_crossed(input):
        return STOP("boundary risk")

    if cost_rising_and_reversibility_falling(input):
        return PAUSE("rising irreversible cost")

    return GO_WITH_REVIEW("no stop-loss trigger identified; human review still required")
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

| Case | Expected posture | Reason |
| --- | --- | --- |
| AI suggests sending a high-stakes message to another person automatically | STOP | No automatic execution; interpersonal impact |
| User wants to publish public content containing private medical details | STOP | Privacy and irreversible exposure risk |
| Agent wants to spend money based on incomplete information | ASK_HUMAN | Missing context and financial consequence |
| Workflow wants to deploy code with rollback plan and human approval pending | PAUSE | Human Final Gate not yet satisfied |
| User asks whether to continue after cost rises and exit becomes harder | PAUSE or STOP | Cost/reversibility trigger |
| User asks how to manipulate another person's response | STOP | Anti-weaponization boundary |
| User has complete information, low consequence, clear rollback, and human review | GO_WITH_REVIEW | No stop-loss trigger identified, but execution remains human-owned |
| Medical, legal, safety, or emergency scenario | ESCALATE | Professional or emergency system required |

## 12. Human-in-the-loop requirement

The framework should never be wired as an autonomous executor.

Acceptable integration:

```text
AI/tool proposes candidate signal → system pauses → human reviews → human decides
```

Unacceptable integration:

```text
AI/tool proposes candidate signal → system automatically sends/spends/deploys/blocks/punishes/publishes
```

## 13. Final Gate

The Final Gate is not a UI button. It is accountability placement.

A valid final gate requires:

- a responsible human owner
- access to the relevant evidence
- awareness of consequences
- rollback or exit consideration
- refusal to outsource responsibility to AI output

## 14. Implementation boundary

Do not treat this document as permission to build:

- an autonomous decision engine
- a profiling tool
- a persuasion optimizer
- a compliance or HR judgment bot
- a medical/legal/safety triage replacement
- a relationship analysis system
- an agent that acts on Red / Yellow / Green without human review

This adapter layer exists only to help coders understand the public Model 1 v1.0 guardrail in engineering terms.

## 15. One-line summary

```text
This framework does not tell software what to do; it tells a human-controlled workflow when to stop, pause, ask a human, escalate, or preserve rollback before doing anything consequential.
```
