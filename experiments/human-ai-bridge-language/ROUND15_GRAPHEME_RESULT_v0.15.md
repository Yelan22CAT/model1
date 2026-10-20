# Bridge-0 Round 15 — Pinned Unicode Grapheme Result

> Status: Experimental v0.15

## Latest verified result

~~~text
243 tests
243 passed
0 failed
~~~

All earlier end-to-end gates remained green.

## Real generated workflow

~~~text
Python 3.12 grapheme backend  ✓
Node.js 20 grapheme backend  ✓
typed semantic comparison    ✓
~~~

Canonical digest:

~~~text
29043ba727215e0bfea405d6b322206bbbed93aa261df0882bf65b7f68262004
~~~

## Reality-triggered failure

The first version failed because the runtime Unicode versions were different:

~~~text
Python 3.12 -> Unicode 15.0.0
Node.js 20  -> Unicode 17.0
~~~

The initial strict runtime-version check rejected Node.

The design was then corrected so runtime Unicode data is observational, while the bounded Bridge Unicode 15.0 semantic profile is carried by the compiler.

## Verified runtime logs after correction

~~~text
BRIDGE_UNICODE_RUNTIME runtime=15.0.0 semantic=15.0 mode=pinned_subset
BRIDGE_UNICODE_RUNTIME runtime=17.0 semantic=15.0 mode=pinned_subset
~~~

Despite runtime-version drift, both backends produced the same Bridge semantic result.

## Negative control

A code-point-counting backend was deliberately substituted for grapheme semantics.

It produced:

~~~text
5f5a27bd1a4284f94cb5e0990aac0a5c012905a0d50ef29bc796502fc82a907c
~~~

and was correctly rejected as HETEROGENEOUS_BACKEND_DRIFT.

## New tested behaviors

Round 15 covers mandatory Unicode semantic version, rejection of the wrong semantic version, mandatory grapheme segmentation contract, a versioned Bridge grapheme profile, deterministic Python/Node compiler output, generated artifact equality, combining-mark normalization, emoji-modifier clustering, ZWJ clustering, regional-indicator flag clustering, CRLF clustering, variation-selector clustering, code-point-vs-grapheme drift detection, runtime Unicode-version observation, backend-independent semantic source, and rejection of vectors outside the bounded profile.

## Main result

v0.15 demonstrates that Bridge can keep a semantic version stable even when the implementation runtimes carry different Unicode versions.

~~~text
Bridge semantic version
        ↓
pinned semantic profile
        ↓
compiler
   ┌────┴────┐
Python      Node
15.0.0      17.0 runtime Unicode
   └────┬────┘
        ↓
same Bridge observable
~~~

## Bounded conclusion

The evidence supports:

> For the bounded v0.15 grapheme profile, Bridge preserved one Unicode 15.0 semantic contract across Python and Node even though their runtime Unicode versions differed.

This does not establish complete UAX #29 support.

## Next frontier

The next high-value problem is semantic-version evolution itself:

~~~text
Bridge semantic profile v1
        ↓ upgrade
Bridge semantic profile v2
~~~

Questions to test include backward compatibility, pinned old semantics, migration-difference reporting, and whether two agents using different Bridge semantic versions can detect incompatibility before exchanging executable meaning.
