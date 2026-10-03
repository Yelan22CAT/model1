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
6e91757ca0921a94ac4300fcee1918f85d862039354da1b542560536083136bf
```

Deterministic generated corpus digest for Python 3.13 reference generation:

```text
f9d47a0dd93bc7d8bc5171dab1465fa11cf1d18794d66f8ffc56c4102ac75f04
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


## Verdict vs diagnostic semantics

The public reproduction exposes two distinct semantic anchors:

- **verdict digest** — proves the PASS/FAIL outcome for each case;
- **diagnostic digest** — additionally proves the first failure reason and therefore the normative gate-priority order.

Expected digests:

```text
verdict:
be6cb05ecb2ca40f7b3fbc7b8421ce76141a0b6ad628ed90bd5415e197f52569

diagnostic:
6e91757ca0921a94ac4300fcee1918f85d862039354da1b542560536083136bf
```

A gate reordering can preserve every PASS/FAIL verdict while changing the first reported failure reason. Such a change is **diagnostic drift**, not automatically verdict drift.

`SameVerdict != SameDiagnostic`


## Stable generator algorithm

The public corpus no longer depends on Python `random.Random` implementation details.

It uses a specified SHA-256 counter PRNG:

```text
u64_i = first 8 bytes of SHA256(UTF8(seed + ":" + counter))
below(n) = u64_i mod n
```

Case-count selection uses fixed integer thresholds, and mutation selection uses deterministic pop-without-replacement indexing.

Therefore:

`Seed != CorpusIdentity`

The corpus identity is the combination of the generator algorithm specification, seed, case count, mutation table, and resulting corpus digest.


## Corpus semantic profile

The generator reads [CORPUS_PROFILE_RC1.json](CORPUS_PROFILE_RC1.json), which freezes:

- generator algorithm identifier;
- seed;
- case count;
- mutation-count thresholds;
- base state;
- ordered mutation table.

Canonical corpus-profile SHA-256:

`4fb956e92acc20d6f54fee1a6b4805d23402a36e12856a6684d122ec2f275f38`

This prevents a silent mutation-table or base-state change from being described as "the same generator" merely because the seed and PRNG algorithm are unchanged.

`SameAlgorithm + SameSeed != SameCorpusSemantics`
