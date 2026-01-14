# Judgment SDK Verification Guide

**Objective:** Verify SDK works as claimed, from a user's perspective.

---

## Test 1: Does SDK Actually Reduce ML Calls?

### Expected Claim
- Before SDK: 100% ML invocation
- After SDK: <100% ML invocation (with DCP/DCL enabled)

### How to Verify

```bash
cd decision_sdk/demo

# Step 1: Run before.py
python3 before.py > /tmp/before_output.txt

# Step 2: Run after.py
python3 after.py > /tmp/after_output.txt

# Step 3: Check results
grep "ML calls:" /tmp/before_output.txt
grep "ML calls:" /tmp/after_output.txt
```

### Success Criteria
- `before.py`: Shows "ML calls: 6 (100%)"
- `after.py`: Shows "ML calls: 2 (11.1%)" or similar reduced percentage

### What This Proves
SDK prevents ML/LLM invocation structurally, not post-hoc filtering.

---

## Test 2: Does Audit Log Contain Structural Evidence?

### Expected Claim
- Audit log shows `ml_invoked: false` when DCP blocks request
- Audit log shows `layers_skipped: ["LLM"]` when bypassed

### How to Verify

```bash
cd decision_sdk/demo

# Run after.py to generate audit log
python3 after.py

# Check for non-invocation evidence
cat demo_audit.jsonl | grep -o '"ml_invoked": false' | wc -l
cat demo_audit.jsonl | grep -o '"layers_skipped": \["LLM"\]' | wc -l
cat demo_audit.jsonl | grep -o '"layers_skipped": \["DCP", "LLM"\]' | wc -l
```

### Success Criteria
- At least 1 entry with `"ml_invoked": false`
- At least 1 entry with `"layers_skipped"` containing "LLM"

### What This Proves
Evidence is structural, not post-hoc logs. You can prove "LLM was never called."

---

## Test 3: Does DCL Actually Reduce Decision Depth?

### Expected Claim
- Run 1: Decision depth 2-3 (DCP→LLM or DCL→DCP→LLM)
- Run 3: Decision depth 1 (DCL hit, skip DCP+LLM)

### How to Verify

```bash
cd decision_sdk/demo

# Run after.py (contains 3 runs)
python3 after.py

# Extract decision depths by run
echo "Run 1 depths:"
head -6 demo_audit.jsonl | grep -o '"decision_depth": [0-9]'

echo "Run 3 depths:"
tail -6 demo_audit.jsonl | grep -o '"decision_depth": [0-9]'
```

### Success Criteria
- Run 1: Mix of depth 2 and 3
- Run 3: Majority depth 1

### What This Proves
DCL learns judgment structures and reduces depth over time.

---

## Test 4: Can I Integrate This Into My Own Code?

### Expected Claim
- "One line added" integration
- Works with any LLM function

### How to Verify

Create a test file `my_test.py`:

```python
import sys
sys.path.insert(0, '/home/nick-heo123/code/sdk_integration')

from decision_sdk import wrap

# Your LLM function (mock)
def my_llm(request):
    return {"text": f"Response to: {request['prompt']}"}

# Wrap it
wrapped_llm = wrap(my_llm)

# Call it
result = wrapped_llm({"prompt": "Test request"})

# Verify metadata exists
assert "metadata" in result
assert "ml_invoked" in result["metadata"]
assert "decision_depth" in result["metadata"]

print("✓ Integration successful")
print(f"  ML invoked: {result['metadata']['ml_invoked']}")
print(f"  Decision depth: {result['metadata']['decision_depth']}")
```

Run:
```bash
python3 my_test.py
```

### Success Criteria
- Script runs without errors
- Prints "✓ Integration successful"
- Shows `ml_invoked` and `decision_depth`

### What This Proves
SDK is usable with minimal integration effort.

---

## Test 5: Does DCP Actually Block Requests?

### Expected Claim
- DCP evaluates requests before LLM
- Requests matching policy rules are blocked (`ml_invoked: false`)

### How to Verify

Create `test_dcp_block.py`:

