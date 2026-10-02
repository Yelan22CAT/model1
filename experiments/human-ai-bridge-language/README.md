# Human–AI Bridge Language (Bridge-0)

> **Experimental / v0.1 / Not production-ready**  
> Provisional name. This is a semantic-language experiment, not a finished programming language.

## One-line purpose

Create a shared semantic layer that humans can learn with low effort and AI systems can parse with low ambiguity.

The goal is **not** to make AI infallible. The goal is to reduce the space in which uncertainty, inference, or missing information can silently become apparent fact.

> **Not to make AI infallible, but to prevent uncertainty from masquerading as fact.**

中文：  
这不是“把中文翻译成英文再给 AI”的方案，而是尝试建立一个**人类与 AI 共用的语义层**。人类向结构化表达走一步，AI 向显式、可审计表达走一步。

---

## Why this experiment exists

Natural language is powerful but often ambiguous:

- subjects may be omitted;
- uncertainty may disappear across turns;
- assumptions may be mistaken for facts;
- missing values may be silently completed;
- permissions and authority may be implicit;
- evidence may be blended with conclusions.

Bridge-0 explores whether a small set of explicit semantic primitives can make these distinctions visible to both humans and machines.

The first target is **communication integrity**, especially:

1. fact / hypothesis / unknown separation;
2. evidence binding;
3. explicit constraints;
4. action / authority separation;
5. verification state;
6. resistance to semantic-state drift.

---

## Core idea

Human natural language and machine execution languages remain useful.

Bridge-0 sits **above** them:

```text
Human language / voice / UI
            ↓
     Semantic compiler
            ↓
        Bridge-0
    shared semantic layer
            ↓
  canonical graph / AST / IR
            ↓
AI model / agent / tool / runtime
            ↓
      verification
```

Chinese, English, or another natural language may be used as the display layer. The semantic core should not depend on one natural language.

---

## v0.1 semantic primitives

| Symbol | Canonical meaning | 中文 |
|---|---|---|
| `○` | Entity | 实体 / 对象 |
| `→` | Action / transition | 动作 / 状态变化 |
| `=` | State / assignment | 状态 / 赋值 |
| `⊙` | Goal | 目标 |
| `■` | Fact claim | 事实主张 |
| `△` | Hypothesis | 假设 |
| `?` | Unknown | 未知 |
| `◆` | Evidence | 证据 |
| `!` | Constraint | 约束 |
| `✓` | Verified state | 已验证 |
| `×` | Forbidden / rejected | 禁止 / 否定 |
| `⏱` | Time | 时间 |

These symbols are **provisional surface notation**. Their semantics matter more than their final glyph design.

---

## Example 1 — unknown must stay unknown

```text
○ Person-A
? [C1] Person-A.age
```

Bridge rule:

```text
? [C1] + no sufficient ◆
→ × promote [C1] to ■
```

Meaning:

> If a value is unknown and has no supporting evidence, it must not be promoted to a factual assertion.

---

## Example 2 — hypothesis cannot silently become fact

```text
△ cause = network_failure
◆ evidence = partial
```

Later processing must preserve the hypothesis state unless an explicit verification transition occurs:

```text
△ + ◆ sufficient + ✓ verification
→ ■
```

No silent state upgrade is allowed.

---

## Example 3 — understanding is not authority

```text
○ Agent-A
→ deploy_change

! authority = human_owner
× Agent-A.approve
✓ human_owner.approve
```

An AI may understand or recommend an action without owning permission to execute it.

---

## Initial design constitution

1. **One core semantic per primitive.**
2. **Unknown is a legal state.**
3. **Every claim carries an epistemic state.**
4. **Evidence is separate from the claim it supports.**
5. **Action does not imply authority.**
6. **Material time, quantity, and units should be explicit.**
7. **Rendering may change; semantics may not drift.**

---

## What Bridge-0 is not

Bridge-0 is not currently:

- a replacement for Python, Rust, Lisp, YAML, JSON, or SQL;
- a claim that hallucinations can be completely eliminated;
- a finished compiler or runtime;
- a new natural language;
- a visual emoji dictionary;
- an autonomous decision authority.

The intended near-term architecture is:

```text
Bridge spec
   ↓
parser
   ↓
canonical IR / AST
   ↓
compiler targets
   ├─ Python
   ├─ GitHub Actions YAML
   ├─ JSON / API
   ├─ MCP / tool calls
   └─ agent runtime
```

Existing languages remain execution backends.

---

## Experimental success criteria

