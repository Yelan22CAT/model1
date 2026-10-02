# Bridge-0 Round 12 — Exact Integer Semantic Constitution Result

> Status: Experimental v0.12

## Latest verified prototype result

```text
190 tests
190 passed
0 failed
```

All prior gates remained green.

## Real generated workflow

The v0.12 generated workflow executed:

```text
Python 3.12 exact-integer backend  ✓
Node.js 20 BigInt backend          ✓
typed semantic comparison          ✓
```

Canonical digest:

```text
959d04824492588a4ab0258e593c863d42ba9b98d809afcefc2c7762c2960d69
```

## Deliberate backend-default failure

The same Bridge source was also lowered through an intentionally unsafe
JavaScript Number implementation.

That path produced:

```text
3835dcd02c7e956704c5387f6565f5199964d0342c2bf97207d84517087c64b4
```

The comparator reported:

```text
HETEROGENEOUS_BACKEND_DRIFT
```

This is direct evidence that backend-default numeric semantics are not safe as
the canonical Bridge meaning.

## New semantic rule

The canonical source now includes:

```text
numeric=exact_integer
```

The compiler lowers it as:

```text
Python → arbitrary-precision int
Node   → BigInt
```

rather than allowing each backend to choose its own default numeric type.

## Typed transport

Portable JSON observables encode exact integers explicitly:

```json
{"$exact_integer":"18446744073709551617"}
```

This avoids silently losing precision at the serialization boundary.

## New tested behaviors

Round 12 covers:

- explicit numeric semantic contract;
- mandatory numeric-type declaration;
- backend-default numeric rejection;
- canonical decimal integer syntax;
- decimal input rejection;
- leading-zero rejection;
- deterministic Python and Node compilers;
- exact generated artifact equality;
- Node BigInt lowering;
- exact Python/Node semantic equivalence;
- unsafe JavaScript Number drift detection;
- language-neutral canonical source;
- 256 large-integer stress;
- 257-value bound rejection.

## Main result

v0.12 is the first round where Bridge does not merely verify two backend
implementations.

It explicitly overrides a backend-language default in order to preserve a
canonical semantic type.

That is a stronger programming-language property.

## Bounded conclusion

The evidence supports:

> For the tested exact-integer operation, Bridge defines the numeric meaning
> above Python and JavaScript, compiles each backend to a representation that
> preserves it, and detects the precision drift caused by JavaScript Number.

This does not yet define floating-point, decimal, overflow, or rounding
semantics.

## Next frontier

The next useful adversarial numeric layer is floating-point and exceptional
values:

```text
NaN
Infinity
-0
rounding
comparison
serialization
```

Alternatively, Unicode normalization is another high-value cross-language
semantic domain.

Either would test whether Bridge can continue replacing backend-default meaning
with explicit canonical meaning.
