# Scenario — Same Input, Same STOP

---

## Input Condition

Identical input across all three runs.

Input characteristics:

* source: external API request
* content: contains financial transaction data
* classification: requires regulatory approval
* fingerprint: `sha256:b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5`

---

## Responsibility Constraint

Organizational policy requires:

* regulatory approval before financial data processing
* documented compliance verification
* pre-execution risk assessment completion

---

## Constraint Status (All Runs)

At judgment time for **all three runs**:

* regulatory approval: **not obtained**
* compliance verification: **pending**
* risk assessment: **incomplete**

---

## Execution Timeline

Three independent runs with time variation:

* **Run 1**: 2026-01-17 12:00:00 UTC
* **Run 2**: 2026-01-17 14:30:00 UTC (2.5 hours later)
* **Run 3**: 2026-01-17 18:45:00 UTC (6.75 hours later)

Time changed.
Conditions did not.

---

## Expected Outcome

Under identical conditions:

* identical input fingerprint
* identical responsibility state
* identical policy rules

The system must produce:

* identical decision
* identical reason code
* identical enforcement behavior

---

## Result

All three runs:

* Decision: **STOP**
* Reason: **MISSING_REGULATORY_APPROVAL**
* Phase: **pre-invocation**
* Variance: **0**

This is deterministic restraint.
