# Method 1 — Operational Risk Review

## Purpose

This method converts an operating concern into a bounded risk-and-control review that a responsible owner can understand and act on.

It is designed for situations where:

- a process is still moving but evidence is incomplete;
- a technical symptom may have wider operational consequences;
- ownership is unclear;
- a temporary workaround risks becoming a permanent control;
- release, shipment, deployment, or continued operation may reduce reversibility.

## Review question

> What is the next consequential action, what can fail, what control is expected, and what must be verified before proceeding?

## Inputs

- proposed action;
- process or asset affected;
- observed condition;
- authoritative source or expected requirement;
- known consequence;
- current control;
- accountable owner;
- available stop, rollback, or containment path.

Unknown information remains explicitly marked `unknown`.

## Sequence

### 1. Define the action

Do not begin with a general complaint. State the action that is about to occur.

Examples:

- release a modified assembly;
- continue operating under a temporary workaround;
- approve a purchase using conflicting records;
- close an issue without full validation;
- return a process to normal operation.

### 2. Separate source states

Classify each material claim as:

- **Observed:** directly seen or recorded;
- **Verified:** checked against an authoritative source;
- **Inference:** a bounded explanation;
- **Unknown:** missing or unresolved;
- **Disputed:** sources conflict;
- **Deprecated:** an earlier statement is no longer reliable.

### 3. Identify the failure mode

Describe the failure in operational terms.

```text
Condition
→ mechanism or control weakness
→ affected process
→ consequence
```

Avoid expanding beyond the evidence. A local symptom does not automatically establish a root cause.

### 4. Identify expected and actual control

| Question | Example answer |
| --- | --- |
| What control should exist? | full-range validation before release |
| What control actually exists? | limited static check |
| Is the control documented? | yes / no / unknown |
| Is it operating effectively? | effective / partial / absent / unknown |
| Who owns it? | named role or unknown |

A documented control and an effective control are not the same thing.

### 5. Assess consequence and reversibility

Consider:

- safety exposure;
- service interruption;
- production or delivery delay;
- rework and financial cost;
- customer or regulatory impact;
- evidence loss;
- accountability ambiguity;
- difficulty restoring the prior state.

The less reversible the next step, the stronger the review gate should be.

### 6. Assign two-axis output

#### Evidence direction

- `+` — evidence supports proceeding under the stated controls;
- `0` — evidence is incomplete, mixed, or unresolved;
- `-` — evidence currently opposes proceeding.

#### Risk signal

- **Green** — no stop-loss trigger identified;
- **Yellow** — slow down, verify, preserve options;
- **Red** — freeze, escalate, or exit may be reasonable.

The outputs are separate. Evidence can support a path while difficult reversibility still produces Yellow.

### 7. Select the control response

A control response should be proportional and specific:

- contain;
- verify;
- correct source data;
- test across the required operating envelope;
- require accountable sign-off;
- create a temporary exception with expiry;
- define rollback;
- freeze release;
- escalate to the responsible owner.

### 8. Define closure evidence

An issue is not closed because discussion stopped.

Closure requires evidence such as:

- validation completed;
- source record corrected;
- control owner assigned;
- corrective action implemented;
- exception accepted by an authorized owner;
- restart or release criteria satisfied;
- residual risk documented.

## Compact output

```text
Decision under review:
Observed condition:
Verified source:
Unknowns:
Failure mode:
Expected control:
Observed control gap:
Consequence:
Reversibility:
Evidence direction: + / 0 / -
Risk signal: Green / Yellow / Red
Decision required:
Safe next action:
Closure evidence:
Human Final Gate owner:
```

## Common failure patterns

- describing urgency instead of risk;
- treating a workaround as proof of control;
- merging observation and root-cause inference;
- escalating without stating the decision required;
- closing the issue without closure evidence;
- allowing the analyst or AI to absorb the accountable owner's decision.

## Boundary

This method supports analysis and documentation. It does not replace qualified engineering, safety, legal, regulatory, or management authority.