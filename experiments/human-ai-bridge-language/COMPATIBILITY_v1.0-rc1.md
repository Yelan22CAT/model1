# Bridge-0 Compatibility Contract — v1.0-rc1 Candidate

> **Experimental / Not Production Ready**

## Default

Compatibility is explicit, scoped, content-bound, and fail-closed.

## Rules

- Same version label is not proof of semantic compatibility.
- Same epoch is not proof of same history/content.
- Mixed semantic generations require an explicit trusted compatibility/migration contract.
- Context transition proofs bind exact source and target contexts.
- Transition compatibility is non-transitive by default.
- Transition chains consume a Compatibility Budget rooted in a trusted context.
- Budget reset requires Fresh Root Revalidation.
- Fresh Root Revalidation does not transfer unrelated authorization/replay/risk budgets.
- Cross-tenant, cluster, environment, subject, operation, and resource identity substitutions fail closed unless explicitly authorized.
- Lossy migrations require explicit scoped acknowledgement and authorization.
- Unknown critical fields fail closed.
- Old receipts are reusable only when all decision-critical dependencies remain compatible/current.

## Terminal trust boundary

`EXTERNAL_TRUST_BOOTSTRAP_REQUIRED` is not a compatibility failure. It is a terminal automatic trust-bootstrap state.

When all independent trust anchors are unavailable, Bridge must fail closed and require an externally governed trust bootstrap. A post-bootstrap system begins a new trust era rather than claiming uninterrupted trust continuity.