# 16 — Security, Procurement and Competition: Separate the Claim Types

**Method status:** Full-Push / Not Frozen; evidence-scoped explanation, not a political conclusion or legal advice.  
**Companion experiment:** Bridge-0 `RFC_POLICY_SCOPE_STATED_RISK_MARKET_EFFECT_MOTIVE.md` (experimental branch).

A procurement restriction has several distinguishable facets. Conflating them causes false certainty:

| Question | Appropriate evidence | Common mistake |
|---|---|---|
| **Legal scope**: whose systems and purchases are covered? | Order's operative text, date, exclusions and waiver procedure | Labeling a bounded government ban as a ban on all users |
| **Stated safety rationale**: what does the agency claim? | Authenticated official statement | Treating an allegation of risk as proof of an incident |
| **Economic consequences**: what suppliers or procurement choices change? | Contract awards, market data, matched before/after comparisons | Assuming an intended beneficiary from a possible effect |
| **Decision-maker motive**: why was the rule adopted? | Decision records, contemporaneous deliberations, comparative treatment | Inferring motive only from beneficiaries or nationality |

Operational checkpoints:

1. Date and identify the primary policy text; do not confuse signed and published dates.
2. Partition government IT, private enterprise, local deployment, external API, licensing and procurement eligibility.
3. Compare model cost on successful validated tasks, including operations and security compliance, not token prices alone.
4. Use task- and version-matched benchmarks. A lower price for some tasks is not proof of universal superiority.
5. Test at least two plausible explanations and identify evidence that would distinguish them.
6. Historical analogies require similar scope, policy tools and outcome metrics, not just similar rhetoric.
7. Preserve `FACT`, `HYPOTHESIS`, `UNKNOWN`, and third-party assertions as separate evidence states.

### Public-document example (2026)

The U.S. DHS DeepSeek exclusion/removal order, Federal Register Doc. [2026-21447](https://public-inspection.federalregister.gov/2026-21447.pdf), applies to covered federal civilian executive-branch IT and procurement; it is not an order prohibiting all individuals or private firms in the United States from using the model. The government's published reasons include software, data, and supply-chain risk concerns. Those are **documented government assertions**, not independent findings that every deployment is compromised.

Excluding a supplier from a procurement channel mechanically changes eligibility; the size of any ensuing commercial advantage and the government decision-makers' motive are **separate empirical questions**. The U.S. [NIST/CAISI evaluation](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro) supports workload-dependent cost comparison, not a blanket assertion that all U.S. models are either cheaper or more expensive.

### Boundary

This is a reusable evidence-adjudication workflow, not an endorsement of a political position. It does not move private Model Root materials to public, approve government purchases, or modify frozen Bridge-0 RC1 semantic anchors.