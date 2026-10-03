# Bridge-0 Semantic Migration & Loss Audit v0.17

> Status: Experimental / executable migration layer

## Purpose

v0.16 introduced explicit semantic-profile compatibility.

v0.17 moves beyond detection and tests actual migration.

The central rule is:

~~~text
successful conversion
!=
lossless semantic migration
~~~

A migration may technically produce a target artifact while silently dropping
meaning.

Therefore Bridge requires:

~~~text
loss_policy=reject_unacknowledged
roundtrip=audit
execution=gate_on_audit
~~~

## Source artifact

The bounded fixture contains more than its core grapheme clusters.

It also carries:

- stable unit IDs;
- semantic labels;
- verification state;
- provenance;
- human-facing notes.

Those fields are intentionally part of the semantic artifact.

## Route 1 — lossless v1 -> v2

The first route changes only the profile identifier.

Round-trip back to v1 reproduces the original artifact.

Result:

~~~text
conversion_success = true
roundtrip.recovered_source = true
loss.lossless = true
lost_paths = []
execution_allowed = true
~~~

## Route 2 — compact v1 -> v3

The second route converts the artifact into a compact cluster-only form.

The conversion itself succeeds.

However, it discards semantic information:

~~~text
$.units[*].id
$.units[*].label
$.units[*].confidence
$.provenance
$.notes
~~~

Round-trip reconstruction cannot recover the source artifact.

Result:

~~~text
conversion_success = true
roundtrip.recovered_source = false
loss.lossless = false
execution_allowed = false
~~~

This is the intended behavior.

## Cross-language result

Generated Python 3.12 and Node.js 20 migration backends produced the same typed
audit manifest:

~~~text
BRIDGE_TYPED_EQUIVALENT
sha256=d4c7412b49ccb2adc69fed4f2f66828f4fa7af81acb39ae2c0ab7c6a94c7b69f
~~~

## Negative control

An intentionally unsafe backend treated conversion success as sufficient
permission and skipped round-trip auditing.

It incorrectly allowed the lossy compact route.

Unsafe digest:

~~~text
17819b0242b4e01051526179dda4a592a2e7cf646c1b8c2e45e08b384bb2c384
~~~

Bridge rejected it as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

## New validator rules

~~~text
V106 migration executable subset integrity
V107 exact backend target set
V108 migration domain/task validity
V109 source artifact and route-set validity
V110 loss / round-trip / execution-gate policy
V111 migration field allowlist
~~~

## Main finding

A successful translator is not automatically a safe migrator.

Bridge therefore separates:

~~~text
conversion success
loss audit
round-trip recovery
execution permission
~~~

These are distinct states.

## Boundary

v0.17 uses one bounded fixture and two deterministic migration routes.

A production migration system would still need:

- schema-level field ownership;
- typed loss classes;
- lossy migration acknowledgement;
- reversible migration proofs;
- migration signatures;
- dependency migration;
- transactional rollback;
- partial-failure handling;
- multi-hop migration planning.