A v0.x prototype is useful only if it can show measurable improvement on real tasks.

Early tests should examine:

- human readability;
- parse success;
- cross-model semantic agreement;
- fact / hypothesis / unknown preservation;
- round-trip semantic invariance;
- tool-call correctness;
- permission preservation;
- error localization;
- token and latency cost;
- hallucination containment rate.

---

## Development method

Do not invent hundreds of symbols in advance.

Start with a minimal core, then test it against real tasks.

```text
real task
→ encode with current primitives
→ identify semantic gap
→ add a primitive only if the gap is real
→ retest
```

The language should grow from failures and use cases, not from decorative syntax.

---

## Public / private boundary

This public experiment intentionally publishes:

- the problem definition;
- the minimal semantic vocabulary;
- public-safe examples;
- open design questions;
- interface-level ideas.

It does **not** publish private case data, hidden thresholds, proprietary runtime logic, or unrestricted execution authority.

---

## Feedback wanted

Useful questions include:

- Is a symbol ambiguous?
- Can two competent readers interpret the same expression differently?
- Can two different AI models preserve the same state?
- Which semantic relationship is missing?
- Can the same concept be expressed with fewer primitives?
- Does a proposed feature belong in the semantic layer, or in a compiler/runtime?

This is a zero-to-one experiment. Breaking examples are more useful than praise.



---

## Round 1 status

The first encoding round is complete using ten public-safe patterns already present in this repository.

Result:

- all ten could be expressed with the current semantic categories;
- no new glyphs were added;
- the main gaps are grammar/IR issues rather than vocabulary size.

Review:

- [Round 1 — Ten Encoding Tests](ROUND1_10_CASES.md)
- [Round 1 — Gap Ledger](ROUND1_GAP_LEDGER.md)
- [Round 1 — Machine-readable Corpus](corpus/round1_cases.json)

The most important first correction is:

```text
? value
```

rather than:

```text
■ value = ?
```

A proposition should carry one explicit epistemic state.


---

## Round 2 status

Round 2 stress-tested harder structures:

- attributed / nested claims;
- conflicting evidence;
- numerical uncertainty;
- multi-agent handoff;
- partial permissions;
- tool failure;
- source version replacement;
- reversible vs irreversible action;
- association vs causation;
- cross-language rendering.

Result:

- still no new glyphs;
- the language now clearly needs a stricter semantic grammar and canonical IR;
- stable IDs, meta-claim separation, typed relations, guarded actions, and label/identity separation are now mandatory.

Review:

- [Round 2 — Stress Tests](ROUND2_STRESS_TESTS.md)
- [Round 2 — Gap Ledger](ROUND2_GAP_LEDGER.md)
- [Round 2 — Machine-readable Corpus](corpus/round2_cases.json)

A key new invariant is:

```text
"A says X"
≠
"X is true"
```

and another:

```text
tool failure / no result
≠
negative world-state fact
```

The next design step is formal grammar + canonical IR, not a larger symbol alphabet.


---

## Round 3 status — authority and provenance composition

Bridge-0 v0.3 now has structured records for:

- permission tuples;
- handoffs;
- guarded state transitions;
- provenance;
- validity windows.

Latest executed CI result:

```text
63 tests
63 passed
0 failed
```

The current suite includes 50 chained handoffs and 100 distinct permission tuples.

Key result:

```text
handoff ≠ permission delegation
permission(read, narrow_scope) ≠ permission(write, broad_scope)
irreversible transition → explicit guard + authority
derived claim → explicit provenance
```

See [Round 3 Result](ROUND3_AUTHORITY_PROVENANCE_RESULT_v0.3.md) and [Structured Semantics v0.3](STRUCTURED_SEMANTICS_v0.3.md).


---

## Round 4 status — delegation, revocation, expiry, replay

Bridge-0 v0.4 now tests authority as a lifecycle rather than a static permission.

```text
grant
→ delegate
→ narrow
→ expire / revoke
→ replay attempt
```

Latest executed lifecycle-enabled CI result:

```text
78 tests
78 passed
0 failed
```

Key tested invariants:

```text
delegation cannot broaden parent authority
root revocation invalidates descendants
child revocation does not revoke parent
expired authority cannot be replayed
new grant after revocation gets a new ID
stale replay epoch is rejected
```

The main Round-4 discovery is a runtime boundary:

> A stale document cannot detect a newer revocation that is completely absent from that document.

Therefore execution-time authority checks need an external current-authority epoch/state source.

See:

