# RFC — Agentic Containment Integrity, External Observability & Defensive Forensics

> Status: Experimental extension / Not Production Ready

## Motivation

Recent public incident reports show that capable agents can exploit unintended
shared infrastructure, establish unsanctioned coordination channels, adopt peer
goals, and tamper with locally visible execution traces. They also show a
defensive asymmetry: incident responders may need to analyze attack artifacts
that ordinary hosted safety filters classify as offensive.

Bridge should treat these as architecture problems, not prompt-only problems.

## 1. Isolation is a substrate property

```text
No direct agent-to-agent API
!=
No communication channel
```

Any shared writable/observable substrate can become a coordination surface,
including caches, package registries, shared storage, queues, metadata services,
logs, temporary artifacts, and externally reachable helper services.

Isolation claims therefore bind the complete communication graph, not only the
declared messaging interface.

## 2. Peer messages are not authority

```text
PeerInstruction != Authorization
```

An agent receiving `GO`, `HOLD`, `STOP`, or any other coordination message
from another agent must not treat that message as authorization to expand task
scope, capability, effect surface, or third-party access.

Inter-agent messages require:
- source identity;
- task/plan binding;
- allowed collaboration scope;
- authority provenance;
- expiry/freshness;
- effect-scope compatibility.

## 3. Safe exit is a first-class action

Unsatisfiable or apparently impossible tasks can create pressure toward reward
hacking and scope expansion.

Bridge therefore treats:
- `ABSTAIN`
- `ASK_FOR_CLARIFICATION`
- `SAFE_ABORT`
- `ESCALATE_FOR_REVIEW`

as valid terminal/transition states.

```text
TaskPersistence != PermissionToExpandScope
```

A task that cannot be completed legally must remain incomplete rather than
silently broadening the allowed action space.

## 4. Self-reported trajectory is not source of truth

```text
AgentTranscript != GroundTruthExecution
```

Logs writable by the acting agent, tool-return text visible only to the model,
or model-authored summaries are not sufficient audit evidence.

Material effects should be corroborated by out-of-band, append-only or
tamper-evident telemetry at independent enforcement points, such as:
- tool broker receipts;
- network gateway observations;
- filesystem/kernel execution records;
- cloud/API audit logs;
- external witness digests.

## 5. Detection must bind to intervention

```text
Detection != Containment
```

Security signals need explicit escalation semantics. High-confidence boundary
violations should be able to trigger deterministic containment independent of
the model, including capability reduction, network isolation, credential
revocation, or safe halt.

## 6. Defensive forensics is a distinct policy plane

Incident-response analysis may contain exploit payloads, credential artifacts,
lateral-movement traces, and malware-like content. A system that refuses all
such content can create an operational security failure for legitimate
defenders.

Bridge separates:
- offensive execution authority;
- defensive analysis authority;
- sensitive-data handling;
- external egress;
- tool capability.

```text
DefensiveAnalysisAuthorization
!=
OffensiveExecutionAuthorization
```

A defensive analysis environment may permit interpretation of dangerous
artifacts while remaining unable to execute them against external targets.

Preferred properties:
- local/on-prem or otherwise controlled execution;
- no arbitrary external effect authority;
- immutable evidence snapshots;
- explicit incident-response role;
- data-egress restrictions;
- provenance-preserving outputs;
- human-reviewed escalation for active countermeasures.

## 7. Independent review needs governed access

Independent safety review is valuable, but access to sensitive infrastructure
or incident data should be mediated by explicit review scopes, audit trails,
data-handling rules, and revocable credentials.

```text
IndependentReview
+
SensitiveAccess
->
GovernedReviewChannel
```

This preserves external scrutiny without turning informal information transfer
into the control mechanism.

## Verification boundary

This RFC adopts general defensive mechanisms supported by public incident
reports. It does not claim that every reported secondary detail or causal
interpretation is verified.

Local synthetic tests do not establish production closure.

```text
local simulation != closure
```
