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


## Environment drift

The semantic anchors are the generated corpus digest and validator output digest. Runtime/OS/action versions are supporting environment evidence.

See:

- [ENVIRONMENT_MANIFEST.json](ENVIRONMENT_MANIFEST.json)
- [verify_environment.py](verify_environment.py)

Interpretation:

- environment changed + semantic digests unchanged -> `REPRODUCTION_ENVIRONMENT_DRIFT`, not automatically a Bridge semantic regression;
- corpus/output digest changed -> semantic drift requiring review;
- CI fails before a semantic result exists -> unverifiable/infrastructure failure, never fail-open.

The reference observed environment was Python 3.13.5, Node 22.16.0, and Ruby 3.3.8. Future patch-version changes are allowed to reproduce the same semantic digests; they are recorded rather than silently treated as identical environments.


## Independent decision oracle

Cross-runtime equality is not treated as semantic correctness by itself.

The public kit therefore also includes:

- [DECISION_PROFILE_RC1.json](DECISION_PROFILE_RC1.json) — declarative ordered decision gates;
- [oracle.py](oracle.py) — an interpreter for the declarative profile;
- [mutation_test.py](mutation_test.py) — gate-omission mutation tests.

Current decision-profile SHA-256:

`7d4a208387828fca13edce21eda492f96707e0503bdbcada2a29eefc1ed08c8c`

CI requires Python, Node.js, Ruby, and the declarative oracle to produce identical public-subset results. Mutation tests must kill all one-gate-omission mutants.

This separates **three implementations** from the **public normative subset definition**; it still does not claim universal correctness beyond that declared profile.


### Decision-profile digest semantics

The decision-profile digest is computed over canonical JSON semantics, not raw file bytes:

- parse JSON;
- serialize as UTF-8;
- sort object keys;
- use compact separators `(',', ':')`;
- hash the canonical bytes with SHA-256.

Formatting-only changes to the JSON file therefore do not create semantic drift.
