> This repository must be interpreted through `docs/JUDGMENT_OS_OVERVIEW.md`.

## Decision ≠ Judgment
Kernel은 지능이 아니다. Echo Judgment Kernel은 판단 권한을 행사하지 않고,
STOP/ESCALATE 충돌과 계약 필수 요건만 봉인한다. 최적화·추론·추천은 어떤
형태로든 금지되며, 인간 혹은 상위 권한이 없는 한 ACCEPT/MODIFY/ESCALATE
중 하나만 선언한다.

## ⚠️ Usage Directive (Read Before Using or Forking)

This repository documents a **judgment-layer architecture** for responsible AI systems.
It is **not** a drop-in product, template, or turnkey SDK.

### What this repository is

* A **structural reference** for where decisions happen
* A **conceptual SDK design** for proving *who decided* and *what was skipped*
* A **pre-invocation judgment model**, not a UI filter or post-hoc logger

### What this repository is NOT

* ❌ A complete production implementation
* ❌ A plug-and-play compliance solution
* ❌ A policy engine without organizational context
* ❌ A replacement for governance, ownership, or human accountability

> Code alone is insufficient.
> Judgment requires **organizational decision context**.

### Important Constraints

Before attempting implementation, understand the following:

1. **Decision meaning depends on context**

   * Fields like `ml_invoked`, `decision_depth`, or `layers_skipped`
     have no value without clearly defined ownership and escalation rules.

2. **This system assumes responsibility, not automation**

   * Blocking, allowing, or skipping layers is meaningless
     unless someone is accountable for the outcome.

3. **Learning layers (e.g. compression / bypass) are not generic**

   * Pattern learning without domain ownership is unsafe.
   * Do **not** enable learning behavior without explicit review authority.

4. **Audit logs are evidence, not explanations**

   * Logs prove what happened.
   * They do not justify why it was acceptable.

### Forking & Reuse Notice

You are free to:

* Study the architecture
* Adapt the concepts
* Implement your own version

You are **not advised** to:

* Treat this as a compliance shortcut
* Deploy without decision ownership
* Assume structural similarity implies functional equivalence

If you build something similar, you are responsible for:

* Defining who owns each decision layer
* Defining escalation and override authority
* Defining failure responsibility

### Why This Directive Exists

Most AI incidents are not caused by bad models.
They are caused by **untraceable decisions**.

This repository exists to make that failure mode explicit.

If you do not know **who will explain the next incident**,
you are not ready to implement this system.

### Final Note

This project favors **structural proof over convenience**.

If you are looking for:

* Faster outputs
* Cheaper inference
* UI-level moderation

This is not the right tool.

If you are preparing for:

* Audits
* Incidents
* Responsibility questions at 3 a.m.

Then you are in the right place.

# Responsible Chatbot Comparison Suite
Demonstrates how pre-decision suppression changes chatbot behavior.


## Runnable Code
See `code/README.md` for a runnable Baseline vs Controlled chatbot comparison.
