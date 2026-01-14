# SDK/API Architecture

How AJT/DCP/DCL attach to your LLM calls.

---

## Architecture Diagram

### SDK Approach (Direct Integration)

```
┌──────────────────────────────────────────────────────────────────┐
│  Your Application Code                                           │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ from responsible_ai import ResponsibleAIClient              ││
│  │                                                              ││
│  │ client = ResponsibleAIClient()                              ││
│  │ result = client.call(your_llm_function, request)            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│                           ↓                                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Responsible AI SDK                                           ││
│  │                                                              ││
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  ││
│  │  │   DCL   │ →  │   DCP   │ →  │   LLM   │ →  │   AJT   │  ││
│  │  │(optional)│    │(default)│    │(your fn)│    │(logger) │  ││
│  │  └─────────┘    └─────────┘    └─────────┘    └─────────┘  ││
│  │      ↓              ↓              ↓              ↓          ││
│  │    query        evaluate         call          log          ││
│  │  hit/miss      ALLOW/HOLD      response       evidence      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
│                           ↓                                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Your LLM Provider (OpenAI, Claude, etc.)                     ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

---

### API/Gateway Approach (Transparent Proxy)

```
┌──────────────────────────────────────────────────────────────────┐
│  Your Application Code (UNCHANGED)                               │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ # Your existing code                                         ││
│  │ response = requests.post(                                    ││
│  │     "https://api.responsible-ai.com/v1/chat",  # ← URL only ││
│  │     json={"prompt": "..."}                                   ││
│  │ )                                                            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────────┐
│  Responsible AI Gateway                                          │
│                                                                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │   DCL   │ →  │   DCP   │ →  │   LLM   │ →  │   AJT   │      │
│  │(optional)│    │(active) │    │ Proxy   │    │(logger) │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│      ↓              ↓              ↓              ↓              │
│    query        evaluate         proxy          log             │
│  hit/miss      ALLOW/HOLD      to LLM        evidence           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────────┐
│  Upstream LLM Provider (OpenAI, Claude, etc.)                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Decision Flow

### Scenario 1: DCL Hit (Depth = 1)

```
Request
  ↓
┌──────────────┐
│     DCL      │  Query: "Is this pattern known?"
│   (Layer 1)  │  Result: HIT (confidence >= threshold)
└──────┬───────┘  Decision: HOLD (from learned structure)
       │
       ↓
   [RETURN]  ← Decision made, DCP and LLM skipped
       │
       ↓
┌──────────────┐
│     AJT      │  Log: decision_depth=1, layers_skipped=["DCP","LLM"]
└──────────────┘
```

**Proof:** `ml_invoked: false`, `dcl_state: "hit"`

---

### Scenario 2: DCP HOLD (Depth = 2)

```
Request
  ↓
┌──────────────┐
│     DCL      │  Query: "Is this pattern known?"
│   (Layer 1)  │  Result: MISS or PARTIAL
└──────┬───────┘  Action: Forward to DCP
       │
       ↓
┌──────────────┐
│     DCP      │  Evaluate: Check policy rules
│   (Layer 2)  │  Result: HOLD
└──────┬───────┘  Reason: "Sensitive request requires review"
       │
       ↓
   [RETURN]  ← Decision made, LLM skipped
       │
       ↓
┌──────────────┐
│     AJT      │  Log: decision_depth=2, layers_skipped=["LLM"]
└──────────────┘
```

**Proof:** `ml_invoked: false`, `dcp_action: "HOLD"`

---

### Scenario 3: DCP ALLOW → LLM (Depth = 3)

```
Request
  ↓
┌──────────────┐
│     DCL      │  Query: "Is this pattern known?"
│   (Layer 1)  │  Result: MISS or PARTIAL
└──────┬───────┘  Action: Forward to DCP
       │
       ↓
┌──────────────┐
│     DCP      │  Evaluate: Check policy rules
│   (Layer 2)  │  Result: ALLOW
└──────┬───────┘  Action: Proceed to LLM
       │
       ↓
┌──────────────┐
│     LLM      │  Call: your_llm_function(request)
│   (Layer 3)  │  Result: Model response
└──────┬───────┘
       │
       ↓
┌──────────────┐
│     AJT      │  Log: decision_depth=3, ml_invoked=true
└──────────────┘
```

**Proof:** `ml_invoked: true`, `dcp_action: "ALLOW"`

---

## SDK vs API Comparison

| Aspect | SDK Approach | API/Gateway Approach |
|--------|--------------|---------------------|
| **Integration** | One line added to code | URL change only |
| **Code changes** | Minimal (wrap LLM call) | None (transparent proxy) |
| **Decision flow** | In-process | Network call |
| **Latency** | Minimal | Network overhead |
| **Control** | Full (local SDK) | Gateway config |
| **Deployment** | App-level | Infrastructure-level |

---

## Where Products Attach

### Audit Line (AJT)

**Attachment point:** Request/Response boundary

```python
# SDK
client.call(llm_function, request)
  ↓
  [DCL → DCP → LLM]
  ↓
AJT.log(request, response, metadata)  ← Logs everything
```

**Gateway:** Same, but at proxy level

---

### Decision Line (DCP)

**Attachment point:** Pre-invocation checkpoint

```python
# SDK
client.call(llm_function, request)
  ↓
  DCL (if enabled)
  ↓
DCP.evaluate(request)  ← Decides ALLOW/HOLD/ESCALATE
  ↓
  [conditional] LLM
```

**Gateway:** Same, evaluated at gateway before proxying

---

### Learning Line (DCL)

**Attachment point:** Request routing layer

```python
# SDK
client.call(llm_function, request)
  ↓
DCL.query(request)  ← Checks for learned pattern
  ↓
  [if hit] Return decision (skip DCP, LLM)
  [if miss] Forward to DCP
```

**Gateway:** Same, routing decision at gateway

---

## Integration Patterns

### Pattern 1: SDK-Only (Recommended for startups)

```python
# Your existing code
def call_llm(prompt):
    return openai.chat.completions.create(...)

# Add one line
from responsible_ai import ResponsibleAIClient
client = ResponsibleAIClient()

# Wrap your call
result = client.call(call_llm, {"prompt": prompt})
```

---

### Pattern 2: API Gateway (Recommended for scale)

```python
# Your existing code (UNCHANGED)
response = requests.post(
    "https://api.your-company.com/llm",
    json={"prompt": prompt}
)

# Behind the scenes: Gateway handles DCL/DCP/LLM/AJT
```

---

### Pattern 3: Hybrid (SDK + Gateway)

```python
# SDK points to your gateway
client = ResponsibleAIClient(api_endpoint="https://your-gateway.com")
result = client.call_api(request)

# Gateway runs DCL/DCP and proxies to LLM
```

---

## Key Principles

**1. Intervention before invocation**
→ DCP decides BEFORE calling LLM, not after

**2. Evidence through logs**
→ AJT records decision_depth, layers_skipped, ml_invoked

**3. Learning at routing layer**
→ DCL operates before DCP, can bypass both DCP and LLM

**4. Model-agnostic**
→ Works with any LLM (OpenAI, Claude, local models)

---

## Why This Architecture?

**SDK approach:**
- Minimal code changes
- Full control
- Local decision flow
- No network dependency

**API/Gateway approach:**
- Zero code changes
- Centralized policy
- Infrastructure-level control
- Easy to update rules

**Both provide:**
- Pre-invocation intervention
- Structural non-invocation evidence
- Decision depth visibility
- Layer bypass capability
