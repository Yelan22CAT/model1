# Bridge-0 Conflict Set & Quorum Semantics v0.6

> Status: Experimental / many-agent reconciliation layer  
> v0.6 adds no new glyphs.

## Purpose

v0.5 kept split-brain state explicit but used pairwise conflicts:

```text
n branches
→ n(n-1)/2 pair records
```

v0.6 replaces that with one conflict set and adds a process for reconciliation evidence.

```text
many divergent states
→ one conflict_set
→ explicit proposal
→ quorum policy
→ independent votes
→ finality certificate
→ execution
```

## Conflict set

```text
◆ [CS1] conflict_set
  members=S1,S2,S3,S4,S5
  domain=authority
  status=open
```

A conflict set must exactly cover one divergent sibling group.

Missing members, extra members, duplicate members, or a set with no real divergence are rejected.

## Reconciliation proposal

```text
→ [P1] propose
  conflict_set=[CS1]
  strategy=explicit
  result_hash=hm
  at=...
```

Automatic last-writer reconciliation remains forbidden.

## Quorum policy

```text
! [Q1] quorum
  voters=validator_a,validator_b,validator_c,validator_d,validator_e
  threshold=3
  independence_min=3
```

Two separate thresholds exist:

1. distinct authorized voters;
2. distinct independence domains.

This is deliberate.

```text
3 votes
from
1 correlated source lineage
≠
3 independent confirmations
```

## Vote

```text
◆ [V1] vote
  voter=validator_a
  proposal=[P1]
  decision=approve
  independence=model_family_a
  evidence_hash=ev1
  at=...
```

Allowed decisions:

```text
approve
reject
abstain
```

Only approve votes can contribute to a finality certificate.

## Finality certificate

```text
✓ [FC1] certificate
  proposal=[P1]
  quorum=[Q1]
  votes=V1,V2,V3
  issued_by=control_plane
  term=1
  at=...
```

The certificate validates the governance/process condition.

It does **not** promote the proposal into a factual claim about the external world.

```text
quorum finality
≠
truth
```

## Execution

```text
→ [X1] execute
  actor=agent_a
  action=deploy
  state=[P1]
  finality=[FC1]
  at=...
```

Execution must reference a certificate that finalizes the exact proposal being executed.

## New validator rules

```text
V044 snapshot lineage validity
V045 conflict_set validity
V046 many-way divergence coverage
V047 reconciliation proposal validity
V048 quorum-policy validity
V049 vote validity
V050 finality-certificate identity / issuer
V051 certificate vote integrity
V052 voter + independence thresholds
V053 certificate term validity
V054 exact-state certificate-bound execution
```

## Scaling tests

### Conflict scaling

The stress suite used:

```text
100 divergent branches
→ 1 conflict_set
```

instead of:

```text
100 branches
→ 4,950 pairwise conflicts
```

### Quorum scaling

The suite also used:

```text
101 eligible voters
67-vote threshold
67 distinct independence domains
→ 1 finality certificate
```

The prototype remained deterministic.

## Critical boundary discovered

The language can enforce that the *labels* for voter identity and independence are distinct.

It cannot prove that:

```text
validator_a
validator_b
validator_c
```

are truly controlled by independent actors or systems.

A malicious operator could lie about identity or independence labels unless an external identity / provenance / attestation layer verifies them.

Therefore:

```text
declared independence
≠
verified independence
```

This becomes the next high-value boundary.

## Non-goals

v0.6 is not:

- a distributed-consensus protocol;
- a proof that majority opinion is true;
- cryptographic identity verification;
- Sybil resistance;
- Byzantine-fault tolerance;
- production access control.

It is a semantic contract that keeps disagreement, reconciliation, voting provenance, and finality distinct.
