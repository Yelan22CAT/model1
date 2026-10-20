# Bridge-0 Round 3 — Authority, Scope, Handoff, Provenance Result

> Status: Experimental v0.3  
> Scope: deterministic semantic-contract tests only.

## Test objective

Round 3 asks:

> Can authority, scope, provenance, and state survive composition across agents without silently broadening or mutating?

The test stack now includes structured:

- permission tuples;
- agent handoffs;
- guarded state transitions;
- provenance edges;
- validity windows;
- version/time preservation.

## Latest verified CI result

```text
63 tests
63 passed
0 failed
v0.2 end-to-end demo: passed
v0.3 composed authority/provenance demo: passed
```

## New invariants tested

### Permission does not broaden silently

```text
permission(agent, read, repo, /docs/**)
≠
permission(agent, write, repo, /docs/**)
≠
permission(agent, read, repo, /**)
```

Changing action or scope changes canonical semantics.

A handoff does not create a new permission for the receiving agent.

### Handoff preserves epistemic state

```text
△ [C1]
→ handoff
→ handoff
→ ...
```

remains:

```text
△ [C1]
```

The suite includes a 50-handoff chain.

### Handoff preserves provenance

v0.3 rejects:

```text
provenance=reset
```

for a normal handoff.

A transformed claim must receive a new claim ID plus an explicit provenance record.

### Irreversible transition requires guard + authority

```text
irreversible=true
→ guard reference required
→ guard must actually be a guard
→ explicit authority required
```

Removing authority or pointing `when=` at an ordinary claim is rejected.

### Provenance must remain acyclic

```text
C2 derived_from C1
C1 derived_from C2
```

is rejected as a provenance cycle.

### Conflicts survive handoff

Supporting and opposing evidence remain conflicting after agent handoff.

The receiving agent does not inherit permission to resolve the conflict merely because it received the claim.

### Superseded source is not erased

Version replacement preserves historical addressability.

```text
source_v2 supersedes source_v1
```

does not delete `source_v1`.

### Large structured sets remain separate

The suite includes 100 distinct permission tuples and verifies they do not merge into a generic shared permission.

## Current bounded conclusion

The current evidence supports:

> Within the tested restricted v0.3 grammar, authority, scope, provenance, epistemic state, and guarded-transition distinctions survived the tested deterministic compositions and adversarial mutations.

This does not establish:

- production authorization security;
- identity/authentication correctness;
- cryptographic capability enforcement;
- complete hallucination elimination;
- safe autonomous execution;
- general language completeness.

## Next likely frontier

The next difficult layer is **delegation and revocation over time**:

```text
grant
→ delegate
→ narrow
→ revoke
→ expire
→ retry / replay
```

That layer should test whether stale or revoked authority can reappear through old context, old handoffs, cached artifacts, or replayed instructions.

That is a different problem from simple permission preservation and should be treated as a separate round.
