# Bridge-0 v1.0-rc1 Public Reproduction Kit

This directory provides a **public-safe deterministic subset** for independent reproduction of the RC decision semantics.

It is intentionally smaller than the private/internal adversarial qualification corpus.

## Reproduce

```bash
python3 generate_corpus.py corpus.json

python3 validator.py corpus.json > python.out
node validator.js corpus.json > node.out
ruby validator.rb corpus.json > ruby.out

sha256sum python.out node.out ruby.out
cmp python.out node.out
cmp python.out ruby.out
```

Expected output digest:

```text
8a3d911a24fd018ef791314d5bba06d2b0fe85e7f30fb6e2dc117fcc40f1bcab
```

Deterministic generated corpus digest for Python 3.13 reference generation:

```text
0dcf5bf318fc8e1988a03267c3b35ba9764130a3e5e8104f7ef1593d0ef35fa5
```

Parameters:

```text
seed = 20261002
cases = 256
spec generation = spec-rc1
```

## Boundary

This kit demonstrates public reproducibility for a bounded, public-safe semantic subset.

It does **not** publish the full private adversarial corpus, sensitive attack fixtures, production thresholds, or unrestricted execution logic.

The larger 20,000-case qualification result remains a separate internal/campaign result. External reviewers should treat this public kit as an independently rerunnable subset, not as access to the entire internal test corpus.
