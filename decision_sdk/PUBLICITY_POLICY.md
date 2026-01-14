# SDK Publicity Policy

**Rule:** Structure is public. Judgment is sealed.

---

## What This SDK Contains (PUBLIC)

✅ **Judgment framework** - how to structure judgment checkpoints
✅ **API interface** - `wrap(callable)` entry point
✅ **Default safe mode** - ALLOW by default, no enforcement
✅ **Evidence logging** - AJT records metadata only
✅ **Layer abstraction** - DCL/DCP/AJT as composable products

**This SDK provides structure, not judgment.**

---

## What This SDK Does NOT Contain (SEALED)

❌ Domain policy rules (what to block/allow)
❌ Termination authority (cannot force STOP)
❌ Indeterminate trigger logic (when to escalate)
❌ Human override procedures (escalation trees)
❌ Case-specific judgment examples (operational data)

**Judgment authority remains external to SDK.**

---

## Why This Boundary Exists

**SDK Layer:** Neutral tool (public)
- Shows "how to judge" structure
- No decision-making power
- Default ALLOW (safe mode)

**Constitution/Policy Layer:** Authority (sealed)
- Defines "what to judge"
- Contains enforcement rules
- Operational judgment logic

---

## Publicity Decision Matrix

| Component | Public? | Reason |
|-----------|---------|--------|
| `wrap.py` | ✅ Yes | Entry point, no judgment logic |
| `dcp.py` | ✅ Yes | Framework only, returns ALLOW/HOLD/ESCALATE |
| `ajt.py` | ✅ Yes | Observation only, no decision-making |
| `dcl.py` | ✅ Yes | Learning structure, no policy |
| `config.py` | ✅ Yes | Default safe mode, no rules |
| Policy rulesets | ❌ No | Domain-specific judgment |
| Constitution | ❌ No | Authority definition |
| AJT Core | ❌ No | Termination enforcement |
| Case data | ❌ No | Operational examples |

---

## Key Design Principle

**SDK returns judgment signals (ALLOW/HOLD/ESCALATE).**
**SDK does NOT execute termination (STOP/INDETERMINATE).**

This separation ensures:
- SDK remains neutral tool
- Authority stays with Constitution
- Judgment responsibility is external

---

## Verification

All public code must satisfy:

```python
# ✅ ALLOWED: Return judgment signal
def evaluate(request):
    return {"action": "HOLD", "reason": "..."}

# ❌ FORBIDDEN: Execute termination
def evaluate(request):
    if condition:
        terminate_process()  # NEVER in SDK
        raise Indeterminate()  # NEVER in SDK
```

---

## Declaration

**This SDK is public by design.**

Framework: Public
Judgment: Sealed

This boundary is permanent.
