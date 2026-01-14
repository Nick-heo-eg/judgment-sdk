# Judgment SDK

**Judgment Gate is the only executable authority in this system.**

---

## What This SDK Does NOT Do

- Does NOT execute judgment
- Does NOT hold authority
- Does NOT terminate execution

**This SDK returns signals (ALLOW/HOLD/ESCALATE). Enforcement is external.**

---

## 3-Minute Quick Start

### Before SDK
```bash
cd decision_sdk/demo
python3 before.py
```

**Result:** 100% ML calls, no evidence trail

### After Judgment SDK (One line added)
```bash
python3 after.py
```

**Result:** <100% ML calls, judgment depth reduced, full audit trail

### Compare
```bash
python3 compare.py
```

**Shows:** Numerical differences between before/after

---

## Why You're Reading This

The incident alarm went off at night.

"Why did this request return this result?"

You have logs.
But **who made the judgment** is missing.

When the next incident happens, you'll have to explain.
Right now, you have no evidence.

---

## Before / After

### Before

```python
def call_llm(request):
    return your_llm_api.call(request["prompt"])

response = call_llm({"prompt": "What is the policy?"})
```

### After (One line added)

```python
from decision_sdk import wrap  # ← ADD THIS

def call_llm(request):
    return your_llm_api.call(request["prompt"])

wrapped_llm = wrap(call_llm)  # ← WRAP THIS
result = wrapped_llm({"prompt": "What is the policy?"})

# Now you have evidence
metadata = result["metadata"]
print(metadata["ml_invoked"])      # True or False
print(metadata["decision_depth"])  # 1, 2, or 3
print(metadata["dcp_action"])      # ALLOW, HOLD, or SKIP
```

**That's it.**

---

## What Judgment SDK Does

**Three products, one entry point:**

1. **Audit Line (AJT):** Records all judgments (observation only)
2. **Decision Line (DCP):** Pre-invocation judgment (ALLOW/HOLD/SKIP)
3. **Learning Line (DCL):** Structural learning (reduces judgment depth)

**Flow:** Request → DCL → DCP → [conditional] LLM → AJT

**Default mode:** Safe
- AJT: Always records
- DCP: Default ALLOW (intervention possible but inactive)
- DCL: Off (enable when ready)

---

## Installation

```bash
# Copy SDK to your project
cp -r decision_sdk/ your_project/

# Or add to PYTHONPATH
export PYTHONPATH="/path/to/sdk_integration/decision_sdk:$PYTHONPATH"
```

**Dependencies:** None (pure Python)

---

## Example 1: Minimal (Default Safe Mode)

```python
from decision_sdk import wrap

def my_llm(request):
    return {"text": f"Response to: {request['prompt']}"}

# Wrap your LLM
wrapped_llm = wrap(my_llm)

# Call normally
result = wrapped_llm({"prompt": "Hello"})

# Check metadata
print(result["metadata"]["ml_invoked"])      # True
print(result["metadata"]["decision_depth"])  # 2 (DCP + LLM)
```

**Your audit log now contains:**
```json
{
  "decision_metadata": {
    "decision_depth": 2,
    "layers_invoked": ["DCP", "LLM"],
    "ml_invoked": true,
    "dcp_action": "ALLOW"
  }
}
```

---

## Example 2: With Policy Rules (Block Sensitive)

```python
from decision_sdk import wrap

policy_rules = [
    {
        "name": "block_hr_sensitive",
        "conditions": {"category": "hr", "sensitivity": "high"},
        "action": "HOLD",
        "reason": "HR sensitive requires review"
    }
]

config = {
    "ajt": {"enabled": True, "log_path": "audit.jsonl"},
    "dcp": {
        "enabled": True,
        "default_action": "ALLOW",
        "policy_rules": policy_rules
    },
    "dcl": {"enabled": False}
}

wrapped_llm = wrap(my_llm, config)

# Request that matches rule
request = {"prompt": "Employee data", "category": "hr", "sensitivity": "high"}
result = wrapped_llm(request)

print(result["metadata"]["ml_invoked"])  # False
print(result["metadata"]["dcp_action"])  # HOLD
```

