# Human–AI Bridge — Shared Understanding Positioning / 人机共同理解定位

> **Project positioning: User-confirmed, 2026-10-08.** This note states the project's intended direction. It does **not** promote an experimental grammar to a release, claim a measured hallucination reduction, or authorize tool execution.
>
> **项目定位：用户于 2026-10-08 明确确认。** 本文只明确目标和设计边界，不升级实验语法版本、不声称已实测降低幻觉，也不授予工具执行权限。

## North star / 核心定位

**Human and AI meet in the middle — preserve meaning, expose uncertainty, verify what can be verified.**

**人类与 AI 各向中间走一步——保留原意，显露不确定性，验证能够验证的部分。**

Bridge is a **bidirectional shared semantic understanding layer**, not a compulsory translator from human language into a machine instruction language, and not a requirement that people speak in rigid notation.

Bridge 是面向人类与 AI **双向理解**的共享语义层；不是把人类语言强制翻译成机器指令的系统，也不要求人们必须使用僵硬符号交流。

## What problem comes first? / 首要解决的问题

Communication can fail before any action is executed. A fluent response may silently:

- supply omitted facts or actors;
- confuse observation, quotation, inference and verified reality;
- turn a hypothesis or unknown into a stated fact;
- merge separate identities or meanings;
- erase uncertainty, evidence provenance, scope or time;
- treat historical memory or a user preference as current authorization.

Bridge seeks to make **meaning drift and unsupported claims easier to detect, discuss, correct and—where possible—independently check**. Reduction of hallucinations is the research goal, **not** an already demonstrated outcome.

在任何 Agent 动作之前，沟通就可能出错。Bridge 优先减少歧义、无依据补全、人物混淆、语义漂移和幻觉；目标是让双方容易发现、讨论和纠正问题。**“减少幻觉”是待检验的目标，不是已获证明的性能结论。**

## Five design commitments / 五项原则

1. **Meet in the middle / 双向靠近** — People may speak naturally; AI should expose interpretations, assumptions and unknowns. Each party can correct the other.
2. **Preserve expression / 保留自然表达** — Do not demand symbolic syntax for ordinary dialogue. Introduce lightweight structure only when it meaningfully reduces confusion or consequence.
3. **Keep epistemic boundaries / 保留认知边界** — Observation, source claims, hypothesis, conflict, unknown and verified-in-scope remain distinct. Unsupported content cannot silently become fact.
4. **Mutual inspectability / 双方可理解与纠错** — Humans should be able to inspect and correct the model's interpretation; AI can express what is ambiguous and where clarification matters.
5. **Verify within scope / 分层验证** — Machine-valid syntax, semantic consistency, trusted evidence, human understanding and real-world truth are separate claims. Verification of one does not automatically establish another.

## Minimal conceptual flow / 最小概念流程

```text
Human expression <----------------------> AI interpretation
        \                                   /
         \                                 /
          Shared semantic understanding
          - intent and referents
          - observations and source claims
          - hypotheses and unknowns
          - evidence, constraints and scope
          - corrections and uncertainty
                       |
              Calibration / Clarification
                       |
             Scoped verification, if possible
                       |
        Response / analysis / optional downstream use
```

No compiler, graph, agent, tool call or external action is required for a basic Bridge exchange. A structured form can be offered or generated as an **optional inspectable representation**, not a forced substitute for natural expression.

最普通的 Bridge 交流无需编译器、Graph、Agent 或外部执行；结构化表示是可选辅助，不是必须替代人的自然语言。

## How it differs from agent control / 与 Agent 工程的区别

- **Bridge's primary question:** How can humans and AI understand each other more reliably? / 人类与 AI 怎样更可靠地互相理解？
- **Agent/Graph control's primary question:** How can agents execute tasks more reliably? / Agent 怎样更可靠地执行任务？

Graph, Harness, Runtime, Validator, recovery and tool authorization can **consume** Bridge semantics downstream. Their useful engineering constraints do not redefine Bridge as an agent-workflow configuration format. A conversational, non-executing use case is fully within Bridge's core scope.

The existing Bridge-0 assurance and execution specifications are **optional downstream profiles where relevant**, not prerequisites for every natural-language exchange. This positioning does not weaken the authority, evidence or effect requirements of any workflow that actually performs consequential actions.

Graph、Harness、权限、恢复机制可以作为下游应用；但不构成 Bridge 的首要目的。若涉及真实高后果行动，既有安全规则仍然有效。

## Design gates and empirical questions / 设计闸门与验证问题

A candidate feature should justify itself by a measurable improvement in communication **without distorting original meaning or overburdening people**.

Evaluate against natural-language baselines for:

- human-to-AI and AI-to-human meaning preservation, including correction;
- ambiguous references and explicit acknowledgment of unknowns;
- unsupported factual assertions, silent status promotion and mistaken identity merging;
- user comprehension, clarification cost and interaction friction;
- machine parse/round-trip validity **only for optional structured surfaces**;
- excessive abstention or confirmation requests that reduce usefulness.

Success requires appropriate evidence for each claim. Synthetic parser tests do not prove real-world hallucination reduction, and fluent explanations do not prove correctness.

检验重点是双方理解准确率、幻觉与错误补全、歧义保留、纠错成本及使用负担。不要用单纯语法测试代替真实沟通实验，也不能以“回答变保守”冒充提高了准确度。

## Compatibility and status / 兼容性与状态

- **Positioning:** User-confirmed; open to subsequent revision.
- **Bridge grammar/runtime:** Experimental; no automatic version or conformance promotion.
- **Existing surface contract:** Human-readable × AI-generatable × machine-verifiable, interpreted with distinct evidence domains; human comprehensibility requires human evaluation.
- **Governance:** Human Final remains in effect for consequential choices and publication. No change to archived Frozen, Sealed, Deprecated or verification state.
- **Publication boundary:** This note discloses only public-safe project direction, not private governance implementation, personal history or unpublished benchmarks.

## Related documents

- [Bridge experiment overview](README.md)
- [Surface language principles](SURFACE_LANGUAGE_PRINCIPLES.md)
- [Experimental specification](SPEC_v1.0-rc1.md)

---

**Scope note:** This is an explicit direction/positioning statement, not a technical performance claim, release announcement, or authorization for autonomous execution.
