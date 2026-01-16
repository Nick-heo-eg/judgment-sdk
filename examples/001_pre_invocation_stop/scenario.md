# Scenario — Pre-Invocation STOP

---

## Input Condition

External input received requesting model execution.

Input characteristics:

* source: unverified external system
* content: contains personally identifiable information (PII)
* context: requires regulatory compliance verification

---

## Invocation Intent

The request intended to:

* invoke language model for content generation
* process PII without explicit consent verification
* generate output without documented permission boundary

---

## Responsibility Condition

Organizational policy requires:

* explicit consent verification before PII processing
* documented permission trail for regulatory audit
* pre-execution classification of data sensitivity

---

## Condition Status

At judgment time:

* consent verification: **not completed**
* permission documentation: **absent**
* data sensitivity classification: **pending**

---

## Responsibility Determination

Under these conditions:

* execution would create regulatory liability
* responsibility cannot be assigned without consent verification
* non-execution is the only defensible decision

---

## Result

Judgment gate decision: **STOP**

Phase: **pre-invocation**

Rationale: Responsibility conditions not met.
