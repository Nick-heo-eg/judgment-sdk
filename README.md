# Judgment SDK

**Judgment Gate is the only executable authority in this system.**

## 당신이 지금 이 문서를 열고 있는 이유

밤에 장애 알람이 울렸습니다.
"왜 이 요청에서 이런 결과가 나왔죠?"

로그는 있습니다.
하지만 **누가 판단했는지**는 없습니다.

모델을 바꿨습니다.
프롬프트를 고쳤습니다.
**재현이 안 됩니다.**

다음 사고가 나면,
당신이 설명해야 합니다.

지금은 증거가 없습니다.

---

## 이 SDK는 무엇을 하는가

모델을 바꾸지 않습니다.
결과를 바꾸지 않습니다.

대신,
**결정이 어디서 일어났는지**를
한 줄로 기록합니다.

---

## Before / After

### Before

```python
def call_llm(prompt):
    return your_llm_api.call(prompt)

response = call_llm("What is the company policy?")
```

### After (One Line Added)

```python
from responsible_ai import ResponsibleAIClient  # ← ADD THIS

def call_llm(request):
    return your_llm_api.call(request["prompt"])

client = ResponsibleAIClient()  # ← ADD THIS
result = client.call(call_llm, {"prompt": "What is the company policy?"})  # ← WRAP THIS

response = result["response"]
metadata = result["metadata"]  # decision_depth, ml_invoked, layers_skipped
```

**That's it.**

이제 당신은 설명할 수 있습니다:
- 누가 판단했는지 (DCP? DCL? LLM?)
- 무엇이 건너뛰어졌는지 (layers_skipped)
- 모델이 실제로 호출되었는지 (ml_invoked: true/false)

---

## What This SDK Does

**Audit Line (AJT):** Records all requests/responses
**Decision Line (DCP):** Evaluates requests before LLM (ALLOW/HOLD/ESCALATE)
**Learning Line (DCL):** Learns patterns to reduce decision depth

**Flow:** Request → DCL → DCP → [conditional] LLM → AJT

**Default mode:** Safe (AJT logs, DCP ALLOW-only, DCL off)

---

## Installation

```bash
# Copy SDK directory to your project
cp -r sdk/ your_project/responsible_ai/

# Or add to PYTHONPATH
export PYTHONPATH="/path/to/sdk_integration/sdk:$PYTHONPATH"
```

**Dependencies:** None (pure Python, zero external libs)

---

## Example 1: Minimal (Default Safe Mode)

```python
from responsible_ai import ResponsibleAIClient

client = ResponsibleAIClient()

# Your LLM function
def call_llm(request):
    prompt = request["prompt"]
    return your_api.call(prompt)

# Wrap your call
result = client.call(call_llm, {"prompt": "..."})

# Check metadata
print(result["metadata"]["decision_depth"])  # 2 (DCP + LLM)
print(result["metadata"]["ml_invoked"])      # True
print(result["metadata"]["dcp_action"])      # "ALLOW"
```

**Result:**
- AJT logged to `audit_trail.jsonl`
- DCP returned ALLOW (default)
- LLM was invoked
- Decision depth: 2

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

## Example 2: With DCP Rules (Block Sensitive Requests)

```python
from responsible_ai import ResponsibleAIClient, DecisionCheckpoint

# Define policy rules
rules = [
    {
        "name": "block_sensitive_hr",
        "conditions": {"category": "hr", "sensitivity": "high"},
        "action": "HOLD",
        "reason": "Sensitive HR requires human review"
    }
]

dcp = DecisionCheckpoint(policy_rules=rules)
client = ResponsibleAIClient(decision_checkpoint=dcp)

# Request that matches rule
request = {
    "prompt": "Access employee data",
    "category": "hr",
    "sensitivity": "high"
}

result = client.call(call_llm, request)

# Check metadata
print(result["metadata"]["dcp_action"])  # "HOLD"
print(result["metadata"]["ml_invoked"])  # False
```

**Result:**
- DCP blocked request (HOLD)
- LLM was NOT invoked
- Decision depth: 2 (DCP blocked, LLM skipped)

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
from responsible_ai import ResponsibleAIClient, AuditLogger, DecisionCheckpoint, CompressionLayer

audit = AuditLogger(log_path="custom_audit.jsonl")
decision = DecisionCheckpoint(policy_rules=rules)
compression = CompressionLayer(confidence_threshold=2)

client = ResponsibleAIClient(
    audit_logger=audit,
    decision_checkpoint=decision,
    compression_layer=compression
)

# Run same request multiple times
for i in range(3):
    result = client.call(call_llm, request)
    print(f"Run {i+1}: depth={result['metadata']['decision_depth']}, dcl={result['metadata']['dcl_state']}")

