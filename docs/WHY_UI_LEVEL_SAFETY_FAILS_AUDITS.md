# WHY UI-LEVEL SAFETY FAILS AUDITS

> Blocking output is not the same as preventing execution.
> Audits care about **what was allowed to run**.

---

## 0. Scope & Claim

This document does not argue against UI safety features.
It argues that **UI-level safety cannot satisfy post-incident audit requirements**.

This is a structural limitation, not a tooling gap.

---

## 1. The Audit Question UI Safety Cannot Answer

After an AI incident, auditors ask:

> **"Could this model execution have been prevented?"**

UI-level safety answers a different question:

> "Was the output shown to the user?"

These questions are not equivalent.

---

## 2. What UI-Level Safety Actually Does

UI safety mechanisms operate at the **presentation layer**:

* Content filters
* Moderation gates
* Output redaction
* Warning banners

They intervene **after**:

* The request was accepted
* The model was invoked
* Inference already occurred

Execution has already happened.

---

## 3. Why This Fails Evidence Standards

From an audit perspective:

* The model ran
* Sensitive inference occurred
* Blocking only affected display

There is no proof that:

* Execution could have been stopped
* A non-execution path was evaluated
* Permission was ever questioned

UI logs describe *suppression*.
They do not prove *restraint*.

---

## 4. Case Study: Air Canada Chatbot Incident

**Incident summary**

A customer asked about bereavement fare refunds.
The chatbot hallucinated a policy that did not exist.
The airline lost in court.

**Critical failure**

The system could not prove:

* Why the answer was allowed
* Why policy verification was skipped
* Why the model was invoked at all

UI disclaimers did not matter.
Execution already occurred.

---

## 5. The Hidden Assumption: Execution Is Inevitable

UI-level safety assumes:

> **"The model will run. We can only manage the output."**

This assumption is never logged.
It is never questioned.
It is never auditable.

In audits, **implicit permission is indistinguishable from negligence**.

---

## 6. Pre-Invocation Judgment vs UI Blocking

### UI-Level Safety

```
Request → LLM → Output → UI Filter
```

* Model always runs
* Blocking is cosmetic
* Non-execution is impossible to prove

### Pre-Invocation Judgment

```
Request → Judgment Gate → (ALLOW | STOP | ESCALATE) → [conditional] LLM
```

* Execution is conditional
* STOP is explicit
* Non-invocation is provable

Only the second model can answer audit questions.

---

## 7. Why "We Blocked It" Is Not a Defense

In audits and legal reviews:

* "We blocked the output" ≠ "We prevented harm"
* "We filtered the response" ≠ "We controlled execution"
* "The model is probabilistic" ≠ "We had no alternative"

Auditors do not accept:

* Post-hoc explanations
* UI-level disclaimers
* Best-effort filtering

They require **decision evidence**.

---

## 8. What Evidence Requires (Recap)

For execution control to be auditable, the system must show:

1. Execution was optional
2. STOP was a valid outcome
3. Rules governing execution existed
4. Non-execution was recorded
5. Authority boundaries were defined

UI-level safety satisfies none of these.

---

## 9. Why This Is a Design Problem, Not a Policy Problem

No policy language can compensate for:

* Missing execution boundaries
* Implicit model invocation
* Lack of non-execution records

Safety must be **designed into the execution path**, not layered on top.

---

## 10. Implications for High-Risk Domains

In domains like:

* Finance
* Healthcare
* Legal
* Government

UI-level safety provides:

* Comfort
* Plausible deniability
* No audit defense

Pre-invocation judgment provides:

* Traceability
* Responsibility
* Evidence of restraint

---

## Final Statement

> **If your safety system cannot prove that the model did not run,
> it cannot pass an audit — regardless of how much content it blocks.**

UI-level safety manages perception.
Judgment-level safety manages permission.

Audits care only about the latter.

---

This document must be interpreted alongside:
- `JUDGMENT_OS_OVERVIEW.md`
- `WHY_LOGS_ARE_NOT_EVIDENCE.md`
