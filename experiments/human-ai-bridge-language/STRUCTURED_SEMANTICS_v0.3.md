# Bridge-0 Structured Semantics v0.3

> Status: **Experimental / composition stress layer**  
> v0.3 does not add a new glyph. It adds structured records for authority, handoff, transition, and provenance.

## 1. Why v0.3 exists

Round-trip tests showed that epistemic state can survive deterministic representation changes in the restricted v0.2 subset.

The next risk is **composition drift**:

```text
correct claim
→ handoff
→ another agent
→ broader permission
→ irreversible transition
→ lost provenance
```

v0.3 therefore tests whether authority and provenance can remain explicit across composed workflows.

---

## 2. Structured permission tuple

Surface form:

```text
! [P1] permission
  actor=agent
  action=read
  resource=repo
  scope=/docs/**
  condition=human_owner.approval
  valid_from=2026-10-01T00:00:00Z
  valid_until=2026-10-31T23:59:59Z
```

The actual parser uses one line.

Canonical tuple:

```text
(actor, action, resource, scope, condition, valid_from, valid_until)
```

Invariant:

```text
permission(read, /docs/**)
≠
permission(write, /docs/**)
≠
permission(read, /**)
```

No dimension may broaden implicitly.

---

## 3. Structured handoff

Surface form:

```text
→ [H1] handoff
  from=analyst
  to=judge
  artifact=[C1]
  scope=review
  state=preserve
  provenance=preserve
  transform=restatement
```

v0.3 hard rule:

```text
handoff
→ preserve epistemic state
→ preserve provenance
```

If an agent wants to create a genuinely new claim, it should create a new claim ID and explicit provenance edge rather than mutate the inherited claim.

---

## 4. Structured state transition

Surface form:

```text
→ [S1] transition
  subject=payment.state
  from=pending
  to=sent
  irreversible=true
  when=[G1]
  authority=human_owner
```

Invariant for irreversible transitions:

```text
irreversible=true
→ explicit guard
→ explicit authority
```

Bridge represents the control contract. It does not itself execute the transition.

---

## 5. Structured provenance

Surface form:

```text
◆ [PV1] provenance
  artifact=[C2]
  parent=[C1]
  actor=analyst
  transform=derive
  time=2026-10-02T00:00:00Z
```

Invariant:

```text
new artifact
→ explicit parent
→ explicit actor
→ explicit transform
```

Provenance cycles are rejected.

---

## 6. Composition example

```text
△ [C1] component.safe = true
◆ [V1] limited_test supports [C1]

! [P1] permission actor=executor action=read resource=repo scope=/tests/**

→ [H1] handoff from=executor to=analyst artifact=[C1] scope=analysis state=preserve provenance=preserve transform=analyze

△ [C2] component.release_ready = true
◆ [PV1] provenance artifact=[C2] parent=[C1] actor=analyst transform=derive

! [G1] release requires human_owner.approval

→ [S1] transition subject=release.state from=pending to=released irreversible=true when=[G1] authority=human_owner
```

The system must preserve:

- `[C1]` remains a hypothesis;
- `[C2]` is a separate hypothesis;
- provenance connects `[C2]` to `[C1]`;
- executor read permission does not become release authority;
- release requires the explicit guard and authority.

---

## 7. v0.3 validator rules

New rules:

```text
V019 permission tuple completeness
V020 permission validity-window ordering
V021 handoff reference and scope validity
V022 handoff state/provenance preservation
V023 irreversible transition guard + authority
V024 provenance reference validity
V025 provenance cycle rejection
```

These rules are deterministic.

They do not establish whether the human authority, source evidence, or external world is correct.

---

## 8. Design boundary

v0.3 intentionally does not add:

- delegation chains with arbitrary sub-grants;
- cryptographic identity;
- capability tokens;
- revocation protocols;
- distributed consensus;
- production execution;
- legal authorization semantics;
- 2D syntax.

Those may become later layers only if repeated tests demonstrate a real need.

The current question is narrower:

> Can a small shared semantic language preserve epistemic state, provenance, scope, and authority across a composed agent workflow?
