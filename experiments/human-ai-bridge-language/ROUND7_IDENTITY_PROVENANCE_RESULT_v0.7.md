# Bridge-0 Round 7 — Identity / Provenance / Anti-Sybil Result

> Status: Experimental v0.7

## Latest executed CI result

```text
126 tests
126 passed
0 failed
```

The v0.7 end-to-end attested-independence demo also passed.

## New tested behaviors

Round 7 covers:

- identity ↔ voter binding;
- trusted attestation issuer policy;
- attestation expiry;
- attestation revocation;
- revocation issuer validation;
- fake voter alias rejection;
- fake independence-label rejection;
- shared model-lineage de-correlation;
- shared runtime-origin de-correlation;
- copied evidence-root de-correlation;
- vote evidence-hash/provenance binding;
- evidence provenance cycle rejection;
- finality still does not become factual truth.

## Stress result

The suite also tested:

```text
67 voters
67 distinct control domains
67 distinct model lineages
67 distinct runtime origins
67 independent evidence roots
→ valid certificate
```

## Main result

The current semantic pipeline now separates:

```text
voter ID
≠ identity
≠ attestation
≠ model lineage
≠ runtime origin
≠ evidence root
≠ finality
≠ truth
```

This is the first round where "independent confirmation" is no longer based only on a user-supplied label.

## Important limitation

The prototype's trusted issuer is still a semantic/configuration concept.

It does not cryptographically prove that an attestation was really issued by that authority.

So the new boundary is:

```text
semantically valid identity chain
≠ cryptographically proven identity chain
```

The next production-oriented layer would need real trust roots / signatures / runtime attestation.

## Bounded conclusion

Within the tested v0.7 semantics, common aliasing and copied-evidence patterns could no longer inflate an independence quorum merely by changing voter names or labels.

This is not full Sybil resistance and does not prove external-world truth.
