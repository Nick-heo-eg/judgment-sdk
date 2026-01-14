# Why SDK/API, Not UI?

**Question:** Why do we attach to SDK/API instead of building Desktop Apps or UI extensions?

**Answer:** Because intervention belongs at the decision layer, not the presentation layer.

---

## The Problem with UI-First Approach

### UI Extensions (ChatGPT Desktop, Claude Desktop, etc.)

**What they can do:**
- Show warnings to users
- Block/filter visible outputs
- Add approval buttons

**What they CANNOT do:**
- Prove ML/LLM was never invoked
- Create audit trail of system decisions
- Learn judgment structures across requests
- Provide legal non-invocation evidence

**Why:** UI runs AFTER the model has already been called.

```
Traditional UI extension:
User → LLM API → Model Inference → UI Filter → Display

Problem: Model was already invoked, even if output is blocked
```

---

## The SDK/API Approach

### Decision Layer Intervention

**What SDK/API can do:**
- Intercept BEFORE model invocation
- Decide whether to call model at all
- Log decision depth and layer bypass
- Provide structural non-invocation evidence

```
SDK/API approach:
User → SDK → DCL → DCP → [conditional] LLM → AJT

Advantage: Model invocation is conditional, not guaranteed
```

---

## Where Each Product Attaches

### Audit Line (AJT)

**Attaches to:** Request/Response boundary
**Records:** Everything that flows through the decision pipeline
**Evidence:** Who decided, when, and which layers were involved

**Why SDK/API:**
- Logs at system level, not user level
- Captures metadata (decision_depth, layers_skipped)
- Creates replay-capable audit trail

---

### Decision Line (DCP)

**Attaches to:** Pre-invocation checkpoint
**Decides:** ALLOW/HOLD/ESCALATE before calling model
**Evidence:** Model was blocked structurally, not post-hoc

**Why SDK/API:**
- Intervenes BEFORE model call
- Can prevent invocation entirely
- Proof: `ml_invoked: false` in logs

---

### Learning Line (DCL)

**Attaches to:** Request routing layer
**Learns:** Which decision patterns repeat
**Effect:** Reduces decision depth (layers bypassed)

**Why SDK/API:**
- Operates at routing level, not output level
- Bypasses downstream layers structurally
- Proof: `layers_skipped: ["DCP", "ML/LLM"]`

---

## Comparison Table

| Feature | UI Extension | SDK/API |
|---------|--------------|---------|
| **Intervention timing** | Post-inference | Pre-invocation |
| **Can prevent model call** | No | Yes |
| **Non-invocation evidence** | No | Yes (logs) |
| **Decision depth visible** | No | Yes |
| **Layer bypass** | No | Yes |
| **Audit trail** | User-level | System-level |
| **Learning across requests** | No | Yes |

---

## Why Not Desktop Apps?

Desktop apps (ChatGPT Desktop, Claude Desktop) are **consumer tools**, not **decision infrastructure**.

**They are good for:**
- User-facing warnings
- Manual approval workflows
- Consumer safety features

**They are NOT good for:**
- System-level decision control
- Audit trails for legal review
- Structural non-invocation
- Enterprise policy enforcement

**Our products attach to SDK/API because:**
1. Decisions happen before invocation (not after)
2. Evidence is structural (not post-hoc)
3. Intervention is architectural (not behavioral)

---

## MCP and Desktop Apps: Demo/Spread Channels Only

**MCP (Model Context Protocol):** Useful for demos and developer experimentation
**Desktop Apps:** Useful for end-user awareness and adoption

**But:** These are **spread channels**, not **core product channels**.

**Why:**
- MCP is consumer-developer focused
- Desktop apps are end-user focused
- Our products are **enterprise SDK/API focused**

**Strategy:**
- Build for SDK/API first (core)
- Use MCP/Desktop for demos (spread)
- Don't confuse distribution with architecture

---

## Where We Attach

### Primary Channel: SDK

```python
from responsible_ai import ResponsibleAIClient

client = ResponsibleAIClient()
result = client.call(your_llm_function, request)
```

**One line added. Decision layer now in place.**

### Secondary Channel: API/Gateway

```
Client → Our API Gateway → [DCL → DCP → conditional LLM] → Response
```

**Transparent proxy. Client code unchanged.**

### Demo/Spread Channels: MCP, Desktop Apps

**Purpose:** Show what's possible
**NOT purpose:** Core product delivery

---

## Key Principle

**"Intervention at the decision layer, not the presentation layer."**

**UI shows outputs. SDK/API controls inputs.**

We attach to SDK/API because that's where decisions are made, not where they're displayed.
