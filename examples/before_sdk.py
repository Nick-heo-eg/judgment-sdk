"""
BEFORE: Calling LLM directly (no responsible AI products)

This is your existing code.
"""


def call_llm(prompt):
    """
    Your existing LLM calling function.

    Could be OpenAI, Claude, or any other model.
    """
    # Simulated LLM call
    return {
        "text": f"Response to: {prompt}",
        "model": "your-model-name"
    }


def main():
    """Your existing application code."""

    # Your existing code - just calls LLM directly
    prompt = "What is the company policy on remote work?"

    response = call_llm(prompt)

    print("Response:", response["text"])


if __name__ == "__main__":
    main()
