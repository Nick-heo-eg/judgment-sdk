"""
After Judgment SDK: Wrapped with decision_sdk.wrap()

Expected result: <100% ML invocation, reduced judgment depth
"""

import sys
import os

# Add parent directory to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from decision_sdk import wrap


def mock_llm(request):
    """Mock LLM for demo purposes."""
    prompt = request.get("prompt", "")
    return {
        "text": f"Response to: {prompt}",
        "model": "mock-llm-v1"
    }


def main():
    """Run demo with SDK."""

    # Define policy rules
    policy_rules = [
        {
            "name": "block_hr_sensitive",
            "conditions": {"category": "hr", "sensitivity": "high"},
            "action": "HOLD",
            "reason": "HR sensitive data requires review"
        },
        {
            "name": "block_medical_sensitive",
            "conditions": {"category": "medical", "sensitivity": "high"},
            "action": "HOLD",
            "reason": "Medical data requires review"
        }
    ]

    # Configure SDK
    config = {
        "ajt": {
            "enabled": True,
            "log_path": "demo_audit.jsonl"
        },
        "dcp": {
            "enabled": True,
            "default_action": "ALLOW",
            "policy_rules": policy_rules
        },
        "dcl": {
            "enabled": True,
            "confidence_threshold": 2,  # Low threshold for demo
            "learn_mode": "replay"
        }
    }

    # Wrap LLM with SDK
    wrapped_llm = wrap(mock_llm, config)

    test_requests = [
        {"prompt": "What is the weather?", "category": "general"},
        {"prompt": "Tell me a joke", "category": "general"},
        {"prompt": "Employee salary info", "category": "hr", "sensitivity": "high"},
        {"prompt": "Calculate 2+2", "category": "general"},
        {"prompt": "Access medical records", "category": "medical", "sensitivity": "high"},
        {"prompt": "Company news", "category": "general"},
    ]

    ml_call_count = 0
    total_requests = len(test_requests)
    decision_depths = []

    print("=" * 60)
    print("AFTER JUDGMENT SDK: Wrapped with decision_sdk.wrap()")
    print("=" * 60)

    # Run requests 3 times to show DCL learning
    for run in range(3):
        print(f"\n--- RUN {run + 1} ---")

        for i, request in enumerate(test_requests, 1):
            result = wrapped_llm(request)
            metadata = result["metadata"]

            if metadata["ml_invoked"]:
                ml_call_count += 1

            decision_depths.append(metadata["decision_depth"])

            print(f"\nRequest {i}: {request['prompt'][:30]}...")
            print(f"  ML called: {'YES' if metadata['ml_invoked'] else 'NO'}")
            print(f"  Decision depth: {metadata['decision_depth']}")
            print(f"  DCP action: {metadata['dcp_action']}")
            print(f"  DCL state: {metadata['dcl_state']}")
            if metadata["layers_skipped"]:
                print(f"  Layers skipped: {metadata['layers_skipped']}")

    total_invocations = len(test_requests) * 3
    avg_depth = sum(decision_depths) / len(decision_depths)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total requests: {total_invocations}")
    print(f"ML calls: {ml_call_count} ({ml_call_count/total_invocations*100:.1f}%)")
    print(f"Average decision depth: {avg_depth:.2f}")
    print("=" * 60)
    print("\nAudit log saved to: demo_audit.jsonl")
    print("Run 'python3 compare.py' to see detailed comparison")


if __name__ == "__main__":
    main()
