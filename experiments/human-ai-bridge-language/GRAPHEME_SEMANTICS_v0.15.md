# Bridge-0 Grapheme Semantics v0.15

> Status: Experimental / pinned Unicode semantic profile

## Purpose

v0.14 defined text identity as NFC-normalized Unicode scalar identity.

v0.15 separates that machine representation from a bounded human-facing grapheme unit.

The canonical source declares:

~~~text
unicode_version=15.0
text_model=unicode_scalar
normalization=NFC
segmentation=extended_grapheme_cluster
profile=bridge_uax29_subset_v1
~~~

## Important real-world failure

The first v0.15 implementation required the backend runtime Unicode version to match the semantic version exactly.

Python 3.12 reported:

~~~text
15.0.0
~~~

Node.js 20 reported:

~~~text
17.0
~~~

The Node backend therefore failed.

This was not treated as a reason to silently change Bridge semantics to Unicode 17.0.

Instead, the compiler architecture was changed.

## Pinned semantic profile

The fixed v0.15 design carries a bounded Bridge-owned Unicode 15.0 profile into both generated backends.

Runtime versions are observed and logged, but are not authoritative for the semantic result.

Observed runtime logs:

~~~text
Python: runtime=15.0.0 semantic=15.0 mode=pinned_subset
Node:   runtime=17.0   semantic=15.0 mode=pinned_subset
~~~

Both backends execute the same bounded normalization and grapheme rules from the Bridge profile.

## Conformance vectors

The v0.15 profile is intentionally limited to an explicit test set:

~~~text
0065+0301
1F44D+1F3FD
1F469+200D+1F4BB
1F1E8+1F1E6
0061+0308+0062
1F468+200D+1F469+200D+1F467+200D+1F466
000D+000A+0061
2764+FE0F
~~~

These cover combining-mark composition, emoji skin-tone modifiers, emoji ZWJ sequences, regional-indicator flags, composed text followed by another scalar, family ZWJ sequences, CRLF behavior, and variation selectors.

## Example distinction

~~~text
1F469+200D+1F4BB
~~~

contains three Unicode scalars but is one grapheme in the v0.15 profile.

So:

~~~text
scalar_count != grapheme_count
~~~

Likewise:

~~~text
0061+0308+0062
~~~

normalizes to:

~~~text
00E4+0062
~~~

and segments as two graphemes:

~~~text
[00E4] [0062]
~~~

## Cross-language result

The generated Python and Node backends produced the same typed semantic observable:

~~~text
BRIDGE_TYPED_EQUIVALENT
sha256=29043ba727215e0bfea405d6b322206bbbed93aa261df0882bf65b7f68262004
~~~

## Negative control

An intentionally unsafe backend counted Unicode code points as if they were graphemes.

It produced:

~~~text
5f5a27bd1a4284f94cb5e0990aac0a5c012905a0d50ef29bc796502fc82a907c
~~~

and was rejected as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

## Validator rules

~~~text
V094 grapheme executable subset integrity
V095 exact target-set validity
V096 pinned Unicode semantic version
V097 grapheme operation validity
V098 text / normalization / segmentation / profile contract
V099 bounded conformance-vector validity
~~~

## Main finding

v0.15 adds an important versioning rule:

~~~text
runtime Unicode version
!= semantic Unicode version
~~~

A backend may run a newer or different Unicode implementation, but Bridge semantics remain pinned unless the semantic profile itself is explicitly upgraded.

## Boundary

bridge_uax29_subset_v1 is not a complete implementation of Unicode UAX #29.

It is a bounded executable semantic profile for the listed vectors.

A production-grade Bridge text system would need complete pinned Unicode property tables, a complete versioned grapheme algorithm, versioned conformance data, compatibility rules for Unicode upgrades, and separate locale and linguistic layers.

The current result proves the architecture, not full Unicode coverage.
