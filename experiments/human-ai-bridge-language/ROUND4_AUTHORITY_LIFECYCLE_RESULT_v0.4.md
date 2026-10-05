# Bridge-0 Round 4 — Delegation / Revocation / Expiry / Replay Result

> Status: Experimental v0.4

## Latest executed CI result

```text
78 tests
78 passed
0 failed
```

Earlier v0.2 and v0.3 end-to-end demos also remained green.

## New tested cases

Round 4 adds tests for:

- grant round-trip;
- narrow delegation;
- broader-scope delegation rejection;
- action-changing delegation rejection;
- delegated authority outliving parent rejection;
- root revocation cascading to descendants;
- child revocation not revoking parent;
- historical replay before revocation;
- replay after revocation rejection;
- stale replay epoch rejection;
- expired authority rejection;
- wrong revoker rejection;
- external epoch check for stale snapshots;
- explicit new grant after revocation;
- 20-level delegation chain followed by root revocation.

## Stress result

A 20-level delegation chain was created.

After revoking the root grant, the deepest delegated authority evaluated inactive.

This tests transitive revocation rather than only one parent-child edge.

## Important discovery

The language/runtime pair can detect:

```text
revoked authority reused in a complete authority history
```

and:

```text
stale replay epoch inside a complete authority history
```

But a stale document that omits the newer revocation can still look internally valid.

Therefore:

```text
static Bridge document
alone
≠
fresh authority state
```

A runtime freshness check is required.

The prototype adds an optional external `expected_epoch` check for this boundary.

## Bounded conclusion

Within the current restricted v0.4 model, the tested delegation, narrowing, expiry, revocation, replay, and transitive-revocation rules behaved deterministically and passed all current tests.

This does not establish production authorization security or complete hallucination prevention.

## Next frontier

The next higher-value tests should target **concurrency and split-brain state**:

```text
two agents
→ different authority snapshots
→ simultaneous actions
→ later reconciliation
```

Questions:

- What if two branches both think they have the latest epoch?
- What if revocation and action occur at nearly the same time?
- What if two authority histories diverge?
- Which state is authoritative after merge?
- Can conflict remain explicit instead of being silently resolved?

That is the next natural stress layer.
