# Bridge-0 Revocation and Replay Resistance v0.19

> Status: Experimental / stateful authorization layer

## Purpose

v0.18 introduced scoped authorization for a known lossy migration.

v0.19 adds state that can invalidate an otherwise well-formed authorization.

New fields:

~~~text
authorization_id
nonce
revocation_epoch
usage=single_use
~~~

These are evaluated together with the earlier bindings:

~~~text
loss acknowledgement
authority
scope
artifact digest
provenance
time window
~~~

## State model

The prototype tracks:

~~~text
used_authorization_ids
used_nonces
revoked_authorization_ids
current_revocation_epoch
~~~

A successful use records both the authorization ID and nonce as consumed.

## Decision rule

Permission requires all checks to pass:

~~~text
token identity matches
nonce matches
known loss is acknowledged
authority and scope match
artifact and provenance match
time window is valid
revocation epoch is current
authorization ID is not revoked
authorization ID is unused
nonce is unused
usage policy is single_use
~~~

If any check fails, the default result is deny.

## Verified scenarios

~~~text
first_use                -> allow
replay_same_token        -> deny
revoked_before_use       -> deny
stale_revocation_epoch   -> deny
tampered_nonce           -> deny
expired_token            -> deny
~~~

A denied attempt does not consume the nonce.

## Cross-language result

Python 3.12 and Node.js 20 produced the same typed state-transition result:

~~~text
sha256=a1f1665730eff44b91546842afd1d16c82491c724bac88822fc4176e26487389
~~~

## Negative control

A deliberately stateless implementation ignored consumed-token state,
revocation state, and epoch freshness.

It produced:

~~~text
d94930809c49ed4f204c041db954b51700f23d324a114855bc7f6d00fe777734
~~~

and the semantic comparator rejected the mismatch.

## Validator rules

~~~text
V121 executable subset integrity
V122 backend target set
V123 single-use authorization task validity
V124 artifact and route binding
V125 authorization ID and nonce format
V126 exact loss acknowledgement
V127 authority, scope, and provenance binding
V128 artifact digest binding
V129 revocation epoch and usage policy
V130 canonical time and observable contract
V131 field allowlist
~~~

## Boundary

This is a deterministic prototype. The state is not yet durable or distributed,
and concurrent use is not yet covered.

The next test should make two workers attempt the same single-use authorization
at the same time and require exactly one successful transition.
