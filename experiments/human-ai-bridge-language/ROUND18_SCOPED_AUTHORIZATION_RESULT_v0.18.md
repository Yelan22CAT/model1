# Bridge-0 Round 18 — Scoped Known-Loss Authorization Result

> Status: Experimental v0.18

## Verified test gates

Cumulative regression suite:

~~~text
298 tests
298 passed
0 failed
~~~

Dedicated v0.18 suite:

~~~text
23 tests
23 passed
0 failed
~~~

All previous end-to-end gates remained green.

## Real generated workflow

~~~text
Python 3.12 authorization backend  ✓
Node.js 20 authorization backend  ✓
typed semantic comparison         ✓
~~~

Canonical digest:

~~~text
625a612b4c150fbb6d3e47394d423710fa05d6c1a299d005dbb97d5248352812
~~~

## Authorized exact-known-loss case

The exact v0.17 loss manifest was acknowledged by the bound authority for the
bound artifact, exact scope and valid time window.

Result:

~~~text
decision = authorized_known_loss
execution_allowed = true
~~~

## Denied adversarial cases

The same authorization machinery denied:

~~~text
expired replay
wrong artifact digest
partial loss acknowledgement
over-broad scope
wrong authority
~~~

The expiry interval is half-open, so evaluation exactly at expires_at is denied.

## Negative control

An intentionally unsafe backend treated authority=fixture_owner as sufficient
permission and ignored scope, artifact binding, loss completeness and expiry.

Unsafe digest:

~~~text
e59021983cd5b1cf7ff383ad7765d9045d0ae5aa254c0ef675c76265792d833a
~~~

It was rejected as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

## Main result

v0.18 connects the earlier authority architecture to semantic migration.

The execution gate is now:

~~~text
known loss
+
explicit acknowledgement
+
authority
+
scope
+
artifact binding
+
provenance
+
time window
        ↓
conditional permission
~~~

This is stronger than both extremes:

~~~text
all lossy migration forbidden
~~~

and:

~~~text
authority present -> allow everything
~~~

## Bounded conclusion

The evidence supports:

> For the bounded v0.18 fixture, Bridge allowed one explicitly acknowledged,
> artifact-bound, scoped and time-valid lossy migration while denying replay,
> artifact mismatch, incomplete acknowledgement, over-broad scope and wrong
> authority consistently across Python and Node.

This is not yet cryptographic authorization.

## Next frontier

The next high-value layer is revocation and replay resistance:

~~~text
authorization token
+
nonce / authorization ID
+
revocation state
+
trusted freshness evidence
        ↓
single-use / revocable permission
~~~

That would test whether an authorization that was valid once can later be
reliably withdrawn or prevented from being replayed.
