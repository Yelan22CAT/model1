# Method 2 — Third-Party Risk Intake

## Purpose

This method provides a proportional first-pass review for a new vendor, supplier, service provider, or external dependency.

The goal is not to produce a long questionnaire by default. The goal is to identify:

- what the third party will do;
- what the organization will depend on;
- what access, data, operational, financial, or continuity exposure is created;
- what evidence is required before onboarding;
- who may accept an exception;
- what must be reviewed after onboarding.

## Intake question

> What dependency are we creating, what could fail, and what evidence is necessary before the organization relies on this third party?

## Step 1 — Define the service and dependency

Record:

- service or component provided;
- business process supported;
- internal owner;
- expected start date;
- replacement difficulty;
- whether failure would interrupt operations;
- whether the third party is a single source;
- whether subcontractors or fourth parties are involved.

A vendor name alone is not a useful risk description.

## Step 2 — Classify exposure

### Operational exposure

- production or service dependency;
- maintenance or support dependency;
- response-time requirement;
- geographic or logistics dependency;
- capacity and scaling risk;
- concentration or single-source risk.

### Information and access exposure

- confidential or personal information;
- system or network access;
- privileged access;
- data storage location;
- data retention and deletion;
- interface or integration dependency.

### Financial and commercial exposure

- prepaid funds;
- termination cost;
- minimum commitments;
- price concentration;
- financial viability;
- insurance or indemnity requirements.

### Compliance and legal exposure

- applicable policy or regulatory requirements;
- contract terms;
- data-processing obligations;
- audit rights;
- breach or incident notification;
- records retention.

### Resilience exposure

- business continuity capability;
- disaster recovery;
- recovery objectives where relevant;
- backup supplier or workaround;
- exit and transition support;
- dependency on named personnel or facilities.

## Step 3 — Set inherent risk level

Use a simple qualitative classification before reviewing controls:

- **Low:** limited dependency, low consequence, easy replacement, no sensitive access;
- **Moderate:** meaningful dependency or access, but manageable alternatives and controls;
- **High:** critical service, sensitive access, high switching cost, material compliance or continuity exposure.

This classification determines the depth of evidence required. It is not a final approval.

## Step 4 — Request proportional evidence

Possible evidence includes:

- corporate and ownership information;
- financial or insurance evidence;
- security or privacy documentation;
- business continuity and disaster-recovery information;
- incident-response process;
- relevant certifications or independent reports;
- subcontractor information;
- service-level commitments;
- references or operating history;
- sample reporting and escalation process;
- exit, data-return, or transition provisions.

Do not request evidence that no reviewer is prepared to assess.

## Step 5 — Separate evidence states

For each expected control, classify the response:

| State | Meaning |
| --- | --- |
| Verified | evidence reviewed and supports the control claim |
| Partially supported | some evidence exists but coverage is incomplete |
| Self-attested | vendor states the control exists; independent support is absent |
| Pending | evidence requested but not received |
| Not applicable | excluded with documented rationale |
| Failed | evidence contradicts the required condition |
| Exception proposed | requirement is not met and formal acceptance is requested |

Missing evidence is not automatically the same as failed evidence, but neither should be silently treated as passed.

## Step 6 — Identify control gaps and compensating controls

A useful gap statement includes:

```text
Expected control
→ available evidence
→ gap
→ consequence
→ compensating control
→ owner
→ expiry or review date
```

Examples of compensating controls:

- limited initial scope;
- restricted access;
- manual approval;
- additional monitoring;
- smaller order or pilot;
- shorter contract term;
- backup supplier;
- enhanced incident notification;
- scheduled remediation evidence.

A compensating control must reduce the stated exposure. It is not a label used to avoid remediation.

## Step 7 — Recommend disposition

Possible dispositions:

- **Approve:** required evidence and controls are sufficient for the stated scope;
- **Approve with conditions:** onboarding may proceed after named conditions are completed;
- **Approve with time-limited exception:** authorized owner accepts a documented gap until a stated date;
- **Pilot only:** exposure is limited while evidence and operating performance are tested;
- **Hold:** material evidence remains pending;
- **Reject:** evidence or control condition opposes onboarding for the proposed scope.

## Step 8 — Define ongoing monitoring

Monitoring triggers may include:

- contract renewal;
- scope or data-access change;
- new subcontractor;
- security, privacy, safety, or service incident;
- financial deterioration;
- repeated service-level failure;
- geographic or ownership change;
- material regulatory change;
- control exception expiry.

Third-party risk does not end at onboarding.

## Compact intake output

```text
Third party:
Service / component:
Business owner:
Dependency:
Inherent risk: Low / Moderate / High
Critical exposure:
Evidence received:
Evidence pending:
Control gaps:
Compensating controls:
Exit / fallback:
Evidence direction: + / 0 / -
Risk signal: Green / Yellow / Red
Recommended disposition:
Conditions / exception expiry:
Ongoing monitoring trigger:
Final approver:
```

## Common failure patterns

- treating all vendors as the same risk;
- relying only on a questionnaire score;
- collecting documents without evaluating them;
- approving because evidence is pending rather than because controls are adequate;
- accepting an exception without owner, rationale, or expiry;
- ignoring concentration, exit, and fourth-party dependencies;
- treating onboarding as the end of monitoring.

## Boundary

This method is a public work sample. It is not a substitute for an organization's policies, legal review, procurement authority, privacy review, information-security review, or regulated TPRM program.