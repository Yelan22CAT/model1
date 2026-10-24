# 20 — Healthcare Data Engineering and Governed Interoperability

**Type:** Public, illustrative data/AI governance method. **Status:** Method Full-Push / Not Frozen (2026-10-24); no clinical validation or production deployment.

Medical and enterprise data may remain in their original systems while different business units, software versions and vendors evolve. A shared query surface is useful only when the meaning, quality, permissions, provenance and accountability of the underlying data survive the translation.

## Distinctions that must not collapse

| Separate questions | Why they matter |
| --- | --- |
| Source record vs normalized record vs clinically validated interpretation | Mapping a value is not proof that its medical or operational meaning is correct. |
| Index or search hit vs semantic equivalence | A similar label is not a verified match for dose, identity, units or historical accounting code. |
| Connectivity vs access rights vs permitted disclosure | The ability to query a record does not permit reuse, export, model training or cross-border transfer. |
| Data cleaning vs de-identification | Correcting missing/invalid values does not remove patient identifiers or eliminate re-identification risk. |
| Standard support vs demonstrated interoperability | DICOM and FHIR implementations may differ by profile, version, private field and workflow. |
| Agent recommendation vs approved state change | Finding a candidate medicine, bed, resource or interpretation is not authority to merge records or execute an action. |
| Research model performance vs clinical clearance vs billing | A model benchmark, permitted use, accountable clinical practice and reimbursement are independent claims. |

## Implementation-oriented review

1. **Preserve source lineage.** Record source system, schema/terminology version, relevant time, ownership and transformations. Do not silently overwrite historical records when mapping into a new reporting standard.
2. **Define a versioned semantic contract.** Document field and unit mappings, identity resolution, unknown attributes, exceptions and the meaning of each published metric.
3. **Check domain permissions.** Independently determine the legitimate purpose, applicable authority, permitted recipients and audit/retention boundaries before data retrieval, disclosure or model use.
4. **Establish source-to-output quality controls.** Detect ambiguous matches, incompatible doses or units, missing links, device-specific fields and unjustified claims that imaging content is de-identified.
5. **Use minimum necessary automation.** Start with deterministic terminology/catalog matching and established workflows. Add AI/agents where evaluated benefits exceed reliability and control costs; never allow a model to grant its own execution authority.
6. **Route consequential decisions to an accountable owner.** A suggested cross-site bed transfer, medication substitution, patient identity merge or imaging finding remains a proposal until validated under the relevant clinical/operational workflow.
7. **Recheck upon change.** An acquired company, new device/software version, new purpose, vocabulary update or changed permission requires affected mapping and end-to-end tests to be revisited.

## Illustrative negative controls (synthetic data only)

| Case | Safe outcome |
| --- | --- |
| Source says `Medicine X 10 mg`; catalog candidate says `Medicine X 100 mg` | Reject automatic merge; escalate ambiguity. |
| Two hospitals reuse the same local patient identifier | Do not combine records without a validated identity linkage. |
| New imaging vendor field is not recognized | Preserve the field and hold the affected interpretation for review; do not silently discard it. |
| A record is technically readable but the requested use is not authorized | Deny or defer access and record the reason without exposing the sensitive payload. |
| An AI model describes an image but lacks validation/approval for the proposed clinical action | Retain advisory-only status; no independent clinical execution. |

## Accountability and evidence

Data engineers own the integration/pipeline implementation and its observable quality; clinical professionals validate clinical meaning and patient-safety decisions; data stewards, security/privacy specialists and authorized owners determine governance and release permissions. Real responsibilities vary by institution and jurisdiction; this table is not a universal legal assignment.

**Evidence gate:** A prototype or local synthetic test establishes only the tested behavior, not interoperability across real hospitals, data-protection compliance, device clearance, reimbursement eligibility or clinical effectiveness. A private illustrative check (18/18 synthetic cases) is not offered as a public benchmark or production proof.

**Relationship:** Complements [AI Data Lifecycle & Connector Privacy Review](05-ai-data-lifecycle-privacy-review.md), [Structured Decision Integrity](08-structured-decision-integrity.md), [Reusable and Agentic Workflow Design](06-reusable-and-agentic-workflow-design.md), and [Task-Authentic and Risk-Proportional Validation](17-task-authentic-risk-proportional-validation.md).

**Public technical references:** [HL7 FHIR Implementation Guide](https://hl7.org/fhir/implementationguide.html) · [DICOM conformance](https://dicom.nema.org/medical/dicom/current/output/chtml/part02/chapter_6.html) · [HHS de-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html).

**Publication boundary:** No private person cards, livestream transcripts, patient records, vendor credentials, private source archives, real-case allegations, implementation thresholds or unrestricted action authority are published here.