- [Authority Lifecycle v0.4](AUTHORITY_LIFECYCLE_v0.4.md)
- [Round 4 Result](ROUND4_AUTHORITY_LIFECYCLE_RESULT_v0.4.md)
- [IR Schema v0.4](IR_SCHEMA_v0.4.json)


---

## Round 5 status — split-brain and reconciliation

Bridge-0 v0.5 now tests concurrent state divergence.

Latest executed CI result:

```text
93 tests
93 passed
0 failed
```

The enforced path is now:

```text
concurrent snapshots
→ explicit divergence
→ explicit conflict
→ explicit merge
→ trusted finality
→ execution
```

Automatic `last_writer` merge is rejected.

A divergent branch cannot finalize itself, and execution must reference finality for the exact state being executed.

A 12-way divergent fork stress test produced 66 pairwise conflicts and passed. This also exposed an O(n²) scaling weakness in the current pairwise conflict representation.

See:

- [Split-Brain Semantics v0.5](SPLIT_BRAIN_SEMANTICS_v0.5.md)
- [Round 5 Result](ROUND5_SPLIT_BRAIN_RESULT_v0.5.md)
- [IR Schema v0.5](IR_SCHEMA_v0.5.json)


---

## Round 6 status — conflict sets and independent quorum evidence

Bridge-0 v0.6 replaces pairwise many-way conflicts with a compact conflict-set representation and separates reconciliation from finality evidence.

Latest executed test result:

```text
112 tests
112 passed
0 failed
```

Key path:

```text
many divergent states
→ one conflict_set
→ explicit reconciliation proposal
→ quorum policy
→ independent votes
→ finality certificate
→ execution
```

Stress results:

```text
100 divergent branches
→ 1 conflict_set
```

instead of 4,950 pairwise conflicts.

And:

```text
101 eligible voters
67 required votes
67 required independence domains
→ certificate passed
```

The validator also blocks duplicate-voter inflation and repeated declared independence domains.

Important boundary:

```text
declared independence
≠
verified independence
```

Bridge can preserve and validate independence labels, but an external identity/provenance attestation layer is needed to prove that two voter identities are actually independent.

See:

- [Conflict Set & Quorum v0.6](CONFLICT_SET_QUORUM_v0.6.md)
- [Round 6 Result](ROUND6_CONFLICT_SET_QUORUM_RESULT_v0.6.md)
- [IR Schema v0.6](IR_SCHEMA_v0.6.json)


---

## Round 7 status — identity, lineage, and evidence provenance

Bridge-0 v0.7 now tests whether multiple apparent voters are actually independent across recorded identity and evidence dimensions.

Latest executed CI result:

```text
126 tests
126 passed
0 failed
```

New separation:

```text
voter ID
≠ identity
≠ control domain
≠ model lineage
≠ runtime origin
≠ evidence root
```

The validator now rejects common quorum-inflation patterns such as:

- a voter name that does not match its identity;
- a fake independence label;
- multiple voters sharing one model lineage;
- multiple voters sharing one runtime origin;
- multiple votes copied from one evidence root;
- expired or revoked identity attestations.

Stress:

```text
67 voters
67 control domains
67 model lineages
67 runtime origins
67 evidence roots
→ valid certificate
```

Important boundary:

```text
semantic attestation
≠ cryptographic attestation
```

The current prototype validates the declared trust chain but does not yet prove the issuer cryptographically.

See:

- [Identity & Evidence Provenance v0.7](IDENTITY_PROVENANCE_v0.7.md)
- [Round 7 Result](ROUND7_IDENTITY_PROVENANCE_RESULT_v0.7.md)
- [IR Schema v0.7](IR_SCHEMA_v0.7.json)


---

## Round 8 status — executable Bridge source

Bridge-0 v0.8 now has a restricted compiler path to a real GitHub Actions backend.

Latest verified prototype result:

```text
136 tests
136 passed
0 failed
```

And the generated workflow itself executed successfully on GitHub.

```text
Bridge source
→ Parser
→ Canonical IR
→ Validator
→ Compiler
→ GitHub Actions YAML
→ GitHub runner
→ real test execution
```

The compiler currently supports only an allowlisted subset:

- checkout;
- setup_python;
- python_module.

Raw shell, unsafe arguments, path traversal, unsupported runners, and arbitrary action injection are rejected.

A useful failure was discovered during this round: the first generated workflow was rejected by the actual GitHub backend because the emitted command syntax was invalid. The compiler was corrected and the generated workflow then ran successfully.

