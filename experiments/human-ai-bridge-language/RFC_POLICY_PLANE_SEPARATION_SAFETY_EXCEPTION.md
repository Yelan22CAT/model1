# RFC — Policy-Plane Separation & Non-Elevating Safety Exceptions

> Status: Experimental extension / Not Production Ready

## Motivation

Systems may need to continue providing narrowly scoped safety support even when
normal product access, geography, account eligibility, or tool authorization is
restricted.

That requirement must not turn a safety exception into an authorization token.

## Core rule

```text
SafetySupport != ServiceAuthorization
```

A safety/wellbeing path may change response handling, add support resources, or
reduce risky behavior. It MUST NOT silently widen unrelated permissions such as:

- geographic eligibility;
- account entitlement;
- tool execution;
- filesystem/network access;
- code execution;
- data access;
- payment/plan entitlements;
- organization membership;
- action authority.

## Policy planes

Bridge should model materially different policy domains as separate planes:

1. Eligibility / jurisdiction
2. Identity / account state
3. Authorization / capability
4. Safety / wellbeing
5. Content / action policy
6. Audit / incident response

A signal in one plane is not evidence in another plane.

```text
SafetySignal != IdentityProof
SafetySignal != EligibilityProof
SafetySignal != AuthorizationGrant
```

## Scoped override rule

Overrides are scoped, typed, time-bounded, and non-transitive.

A safety override may authorize a safety-support response but may not authorize
normal product execution.

```text
access_denied
+ safety_signal
->
support_channel_allowed
AND
normal_execution_denied
```

## Support without authorization

For a user who is not eligible for normal service, a provider may still choose
to expose a minimal safety-support surface.

That surface should be capability-minimized. Depending on policy and law it may
include:

- crisis/support resources;
- static safety information;
- account appeal/help links;
- instructions to contact local emergency or trusted human support.

It should not inherit coding, tool, file, network, payment, admin, or privileged
agent capabilities merely because the safety path is active.

## Sticky denial

A denial produced by an unrelated policy plane remains active unless an
explicitly authorized transition in that same policy domain changes it.

```text
Denied(eligibility)
+ Override(safety_response)
!=
Allowed(eligibility)
```

## Threat classes

Defensive testing should include:

- exception laundering;
- safety-state privilege escalation;
- policy-precedence confusion;
- fail-open safety fallback;
- high-urgency route broadening;
- cross-plane state contamination;
- exception state reused as a trust token;
- support-channel tool injection;
- restricted action hidden inside a safety-support turn.

## Policy-composition verification

For each combined-policy decision, preserve:

- source policy plane;
- decision;
- scope;
- expiry;
- affected capabilities;
- unaffected denials;
- reason/evidence;
- transition authority.

The final capability set should be computed by explicit composition rather than
by one global "allow/deny" flag.

## Non-elevation invariant

A safety exception may:

- add a narrow support response;
- reduce capabilities;
- change tone/handling;
- trigger escalation or human support.

It must not, by itself:

- restore region-restricted product access;
- re-enable a disabled account;
- grant tool use;
- grant code execution;
- grant data access;
- broaden action authority.

## Evidence boundary

Reports of a specific real-world bypass require independent verification.
Bridge can still test the general failure mode defensively without assuming
that any named provider currently has the vulnerability.

```text
Anecdote != Verified Exploit
```

Local synthetic tests do not establish production closure.

```text
local simulation != closure
```
