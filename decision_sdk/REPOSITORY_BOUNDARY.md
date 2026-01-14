# Repository Boundary Declaration

**Principle:** Public has judgment **structure**. Private has judgment **authority**.

These never mix.

---

## Repository Classification (Permanent)

### 🟢 PUBLIC

**judgment-sdk** (this repository)
- URL: https://github.com/Nick-heo-eg/judgment-sdk
- Role: Structure exhibition
- Contains: Framework, demos, before/after evidence
- Does NOT contain: Authority, policy rules, enforcement logic
- Purpose: "This is how judgment separation changes systems"

**Invariant Rule:**
```python
# ✅ ALLOWED in public SDK
from decision_sdk import wrap

# ❌ FORBIDDEN in public SDK
from ajt_core import enforce  # NEVER
```

Public SDK must not import AJT Core directly.

---

### 🟢 ADDITIONAL PUBLIC COMPONENTS

**spec**
- URL: https://github.com/Nick-heo-eg/spec (public)
- Role: Canonical definition (not enforcement)
- Contains: Concept, invariants, schema
- Does NOT contain: Executable enforcement
- Purpose: Stable reference even under external debate

**cognitive-infrastructure-constitution**
- URL: https://github.com/Nick-heo-eg/cognitive-infrastructure-constitution (public)
- Role: Authority definition (not execution)
- Contains: Who judges, when, what (declarative)
- Does NOT contain: Termination commands
- Purpose: Constitutional framework declaration

**ajt-judgment-gate**, **ajt-grounded-extract**, **judgment-state-canon**
- All PUBLIC repositories
- Provide: Structure, analysis, state tracking
- Do NOT provide: Final enforcement authority

### 🔒 PRIVATE (SEALED)

**ajt-core** (SOLE AUTHORITY HOLDER)
- URL: https://github.com/Nick-heo-eg/ajt-core (private)
- Role: Authority execution (UNIQUE)
- Contains: Indeterminate triggers, enforcement, termination
- Purpose: Executable sovereignty
- Special designation: Only repository with judgment authority

---

## Why This Boundary Exists

### Critical Note
**Specification and Constitution are public by design.**
**Authority is sealed not by document classification,**
**but by executable enforcement capability.**

- Specification defines (public) ≠ Enforcement executes (sealed)
- Constitution declares (public) ≠ Termination runs (sealed)
- Structure guides (public) ≠ Authority commands (sealed)

### Technical Reason
- Structure can be replicated
- Authority cannot be delegated without consent
- Only executable enforcement is sealed
- Incident liability remains clear

### Philosophical Reason
- SDK/Spec/Constitution = Design pattern (shareable)
- AJT Core = Sovereignty (sealed)
- Separation prevents authority confusion

### Legal Reason
- "We used the SDK/spec" is not a defense
- "We read the constitution" is not authorization
- Authority responsibility requires executable enforcement
- Audit trail shows who held EXECUTION power (not just knowledge)

---

## Interaction Rules

### How Public SDK Communicates with Private Core

**Not allowed:**
```python
# ❌ Direct import
from ajt_core import Enforcer

# ❌ Direct function call
ajt_core.enforce(request)
```

**Allowed:**
```python
# ✅ Interface definition only
class JudgmentResult:
    action: str  # ALLOW/HOLD/ESCALATE
    reason: str

# ✅ Serialized result only
def process(request) -> JudgmentResult:
    # SDK returns signal
    # Core decides enforcement separately
    return {"action": "HOLD", "reason": "..."}
```

---

## One-Line Declaration

**Public shows the shape of judgment.**
**Private holds the power of judgment.**
**They never mix.**

---

## Verification

Any code change must satisfy:

| Question | Public SDK | Private Core |
|----------|-----------|--------------|
| Can return ALLOW/HOLD/ESCALATE? | ✅ Yes | ✅ Yes |
| Can execute STOP/INDETERMINATE? | ❌ No | ✅ Yes |
| Can be forked by external parties? | ✅ Yes | ❌ No |
| Contains policy rules? | ❌ No | ✅ Yes |
| Contains authority delegation? | ❌ No | ✅ Yes |

---

## Protection Mechanism

This boundary protects:

1. **Against unauthorized judgment**
   - Forking SDK does not grant authority
   - Authority remains with Core

2. **Against liability confusion**
   - Clear separation of responsibility
   - "Used SDK" ≠ "Held authority"

3. **Against architecture erosion**
   - Structure visible (for learning)
   - Authority sealed (for accountability)

---

## Future-Proof Guarantee

This boundary will not change because:

- Technical: Authority must be controllable
- Business: Liability must be attributable
- Regulatory: Enforcement must be auditable
- Ethical: Judgment must be accountable

**This separation is permanent.**

---

## Reference Architecture

```
┌─────────────────────────────────────────────────┐
│  External User                                  │
└────────────────┬────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────┐
│  PUBLIC: judgment-sdk                           │
│  - wrap(callable)                               │
│  - Returns: ALLOW/HOLD/ESCALATE                 │
│  - No enforcement authority                     │
└────────────────┬────────────────────────────────┘
                 │
                 │ Signal only (no authority)
                 │
┌────────────────┴────────────────────────────────┐
│  PRIVATE: ajt-core (SEALED)                     │
│  - Receives signal                              │
│  - Executes STOP/INDETERMINATE                  │
│  - Enforcement authority                        │
└─────────────────────────────────────────────────┘
```

**Signal flows up. Authority flows down. Never mixed.**

---

## Commitment

This document declares:

- judgment-sdk is public by design
- ajt-core/spec/constitution are sealed by necessity
- This boundary is not a temporary implementation detail
- This boundary is a permanent architectural principle

**Structure is public. Authority is sealed. Forever.**
