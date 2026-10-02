# Bridge-0 Authority Lifecycle v0.4

> Status: Experimental / authority-lifecycle stress layer  
> v0.4 adds no new glyphs.

## Purpose

v0.3 showed that scope and authority can survive deterministic handoff.

v0.4 asks a harder question:

> Can authority remain correct after grant, delegation, narrowing, expiry, revocation, and replay?

The main failure target is stale-authority reuse.

## Surface forms

### Grant

```text
! [P1] grant
  grantor=human_owner
  actor=agent_a
  action=read
  resource=repo
  scope=/docs/**
  at=2026-10-02T00:00:00Z
  epoch=1
```

### Delegation

```text
→ [D1] delegate
  parent=[P1]
  from=agent_a
  to=agent_b
  action=read
  resource=repo
  scope=/docs/team/**
  at=2026-10-02T00:10:00Z
  epoch=2
```

Delegation may narrow scope and duration.

It may not broaden action, resource, or scope.

### Revocation

```text
× [R1] revoke
  target=[P1]
  by=human_owner
  at=2026-10-02T01:00:00Z
  epoch=3
```

v0.4 uses a restricted revocation rule: the root grantor revokes.

### Replay

```text
→ [Y1] replay
  target=[H1]
  authority=[D1]
  at=2026-10-02T01:10:00Z
  epoch=3
```

Replay is valid only if the referenced authority is active at replay time and the authority-state epoch is current.

## Core invariants

```text
delegation <= parent authority
```

```text
root revoked
→ descendants inactive
```

```text
child revoked
≠ parent revoked
```

```text
expired authority
≠ active authority
```

```text
new grant after revocation
≠ old grant resurrected
```

The new grant gets a new semantic ID.

## Authority epoch

Every authority mutation carries a positive epoch:

```text
grant       epoch=1
delegate    epoch=2
revoke      epoch=3
```

Epochs are monotonic with authority mutation time.

A replay records the authority epoch it believes is current.

## Critical limitation discovered in Round 4

A static document cannot detect a revocation that is completely absent from that document.

Example:

```text
stale snapshot:
  grant epoch=1
```

If a newer runtime state contains:

```text
revoke epoch=2
```

the stale snapshot alone has no way to know this.

Therefore Bridge-0 requires an **external current-authority epoch check** at execution time:

```text
local authority epoch
must equal
runtime authority epoch
```

This is a boundary between language semantics and runtime state.

The language can make stale authority detectable only if the runtime supplies authoritative freshness.

## New validator rules

```text
V026 lifecycle epoch validity/order
V027 lifecycle timestamp validity
V028 grant integrity
V029 delegation parent/holder validity
V030 delegation non-broadening
V031 revocation validity
V032 inactive-authority replay rejection
V033 external stale-snapshot detection
V034 replay epoch mismatch
```

## Scope

v0.4 scope containment is intentionally restricted to absolute path-like scopes.

Examples:

```text
/**           contains /docs/**
/docs/**      contains /docs/team/**
/docs/team/** does not contain /docs/**
```

This is a prototype containment model, not a general authorization language.

## Non-goals

v0.4 does not claim to implement:

- cryptographic capability tokens;
- distributed revocation;
- authentication;
- legal authorization;
- secure production execution;
- complete access-control policy languages.

The test objective remains semantic integrity.
