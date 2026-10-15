
from judge import judge_answer


def is_subsequence(expected, actual):
    """Check whether required tools appear in the right order."""

    position = 0

    for tool in actual:
        if position < len(expected) and tool == expected[position]:
            position += 1

    return position == len(expected)


def evaluate_agent(result, scenario, use_llm_judge=False):
    """Evaluate an agent's answer and recorded tool calls."""

    answer = result["answer"]
    calls = result["trace"]["tool_calls"]

    called_tools = [call["name"] for call in calls]

    # Check tool usage and execution constraints.
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
    }

    judgment = None

    if use_llm_judge:
        # Evaluate the meaning of the answer with the LLM judge.
        judgment = judge_answer(
            question=scenario["question"],
            expected_facts=scenario["expected_text"],
            agent_answer=answer,
        )

        checks["semantic_answer_correct"] = judgment["correct"]

    else:
        # Preserve the original exact-text evaluation.
        checks["answer_contains_expected_text"] = all(
            text.lower() in answer.lower()
            for text in scenario["expected_text"]
        )

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
        "judge": judgment,
    }
