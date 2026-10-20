# Bridge-0 Binary64 Floating Semantics v0.13

> Status: Experimental / explicit floating-point semantic constitution

## Purpose

v0.13 deliberately tests floating-point meanings that backend languages and JSON can treat differently.

The canonical source now declares:

~~~text
numeric=binary64
rounding=ties_to_even
~~~

The conformance vector contains:

~~~text
nan
+inf
-inf
-0
+0
2.5
3.5
-2.5
-3.5
~~~

## Canonical rules

For this prototype:

~~~text
binary64 = IEEE-754 binary64 value domain
ties_to_even = a half-way value rounds to the even integer
~~~

Examples:

~~~text
 2.5 ->  2
 3.5 ->  4
-2.5 -> -2
-3.5 -> -4
~~~

Bridge also preserves NaN, positive infinity, negative infinity, positive zero and negative zero as distinct semantic classes.

## Backend lowering

Python lowers binary64 to Python float and uses its matching ties-to-even round behavior.

Node lowers binary64 to JavaScript Number, but the compiler generates an explicit roundTiesToEven function instead of inheriting Math.round behavior.

## Typed transport

Exceptional values and signed zero use tagged values:

~~~json
{"$binary64":"nan"}
{"$binary64":"+inf"}
{"$binary64":"-inf"}
{"$binary64":"+0"}
{"$binary64":"-0"}
~~~

Rounded integral results use the existing exact-integer transport.

## Verified result

The generated Python 3.12 and Node.js 20 backends produced the same typed observable:

~~~text
BRIDGE_TYPED_EQUIVALENT
sha256=c69af06968a78f866e35c797333f82149670d399f048b37614a9150babbfad73
~~~

## Unsafe-backend negative control

An intentionally unsafe Node implementation used backend defaults: Math.round plus raw JSON floating values.

It produced:

~~~text
8b0ed6dda5f8894207fb0274b1e79a43eb8d5c602dd78dda23cfaf24f9d140db
~~~

and was rejected as HETEROGENEOUS_BACKEND_DRIFT.

The unsafe path exposed real differences:

- NaN and infinities collapse to null under JSON stringification.
- Negative zero collapses to ordinary zero.
- Math.round(2.5) gives 3 instead of ties-to-even 2.
- Math.round(-3.5) gives -3 instead of ties-to-even -4.

## Validator rules

~~~text
V084 float executable subset integrity
V085 exact target-set validity
V086 operation cardinality / operation validity
V087 numeric + rounding + observable contract
V088 edge-vector and canonical-token validity
~~~

## Main finding

Backend language behavior is not the canonical Bridge meaning.

The compiler may use native behavior when it preserves the Bridge contract, but must synthesize preserving behavior when it does not.

## Boundary

This is not a complete IEEE-754 specification. NaN payloads, signaling NaN, subnormals, overflow, underflow, fused operations, all rounding modes and transcendental functions remain outside v0.13.
