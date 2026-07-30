# Control Gap Log

Use this register to track the difference between an expected control and the condition actually supported by evidence.

## Register

| ID | Process / third party / system | Expected control | Evidence reviewed | Actual condition | Gap classification | Consequence | Compensating control | Owner | Due date | Status | Closure evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CG-001 |  |  |  |  | Missing / Partial / Ineffective / Unverified / Expired / Not applicable |  |  |  |  | Open / In progress / Exception / Closed / Deprecated |  |

## Gap classification

### Missing

The expected control does not exist or has not been provided.

### Partial

The control covers only part of the required scope.

### Ineffective

The control exists but available evidence shows that it is not operating as intended.

### Unverified

The control is claimed, but evidence is insufficient to confirm it.

### Expired

The control, test, approval, exception, or evidence is no longer current.

### Not applicable

The control is excluded with documented rationale and accountable approval.

## Required fields for a usable gap

A control gap should answer:

```text
What control was expected?
What evidence was reviewed?
What condition was actually found?
What consequence can result?
Who owns correction or acceptance?
What temporary control exists?
When must the gap be reviewed?
What evidence will prove closure?
```

## Status rules

### Open

The gap is identified and no adequate remediation or accepted exception is in place.

### In progress

A named owner and remediation action exist, but closure evidence is not complete.

### Exception

An authorized owner has accepted the residual risk for a defined scope and expiry date.

An exception should include:

- reason;
- scope;
- residual risk;
- compensating control;
- approver;
- expiry date;
- review trigger.

### Closed

The required closure evidence has been reviewed and supports closure.

Discussion, intent, or task completion alone is not closure evidence.

### Deprecated

The gap record is no longer active because the process, control requirement, or earlier classification changed. The history remains visible.

## Escalation triggers

Escalate when:

- the gap affects safety, authorization, privacy, legal, regulatory, or contractual requirements;
- a high-consequence action is planned before remediation;
- the control owner is unknown;
- the due date or exception expiry is missed;
- the compensating control is not operating;
- the same gap recurs;
- operational dependency or exposure increases;
- evidence shows the risk is greater than originally assessed.

## Closure quality check

Before marking a gap closed, verify:

- the expected control is still current;
- the evidence covers the stated scope;
- the control is implemented, not merely planned;
- the accountable owner accepts closure;
- related records and procedures are updated;
- ongoing monitoring is defined where needed;
- residual risk is not hidden by wording changes.

## Compact management view

```text
Open critical gaps:
Overdue gaps:
Exceptions approaching expiry:
Repeated gaps:
Gaps without owners:
Gaps affecting high-consequence actions:
Decisions required from management:
```

## Use boundary

This template is a public work sample. Organizations should adapt it to their own risk taxonomy, policy requirements, materiality criteria, systems, and approval authority.