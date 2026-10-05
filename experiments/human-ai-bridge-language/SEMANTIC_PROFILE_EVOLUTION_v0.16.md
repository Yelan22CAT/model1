# Bridge-0 Semantic Profile Evolution v0.16

> Status: Experimental / compatibility-handshake layer

## Purpose

v0.15 proved that Bridge can pin a semantic profile above runtime Unicode
versions.

v0.16 asks the next question:

> What happens when the Bridge semantic profile itself changes?

The canonical source declares:

~~~text
domain=grapheme
profiles=grapheme_v1,grapheme_v2,grapheme_v3_breaking
policy=behavioral_manifest
migration=explicit
~~~

The compatibility decision is based on observable semantic behavior, not only
on a version string.

## Synthetic profile fixtures

The v0.16 profile fixtures are deliberately small and synthetic.

They are not claims about Unicode-standard version history.

### grapheme_v1

~~~text
version = 1.0.0
~~~

Defines three existing behaviors.

### grapheme_v2

~~~text
version = 1.1.0
~~~

Preserves every v1 behavior and adds one new vector.

Result:

~~~text
relation = backward_compatible_extension
exchange_allowed = true
migration_required = false
~~~

### grapheme_v3_breaking

~~~text
version = 1.2.0
~~~

Intentionally changes an already-defined v1 behavior while keeping the same
major version.

Result:

~~~text
semver_same_major_claim = true
relation = breaking
exchange_allowed = false
migration_required = true
~~~

This is an adversarial fixture designed to prove that a compatible-looking
version label cannot override a behavioral incompatibility.

## Behavioral manifest

Compatibility is computed from:

~~~text
added semantic vectors
removed semantic vectors
changed semantic vectors
~~~

Rules:

~~~text
removed or changed
→ breaking
→ exchange denied
→ explicit migration required

only added
→ backward-compatible extension
→ exchange allowed

no difference
→ equivalent
~~~

## Cross-language result

Generated Python 3.12 and Node.js 20 backends produced the same typed
compatibility manifest:

~~~text
BRIDGE_TYPED_EQUIVALENT
sha256=20fd68bc27a33a3ad2ae3390e1d0f396712c2e0aafcd21029064a5a45f09f072
~~~

## Negative control

An intentionally unsafe backend used only the major version number.

Because all three fixtures use major version 1, that backend incorrectly allowed
the breaking v3 profile.

Its observable digest was:

~~~text
4826d5227bac1dd6246baae97197a2e455b83f230df59a22c5eca49315c03acb
~~~

and Bridge rejected it as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

## New validator rules

~~~text
V100 compatibility executable subset integrity
V101 exact backend target set
V102 compatibility domain / task validity
V103 pinned profile set
V104 behavioral policy / explicit migration contract
V105 compatibility field allowlist
~~~

## Main finding

Semantic version labels are metadata.

They are not proof of semantic compatibility.

~~~text
same major version
!= same executable meaning
~~~

Bridge therefore makes compatibility an explicit semantic handshake:

~~~text
profile A
+
profile B
+
behavioral manifest
        ↓
compatible / migration required / reject
~~~

## Boundary

v0.16 compares small bounded profile manifests.

A production design would need cryptographic profile identifiers, canonical
manifest hashing, signed migration descriptions, dependency closure,
transitive-compatibility rules, rollback semantics, and multi-profile
negotiation.
