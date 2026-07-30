# Risk Review Template

Use this template to convert an operating concern into a concise, reviewable decision package.

## 1. Review scope

```text
Process / service / asset:
Business owner:
Technical or control owner:
Date of review:
Reviewer:
Proposed consequential action:
Decision deadline, if any:
```

## 2. Situation summary

Describe the issue in two to five sentences.

```text
What happened or is being proposed?
Why does it require review now?
What process, customer, system, vendor, or operation is affected?
```

## 3. Source-state table

| Material claim | Source | Date / version | State | Notes |
| --- | --- | --- | --- | --- |
|  |  |  | Verified / Observed / Inferred / Pending / Unknown / Contradicted / Deprecated |  |

## 4. Evidence direction

```text
Direction: + / 0 / -
Rationale:
Scope and time limit of the conclusion:
```

- `+` — current evidence supports the proposed path;
- `0` — evidence is incomplete, mixed, or unresolved;
- `-` — current evidence opposes the proposed path.

## 5. Risk and control review

| Area | Review question | Finding |
| --- | --- | --- |
| Boundary | Is a safety, authorization, privacy, contract, validation, or policy boundary involved? |  |
| Consequence | What could change if the action proceeds? |  |
| Reversibility | Can the action be stopped, corrected, or rolled back? |  |
| Responsibility | Who owns approval, exceptions, remediation, and closure? |  |
| Expected control | What should prevent or detect failure? |  |
| Actual control | What control is operating now? |  |
| Control gap | What is missing, partial, ineffective, or unverified? |  |
| Resilience | What happens if the process or dependency fails? |  |

## 6. Risk signal

```text
Signal: Green / Yellow / Red
Rationale:
```

- **Green:** no material stop-loss trigger identified;
- **Yellow:** slow down, verify, and preserve options;
- **Red:** freeze, escalate, or exit may be reasonable.

## 7. Options

| Option | Benefit | Risk | Reversibility | Required owner |
| --- | --- | --- | --- | --- |
| Proceed |  |  |  |  |
| Proceed with conditions |  |  |  |  |
| Pilot / limited scope |  |  |  |  |
| Hold for evidence |  |  |  |  |
| Freeze / reject / exit |  |  |  |  |

## 8. Recommended control response

```text
Immediate containment:
Evidence required:
Control correction:
Compensating control:
Escalation required:
Rollback or exit path:
```

## 9. Reversal condition

State what evidence would change the current conclusion.

```text
The conclusion should be reconsidered if:
1.
2.
3.
```

## 10. Decision required

```text
Decision owner:
Decision requested:
Required by:
Residual risk to be accepted:
Exception expiry, if applicable:
```

## 11. Closure evidence

```text
What must exist before the issue is considered closed?
- validation result;
- corrected source record;
- implemented control;
- assigned owner;
- completed remediation;
- accepted residual risk;
- restart / release approval;
- monitoring plan.
```

## 12. Compact executive summary

```text
Conclusion:
Decisive evidence:
Unknowns:
Evidence direction:
Risk signal:
Control gap:
Reversal condition:
Safe next action:
Human Final Gate owner:
```

## Use boundary

This template supports structured analysis and communication. It does not replace an organization's required legal, regulatory, engineering, safety, security, privacy, financial, or management review.