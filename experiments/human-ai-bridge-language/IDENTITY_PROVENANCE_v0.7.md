# Bridge-0 Identity & Evidence Provenance v0.7

> Status: Experimental / anti-Sybil semantic layer  
> v0.7 adds no new glyphs.

## Purpose

v0.6 could distinguish multiple declared voters and declared independence domains.

It could not answer:

> Are these actually independent sources, or are they aliases of the same model/runtime/operator/evidence?

v0.7 therefore adds explicit identity, attestation, runtime/model lineage, and evidence provenance.

The new target is:

```text
vote
→ identity
→ attestation
→ control domain
→ model lineage
→ runtime origin
→ evidence provenance
→ quorum
```

## Identity

```text
○ [I1] identity
  subject=validator_a
  control_domain=org_a
  model_lineage=model_a
  runtime_origin=runtime_a
```

These dimensions remain separate.

## Attestation

```text
◆ [AT1] attest
  identity=[I1]
  issuer=identity_ca
  status=valid
  valid_from=...
  valid_until=...
```

Attestation can later be revoked:

```text
× [AR1] revoke_attestation
  target=[AT1]
  by=identity_ca
  at=...
```

The current prototype validates semantic issuer/binding/time rules.

It does **not** yet implement cryptographic signatures or PKI.

## Evidence provenance

```text
◆ [EP1] evidence_provenance
  evidence_hash=ev1
  source_identity=[I1]
  attestation=[AT1]
  origin=sensor_a
  parent=none
  at=...
```

Derived/copied evidence points back to a provenance parent instead of pretending to be a fresh independent source.

## Attested vote

```text
◆ [V1] vote
  voter=validator_a
  proposal=[P1]
  decision=approve
  independence=org_a
  evidence_hash=ev1
  identity=[I1]
  attestation=[AT1]
  provenance=[EP1]
  at=...
```

The voter name, identity subject, declared independence label, attestation, and evidence provenance must agree.

## Independence de-correlation

A certificate must satisfy independence across multiple dimensions:

```text
distinct control domains
distinct model lineages
distinct runtime origins
distinct evidence roots
```

So:

```text
three aliases
→ same model backend
→ not three independent confirmations
```

and:

```text
three voters
→ copied from one evidence root
→ not three independent evidence sources
```

## Evidence threshold

v0.7 adds:

```text
evidence_min
```

to quorum policy.

Example:

```text
! [Q1] quorum
  voters=A,B,C
  threshold=3
  independence_min=3
  evidence_min=3
```

The certificate must satisfy all three conditions.

## New validator rules

```text
V055 identity integrity
V056 attestation binding / trusted issuer / validity
V057 attestation revocation validity
V058 evidence provenance binding
V059 vote-to-identity/attestation binding
V060 vote-to-evidence provenance binding
V061 evidence_min validity
V062 evidence provenance cycle rejection
V063 attested control/model/runtime independence
V064 independent evidence-root threshold
```

## Important boundary

The current v0.7 prototype can validate:

- that identity fields are internally consistent;
- that an attestation comes from a configured trusted issuer name;
- that votes bind to identity and provenance records;
- that independence is de-correlated across recorded dimensions.

It cannot prove that the issuer itself is authentic.

Therefore:

```text
semantic attestation
≠
cryptographic attestation
```

Production-grade identity would require an external trust mechanism such as:

- cryptographic signatures;
- device/runtime attestation;
- certificate chains;
- hardware-backed identity;
- independent registry / trust root.

Bridge should carry those results, not invent them.

## Core principle

```text
many voices
≠ many independent sources
```

and:

```text
many independent sources
≠ truth
```

They improve evidence quality, but reality verification remains a separate layer.
