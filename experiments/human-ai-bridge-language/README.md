# Human–AI Bridge Language (Bridge-0)

> **Experimental / v0.1 / Not production-ready**  
> Provisional name. This is a semantic-language experiment, not a finished programming language.

> **Positioning confirmed 2026-10-08:** Human and AI meet in the middle — preserve meaning, expose uncertainty, verify what can be verified.  
> **定位确认：** 人类与 AI 各向中间走一步——保留原意，显露不确定性，验证能够验证的部分。  
> Bridge is a **bidirectional mutual-understanding layer**, not compulsory human-to-machine translation or an Agent workflow language. Natural conversation stays natural; structured notation is optional when useful.  
> **[Read the bilingual positioning statement / 中英双语核心定位](POSITIONING_SHARED_UNDERSTANDING.md).**

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

Human natural language and machine execution languages remain useful. Bridge-0 does not require every utterance to be compiled into formal instructions.

```text
Human expression <----> AI interpretation
              shared meaning
        (intent, claims, evidence,
         ambiguity, constraints, unknowns)
                   |
         clarification / calibration
                   |
          scoped verification
                   |
    answer / optional structured form
                   |
     optional Agent / Graph / runtime
```

The lower layers (canonical IR, formal validation, tool/runtime execution and recovery) remain available when a use case genuinely requires them. They are **not a compulsory pathway for ordinary conversation**. Chinese, English and other natural languages may be used freely as the human-facing expression layer.

---

## Surface language design principle

Bridge-0 now treats the surface language as a three-party contract:

```text
Human-readable
× AI-generatable
× Machine-verifiable
= viable Bridge surface
```

The governing rule is:

> **Expose what affects correctness; hide what only affects implementation.**

This is a forward constraint and an audit rule for existing syntax, not a mandate to rewrite the language from scratch. Existing constructs remain when they satisfy the contract; failing constructs are revised, migrated, or deprecated explicitly.

Automated tests may establish parseability, canonical equivalence, deterministic validation, and declared AI-generation conformance. They do **not** by themselves prove human comprehension; human-readability claims require separate human evidence.

See [Surface Language Design Principles](SURFACE_LANGUAGE_PRINCIPLES.md).

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

## License

Bridge-0 public materials in this directory are licensed under the **Apache License 2.0** unless a specific file states otherwise.

Why Apache-2.0 rather than MIT for this experiment:

- it remains permissive for research, commercial use, modification, and redistribution;
- it includes an explicit patent-license grant and patent-termination mechanism;
- it requires preservation of relevant notices and prominent notice of modified files;
- it does not impose copyleft or require derivative projects to publish their source code.

For a semantic protocol/compiler/runtime experiment intended for cross-implementation and possible enterprise adoption, those explicit patent and attribution terms are preferable to MIT's shorter but less explicit treatment.

Scope boundary:

- the license applies to material actually published in `experiments/human-ai-bridge-language/` under this repository;
- it does **not** grant rights to unpublished Model Root material, private datasets, customer or employer data, hidden thresholds, private runtime packs, or other material not included in the licensed work;
- third-party components retain their own licenses and notices;
- no trademark, personal-identity, customer-data, or private-system rights are granted by the Apache-2.0 license.

See [LICENSE](LICENSE).

License choice is separate from claims of novelty, inventorship, patentability, or ownership of unpublished material.

---

## Experimental architecture RFCs

