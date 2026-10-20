# Bridge-0 Round 19 — Single-Use Authorization Result

> Status: Experimental v0.19

## Verified test gates

Cumulative regression suite:

~~~text
322 tests
322 passed
0 failed
~~~

Dedicated v0.19 suite:

~~~text
24 tests
24 passed
0 failed
~~~

## Cross-language result

Python 3.12 and Node.js 20 produced the same typed state-transition result.

~~~text
sha256=a1f1665730eff44b91546842afd1d16c82491c724bac88822fc4176e26487389
~~~

Verified scenarios:

~~~text
first_use                allow
replay_same_token        deny
revoked_before_use       deny
stale_revocation_epoch   deny
tampered_nonce           deny
expired_token            deny
~~~

The first successful use records the authorization ID and nonce as consumed.
A second use of the same pair is rejected.

## Negative control

A deliberately stateless implementation ignored used-token state, revocation
state, and revocation-epoch freshness.

Its digest was:

~~~text
d94930809c49ed4f204c041db954b51700f23d324a114855bc7f6d00fe777734
~~~

The comparator detected semantic drift.

## Main result

v0.19 adds a stateful lifecycle:

~~~text
issued -> valid -> consumed -> replay denied
issued -> revoked -> denied
stale epoch -> denied
~~~

## Boundary

This prototype uses deterministic in-memory fixture state. It does not yet
cover durable atomic storage, concurrent redemption, signed credentials, or
distributed revocation services.

## Next frontier

The next high-value test is concurrency-safe redemption:

~~~text
two agents
+
same single-use authorization
+
same time
        ↓
atomic compare-and-consume
        ↓
exactly one successful transition
~~~
