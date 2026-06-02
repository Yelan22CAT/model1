# Control Vocabulary — Public Interface Layer

> A public translation layer for coders, GRC readers, AI safety readers, and risk-oriented reviewers.  
> This file does not change Model 1 v1.0. It only maps Model 1 terms to adjacent control-language vocabulary.

## 1. Purpose

Many adjacent fields already use words such as:

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
```

Model 1 v1.0 may look similar at the vocabulary level, but its control target is different.

Most adjacent systems ask:

```text
How should an AI system, agent, platform, or enterprise workflow execute safely?
```

Model 1 v1.0 asks:

```text
How does a person preserve the right to pause, stop, audit, exit, or refuse continuation before irreversible cost increases?
```

This repository is therefore not an AI governance platform, not an enterprise GRC toolkit, and not an agent execution gate.

It is a **human judgment gate**.

## 2. Core distinction

| Adjacent pattern | Model 1 v1.0 position |
| --- | --- |
| Agent execution gate | Human judgment gate |
| AI decides whether to proceed | Human retains final judgment |
| System policy enforcement | First-person boundary preservation |
| Automated control plane | Human-owned pause / stop / exit layer |
| Risk score drives workflow | Signal informs human review |
| Compliance artifact | Decision trace / judgment scaffold |

## 3. Vocabulary mapping

| Model 1 term | Adjacent control-language term | Important difference |
| --- | --- | --- |
| **Human Final Gate** | human-in-the-loop / approval gate | The human does not merely approve an AI action; the human owns the final judgment and responsibility. |
| **Freeze** | circuit breaker / risk hold | Freeze is a pause for human review, not automatic enforcement or punishment. |
| **Red Signal** | high-risk state / stop condition | Red indicates a stop-loss trigger; it does not authorize retaliation, blocking, punishment, or automated action against anyone. |
| **Yellow Signal** | warning state / degraded confidence | Yellow means slow down and preserve options; it does not mean “continue automatically with caution.” |
| **Green Signal** | low-risk state / pass condition | Green means no stop-loss trigger was identified from the stated input; it is not permission to execute. |
| **Scope Lock** | policy scope / use-case boundary | Scope Lock prevents misuse before analysis begins, especially third-person profiling or manipulation. |
| **Boundary Check** | constraint validation | The constraint belongs to the human user; it is not a system-imposed optimization target. |
| **Cost / Reversibility Check** | rollback / blast-radius / exposure check | The focus is whether continuing reduces the human's ability to stop, recover, or return to baseline. |
| **Referee Trace** | audit trail / decision trace | Trace explains how judgment was reached; it is not a compliance certification or legal defense. |
| **Exit Key** | rollback / optionality / reversibility | Exit protects the user's ability to stop participation without further irreversible cost. |
| **First-person-only boundary** | data minimization / misuse prevention | The model evaluates the user's own exposure and next step, not another person's psychology or weaknesses. |
| **Anti-weaponization** | abuse-prevention control | The model must not be converted into persuasion, manipulation, profiling, or pressure tooling. |

## 4. What this file is not

This file is not:

- an ISO 42001 mapping
- a NIST AI RMF mapping
- an EU AI Act compliance guide
- a GRC control catalog
- a policy enforcement design
- a risk scoring methodology
- an agent safety benchmark
- a software implementation plan

Those frameworks may use adjacent vocabulary, but Model 1 v1.0 should not be inflated into a governance platform.

## 5. Safe interpretation

A safe interpretation is:

```text
Model 1 v1.0 is a first-person decision guardrail.
It helps identify when continued participation may create irreversible cost.
It preserves human pause, audit, exit, and final judgment.
```

For a coder, this means:

```text
Do not ask only how to run the workflow.
Ask whether the next step should be allowed to continue without a human pause.
```

For a risk reader, this means:

```text
Do not treat the model as a compliance framework.
Treat it as a narrow judgment scaffold for preserving human control under rising cost and reduced reversibility.
```

## 6. Unsafe interpretation

An unsafe interpretation is:

```text
Use Model 1 to score people.
Use Model 1 to decide who is risky.
Use Model 1 to automate stops, blocks, punishments, or escalations against others.
Use Model 1 as a compliance badge.
Use Model 1 as an enterprise AI governance platform.
Use Model 1 as an agent execution controller.
```

These uses are out of scope.

## 7. Go / Pause / Stop language

Coder-facing or workflow-facing readers may translate the public signal into posture language:

| Public signal | Control posture | Meaning |
| --- | --- | --- |
| Green | GO_WITH_REVIEW | No stop-loss trigger identified; human review still owns execution. |
| Yellow | PAUSE | Risk, ambiguity, or reduced reversibility is increasing; preserve rollback and check facts. |
| Red | STOP | Boundary or irreversible-cost risk is present; freeze or exit is reasonable. |
| Unknown | ASK_HUMAN | Missing information prevents safe interpretation. |
| Professional / emergency / high-consequence domain | ESCALATE | Route to qualified human, responsible owner, or proper authority. |

This mapping does not create execution authority.

## 8. Public version boundary

Public v1.0 exposes only a narrow scaffold:

```text
Scope Lock
Boundary Check
Cost / Reversibility Check
Green / Yellow / Red Signal
Human Final Gate
```

Public v1.0 does not release:

```text
private case chains
runtime thresholds
observer packs
calibration logic
Model2 / Model3 material
enterprise GRC mappings
policy enforcement mechanisms
agent execution logic
```

## 9. One-line distinction

```text
Adjacent systems often control how AI executes; Model 1 controls whether a human should preserve the right to pause, stop, audit, exit, or refuse continuation before execution proceeds.
```
