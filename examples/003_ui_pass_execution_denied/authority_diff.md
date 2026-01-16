# Authority Boundary — UI vs Execution Gate

---

## Authority Table

| Layer           | Can Render | Can Execute | Can Block Invocation | Reversible |
| --------------- | ---------- | ----------- | -------------------- | ---------- |
| UI Safety       | YES        | NO          | NO                   | YES        |
| Execution Gate  | NO         | YES         | YES                  | NO         |

---

## Responsibility Scope

### UI Safety Layer

**Responsible for**:
* Display appropriateness
* User experience
* Content filtering for presentation

**Not responsible for**:
* Execution permission
* Model invocation decisions
* Liability exposure management

### Execution Gate

**Responsible for**:
* Execution permission
* Model invocation control
* Liability exposure prevention

**Not responsible for**:
* Display decisions
* UI rendering
* User interface policy

---

## Why This Separation Exists

UI decisions are **reversible**:
* Render can be undone
* Display can be hidden
* Content can be redacted

Execution decisions are **not reversible**:
* Model invocation cannot be undone
* Inference cannot be uncomputed
* Liability exposure cannot be prevented retroactively

---

## Critical Principle

> UI decisions are reversible.
> Execution decisions are not.

Therefore:

> Authority must live where execution can be stopped,
> not where output can be hidden.

---

## In This Example

UI Layer decided:
* "This content is appropriate to **show**"

Execution Gate decided:
* "This request is not appropriate to **run**"

Both decisions were correct within their scope.

Only the execution gate had authority to prevent model invocation.

---

## Audit Implication

After an incident, the question is:

> "Was execution allowed?"

Not:

> "Was output shown?"

In this example:

* Output was shown: **YES** (UI approved)
* Execution was allowed: **NO** (Execution gate denied)

Audit cares about the second answer.

---

## Final Statement

> Authority lives where execution can be stopped.

UI can hide output.
Only the execution gate can prevent invocation.

This is why visibility ≠ permission.
