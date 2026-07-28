# Control Vocabulary — Public Interface Layer

> A public translation layer for coders, GRC readers, AI safety readers, and risk-oriented reviewers.  
> This file does not change Model 1 v1.0. It maps the public judgment interface into adjacent control-language vocabulary.

## 1. Purpose

Adjacent fields already use terms such as:

```text
gate
human-in-the-loop
approval gate
audit trail
policy enforcement
risk scoring
agent safety
kill switch
circuit breaker
rollback
confidence state
evidence quality
```

Model 1 v1.0 may look similar at the vocabulary level, but its control target is different.

Most adjacent systems ask:

```text
How should an AI system, agent, platform, or enterprise workflow execute safely?
```

Model 1 v1.0 asks:

```text
What is fact, inference, and unknown?
What does the present evidence say about my proposed next step?
Should I preserve the right to pause, audit, roll back, exit, or refuse continuation?
```

This repository is not an AI governance platform, enterprise GRC toolkit, agent execution gate, or risk-scoring product.

It is a **human judgment gate**.

## 2. Core distinction

| Adjacent pattern | Model 1 v1.0 position |
| --- | --- |
| Agent execution gate | Human judgment gate |
| AI decides whether to proceed | Human retains final judgment |
| System policy enforcement | First-person boundary preservation |
| Automated control plane | Human-owned pause / stop / exit layer |
| Risk score drives workflow | Direction and signal inform human review |
| Confidence score | Bounded fact / inference / unknown separation |
| Compliance artifact | Decision trace / judgment scaffold |

## 3. Two-axis public output

Model 1 separates two outputs that are often incorrectly collapsed.

### Evidence direction

| Model 1 direction | Adjacent language | Important difference |
| --- | --- | --- |
| `+` Support | evidence supports / positive case | Bounded by present scope and evidence; not approval. |
| `0` Unresolved | insufficient evidence / indeterminate | A valid state that preserves judgment; not hidden approval or rejection. |
| `-` Oppose | evidence against / negative case | Describes the current case against the path; not punishment or automatic denial. |

### Action-risk signal

| Model 1 signal | Adjacent language | Important difference |
| --- | --- | --- |
| Green | low-risk state / pass condition | No stop-loss trigger identified; not permission to execute. |
| Yellow | warning / hold / degraded assurance | Slow down, verify, preserve options; not automatic continuation. |
| Red | high-risk state / stop condition | Freeze or exit may be reasonable; not retaliation, blocking, or punishment. |

Direction asks what the evidence says. Signal asks how strongly the person should pause before acting.

## 4. Vocabulary mapping

| Model 1 term | Adjacent control-language term | Important difference |
| --- | --- | --- |
| **Observation / Verified fact** | source-backed evidence | Verification is bounded and current; it is not permanent truth. |
| **Hypothesis / Inference** | candidate interpretation | Must preserve uncertainty and alternatives. |
| **Verification Pending / Unknown** | incomplete evidence state | Must not be filled with model guesses merely to complete a workflow. |
| **Deprecated** | retired state / superseded version | Preserved for history but no longer active. |
| **Semantic localization** | presentation layer / user-facing wording | Wording may change; canonical state must not. |
| **Human Final Gate** | human-in-the-loop / approval gate | The human does not merely approve an AI action; the human owns final judgment and responsibility. |
| **Freeze** | circuit breaker / risk hold | A pause for human review, not automatic enforcement or punishment. |
| **Scope Lock** | policy scope / use-case boundary | Prevents misuse before analysis, especially profiling or manipulation. |
| **Boundary Check** | constraint validation | The constraint belongs to the human user; it is not a system optimization target. |
| **Consequence Check** | impact / blast-radius review | Focuses on the real-world effect of the proposed next action. |
| **Cost / Reversibility Check** | rollback / exposure check | Focuses on whether the human can still stop, correct, withdraw, or return to baseline. |
| **Reversal condition** | falsifier / decision-changing evidence | States what evidence would materially change the current conclusion. |
| **Compact decision-support output** | structured decision summary | Shows conclusion, evidence, unknowns, reversal condition, and one safe next step without claiming hidden reasoning is proof. |
| **Referee Trace** | audit trail / decision trace | Explains the visible judgment surface; it is not compliance certification or legal defense. |
| **Exit Key** | rollback / optionality | Protects the user's ability to stop participation without further irreversible cost. |
| **First-person-only boundary** | data minimization / misuse prevention | Evaluates the user's own exposure and next step, not another person's psychology or weaknesses. |
| **Anti-weaponization** | abuse-prevention control | Prohibits persuasion, manipulation, profiling, pressure, and human ranking. |

## 5. Safe interpretation

```text
Model 1 v1.0 is a first-person judgment guardrail.
It separates evidence state from action-risk posture.
It preserves human pause, verification, rollback, exit, and final responsibility.
```

For a coder:

```text
Do not ask only how to run the workflow.
Ask what is verified, what remains unresolved,
and whether the next step should continue without a human pause.
```

For a risk reader:

```text
Do not treat the model as a compliance framework or scoring system.
Treat it as a narrow scaffold for uncertainty-aware human judgment
under rising consequence and reduced reversibility.
```

## 6. Unsafe interpretation

The following uses are out of scope:

```text
Use + / 0 / - to rank people.
Use Green / Yellow / Red to automate blocks, punishment, or access denial.
Use Model 1 to decide who is risky.
Use the framework as a compliance badge.
Use it as an enterprise AI governance platform.
Use it as an agent execution controller.
Reconstruct private thresholds, observers, market models, or anti-poisoning internals.
```

## 7. Workflow posture mapping

| Evidence direction | Risk signal | Possible posture | Meaning |
| --- | --- | --- | --- |
| `+` | Green | GO_WITH_REVIEW | Evidence supports the path and no stop-loss trigger is identified; human review still owns execution. |
| `+` | Yellow | PAUSE | Evidence may support the path, but consequence, rollback, or ownership requires more review. |
| `0` | Yellow | PAUSE / ASK_HUMAN | Evidence is unresolved; gather information and preserve options. |
| `0` | Red | STOP / ESCALATE | Evidence is unresolved and a hard control, validation, or authorization gap is present. |
| `-` | Yellow | PAUSE / RECONSIDER | Evidence currently opposes the path; choose a reversible alternative or gather decisive evidence. |
| `-` | Red | STOP | Evidence opposes the path and a hard boundary or irreversible-risk condition is present. |
| not evaluated | any | ESCALATE | Professional, emergency, or out-of-scope judgment requires the proper human authority. |

This mapping creates no execution authority.

## 8. Public version boundary

Public v1.0 exposes only a narrow scaffold:

```text
Scope Lock
Fact / Inference / Unknown separation
Evidence Direction: + / 0 / -
Boundary / Consequence / Reversibility Check
Green / Yellow / Red Risk Signal
Compact Decision-Support Output
Human Final Gate
```

Public v1.0 does not release:

```text
private case chains
runtime thresholds
observer packs
calibration chains
detailed market or interaction models
anti-poisoning implementation internals
enterprise GRC mappings
policy enforcement mechanisms
agent execution logic
```

## 9. One-line distinction

```text
Adjacent systems often control how AI executes;
Model 1 preserves how a human separates evidence from uncertainty
and decides whether to pause, stop, audit, roll back, exit,
or refuse continuation before execution proceeds.
```
