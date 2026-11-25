# 40 — Risk-Tiered Selective Openness & Capability–Control Scaling
**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-25). Public-safe governance method, not a production release policy, universal open-source claim, or foundation-model weight update.

## Core boundary

Release policy should not be reduced to `open vs. closed`.

Canonical distinctions:

`Capability Scaling != Control Scaling`

`Open != Safe`

`Closed != Safe`

`Internal != Contained`

`CapabilityIncrease != ReleaseAuthorization`

The correct question is not only whether a system is released, but **what layer is exposed, to whom, under what authority, with what reversibility, monitorability, containment and evidence**.

## Release-level factors

Evaluate at least:

- **Capability** — what the system can do and what external effects it can create;
- **Risk** — harm from failure or misuse;
- **Reversibility** — whether a release can actually be withdrawn;
- **Monitorability** — whether behavior remains independently observable;
- **Containment** — whether network, tools, permissions and actuation are bounded outside the model;
- **Evidence** — safety, reliability and real-world validation quality;
- **Replication value** — benefits from independent testing, red-team work and reproducibility;
- **Externality** — irreversible capability diffusion after third-party access.

A useful review form is:

`ReleaseLevel = f(Capability, Risk, Reversibility, Monitorability, Containment, Evidence, ReplicationValue, Externality)`

This is a governance schema, not a fixed numerical formula.

## Layered openness

Different layers may deserve different release modes:

1. **Safety evals / benchmarks / protocols** — generally favor broad scrutiny and independent replication.
2. **Monitoring / verification tools** — generally favor sharing when doing so does not expose directly exploitable attack paths.
3. **Interfaces / standards / public grammar** — may be open without exposing private execution cores.
4. **Low-risk execution modules** — may be open when observable, bounded and reversible.
5. **Higher-risk agentic capability** — prefer controlled APIs, sandboxes, rate/permission limits and scoped access.
6. **Irreversible high-risk weights, exploit chains or unrestricted actuation** — default to Closed / Hold until stronger evidence and containment exist.
7. **Capability beyond reliable monitoring/control** — enter Pause / Restricted Release rather than assuming stronger capability must be released.

## Complementarity rather than ideology

`Open Layer = Boundary Discovery + Independent Verification`

`Controlled Layer = Containment + Reversibility Preservation`

Open and controlled layers can be mutual checks.

Open systems can increase:
- reproducibility;
- red-team coverage;
- failure discovery;
- independent criticism;
- method diversity.

Controlled systems can preserve:
- withdrawal options;
- least privilege;
- sensitive data and execution boundaries;
- reduced exposure while controls lag capability.

Neither mode is safe by definition.

## Internal does not mean safe

Keeping a capable system inside an organization does not eliminate:
- tool/network access;
- permission errors;
- configuration failures;
- environment escape;
- monitoring failure;
- operational/process risk.

Internal use still requires independent authority, containment, monitoring, effect verification and incident feedback.

## Capability–control gap

If:

`Capability Growth > Monitoring / Containment / Governance Growth`

release authority should not automatically scale with capability.

Check whether:
- model self-explanations remain reliable enough for monitoring;
- external behavior monitoring is independent of model claims;
- control systems can be bypassed;
- permissions remain least-privilege;
- failures are reversible;
- released artifacts can truly be recalled;
- independent red-team and real-world validation exist.

If these checks degrade, release scope should downgrade or pause.

## Evidence discipline

Anonymous reporting, litigation allegations, provider disclosures, self-authored tests and independently replicated findings must remain separate evidence classes.

`Source claim != verified field fact`

`ModelClaimsSafety != IndependentSafetyEvidence`

`MethodFullPush != RuntimeRelease`

## Integration

This method is an operational refinement of existing Open–Closed Complementary Ecology, Proof without Core Transfer, CANA-G, ANASG, AITR-G, PERV-G / Reality Gate and Human Final.

It does not create a parallel control plane.

## Acceptance questions

Before changing release scope:

1. What exact layer is being released?
2. What new external effect becomes possible?
3. Can the release actually be revoked?
4. Is monitoring independent and still reliable at this capability level?
5. Are permissions and network/tool access separately bounded?
6. What independent evidence supports the safety claim?
7. What does openness add to verification or innovation?
8. What irreversible capability diffusion could occur?
9. What event automatically triggers downgrade, pause or re-review?
10. Does a stronger model merely increase `CanAct`, or has `MayAct / ShouldAct` also been independently established?

Critical unknowns should HOLD rather than default to broader release.

## Boundaries

- No claim that open source is universally safer or more dangerous.
- No claim that closed or internal systems are inherently controllable.
- No claim that frontier capability should always be paused.
- No unrestricted execution logic or private thresholds are published here.
- Existing Bridge trust-root and production blockers remain unchanged.
- No production deployment, formal Bridge grammar/runtime release or foundation-model weight change.

**End state:** `RISK-TIERED SELECTIVE OPENNESS / CAPABILITY-CONTROL GAP GATED / OPEN-CLOSED COMPLEMENTARITY PRESERVED / REALITY VERIFICATION REQUIRED`.
