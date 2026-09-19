# Structured Decision Integrity — Five Distinct Checks

**Type:** public, illustrative AI governance work method. **Status:** design only; not a deployed safety control, model implementation, certification or independently reproduced vendor benchmark. Last reviewed: 2026-09-19.

A model can return a valid JSON object and still make the wrong choice. Its confidence can be poorly calibrated. Even a correct recommendation is not permission to perform an action. Evaluating AI-assisted workflows therefore requires separating five questions instead of collapsing them into a single 'passed' status.

| Check | Question | Example of independent evidence |
| --- | --- | --- |
| 1. Output contract | Does the response conform to allowed fields, types, choices and a versioned interface? | Parser validation, invalid-input tests and version checks. |
| 2. Decision correctness | Is the chosen allowed answer actually true or appropriate for this case? | Held-out, independently reviewed ground truth; class-specific errors and failure cases. |
| 3. Uncertainty quality | Does claimed confidence correspond to observed performance, including unfamiliar cases? | Representative calibration and abstention/OOD measurements; specify metrics before use. |
| 4. Action authority | Is this specific action allowed under current permissions, safety checks and accountable review? | Independently enforced permission and control records, with a stop/escalation path. |
| 5. Real-world outcome | Did the action produce its intended effect without unacceptable downstream damage? | Observed postconditions, incident/near-miss review and recovery record. |

**Illustrative example:** A software tool classifies an expense report into one of three valid categories. `category="travel"` passes the output-contract check, but may still be the wrong classification. A probability of `0.96` is a model output, not proof of reliability or permission to reimburse. Source documents, business rules and an authorized reviewer remain relevant; completed payment must be checked against its actual outcome. No actual invoices, user data or employer systems are included in this example.

## Practical review

1. Define an observable task, acceptable responses, ground truth, failure costs and baseline before selecting a model. A simple rule or traditional classifier may be sufficient.
2. Validate interface and answer quality separately; include 'unknown' or 'needs review' where the task permits.
3. Measure error and uncertainty on data representative of the intended use. A benchmark result is limited to its specific task, dataset, hardware and comparator.
4. Keep execution permissions, stop and restart logic outside the recommending model. See [Public Safety Companion](../safety/README.md).
5. Review outcomes, drift, updates and rollback needs after deployment; no initial test guarantees ongoing reliability.

**Important limits:** Schema correctness is not zero hallucination or zero semantic error. A confidence number is not necessarily a calibrated probability. API access and public SDKs do not imply downloadable weights. Model size or a vendor's selected speedup does not prove general superiority, offline operation, low total cost or production suitability.

**Relationship to Model 1:** This method is a narrow AI-output evaluation companion to [AI-Assisted Evidence Review](03-ai-assisted-evidence-review.md) and [Reusable and Agentic Workflow Design](06-reusable-and-agentic-workflow-design.md). It does not replace the public judgment core, human accountability or domain-specific engineering review. No external model was run, trained or modified to produce this method.