- [Adaptive Workload Routing, Reasoning Budget & Structural Distillation](RFC_ADAPTIVE_WORKLOAD_ROUTING_REASONING_BUDGET.md) — routes by workload/capability/trust constraints, keeps reasoning budget separate from authority, and treats popularity as adoption evidence rather than capability proof.
- [Reality-Final Verification, Requirement/Model Gaps & Assurance Revision](RFC_REALITY_FINAL_VERIFIER_TWO_GAPS_ASSURANCE_REVISION.md) — treats requirements, world models and evaluators as fallible proxies; deployment evidence can invalidate prior acceptance, so assurance is revisionary rather than permanent closure.
- [Semantic-First AI Programming Assurance](RFC_SEMANTIC_FIRST_AI_PROGRAMMING_ASSURANCE.md) — keeps AI-generated code subordinate to explicit semantics, verification capacity, traceability, reversibility, observability, independent review, bounded change scope, and production-readiness gates.
- [Adaptive Deliberation Policy](RFC_ADAPTIVE_DELIBERATION_POLICY.md) — routes among direct, sequential, sampled, search/backtrack, and critique/refine strategies while keeping sample count separate from evidence independence and reasoning strategy separate from authority.
- [State-Bound Planning, Replanning & Reality Checkpoints](RFC_STATE_BOUND_PLANNING_REPLAN.md) — treats plans as versioned dependency graphs bound to current state, capabilities, authority and runtime reality; material drift triggers revalidation or replanning.
- [Tool Capability Binding, Dynamic Registry & Safe Invocation](RFC_TOOL_CAPABILITY_BINDING_DYNAMIC_REGISTRY_SAFE_INVOCATION.md) — treats tools as typed, versioned capability contracts; separates discovery from current binding, schema validity from semantic safety, functional fit from least privilege, and tool-call construction from authorized external effect.

## v0.200 verification milestone

The post-v0.50 adversarial campaign has reached a new public checkpoint at **v0.200**. The milestone summarizes structural work on surface/IR separation, heterogeneous execution, multi-interface agents, task factories, policy-plane anti-bypass rules, agent containment, external observability, Byzantine/collusion resistance, and trust recovery.

See [Verification Status — v0.200](VERIFICATION_STATUS_v0.200.md).

The v0.200 result remains **Experimental / Local Synthetic Test Only / Not Production Ready**.

## v0.250 verification milestone

Bridge-0 has reached the next consolidated local-adversarial checkpoint at **v0.250**.

The post-v0.200 campaign adds structural coverage for trust-assumption invalidation, approval/effect binding, causal and rollback-resistant execution history, reasoning-budget non-elevation, context provenance, constrained model routing, means-constrained agency, requirement/model/evaluation gaps, verification capacity, comprehension debt, and adaptive deliberation strategies.

The v0.250 selected milestone regression used 25 representative material invariants across 100,000 synthetic cases:

```text
attack cases:                    80,090
weak 23/25-enough false accepts: 66,796
strict all-material false accepts:     0
strict all-material false rejects:     0
```

See [Verification Status — v0.250](VERIFICATION_STATUS_v0.250.md).

Boundary:

```text
selected milestone regression != every historical bundle re-executed
local simulation != closure
```

The v0.250 milestone does **not** advance the separate remote-verification high-water by itself.

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


---

## Round 16 status — semantic profile evolution

Bridge-0 v0.16 now treats semantic-version compatibility as an executable
handshake rather than trusting version labels.

Verified gates:

~~~text
cumulative regression: 243 passed
dedicated v0.16:       16 passed
~~~

Real Python 3.12 and Node.js 20 compatibility backends produced the same typed
manifest:

~~~text
20fd68bc27a33a3ad2ae3390e1d0f396712c2e0aafcd21029064a5a45f09f072
~~~

A safe v1 -> v2 extension was accepted.

A synthetic same-major v1 -> v3 breaking change was rejected because an
existing behavior changed, despite the version labels looking semver-compatible.

An intentionally unsafe semver-major-only backend produced a different digest
and was rejected as HETEROGENEOUS_BACKEND_DRIFT.

Core rule:

~~~text
version label
!= proof of semantic compatibility
~~~

See:

- [Semantic Profile Evolution v0.16](SEMANTIC_PROFILE_EVOLUTION_v0.16.md)
- [Round 16 Result](ROUND16_SEMANTIC_COMPATIBILITY_RESULT_v0.16.md)
- [IR Schema v0.16](IR_SCHEMA_v0.16.json)
- [Executable Bridge Source v0.16](executable_v0.16.bridge)


---

## Round 17 status — executable semantic migration

Bridge-0 v0.17 now distinguishes successful conversion from lossless semantic
migration.

Verified gates:

~~~text
cumulative regression: 275 passed
dedicated v0.17:       16 passed
~~~

Real Python 3.12 and Node.js 20 migration backends produced the same typed
audit manifest:

~~~text
d4c7412b49ccb2adc69fed4f2f66828f4fa7af81acb39ae2c0ab7c6a94c7b69f
~~~

The lossless v1 -> v2 route round-tripped exactly and was permitted.

