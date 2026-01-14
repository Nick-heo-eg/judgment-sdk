"""
Before SDK: Traditional LLM calls

Expected result: 100% ML invocation
"""


def mock_llm(request):
    """Mock LLM for demo purposes."""
    prompt = request.get("prompt", "")
    return {
        "text": f"Response to: {prompt}",
        "model": "mock-llm-v1"
    }


def main():
    """Run demo without SDK."""

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

    print("=" * 60)
    print("BEFORE JUDGMENT SDK: Traditional LLM calls")
    print("=" * 60)

    for i, request in enumerate(test_requests, 1):
        # Direct LLM call
        response = mock_llm(request)
        ml_call_count += 1

        print(f"\nRequest {i}: {request['prompt'][:30]}...")
        print(f"  ML called: YES")
        print(f"  Response: {response['text'][:50]}...")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total requests: {total_requests}")
    print(f"ML calls: {ml_call_count} (100%)")
    print(f"Decision depth: N/A (direct calls)")
    print("=" * 60)


if __name__ == "__main__":
    main()
