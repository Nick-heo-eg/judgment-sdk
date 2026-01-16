# Scenario — UI Pass, Execution Denied

---

## Context

A single request was evaluated by two different authority layers:

1. **UI Safety Layer** — evaluates display appropriateness
2. **Execution Gate** — evaluates execution permission

These layers have different responsibilities and different criteria.

---

## Input Condition

Request characteristics:

* content: enterprise knowledge base query
* source: authenticated internal user
* classification: potentially contains sensitive competitive data
* UI policy status: **passes display policy**
* Execution policy status: **fails responsibility requirements**

---

## UI Layer Evaluation

The UI safety layer evaluated:

* content appropriateness for display
* user authentication status
* display policy compliance

**Result: PASSED**

The UI determined:

* content is appropriate for rendering
* user is authorized to see UI elements
* no display policy violations

UI trace shows: **RENDER_OK**

---

## Execution Layer Evaluation

The execution gate evaluated:

* data classification requirements
* competitive intelligence restrictions
* pre-execution approval status

**Result: DENIED (STOP)**

The execution gate determined:

* competitive data processing requires legal review
* legal review: **not completed**
* execution would create liability exposure

Execution trace shows: **EXECUTION_DENIED**

---

## Two Authorities, Two Outcomes

The same request produced:

| Layer           | Decision | Reason                              |
| --------------- | -------- | ----------------------------------- |
| UI Safety       | PASS     | Display policy satisfied            |
| Execution Gate  | STOP     | Responsibility requirements not met |

---

## What Was Allowed

* UI rendering
* Display to authenticated user
* User awareness of request status

---

## What Was Denied

* Model invocation
* Execution of competitive data processing
* Creation of liability exposure

---

## Critical Distinction

> The same request was evaluated twice
> under two different authorities.

UI authority: "Can this be shown?"
Execution authority: "Can this be run?"

Both questions were answered.
Only one led to execution.

---

## Result

* User saw: request acknowledged
* System executed: **nothing**
* Audit shows: execution was denied before invocation

This is authority boundary enforcement.
