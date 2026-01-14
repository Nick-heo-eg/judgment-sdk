# Product Map

**Judgment Gate is the only executable authority in this system.**

---

## Product ↔ Code Mapping

| Product Name | Code / Artifact | Authority | Visibility |
|--------------|----------------|-----------|------------|
| **Judgment Gate** | `decision_sdk/decision/dcp.py`, `decision_sdk/wrap.py` | **YES** | SDK: PUBLIC, Core: PRIVATE |
| Judgment SDK | `decision_sdk/` (wrapper) | NO | PUBLIC |
| Audit Add-On | `artifacts/`, `decision_sdk/audit/` | NO | PUBLIC |
| Knowledge Firewall | deployment topology (not implemented) | NO | N/A |
| State Canon | External: `judgment-state-canon` repo | NO | PUBLIC |

---

## Authority Location

**Question:** "Where in this repository can code actually stop execution?"

**Answer:** `decision_sdk/wrap.py` → signals only (ALLOW/HOLD/ESCALATE)

**Note:** Actual enforcement authority resides in `ajt-core` (private repository).

---

## Logical Structure (Declaration)

```
/gate (concept)
  - Judgment authority
  - Execution enforcement
  - Location: ajt-core (private repo)

/interfaces (public)
  - decision_sdk/ (wrapper)
  - artifacts/ (evidence)
  - examples/ (demos)

/standards (public)
  - spec (external repo)
  - constitution (external repo)
  - state-canon (external repo)
```

---

## Does NOT Do

### Judgment Gate
- Does NOT decide correctness
- Does NOT optimize output
- Does NOT improve accuracy

### Judgment SDK
- Does NOT execute judgment
- Does NOT hold authority
- Does NOT terminate execution

### Audit Add-On
- Does NOT analyze causes
- Does NOT provide recommendations
- Does NOT predict outcomes

### Knowledge Firewall
- Does NOT inspect content meaning
- Does NOT filter by topic
- Does NOT rate quality

---

## This Map Is Authority

When product names conflict with code location, this map is the reference.
