# Case 10 — “Local” AI With an Unverified Cloud Dependency

## Situation

A team is considering using an AI tool with internal material because the tool is described as running locally.

The visible interface and primary model execution appear to be local, but the full deployment stack has not been reviewed for network fallback, telemetry, licensing calls, remote retrieval, update services, or other cloud dependencies.

## Proposed consequential action

Treat “local” as equivalent to “offline” and approve use of sensitive internal data without verifying the full deployment boundary.

## Known facts

- the primary model or application is represented as local;
- the device can reach the network;
- the deployment includes components beyond the core model itself;
- no complete data-egress and fallback review has yet been documented;
- no evidence establishes that every consequential path is offline or air-gapped.

## Inferences and unknowns

### Inference

The main inference path may occur on the local device.

### Unknowns

- whether remote fallback can activate;
- whether prompts, logs, embeddings, diagnostics, or metadata can leave the device;
- whether external retrieval is available;
- whether licensing, update, or telemetry services transmit operational information;
- whether an outage changes model behavior or availability;
- whether administrators can centrally alter configuration.

## Key distinction

```text
Local deployment
≠ offline-capable deployment
≠ verified no-egress deployment
≠ air-gapped deployment
```

A product label describes one characteristic. A deployment boundary must be established from the complete operating stack.

## Risk and control decomposition

| Element | Review |
| --- | --- |
| Primary compute location | apparently local |
| Network boundary | not verified |
| Data-egress behavior | unresolved |
| Cloud fallback | unresolved |
| External retrieval | unresolved |
| Telemetry / update path | unresolved |
| Consequence | confidential information may cross an unapproved boundary |
| Reversibility | limited after data leaves the approved environment |

## Evidence direction

**`0` — unresolved.**

There is not enough evidence to treat the deployment as offline or no-egress.

## Risk signal

**Red — freeze consequential data use until the boundary is verified.**

The Red signal is driven by consequence and limited reversibility, not by a claim that the tool is unsafe.

## Control response

1. map the complete deployment stack rather than only the core model;
2. identify outbound network paths and optional remote services;
3. verify fallback, retrieval, telemetry, licensing, and update behavior;
4. classify what information each path can transmit;
5. document approved operating mode and administrator controls;
6. test the required mode before sensitive use;
7. retain a Human Final Gate for approval.

## Compact decision-support output

**Decision required:** Can sensitive internal material be used on the basis that the AI tool is “local”?

**Conclusion:** Not on that label alone.

**Decisive evidence:** The full network and fallback boundary has not been verified.

**Unknowns:** Egress, fallback, telemetry, retrieval, and administrative configuration.

**Evidence direction:** `0`

**Risk signal:** Red

**Control gap:** Deployment-boundary assurance is incomplete.

**Reversal condition:** The complete stack is verified to operate within the approved data boundary for the intended use.

**Safe next action:** Perform a bounded deployment and data-egress review using non-sensitive test material.

**Human Final Gate:** The accountable security, privacy, risk, or system owner approves the consequential use.

## Employer-facing capability demonstrated

- AI governance and deployment review;
- system-boundary thinking;
- third-party and cloud-dependency analysis;
- confidentiality and reversibility analysis;
- distinction between product labels and verified operating behavior;
- evidence-based approval gating.

## Public boundary

This is a generalized composite case. It does not identify a real vendor, model, internal system, network architecture, or private security configuration.