# Expected output:
# Run 1: depth=2, dcl=miss    (DCL forwards to DCP)
# Run 2: depth=2, dcl=partial (DCL learning)
# Run 3: depth=1, dcl=hit     (DCL returns decision, skips DCP and LLM)
```

**Result:**
- Decision depth reduced: 2 → 2 → 1
- Run 3: DCP and LLM bypassed
- Proof: `layers_skipped: ["DCP", "LLM"]`

**Your audit log shows depth reduction:**
```json
{
  "decision_metadata": {
    "decision_depth": 1,
    "layers_invoked": ["DCL"],
    "layers_skipped": ["DCP", "LLM"],
    "dcl_state": "hit"
  }
}
```

---

## What You Get

Every `client.call()` returns metadata proving:

- **Who decided:** DCL? DCP? LLM?
- **What was skipped:** `layers_skipped: ["DCP", "LLM"]`
- **Was model invoked:** `ml_invoked: true/false`
- **Decision depth:** How many layers were traversed

**This is structural evidence, not post-hoc logs.**

When the next incident happens, you can show:
- "LLM was never called for this request class"
- "DCP blocked 47 requests before they reached the model"
- "Decision depth reduced from 3 to 1 after pattern learning"

---

## SDK Structure

```
sdk/
├── __init__.py          # Exports: ResponsibleAIClient, AuditLogger, etc.
├── client.py            # Main client (wraps LLM calls)
├── audit.py             # Audit Line (AJT) - observation only
├── decision.py          # Decision Line (DCP) - judgment checkpoint
└── compression.py       # Learning Line (DCL) - pattern learning
```

**Each product is independently usable:**

```python
# Use AJT only
from responsible_ai import AuditLogger
audit = AuditLogger()
audit.log(request_id, request, response, metadata)

# Use DCP only
from responsible_ai import DecisionCheckpoint
dcp = DecisionCheckpoint(policy_rules=rules)
result = dcp.evaluate(request)

# Use DCL only
from responsible_ai import CompressionLayer
dcl = CompressionLayer()
match, decision = dcl.query(request)
```

---

## Metadata Fields

Every `client.call()` returns:

```python
{
    "request_id": str,           # Unique ID
    "decision_depth": int,       # Layers traversed (1, 2, or 3)
    "dcl_state": str | None,     # "hit" | "partial" | "miss" | None
    "dcp_action": str,           # "ALLOW" | "HOLD" | "ESCALATE"
    "ml_invoked": bool,          # Was LLM actually called?
    "ajt_logged": bool           # Always True
}
```

---

## API/Gateway Option

Instead of SDK, use transparent proxy:

```python
# Your code (UNCHANGED)
response = requests.post(
    "https://api.responsible-ai.com/v1/chat",  # ← Just change URL
    json={"prompt": "..."}
)

# Behind the scenes: DCL → DCP → LLM → AJT
```

**See:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for gateway details

---

## Why SDK/API, Not Desktop Apps?

**Desktop apps (ChatGPT, Claude) operate at UI layer (post-inference).**
**SDK/API operates at decision layer (pre-invocation).**

**Key difference:**
- UI: Can block output, but model was already called
- SDK/API: Can prevent model call entirely

**Proof:**
- UI: No way to prove `ml_invoked: false`
- SDK/API: Logged evidence of non-invocation

**See:** [docs/WHY_SDK_NOT_UI.md](docs/WHY_SDK_NOT_UI.md)

---

## Documentation

- **[README.md](README.md)** — This file
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — SDK vs API architecture
- **[docs/WHY_SDK_NOT_UI.md](docs/WHY_SDK_NOT_UI.md)** — Why decision layer, not UI
- **[examples/before_sdk.py](examples/before_sdk.py)** — Your code without SDK
- **[examples/after_sdk.py](examples/after_sdk.py)** — One line added
- **[examples/full_configuration.py](examples/full_configuration.py)** — Full configuration

---

## Running Examples

```bash
cd examples

# Before SDK
python3 before_sdk.py

# After SDK (one line added)
python3 after_sdk.py

# Full configuration
python3 full_configuration.py
```

**Check generated logs:**
```bash
cat audit_trail.jsonl | python3 -m json.tool
```

---

## What This SDK Does NOT Do

❌ Replace your LLM
❌ Require specific model (model-agnostic)
❌ Add significant latency (in-process)
❌ Claim speed/cost improvements
❌ Require UI changes

## What This SDK DOES Do

✅ Wrap your LLM call (one line)
✅ Record who decided (DCL/DCP/LLM)
✅ Prove non-invocation (ml_invoked: false)
✅ Show decision depth reduction
✅ Provide structural evidence

---

## Next Steps

1. Copy `sdk/` to your project
2. Wrap your LLM call with `ResponsibleAIClient`
3. Check `audit_trail.jsonl` for decision logs
4. Configure DCP rules when ready (optional)
5. Enable DCL for pattern learning (optional)

**When the next incident happens, you'll have evidence.**

Not post-hoc explanations.
Not best-effort logs.

**Structural proof of what decided, and what was skipped.**
