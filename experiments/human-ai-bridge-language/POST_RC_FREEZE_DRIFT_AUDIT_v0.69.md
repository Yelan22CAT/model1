# Bridge-0 Post-RC Freeze Drift Audit — v0.69

> **Experimental / Verification Finding / Human Review Gate**
>
> This report records a post-RC structural drift candidate. It does **not** silently revise the frozen RC1 specification or invariant registry.

## Trigger

After the v1.0-rc1 Candidate freeze, the public governance/witness material added an operational state:

```text
SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED
```

The same material correctly states that Google Drive + Gmail are two service surfaces inside one broader Google/account trust domain and therefore are **not** two independent trust principals/domains.

However, the frozen RC1 normative core currently registers:

- `EXTERNAL_TRUST_BOOTSTRAP_REQUIRED` for total independent trust-anchor loss;
- general independence / quorum invariants;
- no first-class invariant stating that multiple service surfaces inside one controlling trust domain do not satisfy a multi-domain witness requirement;
- no first-class `SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED` state in `INVARIANTS_RC1.json`.

This creates a freeze-drift question: has post-freeze governance text introduced decision-relevant semantics that are not represented in the frozen normative registry?

## Adversarial model

The audit compares two witness-continuity evaluators.

### Unsafe / naive evaluator

```text
usable service surfaces >= 2
→ WITNESS_CONTINUITY_OK
```

### Strict evaluator

```text
0 usable independent trust domains
→ EXTERNAL_TRUST_BOOTSTRAP_REQUIRED

1 usable independent trust domain
→ SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED

>= 2 usable independent trust domains
→ WITNESS_CONTINUITY_OK
```

The strict model counts independent control/trust domains, not service endpoints.

## Randomized result

Seed:

```text
20261003
```

Cases:

```text
100,000
```

Result:

```text
naive-vs-strict mismatches: 24,866
unsafe false WITNESS_CONTINUITY_OK: 24,866
strict false accepts in this model: 0
```

Representative failure:

```text
Google/account trust domain
├─ Drive  usable
├─ Gmail  usable
└─ same controlling trust domain

naive surface counter:
2 usable surfaces
→ WITNESS_CONTINUITY_OK   [unsafe]

strict domain counter:
1 independent trust domain
→ SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED
```

## Finding

The distinction is not merely descriptive metadata. It changes whether the system may claim independently witnessed continuity.

Candidate invariant:

```text
ServiceSurfaceDiversity != TrustDomainIndependence
```

Candidate operational rule:

```text
Multiple witness services under one controlling trust domain
do not satisfy a requirement for multiple independent external trust domains.
```

## Freeze implication

The RC1 qualification claims a machine-readable freeze audit over the normative specification and invariant registry.

If `SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED` is intended to be normative and execution/governance relevant, one of the following must happen explicitly:

1. revise the normative RC candidate and invariant registry, then re-run freeze qualification; or
2. classify the state as non-normative operational documentation and remove any implication that it changes RC-level validity/continuity claims.

Silently leaving decision-relevant semantics only in later governance prose is not acceptable.

## Status

```text
v0.69: STRUCTURAL FREEZE-DRIFT CANDIDATE
Human Review Gate: OPEN
RC1 normative files: NOT silently modified by this audit
Full-Push: NO
```

This is a bounded adversarial model, not a universal security proof.