That failure establishes a new rule:

```text
compiler unit tests
≠
backend acceptance
```

The real backend must remain in the verification loop.

See:

- [Executable Source v0.8](EXECUTABLE_SOURCE_v0.8.md)
- [Round 8 Result](ROUND8_EXECUTABLE_SOURCE_RESULT_v0.8.md)
- [IR Schema v0.8](IR_SCHEMA_v0.8.json)
- [Executable Bridge Source](executable_v0.8.bridge)


---

## Round 9 status — multi-backend equivalence

Bridge-0 v0.9 now measures backend drift instead of assuming all compiler
targets preserve behavior.

Latest verified prototype result:

```text
148 tests
148 passed
0 failed
```

The real generated workflow also passed:

```text
same Bridge source
├→ GitHub Actions path
└→ local deterministic runner
          ↓
BRIDGE_BACKEND_EQUIVALENT
```

Verified observable hash:

```text
53b7aef77cb78d64ca2518d7651b97aba18cf2d94790e3e548ef3da667f67657
```

A deliberate mismatch was also injected and correctly reported as
`BACKEND_DRIFT`.

Current evidence is implementation-path equivalence on the same Ubuntu/Python
runtime, not yet full cross-platform equivalence.

See:

- [Multi-Backend Equivalence v0.9](MULTI_BACKEND_EQUIVALENCE_v0.9.md)
- [Round 9 Result](ROUND9_MULTI_BACKEND_RESULT_v0.9.md)
- [IR Schema v0.9](IR_SCHEMA_v0.9.json)
- [Executable Bridge Source v0.9](executable_v0.9.bridge)


---

## Round 10 status — heterogeneous runtime typed equivalence

Bridge-0 v0.10 now tests the same Bridge source across three different operating-system runners using a typed JSON semantic observable.

Latest verified prototype result:

```text
161 tests
161 passed
0 failed
```

Real generated workflow:

```text
Ubuntu   ✓
Windows  ✓
macOS    ✓
compare  ✓
```

Canonical semantic digest:

```text
d2bd73193dfdf95314fb1b2c53e53690ec14d97aef21b9e8f671b94e063159d5
```

The comparator ignores incidental JSON formatting differences and compares the typed value instead.

A deliberate semantic mutation was also detected as `HETEROGENEOUS_BACKEND_DRIFT`.

See:

- [Heterogeneous Runtime v0.10](HETEROGENEOUS_RUNTIME_v0.10.md)
- [Round 10 Result](ROUND10_HETEROGENEOUS_RESULT_v0.10.md)
- [IR Schema v0.10](IR_SCHEMA_v0.10.json)
- [Executable Bridge Source v0.10](executable_v0.10.bridge)


---

## Round 11 status — first verified cross-language compiler target

Bridge-0 v0.11 now compiles one language-neutral semantic operation into two
different implementation languages.

Latest verified prototype result:

```text
175 tests
175 passed
0 failed
```

Real generated workflow:

```text
Bridge source
├→ Python 3.12 backend  ✓
└→ Node.js 20 backend  ✓
          ↓
typed semantic compare ✓
```

Canonical result digest:

```text
d4198466737cdf57b1f75243ea8d6200b4bd3e8c3e05cf8b79ac53673ca12e8a
```

The canonical Bridge source contains no Python module or JavaScript command.
Both backend programs are generated from the same semantic operation.

A deliberate mutation in one backend was correctly detected as
`HETEROGENEOUS_BACKEND_DRIFT`.

See:

- [Cross-Language Compiler v0.11](CROSS_LANGUAGE_COMPILER_v0.11.md)
- [Round 11 Result](ROUND11_CROSS_LANGUAGE_RESULT_v0.11.md)
- [IR Schema v0.11](IR_SCHEMA_v0.11.json)
- [Executable Bridge Source v0.11](executable_v0.11.bridge)


---

## Round 12 status — exact integer semantics above backend defaults

Bridge-0 v0.12 now defines an explicit canonical numeric contract:

```text
numeric=exact_integer
```

Latest verified prototype result:

```text
190 tests
190 passed
0 failed
```

Real generated backends:

```text
Bridge exact_integer
├→ Python arbitrary-precision int  ✓
└→ Node.js BigInt                  ✓
          ↓
typed semantic compare             ✓
```

Canonical digest:

```text
959d04824492588a4ab0258e593c863d42ba9b98d809afcefc2c7762c2960d69
```