The compact v1 -> v3 route converted successfully but lost IDs, labels,
verification state, provenance and notes. Its round trip failed and execution
was denied.

An intentionally unsafe backend that treated conversion success as sufficient
permission produced a different digest and was rejected as
HETEROGENEOUS_BACKEND_DRIFT.

Core rule:

~~~text
successful conversion
!=
lossless migration
~~~

See:

- [Semantic Migration & Loss Audit v0.17](SEMANTIC_MIGRATION_LOSS_AUDIT_v0.17.md)
- [Round 17 Result](ROUND17_MIGRATION_RESULT_v0.17.md)
- [IR Schema v0.17](IR_SCHEMA_v0.17.json)
- [Executable Bridge Source v0.17](executable_v0.17.bridge)


---

## Round 18 status — scoped known-loss authorization

Bridge-0 v0.18 now allows a deliberately lossy migration only when the known
loss is explicitly acknowledged and the authorization is bound to the exact
authority, scope, artifact, provenance and validity window.

Verified gates:

~~~text
cumulative regression: 298 passed
dedicated v0.18:       23 passed
~~~

Real Python 3.12 and Node.js 20 authorization backends produced the same typed
decision manifest:

~~~text
625a612b4c150fbb6d3e47394d423710fa05d6c1a299d005dbb97d5248352812
~~~

The exact acknowledged migration was allowed.

Expired replay, wrong artifact, incomplete acknowledgement, over-broad scope
and wrong authority were denied.

An intentionally unsafe backend that treated the authority label alone as
blanket permission produced a different digest and was rejected as
HETEROGENEOUS_BACKEND_DRIFT.

Core rule:

~~~text
acknowledgement
+
authority
+
scope
+
artifact binding
+
provenance
+
time validity
=
conditional permission
~~~

See:

- [Scoped Known-Loss Authorization v0.18](SCOPED_LOSS_AUTHORIZATION_v0.18.md)
- [Round 18 Result](ROUND18_SCOPED_AUTHORIZATION_RESULT_v0.18.md)
- [IR Schema v0.18](IR_SCHEMA_v0.18.json)
- [Executable Bridge Source v0.18](executable_v0.18.bridge)


---

## Round 19 status — revocation and replay resistance

Bridge-0 v0.19 now treats scoped authorization as a stateful, single-use transition rather than a reusable label.

~~~text
cumulative regression: 322 passed
dedicated v0.19:       24 passed
~~~

Python 3.12 and Node.js 20 produced the same typed result:

~~~text
a1f1665730eff44b91546842afd1d16c82491c724bac88822fc4176e26487389
~~~

Verified behavior:

~~~text
first use              -> allow
same-token replay      -> deny
revoked token          -> deny
stale revocation epoch -> deny
tampered nonce         -> deny
expired token          -> deny
~~~

A deliberately stateless backend ignored consumption and revocation state, produced a different digest, and was rejected as semantic drift.

Core rule:

~~~text
valid once != valid forever
~~~

See:

- [Revocation & Replay Resistance v0.19](REVOCATION_REPLAY_RESISTANCE_v0.19.md)
- [Round 19 Result](ROUND19_REPLAY_RESULT_v0.19.md)
- [IR Schema v0.19](IR_SCHEMA_v0.19.json)
- [Executable Bridge Source v0.19](executable_v0.19.bridge)


---

## v0.20–v0.50 assurance consolidation

Bridge-0 has completed a second experimental phase beyond the original v0.1–v0.19 language/runtime work.

The later campaign tests whether evidence, trust, authorization, confidence, review, planning, execution, recovery, and restore state remain coherent under adversarial composition.

The v0.50 consolidation introduces a first-class **Assurance Context**:

```text
per-layer validity
+ exact dependency graph
+ one coherent assurance context
+ current execution-context recheck
= candidate end-to-end PASS
```

Core rule:

```text
All layers individually valid != End-to-end valid
```

Public consolidation documents:

- [Assurance Architecture v0.50](ASSURANCE_ARCHITECTURE_v0.50.md)
- [Verification Status v0.20–v0.50](VERIFICATION_STATUS_v0.50.md)

Current maturity remains:

```text
Experimental / v0.x / Not Production Ready
```

