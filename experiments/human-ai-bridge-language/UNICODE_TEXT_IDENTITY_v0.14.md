# Bridge-0 Unicode Text Identity Semantics v0.14

> Status: Experimental / explicit text-identity semantic constitution

## Purpose

v0.12 and v0.13 established that Bridge numeric meaning must not be inherited
silently from backend defaults.

v0.14 applies the same principle to text.

Visually identical text can have different Unicode scalar sequences.

Example:

~~~text
é

U+00E9
vs
U+0065 U+0301
~~~

Raw sequence equality would treat them as different.

The v0.14 canonical source therefore declares:

~~~text
text_model=unicode_scalar
normalization=NFC
identity=normalized_scalar_sequence
~~~

## Canonical identity rule

For this prototype:

~~~text
text A == text B
iff
NFC(scalar_sequence(A)) == NFC(scalar_sequence(B))
~~~

Backend raw storage is not the identity rule.

## Conformance vectors

The test set includes:

~~~text
00E9
0065+0301

00C5
0041+030A
212B

AC00
1100+1161

0065+0323+0301
0065+0301+0323

1F600
1F469+200D+1F4BB
~~~

These cover:

- composed vs decomposed Latin text;
- canonical-equivalent Angstrom forms;
- Hangul composition;
- combining-mark canonical reordering;
- supplementary-plane scalar values;
- a multi-scalar emoji ZWJ sequence.

## Backend lowering

### Python 3.12

Bridge scalar tokens are decoded with scalar-value construction and normalized
with Unicode NFC before being re-encoded as canonical scalar tokens.

### Node.js 20

Bridge scalar tokens are decoded with String.fromCodePoint, normalized with
String.prototype.normalize('NFC'), and enumerated with code-point-aware
iteration rather than UTF-16 code-unit indexing.

## Typed transport

Canonical text identity is transported as an explicit normalized scalar token:

~~~json
{"$unicode_nfc":"00E9"}
~~~

Examples:

~~~text
00E9       -> 00E9
0065+0301  -> 00E9

00C5       -> 00C5
0041+030A  -> 00C5
212B       -> 00C5

AC00       -> AC00
1100+1161  -> AC00
~~~

Combining-mark order is also normalized:

~~~text
0065+0323+0301
0065+0301+0323
        ↓
1EB9+0301
~~~

## Real cross-language result

Generated Python and Node backends both passed.

Canonical typed digest:

~~~text
1c0acbd4243ec0a4bba6a99350c7aa44596cd6b261b16f4f256f09e11d6d6b05
~~~

## Deliberate unsafe backend

A negative-control Node backend intentionally treats the raw scalar sequence as
the identity value and skips NFC normalization.

It produced:

~~~text
0d830bf9185c168995226235317165cdffaefc40e7a32fb378797d9b8ca1ca21
~~~

and was rejected as:

~~~text
HETEROGENEOUS_BACKEND_DRIFT
~~~

This demonstrates that raw code-point sequence equality does not satisfy the
declared Bridge text identity contract.

## Validator rules

~~~text
V089 Unicode executable subset integrity
V090 exact target-set validity
V091 text operation cardinality / operation validity
V092 text model + normalization + identity contract
V093 scalar-token and conformance-vector validity
~~~

The validator rejects:

- missing normalization policy;
- backend-default normalization;
- raw-sequence identity;
- lowercase/non-canonical scalar notation;
- surrogate code points;
- code points above U+10FFFF;
- duplicate conformance tokens;
- missing required edge vectors;
- unsupported fields.

## Important boundary

NFC-normalized scalar-sequence identity is not the same thing as
user-perceived-character identity.

For example:

~~~text
1F469+200D+1F4BB
~~~

is multiple Unicode scalar values but may render as one grapheme-like visual
unit.

Therefore:

~~~text
normalized scalar identity
!= grapheme-cluster identity
!= visual identity
!= linguistic identity
~~~

v0.14 intentionally defines only the first of those.

A second boundary is Unicode-version dependence. The current prototype relies
on the Unicode data shipped with Python 3.12 and Node.js 20. A production
semantic constitution should pin or attest the Unicode version instead of
assuming runtime versions remain aligned.
