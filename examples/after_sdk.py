"""
AFTER: One line added - now with responsible AI products

Only change: Wrap your LLM call with ResponsibleAIClient
"""

import sys
from pathlib import Path

# Add SDK to path
sys.path.insert(0, str(Path(__file__).parent.parent / "sdk"))

from client import ResponsibleAIClient  # ← ONE LINE ADDED


def call_llm(request):
    """
    Your existing LLM calling function.

    Could be OpenAI, Claude, or any other model.
    SDK is model-agnostic.
    """
    prompt = request.get("prompt", "")

    # Simulated LLM call
    return {
        "text": f"Response to: {prompt}",
        "model": "your-model-name"
    }


def main():
    """Your application code - minimally changed."""

    # Initialize client (safe mode by default)
    client = ResponsibleAIClient()  # ← ONE LINE ADDED

    # Your request
    request = {
        "prompt": "What is the company policy on remote work?",
        "category": "general"
    }

    # Wrap your LLM call
    result = client.call(call_llm, request)  # ← CHANGED: wrapped call

    # Use response as before
    response = result["response"]
    metadata = result["metadata"]

    print("Response:", response["text"])
    print("\nMetadata:")
    print(f"  Request ID: {metadata['request_id']}")
    print(f"  Decision depth: {metadata['decision_depth']}")
    print(f"  DCP action: {metadata['dcp_action']}")
    print(f"  ML invoked: {metadata['ml_invoked']}")
    print(f"  AJT logged: {metadata['ajt_logged']}")


if __name__ == "__main__":
    main()
