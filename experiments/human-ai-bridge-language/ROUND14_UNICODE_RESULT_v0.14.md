# Bridge-0 Round 14 — Unicode Text Identity Result

> Status: Experimental v0.14

## Latest verified prototype result

~~~text
225 tests
225 passed
0 failed
~~~

All prior end-to-end gates remained green.

## Real generated workflow

~~~text
Python 3.12 Unicode backend  ✓
Node.js 20 Unicode backend  ✓
typed semantic comparison   ✓
~~~

Canonical digest:

~~~text
1c0acbd4243ec0a4bba6a99350c7aa44596cd6b261b16f4f256f09e11d6d6b05
~~~

## Explicit text semantic rules

The source now declares:

~~~text
text_model=unicode_scalar
normalization=NFC
identity=normalized_scalar_sequence
~~~

## Verified canonical equivalences

~~~text
00E9 == 0065+0301
00C5 == 0041+030A == 212B
AC00 == 1100+1161
0065+0323+0301 == 0065+0301+0323
~~~

The last pair normalizes to:

~~~text
1EB9+0301
~~~

Supplementary-plane scalars and a ZWJ emoji sequence were also preserved with
code-point-aware handling.

## Negative control

The unsafe raw-sequence backend skipped normalization.

It produced:

~~~text
0d830bf9185c168995226235317165cdffaefc40e7a32fb378797d9b8ca1ca21
~~~

instead of:

~~~text
1c0acbd4243ec0a4bba6a99350c7aa44596cd6b261b16f4f256f09e11d6d6b05
~~~

and was correctly rejected as HETEROGENEOUS_BACKEND_DRIFT.

## New tested behaviors

Round 14 covers:

- mandatory Unicode scalar text model;
- mandatory NFC normalization;
- normalized-scalar identity contract;
- composed/decomposed Latin equivalence;
- Angstrom canonical equivalence;
- Hangul composition equivalence;
- combining-mark canonical reordering;
- supplementary-plane scalar handling;
- ZWJ multi-scalar sequence preservation;
- surrogate rejection;
- out-of-range scalar rejection;
- canonical uppercase scalar notation;
- deterministic Python and Node compilers;
- exact generated-artifact equality;
- raw-sequence backend drift detection.

## Main result

v0.14 extends Bridge semantic ownership from numbers into text identity.

The canonical meaning is now:

~~~text
Bridge text identity
-> Unicode scalar sequence
-> NFC normalization
-> normalized scalar equality
~~~

rather than whatever raw string representation a backend happens to use.

## Bounded conclusion

The evidence supports:

> For the tested Unicode normalization vectors, Bridge generated Python and Node
> implementations that produced the same NFC-normalized scalar identity and
> detected drift from a raw-sequence backend.

This does not define grapheme-cluster identity, visual identity, locale-aware
collation, case folding, or full linguistic equivalence.

## Next frontier

Two especially valuable next tests emerged:

1. pin / attest Unicode data version so normalization and segmentation are not
   silently runtime-version dependent;
2. define grapheme-cluster semantics separately from scalar-sequence identity.

Those would test whether Bridge can distinguish machine text representation
from the units humans perceive as characters.
