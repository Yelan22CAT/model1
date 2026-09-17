# Method 07 — Dual-Speed Development and Evidence-Gated Release

> A public, employer-readable change-and-release review method for mixed hardware, software and AI work. This is a **design and documentation sample**, not an implemented process, safety certification, installed controller or automated release system.

## Purpose

A software module may be cheap to revise while its physical interface, purchased parts, test evidence or operational consequences are expensive to change. The goal is not to force every team into one lifecycle, but to ask: **what evidence and approval are required when a fast-moving component crosses a slower or safety-relevant system boundary?**

Use this method during a consequential change review, integration planning, supplier/component substitution, AI-assisted release proposal, or operational reassessment. Scope it to the actual product, hazards and responsible owner; the examples here are synthetic.

## Distinguish four commonly conflated mechanisms

| Term | What it describes | What it does not imply |
| --- | --- | --- |
| Waterfall | A largely sequential development lifecycle | Every review or release gate must be waterfall |
| Stage-Gate | Project milestones with explicit review or go/hold decisions | All work between gates must be strictly sequential |
| Agile | Iterative/adaptive delivery and feedback practices | Evidence, documentation and formal reviews can be skipped |
| CI/CD | Practices for frequent integration and delivery/deployment | A green pipeline certifies a physical product or authorizes deployment |

This is not a claim that one method has disappeared or universally dominates a particular industry. NASA's [Software Life Cycle guidance](https://swehb.nasa.gov/spaces/7150/pages/16449735/SWE-019%2B-%2BSoftware%2BLife%2BCycle) discusses multiple lifecycle choices, including waterfall and iterative approaches. Robert Cooper's [2024 article distinguishing Stage-Gate from waterfall](https://doi.org/10.1109/EMR.2024.3426228) addresses a common terminology error; the [2016 Agile–Stage-Gate hybrid paper](https://www.researchgate.net/publication/301567196_The_Agile-Stage-Gate_Hybrid_Model_A_Promising_New_Approach_and_a_New_Research_Opportunity) documents their combination in physical-product development. These sources do not verify the practices of any specific employer.

## Public architecture

```text
Documented requirements / accountable owner
       |
       +--> Software or AI: small iteration → test → revise --+
       |                                                      |
       +--> Physical product: design → prototype → verify ----+
                                                              |
                  Changed interface and dependency review <--+
                                  |
                     Evidence and safety review
                                  |
                      Accountable release decision
                                  |
                    Observe deployed or test outcome
                                  |
                 Reassess on a material state change
```

A local prototype can iterate without automatically granting authority to modify an integrated product. Phase transitions and approvals should be proportionate to the actual change and consequences.

## Seven review questions

1. **Scope:** What exactly changed: documentation, software, model, firmware, electrical component, mechanics, supplier, or the integrated system? Is the operating environment different?
2. **Evidence:** Which requirements and test results are current for this version? Which are stale, unsupported, unknown or contradicted by newer observations?
3. **Interface:** Could the change affect dimensions, units, timing, input/output contracts, power, data access, error behavior or compatibility?
4. **Propagation:** Which dependent components, suppliers, test plans and already released products may be affected? A change in one module can invalidate evidence in another.
5. **Safety and authority:** Are protective functions independently established? Who is authorized to approve a live or otherwise consequential release? AI proposals and test reports do not approve themselves.
6. **Release:** What acceptance criteria, test configuration, exceptions, rollback or containment options and sign-off apply to the actual scope?
7. **Reality:** What post-change observation would confirm the intended outcome? What material change or failure would reopen this review?

Keep the review proportional and auditable. Not every edit requires a full-system retest; every consequential change needs a justified decision about which evidence must be refreshed.

## Synthetic example: a sensor interface revision

A hypothetical equipment team updates a software classifier after changing a sensor component. The classifier passes its unit tests, but the replacement sensor uses a different scaling convention. Before using the new pair on live machinery, a reviewer identifies the changed interface, checks conversion and fault behavior, tests the integrated configuration, confirms that independent protective functions remain effective, and records the authorized disposition. If data or tests are missing, hold that release and continue only scoped non-consequential testing.

This example is invented for teaching and does not describe an actual workplace, incident, product, regulatory result or test run.

## Relationship to other public methods

- [Method 04 — Change-Triggered Reassessment](04-change-triggered-reassessment.md): a material change may make earlier approval evidence stale; refresh what the change affects.
- [Method 06 — Reusable Workflows + Bounded Agentic Proposals](06-reusable-and-agentic-workflow-design.md): deterministic checks and optional AI proposals produce evidence and drafts, not automatic sign-off.
- [Public safety design principles](../safety/DESIGN_PRINCIPLES.md): preserve independent pause/review and human final authority.

## Compact reviewer output

```text
Change and affected versions:
Requirement / acceptance evidence:
Interface and dependency impact:
Evidence current / stale / missing:
Safety and control owner:
Tests completed / not performed:
Reversal or containment condition:
Decision required and responsible human:
Post-release observation / recheck trigger:
```

**Evidence boundary:** This public method demonstrates risk-based engineering governance. It contains no private employer incident, named third-party anecdote, proprietary configuration, internal observer pack, hidden thresholds, full private-engine structure or executable autonomous control. Publication of a Markdown page is not implementation, test success, compliance approval or authorization to operate a physical system.

**One-line principle:** Local iteration can be fast; crossing an interface, safety or consequential-release boundary requires current evidence and accountable authorization.
