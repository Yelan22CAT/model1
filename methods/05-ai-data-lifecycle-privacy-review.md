# Method 5 — AI Data Lifecycle & Connector Privacy Review

> A public-safe review checklist, not legal advice, compliance certification, a claim about any reader's account, or an automated enforcement tool.

## Why this method exists

AI workflows cross several boundaries that are often mistakenly treated as one:

```text
Source visibility
≠ permission to collect or reuse personal data
≠ repository visibility
≠ third-party app / connector access
≠ provider storage and training terms
≠ permission to publish output
```

A private repository restricts public GitHub access; it does not by itself establish how any authorized connector processes, stores, retains, transfers or potentially reuses data. Check the specific tool, account, agreement and permissions instead of assuming an incident or assuming complete confidentiality.

## Regulatory source and scope

The Canadian federal privacy commissioner and privacy regulators in Quebec, British Columbia and Alberta published joint findings about OpenAI's earlier ChatGPT practices on **May 6, 2026**. The investigation principally concerned GPT-3.5 and GPT-4; later models and separate image/video services were **not directly assessed**. Regulators identified concerns about overcollection, consent/transparency, personal-information accuracy, access/correction/deletion, and accountability/retention. Their outcomes differed: federal well-founded/conditionally resolved; BC and Alberta well-founded/unresolved; Quebec conditionally resolved on several issues but unresolved on consent. The report also records measures introduced and future commitments; these must not be conflated.

Official primary sources:

- [OPC backgrounder, May 6, 2026](https://www.priv.gc.ca/en/opc-news/news-and-announcements/2026/bg-info_openai_260506/)
- [Underlying joint investigation overview, PIPEDA Findings #2026-002](https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/2026/pipeda-2026-002-overview/)

These are *findings issued by the regulators about the specified practices and period*, not proof of the present settings of an individual account or of every subsequent product. This repository has no affiliation with or endorsement from the regulators or OpenAI.

## Narrow review flow

```text
Proposed AI-assisted transfer / processing / public release
→ 1. Identify the source and intended purpose
→ 2. Classify personal, sensitive and third-party data
→ 3. Verify authorization / lawful basis or applicable exception with an owner
→ 4. Minimize / redact / use synthetic fixtures where possible
→ 5. Inspect destination, connector scope and repository visibility
→ 6. Check applicable data-use, training, retention and deletion terms
→ 7. Check output accuracy, correction, access and downstream exposure
→ 8. Record unknowns, evidence, accountable reviewer and reversal condition
→ Human Final Gate: allow minimum / revise / defer / do not transfer
```

Do not automatically map a privacy risk to a legal violation. Laws and obligations vary by jurisdiction, data type and context; refer consequential compliance issues to qualified privacy/legal personnel.

## Review questions

| Boundary | Verify before use |
| --- | --- |
| Source | Where did the material come from? Does it contain information about people not participating in this workflow? |
| Purpose | Why is each field needed? Is an identifiable copy necessary? |
| Repository | Is it public or private? Could branch history, issues, PRs, comments or CI logs expose it? |
| Connector | Which installation, repositories, permissions and tools are granted? Can access be narrowed or revoked? |
| Provider | Which actual agreement, data controls, training settings, retention rules, transfers and subprocessors apply to this workspace? |
| Output | Are claims about a person traceable and correctable? Might an answer reveal sensitive information? |
| Lifecycle | Who owns access, correction, deletion, incident response and periodic reassessment? |

**Important:** Deleting a local file or GitHub document does not prove that all previously transferred copies, logs or model-related representations have been erased. Verify the relevant provider's actual processes and commitments.

## Example: private repo to AI connector (synthetic)

An engineer wants an assistant to summarize a private project document. They first remove third-party identifiers, restrict the connector to the necessary repository and permissions where supported, verify applicable service data-use terms, avoid posting source text in a public PR or CI log, and approve a redacted summary after checking provenance. If any important processing or retention condition is unknown, record `UNKNOWN` and seek evidence rather than reporting `SAFE` or `BREACH`.

## Evidence-based output

```text
Task and purpose:
Data classes and source provenance:
Repository visibility:
Connector authorization and actual scopes:
Applicable provider processing / training / retention terms:
Redactions and minimization:
Access / correction / deletion pathways:
Unknowns / contradictions:
Evidence and review date:
Human owner:
Decision: minimum transfer / revise / defer / do not transfer
Reassessment trigger:
```

## Boundaries

- Private GitHub does not imply offline or air-gapped processing.
- Access authorization is not consent for every secondary use or publication.
- Publicly accessible information is not automatically exempt from all privacy obligations.
- Do not infer that an individual's repository was leaked or used for training from a regulator's investigation of historical practices.
- This document introduces no code, permissions, monitoring, real-world access or automatic enforcement; these controls must be implemented and tested separately.
- Never include private case archives, identifiable people, secrets, full interaction protocols or hidden runtime logic in a public example.

**Compact principle:** Access, processing, training, retention and publication are separate permission and evidence decisions.
