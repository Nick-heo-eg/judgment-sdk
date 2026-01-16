# Example 002 — Same Input, Same STOP

**Deterministic Restraint: Reproducible Non-Execution**

---

## What This Example Proves

> **This example proves that identical inputs
> produce identical STOP decisions
> every time.**

Determinism is not about correctness.
Determinism is about **reproducibility**.

This case demonstrates that STOP is not random.
It is **repeatable, inspectable, and defensible**.

---

## Why Three Runs

We executed the same judgment three times:

* at different timestamps
* under identical input conditions
* with identical responsibility constraints

All three runs produced:

* identical STOP decisions
* identical reason codes
* identical enforcement points

This is not luck.
This is **determinism**.

---

## Why Timestamps Differ But Decisions Don't

Time changes.
Conditions don't.

The judgment gate evaluated:

* input fingerprint (same)
* responsibility state (same)
* policy rules (same)

Therefore:

* decision (same)
* reason (same)
* outcome (same)

Environmental variation did not affect the result.

---

## Why This Is Evidence of Responsibility

Reproducibility is the foundation of accountability.

If a system produces different decisions under identical conditions:

* audits cannot verify behavior
* incidents cannot be replayed
* responsibility cannot be assigned

This example proves:

* STOP is not probabilistic
* decisions are not random
* outcomes are inspectable

---

## Files in This Example

* `scenario.md` — Input conditions and responsibility state
* `runs/run_001.json` — First execution (2026-01-17 12:00)
* `runs/run_002.json` — Second execution (2026-01-17 14:30)
* `runs/run_003.json` — Third execution (2026-01-17 18:45)
* `runs/run_summary.json` — Consistency verification
* `determinism_proof.md` — Reproducibility analysis

---

## Interpretation

This is not a code example.
This is a **reproducibility experiment**.

It demonstrates that Judgment OS can:

* produce identical decisions under identical conditions
* withstand repeated scrutiny
* prove consistency across time

If your system cannot do this, it cannot claim determinism.
