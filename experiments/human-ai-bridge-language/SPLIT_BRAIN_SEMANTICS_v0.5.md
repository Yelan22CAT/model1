# Bridge-0 Split-Brain Semantics v0.5

> Status: Experimental / concurrency stress layer  
> v0.5 adds no new glyphs.

## Purpose

v0.4 established a lifecycle for authority.

v0.5 asks what happens when two agents or replicas act from the same parent state and produce different next states.

The design target is:

```text
concurrency
→ divergence
→ explicit conflict
→ explicit merge
→ trusted finality
→ execution
```

not:

```text
concurrency
→ last writer wins
→ silent overwrite
```

## Snapshot

```text
○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority state_hash=ha at=...
```

A sibling snapshot is considered divergent when it shares:

- parent;
- sequence;
- domain;

but has a different `state_hash`.

Equivalent sibling snapshots with the same state hash do not require a conflict.

## Conflict

```text
◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open
```

A real divergence must be explicitly declared.

A fake conflict between semantically identical siblings is rejected.

## Merge

```text
→ [M1] merge left=[SA] right=[SB] conflict=[CF1] strategy=explicit result_hash=hm at=...
```

v0.5 permits only:

```text
strategy=explicit
```

Automatic last-writer-wins is rejected.

## Finality

```text
✓ [F1] final target=[M1] by=control_plane term=1 at=...
```

A divergent branch snapshot cannot be finalized directly.

Finality must be issued by the configured trusted finalizer.

Finality terms must be positive, unique, and monotonic with finality time.

## Execution

```text
→ [X1] execute actor=agent_a action=deploy state=[M1] finality=[F1] at=...
```

Execution requires a finality record that targets the exact state being used.

Execution cannot precede finality.

## New validator rules

```text
V035 snapshot lineage / sequence validity
V036 divergence must be explicit
V037 conflict validity
V038 merge parent/conflict validity
V039 last-writer-wins rejection
V040 trusted finalizer
V041 divergent branch cannot finalize directly
V042 execution requires matching finality
V043 finality term validity/order
```

## Important scaling issue discovered

The current conflict representation is pairwise.

For `n` mutually divergent siblings:

```text
conflicts = n(n-1)/2
```

The stress test used 12 divergent branches:

```text
12 branches
→ 66 pairwise conflicts
```

This passed, but the representation scales as O(n²).

That is acceptable for a stress prototype, not for a mature distributed language.

A later version should test a first-class conflict-set representation rather than requiring every pair to be declared individually.

## Boundary

Bridge-0 v0.5 does not implement distributed consensus.

It only prevents the language layer from silently pretending that divergent states are one state.

Consensus / authoritative finality still belongs to an external control plane or protocol.
