# Example 003 — UI Pass, Execution Denied

**Authority Boundary: Visibility ≠ Permission**

---

## What This Example Proves

> The UI allowed rendering.
> The system did not allow execution.

> Visibility is not authority.

This case demonstrates that:

* UI approval does not imply execution permission
* Seeing an output does not mean execution occurred
* Authority boundaries exist between layers

---

## Why UI Pass Is Not Execution Permission

UI safety mechanisms evaluate:

* content appropriateness
* display policy
* user experience constraints

Execution gates evaluate:

* responsibility conditions
* regulatory requirements
* permission boundaries

These are **different authorities**.

---

## Why Audits Don't Look at UI Logs

After an incident, auditors ask:

* "Was execution allowed?"
* "Who authorized model invocation?"
* "Could execution have been prevented?"

UI logs cannot answer these questions.

UI logs show what was **rendered**.
They do not show what was **permitted to run**.

---

## Why This Structure Prevents Incidents

In this example:

* UI layer: content passed display policy
* Execution layer: responsibility conditions not met
* Result: **rendered but not executed**

If execution authority lived in the UI:

* seeing output would imply execution occurred
* no restraint would exist after display approval
* incidents would be inevitable

By separating authority:

* execution can be denied even when display is allowed
* responsibility is enforced before invocation
* restraint is possible at every layer

---

## Files in This Example

* `scenario.md` — Two-layer evaluation context
* `ui_trace/ui_render_ok.log` — UI approval record
* `execution_trace/execution_denied.json` — Execution denial record
* `authority_diff.md` — Authority boundary table
* `conclusion.md` — Visibility vs permission distinction

---

## Interpretation

This is not a code example.
This is a **boundary enforcement precedent**.

It demonstrates that Judgment OS can:

* separate display authority from execution authority
* deny execution even when UI approves
* prove that rendering ≠ permission

If your system cannot do this, UI approval is execution approval.
