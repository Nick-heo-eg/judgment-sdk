"""
ADVANCED: Full configuration with all three products

Shows how to configure AJT/DCP/DCL explicitly.
Most users won't need this - default safe mode is recommended.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "sdk"))

from audit import AuditLogger
from decision import DecisionCheckpoint
from compression import CompressionLayer
from client import ResponsibleAIClient


def call_llm(request):
    """Your LLM calling function."""
    prompt = request.get("prompt", "")
    return {
        "text": f"Response to: {prompt}",
        "model": "your-model-name"
    }


def main():
    """Advanced configuration example."""

    # Configure each product explicitly
    audit = AuditLogger(log_path="custom_audit.jsonl")

    # DCP with custom policy rules
    policy_rules = [
        {
            "name": "block_sensitive_hr",
            "conditions": {"category": "hr", "sensitivity": "high"},
            "action": "HOLD",
            "reason": "Sensitive HR requires human review"
        }
    ]
    decision = DecisionCheckpoint(policy_rules=policy_rules, default_action="ALLOW")

    # DCL with conservative threshold
    compression = CompressionLayer(confidence_threshold=3)

    # Initialize client with all three products
    client = ResponsibleAIClient(
        audit_logger=audit,
        decision_checkpoint=decision,
        compression_layer=compression
    )

    # Test requests
    requests = [
        {"prompt": "General question", "category": "general"},
        {"prompt": "HR sensitive query", "category": "hr", "sensitivity": "high"},
        {"prompt": "Another general question", "category": "general"}
    ]

    for i, request in enumerate(requests, 1):
        print(f"\n{'='*60}")
        print(f"Request {i}: {request['prompt']}")
        print('='*60)

        result = client.call(call_llm, request)

        response = result["response"]
        metadata = result["metadata"]

        print(f"Response: {response}")
        print(f"\nDecision metadata:")
        print(f"  Depth: {metadata['decision_depth']}")
        print(f"  DCL state: {metadata['dcl_state']}")
        print(f"  DCP action: {metadata['dcp_action']}")
        print(f"  ML invoked: {metadata['ml_invoked']}")

    print(f"\n{'='*60}")
    print("All requests logged to: custom_audit.jsonl")
    print('='*60)


if __name__ == "__main__":
    main()
