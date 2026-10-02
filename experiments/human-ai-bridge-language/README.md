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
■ age = ?
◆ evidence = none
```

Bridge rule:

```text
? + no ◆  →  × assert-as-fact
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