The next phase is convergence testing rather than declaring v1.0 by version count alone.

---

## v1.0-rc1 candidate

Bridge-0 has entered release-candidate qualification after the v0.20–v0.65 adversarial assurance campaign.

Qualification evidence:

- five consecutive orthogonal convergence passes with no new structural SPEC revision;
- v0.66 cumulative assurance regression;
- v0.67 exact Python/Node/Ruby RC-corpus reproduction;
- v0.68 specification/compatibility freeze audit.

Public RC documents:

- [Specification v1.0-rc1 Candidate](SPEC_v1.0-rc1.md)
- [Compatibility Contract v1.0-rc1 Candidate](COMPATIBILITY_v1.0-rc1.md)
- [RC Qualification v1.0-rc1](RC_QUALIFICATION_v1.0-rc1.md)
- [Public RC1 Reproduction Kit](public_repro_rc1/README.md)

Current status remains:

```text
v1.0-rc1 Candidate
Experimental
Not Production Ready
```

The v0.56 terminal boundary is normative: total loss of all independent trust anchors enters `EXTERNAL_TRUST_BOOTSTRAP_REQUIRED`; Bridge does not invent a new internal trust root.

---


### Experimental architecture RFCs
- [Agentic Containment Integrity, External Observability & Defensive Forensics](RFC_AGENTIC_CONTAINMENT_OBSERVABILITY_DEFENSIVE_FORENSICS.md) — treats shared substrates as potential side channels, peer messages as non-authoritative, safe exit as first-class, external telemetry as audit truth, and defensive forensics as a distinct policy plane.
- [Policy-Plane Separation & Non-Elevating Safety Exceptions](RFC_POLICY_PLANE_SEPARATION_SAFETY_EXCEPTION.md) — separates safety/wellbeing handling from eligibility, identity, authorization and tool capability; safety support must not become a privilege-escalation path.

- [Multi-Interface Execution & Verifiable Task Factory](RFC_MULTI_INTERFACE_EXECUTION_TASK_FACTORY.md) — interface-neutral task semantics, GUI/code/MCP/API route selection, cross-interface state-equivalence checks, trajectory evidence, and verifiable hybrid-task generation.

## Feedback and external review

Feedback is welcome through GitHub so that technical discussion stays attached to the public experiment.

Preferred channels:

- comment on [draft PR #22](https://github.com/Yelan22CAT/model1/pull/22);
- leave inline review comments on specific changed lines/files;
- open a GitHub Issue for a reproducible ambiguity, counterexample, security concern, compatibility break, or independent reproduction result.

Please include, when possible:

- the exact file/spec section;
- a minimal breaking example or counterexample;
- expected vs observed behavior;
- runtime/version information for reproduction;
- whether the issue affects semantics, trust, authorization, planning, execution, recovery, or compatibility.

Breaking examples and independent reproductions are more useful than general praise.

No private email address is required for review; GitHub notifications can deliver repository feedback according to each account's notification settings.

## Current RC governance state

The experiment remains **v1.0-rc1 Candidate / Experimental / Not Production Ready**.

Current governance and reproducibility state:

- protected `main` carries the authoritative RC governance baseline;
- **Material Projection v3** (`bridge-material-v3`) is the current externally witnessed material projection;
- Material Projection v1 and v2 remain frozen for historical witness interpretation;
- current material-state SHA-256: `1eaea2d0e7c106c973b78ab7209f33937bad12bbea78fb04303c151458a4ca93`;
- current external witness generation: **6**;
- off-GitHub witness surfaces currently use Google Drive + Gmail as two service surfaces inside one broader Google/account trust domain;
- private email addresses and raw provider object IDs are not public contact metadata;
- the public feedback path remains GitHub PR comments, inline reviews, and Issues;
- if the whole Google/account witness domain is unavailable or untrusted, the explicit boundary is `SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED`; GitHub alone does not recreate independent witness continuity.

Material Projection v3 additionally binds governance claim-scope fields and fails closed on unknown top-level or governance fields unless explicitly classified.


### Material Projection v3 canonicalization

Material Projection v3 NFC-normalizes all string values and object keys before canonical key sorting, rejects post-NFC key collisions, preserves array order, and serializes UTF-8 JSON. Historical v1/v2 witness semantics are not redefined.