A deliberate Node implementation using ordinary JavaScript `Number` produced
a different digest and was correctly rejected as `HETEROGENEOUS_BACKEND_DRIFT`.

This is the first round where Bridge explicitly overrides a backend-language
default to preserve canonical semantics.

See:

- [Exact Integer Semantics v0.12](EXACT_INTEGER_SEMANTICS_v0.12.md)
- [Round 12 Result](ROUND12_EXACT_INTEGER_RESULT_v0.12.md)
- [IR Schema v0.12](IR_SCHEMA_v0.12.json)
- [Executable Bridge Source v0.12](executable_v0.12.bridge)


---

## Round 13 status — binary64 floating semantics

Bridge-0 v0.13 now defines an explicit floating-point contract instead of inheriting backend defaults.

Verified prototype result:

~~~text
207 tests
207 passed
0 failed
~~~

The canonical source declares:

~~~text
numeric=binary64
rounding=ties_to_even
~~~

Real Python 3.12 and Node.js 20 generated backends produced the same typed semantic observable:

~~~text
c69af06968a78f866e35c797333f82149670d399f048b37614a9150babbfad73
~~~

An intentionally unsafe Node backend using Math.round and raw JSON floating serialization produced a different digest and was correctly rejected as HETEROGENEOUS_BACKEND_DRIFT.

This round preserves NaN, both infinities, positive/negative zero, and ties-to-even half-way rounding through explicit Bridge semantics and tagged transport.

See:

- [Binary64 Floating Semantics v0.13](BINARY64_FLOAT_SEMANTICS_v0.13.md)
- [Round 13 Result](ROUND13_BINARY64_RESULT_v0.13.md)
- [IR Schema v0.13](IR_SCHEMA_v0.13.json)
- [Executable Bridge Source v0.13](executable_v0.13.bridge)


---

## Round 14 status — Unicode text identity

Bridge-0 v0.14 now defines canonical Unicode text identity above backend raw
string representation.

Latest verified prototype result:

~~~text
225 tests
225 passed
0 failed
~~~

Canonical source contract:

~~~text
text_model=unicode_scalar
normalization=NFC
identity=normalized_scalar_sequence
~~~

Real Python 3.12 and Node.js 20 backends produced the same typed semantic
observable:

~~~text
1c0acbd4243ec0a4bba6a99350c7aa44596cd6b261b16f4f256f09e11d6d6b05
~~~

Verified canonical equivalences include composed/decomposed Latin text,
Angstrom forms, Hangul composition, and combining-mark reordering.

An intentionally unsafe raw-sequence backend skipped NFC normalization and was
correctly rejected as HETEROGENEOUS_BACKEND_DRIFT.

v0.14 also explicitly keeps normalized scalar identity separate from grapheme,
visual, and linguistic identity.

See:

- [Unicode Text Identity v0.14](UNICODE_TEXT_IDENTITY_v0.14.md)
- [Round 14 Result](ROUND14_UNICODE_RESULT_v0.14.md)
- [IR Schema v0.14](IR_SCHEMA_v0.14.json)
- [Executable Bridge Source v0.14](executable_v0.14.bridge)


---

## Round 15 status — pinned Unicode grapheme semantics

Bridge-0 v0.15 now separates Unicode scalar identity from a bounded grapheme
semantic layer and pins that layer to an explicit semantic Unicode version.

Latest verified result:

~~~text
243 tests
243 passed
0 failed
~~~

Real runtime observation:

~~~text
Python 3.12 runtime Unicode = 15.0.0
Node.js 20 runtime Unicode = 17.0
Bridge semantic Unicode = 15.0
~~~

The first strict runtime-version implementation failed on Node because its
runtime Unicode version had advanced to 17.0.

The corrected compiler carries a bounded Bridge-owned Unicode 15.0 profile into
both backends, so runtime Unicode data is observed but does not silently
redefine Bridge semantics.

Verified typed digest:

~~~text
29043ba727215e0bfea405d6b322206bbbed93aa261df0882bf65b7f68262004
~~~

An unsafe code-point-counting backend produced a different digest and was
rejected as HETEROGENEOUS_BACKEND_DRIFT.

The current profile is deliberately bounded and is not a complete UAX #29
implementation.

See:

- [Grapheme Semantics v0.15](GRAPHEME_SEMANTICS_v0.15.md)
- [Round 15 Result](ROUND15_GRAPHEME_RESULT_v0.15.md)
- [IR Schema v0.15](IR_SCHEMA_v0.15.json)
- [Executable Bridge Source v0.15](executable_v0.15.bridge)
