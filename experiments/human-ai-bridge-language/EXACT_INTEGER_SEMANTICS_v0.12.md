# Bridge-0 Exact Integer Semantics v0.12

> Status: Experimental / explicit numeric semantic constitution

## Purpose

v0.11 proved that one Bridge semantic operation could compile to Python and
Node.js and preserve a typed result.

v0.12 deliberately chooses a case where the backend languages do not share the
same default numeric semantics.

Python integers are arbitrary precision.

JavaScript `Number` cannot represent every integer above
`2^53 - 1` exactly.

Therefore Bridge must not inherit the backend default.

## Canonical contract

The source now states:

```text
numeric=exact_integer
```

Example:

```text
⊙ [P1] program
  name=bridge0_v012_exact_integer
  targets=python312,node20

→ [C1] compute
  op=stats
  numeric=exact_integer
  values=9007199254740991,9007199254740993,
         -9007199254740995,18446744073709551617
  observe=json_value
```

The values intentionally cross JavaScript's safe-integer boundary.

## Bridge semantic rule

```text
exact_integer
= mathematical signed integer
= no precision loss
= no backend-dependent rounding
```

Backend defaults are implementation details, not canonical semantics.

## Lowering rules

### Python target

```text
exact_integer
→ Python int
```

### Node target

```text
exact_integer
→ JavaScript BigInt
```

The Node compiler emits `n`-suffixed literals and BigInt arithmetic.

It does not use JavaScript Number for canonical exact-integer operations.

## Typed observable encoding

JSON itself does not provide a portable arbitrary-precision integer contract.

Therefore exact integers are serialized using an explicit tagged decimal form:

```json
{"$exact_integer":"18446744073709551617"}
```

A result is therefore structurally explicit:

```json
{
  "count": {"$exact_integer":"4"},
  "max":   {"$exact_integer":"18446744073709551617"},
  "min":   {"$exact_integer":"-9007199254740995"},
  "sum":   {"$exact_integer":"18455751272964292606"}
}
```

The string is transport representation.

The semantic type remains `exact_integer`.

## Real cross-language verification

The generated Python and Node backends both passed.

Their typed observable comparison produced:

```text
BRIDGE_TYPED_EQUIVALENT
sha256=959d04824492588a4ab0258e593c863d42ba9b98d809afcefc2c7762c2960d69
```

## Deliberate unsafe backend

The test suite also generates an intentionally wrong Node implementation that
uses ordinary JavaScript Number semantics.

It produces a different semantic digest:

```text
safe exact-integer:
959d04824492588a4ab0258e593c863d42ba9b98d809afcefc2c7762c2960d69

unsafe Number backend:
3835dcd02c7e956704c5387f6565f5199964d0342c2bf97207d84517087c64b4
```

and is rejected as:

```text
HETEROGENEOUS_BACKEND_DRIFT
```

This is the intended result.

## Parser / validator restrictions

v0.12 rejects:

- missing numeric contract;
- `numeric=backend_default`;
- decimal values;
- non-canonical integer text such as leading-zero forms;
- unknown backend targets;
- more than 256 values;
- backend-specific fields inside the canonical semantic task.

## New validator rules

```text
V079 exact-integer executable subset integrity
V080 exact target-set validity
V081 operation cardinality / operation validity
V082 explicit numeric and observable contract
V083 canonical exact-integer input and bounds
```

## Main finding

The round demonstrates a key language-design rule:

> Backend numeric types must not silently define Bridge numeric semantics.

The compiler must lower from Bridge's semantic type into an implementation that
preserves that type.

```text
Bridge exact_integer
≠ Python int semantics by definition
≠ JavaScript Number semantics by definition

Bridge exact_integer
→ backend-specific representation that preserves the Bridge contract
```

## Boundary

Only exact signed integer semantics are defined here.

The following remain separate future semantic contracts:

- decimal arithmetic;
- IEEE-754 binary floating point;
- NaN / Infinity;
- negative zero;
- overflow policy for bounded integers;
- rounding modes;
- units and dimensional arithmetic.

They must not be inferred automatically from a backend language.
