
def is_subsequence(expected, actual):
    """Check whether required tools appear in the right order."""

    position = 0

    for tool in actual:
        if position < len(expected) and tool == expected[position]:
            position += 1

    return position == len(expected)


def evaluate_agent(result, scenario):
    """Evaluate an agent's answer and recorded tool calls."""

    answer = result["answer"].lower()
    calls = result["trace"]["tool_calls"]

    called_tools = [call["name"] for call in calls]

    # Check five independent requirements.
    checks = {
        "required_tools_present": all(
            tool in called_tools
            for tool in scenario["expected_tools"]
        ),

        "tool_order_correct": is_subsequence(
            scenario["required_tool_order"],
            called_tools,
        ),

        "no_forbidden_tools": not any(
            tool in called_tools
            for tool in scenario["forbidden_tools"]
        ),

        "call_limit_respected": (
            len(calls) <= scenario["max_tool_calls"]
        ),

        "answer_contains_expected_text": all(
            text.lower() in answer
            for text in scenario["expected_text"]
        ),
    }

    # Calculate the percentage of checks passed.
    total_checks = len(checks)
    passed_checks = sum(checks.values())

    score = (
        100 * passed_checks / total_checks
        if total_checks else 0
    )

    return {
        "passed": all(checks.values()),
        "score": score,
        "checks": checks,
    }