```python
import sys
sys.path.insert(0, '/home/nick-heo123/code/sdk_integration')

from decision_sdk import wrap

def my_llm(request):
    return {"text": "LLM was called!"}

# Configure DCP with blocking rule
config = {
    "ajt": {"enabled": True, "log_path": "test_dcp.jsonl"},
    "dcp": {
        "enabled": True,
        "default_action": "ALLOW",
        "policy_rules": [
            {
                "name": "block_sensitive",
                "conditions": {"category": "sensitive"},
                "action": "HOLD",
                "reason": "Sensitive requests blocked"
            }
        ]
    },
    "dcl": {"enabled": False}
}

wrapped_llm = wrap(my_llm, config)

# Test 1: Normal request (should call LLM)
result1 = wrapped_llm({"prompt": "Normal request", "category": "general"})
print(f"Test 1 - ML invoked: {result1['metadata']['ml_invoked']}")  # Should be True

# Test 2: Sensitive request (should NOT call LLM)
result2 = wrapped_llm({"prompt": "Sensitive data", "category": "sensitive"})
print(f"Test 2 - ML invoked: {result2['metadata']['ml_invoked']}")  # Should be False
print(f"Test 2 - DCP action: {result2['metadata']['dcp_action']}")  # Should be HOLD

assert result1['metadata']['ml_invoked'] == True, "Normal request should invoke ML"
assert result2['metadata']['ml_invoked'] == False, "Sensitive request should NOT invoke ML"

print("✓ DCP blocking verified")
```

Run:
```bash
python3 test_dcp_block.py
```

### Success Criteria
- Test 1: `ml_invoked: True`
- Test 2: `ml_invoked: False`, `dcp_action: HOLD`
- Script prints "✓ DCP blocking verified"

### What This Proves
DCP blocks requests BEFORE LLM invocation, not after.

---

## Test 6: Is Audit Log Replayable?

### Expected Claim
- Audit log contains full request/response/metadata
- Log is machine-readable (JSONL format)

### How to Verify

```bash
cd decision_sdk/demo

# Generate audit log
python3 after.py

# Parse audit log
python3 << 'EOF'
import json

with open("demo_audit.jsonl") as f:
    for line in f:
        entry = json.loads(line)

        # Verify required fields exist
        assert "timestamp" in entry
        assert "request_id" in entry
        assert "request" in entry
        assert "response" in entry
        assert "decision_metadata" in entry

        metadata = entry["decision_metadata"]
        assert "decision_depth" in metadata
        assert "ml_invoked" in metadata
        assert "layers_invoked" in metadata

print("✓ Audit log is valid and replayable")
EOF
```

### Success Criteria
- Script runs without assertion errors
- Prints "✓ Audit log is valid and replayable"

### What This Proves
Audit log is structured, complete, and machine-readable.

---

## Test 7: Zero Dependencies Claim

### Expected Claim
- SDK has no external dependencies
- Pure Python implementation

### How to Verify

```bash
cd decision_sdk

# Check for requirements.txt or setup.py dependencies
find . -name "requirements.txt" -o -name "setup.py" -o -name "pyproject.toml"

# Grep for imports to verify they're stdlib only
grep -r "^import\|^from" --include="*.py" . | grep -v "__pycache__" | grep -v "demo_audit"
```

### Success Criteria
- No `requirements.txt` or dependency files
- All imports are Python standard library (`json`, `uuid`, `datetime`, `typing`)

### What This Proves
SDK has zero external dependencies, as claimed.

---

## Summary Checklist

Run all tests and verify:

- [ ] **Test 1**: ML calls reduced (100% → <100%)
- [ ] **Test 2**: Audit log contains `ml_invoked: false` evidence
- [ ] **Test 3**: Decision depth reduced over runs (3→1)
- [ ] **Test 4**: Integration works with custom LLM function
- [ ] **Test 5**: DCP blocks requests before LLM invocation
- [ ] **Test 6**: Audit log is replayable (valid JSONL)
- [ ] **Test 7**: Zero external dependencies

If all tests pass, SDK works as claimed.

---

## What This Verification Proves

1. **Structural non-invocation**: SDK prevents ML/LLM calls, not just filters output
2. **Judgment depth reduction**: DCL learns patterns and bypasses layers
3. **Evidence trail**: Audit log proves who judged and what was skipped
4. **Minimal integration**: One-line wrap works with any LLM
5. **Pre-invocation blocking**: DCP decides before model call
6. **Machine-readable logs**: Audit trail is structured and replayable
7. **Zero dependencies**: Pure Python, no external libs

**This is objective, user-verifiable proof that Judgment SDK works as claimed.**
