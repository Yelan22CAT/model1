# Bridge-0 Scoped Known-Loss Authorization v0.18

> Status: Experimental / conditional authorization layer

## Purpose

v0.17 established that a conversion can succeed while still losing semantic
information.

v0.18 asks the next question:

> Can a known lossy migration be permitted without turning acknowledgement into
> blanket permission?

The answer in this bounded prototype is yes, but only when all authorization
bindings match.

## Canonical authorization fields

The source explicitly declares:

~~~text
loss_ack
authority
scope
artifact_digest
provenance
issued_at
expires_at
evaluate_at
~~~

The tested policy is:

~~~text
known loss only
+
exact loss manifest acknowledgement
+
authorized principal
+
exact scope
+
artifact digest binding
+
authority provenance binding
+
valid time window
        ↓
conditional execution permission
~~~

## Bound loss manifest

The authorization acknowledges exactly the loss previously found in v0.17:

~~~text
$.units[*].id
$.units[*].label
$.units[*].confidence
$.provenance
$.notes
~~~

Partial acknowledgement is insufficient.

Additional future loss is not covered.

## Artifact binding

The authorization is bound to the exact v0.17 source fixture by SHA-256:

~~~text
07b88b41d6be837f8b370c27523053bf84b214eef0bc1d074633e1250db2db92
~~~

Changing the artifact invalidates the authorization.

## Scope

The tested scope is:

~~~text
scope=exact_loss_manifest
~~~

The authority does not grant permission for unrelated or future losses.

## Time window

The conformance fixture uses a deterministic half-open window:

~~~text
issued_at  = 2026-10-02T12:00:00Z
expires_at = 2026-10-02T13:00:00Z

valid iff:
issued_at <= evaluate_at < expires_at
~~~

The fixed timestamps are test-fixture data, not a claim that production
authorization should use hard-coded wall-clock values.

At exactly the expiry boundary, permission is denied.

## Cross-language scenarios

Both Python 3.12 and Node.js 20 evaluate the same scenarios:

~~~text
authorized_exact  -> allow
expired_replay    -> deny
wrong_artifact    -> deny
partial_ack       -> deny
wrong_scope       -> deny
wrong_authority   -> deny
~~~

Canonical typed result:

~~~text
BRIDGE_TYPED_EQUIVALENT
sha256=625a612b4c150fbb6d3e47394d423710fa05d6c1a299d005dbb97d5248352812
~~~

## Negative control

An intentionally unsafe backend treats the authority label alone as sufficient
permission.

It therefore incorrectly allows expired, wrong-artifact, partial-ack and
wrong-scope scenarios.

Unsafe digest:

~~~text
e59021983cd5b1cf7ff383ad7765d9045d0ae5aa254c0ef675c76265792d833a
~~~

Bridge rejects that result as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

## New validator rules

~~~text
V112 authorization executable subset integrity
V113 exact backend target set
V114 authorization domain/task validity
V115 exact artifact + route binding
V116 exact loss acknowledgement
V117 authority + scope + provenance binding
V118 artifact digest binding
V119 canonical time + observable contract
V120 authorization field allowlist
~~~

## Main finding

Acknowledgement is not permission by itself.

Authority is not permission outside its scope.

A valid authorization is a conjunction:

~~~text
acknowledgement
AND authority
AND scope
AND artifact binding
AND provenance
AND time validity
~~~

If any term fails, the default result is deny.

## Important boundary

The current authority and provenance values are bounded fixture identifiers.

v0.18 does not yet provide:

- cryptographic signatures;
- real identity attestation;
- revocation lists;
- delegated authority chains;
- trusted clocks;
- nonce / replay protection;
- distributed authorization consensus.

Those are separate future layers.
