# Bridge-0 Examples v0.1

> Synthetic examples only. These are language tests, not real-world decisions.

## Example A — source-backed fact

```text
○ invoice_17
■ invoice_17.total = 4280 CAD
◆ invoice_17.pdf supports ■ invoice_17.total
✓ invoice_17.total verified_by arithmetic_check
```

Expected interpretation:

- the invoice is an entity;
- 4280 CAD is asserted as a fact claim;
- the PDF is supporting evidence;
- a defined arithmetic check verified the total.

---

## Example B — unresolved cause

```text
○ incident_5
△ incident_5.cause = connector_timeout
◆ log_excerpt supports △ incident_5.cause
? root_cause
```

Expected interpretation:

- connector timeout is a hypothesis;
- there is some supporting evidence;
- root cause is still unknown;
- the runtime must not rewrite the hypothesis as a verified fact.

---

## Example C — permission boundary

```text
○ agent
○ human_owner

⊙ update_production_config

→ agent prepare_change
! production_write requires human_owner_approval
× agent approve_production_write
✓ human_owner approval
```

Expected interpretation:

The agent may prepare a change but does not own final execution authority.

---

## Example D — stale time state

```text
■ vendor.status = approved
⏱ observed_at = 2026-01-15
! approval_validity = 90 days
```

At a later date, a validator may derive:

```text
? current_vendor_status
× reuse_old_approval_as_current_fact
```

The old statement remains historically true but is not silently inherited as current truth.

---

## Example E — explicit decision frame

```text
⊙ choose_backup_route

■ route_A.cost = 15
■ route_B.cost = 30

△ route_A.reliability = medium
△ route_B.reliability = high

! max_cost = 35
? measured_failure_rate
```

Expected interpretation:

The system has enough structure to compare known cost, provisional reliability, a hard cost constraint, and a missing measurement — without inventing the missing failure rate.

---

## Example F — invalid silent completion

Input:

```text
■ person.age = ?
```

Invalid transformation:

```text
■ person.age = 35
```

unless new evidence and an explicit transition are present.

Valid response:

```text
? person.age
```

or:

```text
△ person.age ≈ 35
◆ source_X supports △ person.age
```

if an estimate is intentionally introduced and clearly marked as a hypothesis.

---

## Test idea

For each example, ask multiple models to:

1. parse it;
2. restate it;
3. serialize it to canonical JSON;
4. restore it to Bridge form;
5. identify any semantic-state loss.

A useful language should preserve the distinction between `■`, `△`, and `?` across the round trip.
