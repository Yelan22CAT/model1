# Single-Action Control Review — Public Method Note

**Date:** 2026-09-18  
**Status:** Human-reviewed method summary; documentary design only. No code installed, tests run, operational protection demonstrated, or external repository certified.

## Question

Some tools expose a single visible action—pause, refuse, block, ask, disable, or withhold a completion claim—but the useful design lies behind that action. Review the trigger, evidence, authority, failure behavior, scope, and resumption conditions rather than ranking projects by GitHub stars.

This method complements the existing Human Catch-up Gate and the Dual-Key Resume Lock. It does **not** disclose or replace private Model Root internals.

## Minimal review worksheet

For any candidate, record:

1. **Visible action:** Exactly what can it do, and at what lifecycle point?
2. **Decision basis:** Which inputs and evidence states are distinguished? Is a failed lookup different from a verified absence?
3. **Authority:** Who defines the policy, approves exceptions, and decides whether execution can restart?
4. **Failure behavior:** If the hook, data source, or adapter fails, does the control block, defer, warn, or silently disappear?
5. **Scope:** Does it affect one request, one agent, a feature, a project, or a whole fleet?
6. **Trace:** Can a reviewer tell why it acted or declined to act, without treating a successful tool invocation as proof of a valid conclusion?
7. **Recovery:** Are state changes, repeated requests, and irreversible effects considered before restarting?
8. **Evidence of effectiveness:** Are demonstrations, unit tests, host compatibility, and production outcomes clearly separated?

## Public observations from external source material

These are examples of design questions, not endorsements or security assessments:

| External example | Visible primitive | Narrow lesson for review |
| --- | --- | --- |
| [PolicyApprovalGate](https://github.com/nobuo-miura/PolicyApprovalGate) | deny / ask before tool use | Inspect deterministic policy checks and host-specific limits. |
| [handrail](https://github.com/svyatov/handrail) | block a matching call | Check effective rule precedence and explicitly reported adapter degradation. |
| [abstain](https://github.com/seekdaseek/abstain) | refuse an action | Keep observed absence separate from missing measurements; record refusals. |
| [leadline](https://github.com/Nazim22/leadline) | withhold completion | Verify that actual evidence meets the task obligation, not merely that a tool was invoked. |
| [guardplane](https://github.com/mkadri85/guardplane) | pause an agent | Examine intervention scope, reversibility, and human escalation. |
| [AgentFuse](https://github.com/SuperMarioYL/agentfuse) | stop at budget | Treat resource expenditure as a decision condition; distinguish estimates from bills and bypass traffic. |
| [feature-flag-rs](https://github.com/mizcausevic-dev/feature-flag-rs) | disable a feature | Distinguish disabling future behavior from undoing earlier effects. |
| [human-mcp](https://github.com/LIghtJUNction/human-mcp) | ask a person | Make the task, authority, timeout, and handoff explicit. |
| [agentic-abstention-mini](https://github.com/tonbistudio/agentic-abstention-mini) | stop futile attempts | Measure both late stopping and mistaken early stopping; its own README labels its experiment educational. |

Read each upstream repository's current code, tests, license, and limitations before considering any implementation. These links indicate source provenance, not approval to copy software or data.

## Public synthesis

A single action is an **interface**, not a complete control. A plausible design separates:

```text
observable state / declared evidence
  -> bounded evaluation
  -> action: continue | pause | deny | ask | abstain
  -> explicit reason and trace
  -> independent review before consequential resumption
```

A `Stop` hook that blocks an unsupported completion claim is not the same as a pre-execution pause. A feature disablement is not rollback. A tool call is not a verified result. Missing data is not evidence of zero. These distinctions should be assessed individually.

## Demonstration versus deployment

This document records a comparative reading exercise and an assessment method only. It does not claim a complete GitHub census, repository security audit, benchmark reproduction, runtime integration, hardware safety approval, or an enabled stop switch. Operational deployment requires separate authorization, independent testing, and documented control ownership.

**Publication boundary:** Public educational abstraction only; no private cases, thresholds, observer packs, calibration chains, internal anti-poisoning design, or unrestricted execution controls are published here.