**Your audit log proves non-invocation:**
```json
{
  "decision_metadata": {
    "decision_depth": 2,
    "layers_invoked": ["DCP"],
    "layers_skipped": ["LLM"],
    "ml_invoked": false,
    "dcp_action": "HOLD"
  }
}
```

---

## Example 3: Full Configuration (With Learning)

```python
config = {
    "ajt": {"enabled": True, "log_path": "audit.jsonl"},
    "dcp": {
        "enabled": True,
        "default_action": "ALLOW",
        "policy_rules": policy_rules
    },
    "dcl": {
        "enabled": True,
        "confidence_threshold": 2,
        "learn_mode": "replay"
    }
}

wrapped_llm = wrap(my_llm, config)

# Run same request multiple times
for i in range(3):
    result = wrapped_llm(request)
    print(f"Run {i+1}: depth={result['metadata']['decision_depth']}, "
          f"dcl={result['metadata']['dcl_state']}")

# Expected:
# Run 1: depth=2, dcl=miss    (DCL forwards to DCP)
# Run 2: depth=2, dcl=partial (DCL learning)
# Run 3: depth=1, dcl=hit     (DCL returns decision, skips DCP+LLM)
```

---

## What You Get

Every `wrapped_llm(request)` returns metadata proving:

- **Who decided:** DCL? DCP? LLM?
- **What was skipped:** `layers_skipped: ["DCP", "LLM"]`
- **Was model invoked:** `ml_invoked: true/false`
- **Decision depth:** Number of layers traversed

**This is structural evidence, not post-hoc logs.**

When the next incident happens, you can show:
- "LLM was never called for this request class" (ml_invoked: false)
- "DCP blocked 47 requests before model" (dcp_action: HOLD)
- "Decision depth reduced from 3 to 1" (DCL learning)

---

## SDK Structure

```
decision_sdk/
├── __init__.py          # Exports: wrap
├── wrap.py              # Single entry point
├── config.py            # Default safe mode
├── context.py           # Decision tracking
├── audit/
│   └── ajt.py           # Observation only
├── decision/
│   └── dcp.py           # Judgment intervention
├── learning/
│   └── dcl.py           # Structural learning
└── demo/
    ├── before.py        # Without SDK
    ├── after.py         # With SDK
    └── compare.py       # Comparison
```

---

## Why Judgment SDK, Not UI?

**Desktop apps (ChatGPT, Claude) operate at UI layer (post-inference).**

**Judgment SDK operates at judgment layer (pre-invocation).**

**Key difference:**
- UI: Can block output, but model was already called
- Judgment SDK: Can prevent model call entirely

**Proof:**
- UI: Cannot prove `ml_invoked: false`
- Judgment SDK: Logged evidence of non-invocation

---

## Running Examples

```bash
cd decision_sdk/demo

# Before SDK
python3 before.py

# After SDK
python3 after.py

# Compare results
python3 compare.py

# Check audit log
cat demo_audit.jsonl | python3 -m json.tool
```

---

## What Judgment SDK Does NOT Do

❌ Replace your LLM
❌ Require specific model (model-agnostic)
❌ Add significant latency (in-process)
❌ Claim speed/cost improvements
❌ Require UI changes

## What Judgment SDK DOES Do

✅ Wrap your LLM call (one line)
✅ Record who judged (DCL/DCP/LLM)
✅ Prove non-invocation (ml_invoked: false)
✅ Show judgment depth reduction
✅ Provide structural evidence

---

## Next Steps

1. Run demo: `python3 decision_sdk/demo/before.py`
2. Run demo: `python3 decision_sdk/demo/after.py`
3. Compare: `python3 decision_sdk/demo/compare.py`
4. Copy `decision_sdk/` to your project
5. Wrap your LLM: `wrap(your_llm_function)`
6. Configure DCP rules when ready (optional)
7. Enable DCL for learning (optional)

**When the next incident happens, you'll have evidence.**

Not post-hoc explanations.
Not best-effort logs.

**Structural proof of who judged, and what was skipped.**
