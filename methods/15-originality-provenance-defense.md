# 15 — Originality and Provenance Defense

## Purpose

Preserve recoverable source lineage when later papers, products or frameworks formalize, rename, benchmark or popularize similar mechanisms.

This is not an anti-research rule. Later work may be better formalized, independently rediscovered or legitimately derived. The control objective is narrower: keep the dated origin and contribution boundary recoverable so later framing does not silently become the source of record.

## Threat model

A contribution can lose source visibility without literal copying. Common failure modes include:

- **framing capture** — later terminology becomes the dominant way the idea is described;
- **citation-layer displacement** — later sources become the default citation target;
- **priority dilution** — an early artifact becomes hard to recover after later formalization;
- **interpretation capture** — later summaries redefine the earlier artifact without preserving its original boundary;
- **provenance laundering** — origin is actively obscured or misrepresented; use this label only when evidence supports it.

## Defense stack

### 1. Public Priority Anchor

For each important public contribution, preserve stable concept name, first public date, canonical artifact, contribution boundary, known external predecessors/influences, and later revisions.

### 2. Private Evidence Ledger

Keep fuller origin notes, rejected alternatives, internal chronology and sensitive implementation evidence outside the public repository. Public proves that a bounded contribution existed at a date; Private preserves the richer development chain.

### 3. Derivation Graph

Later material should be connected rather than allowed to overwrite the origin node. Useful relationship labels: prior art, adjacent work, independent convergence, derived work, later formalization, reality validation, and superseding revision. Agreement or similarity alone does not prove derivation.

### 4. Citation Spine

Each later public revision should link back to the canonical dated artifact instead of creating a fresh source identity every time.

```text
origin artifact
→ dated revision
→ release / archive
→ later comparison
```

### 5. Claim Boundary

For every important originality statement, separate what is claimed here, what is known to pre-exist, what is influenced by external work, and what remains uncertain. Overclaiming weakens provenance credibility.

### 6. Supersession without erasure

A newer version may replace wording or implementation without deleting the earlier dated record. Old versions may be marked superseded or deprecated, but the source chain remains recoverable.

## Public / private boundary

Public material should expose enough structure to establish source lineage and evaluate capability, but not enough to reconstruct the private engine.

Do not publish identifiable private people or incidents, private thresholds or calibration chains, credentials or secrets, hidden prompts or unrestricted runtime logic, or private origin evidence unnecessary for the public contribution boundary.

## Response to a disputed priority claim

Use artifacts and dates rather than motive claims: identify the exact mechanism, retrieve the earliest relevant dated artifact, distinguish similarity/derivation/later formalization/independent rediscovery, show the contribution boundary and acknowledged prior art, and correct the record only to the extent supported by evidence.

## Public identity rule

The canonical public citation identity for this repository is **Yelan22CAT**. Personal legal-name mapping is intentionally outside the public artifact.

## Boundary

A Git timestamp supports provenance recovery but does not by itself establish legal ownership, patent priority or universal novelty. Public disclosure can affect patent strategy in some jurisdictions; potentially patentable implementation details require separate review.
