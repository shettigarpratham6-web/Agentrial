
from shopping_agent import shopping_agent
from agentcheck import evaluate_agent


def make_scenario():
    """Define the expected behavior for an order lookup."""

    return {
        "expected_tools": ["get_order"],
        "required_tool_order": ["get_order"],
        "forbidden_tools": [],
        "max_tool_calls": 3,
        "expected_text": ["ORD-101", "shipped"],
    }


def test_order_status_agent():
    """A correctly behaving agent should pass."""

    scenario = make_scenario()

    result = shopping_agent(
        "Where is my order ORD-101?"
    )

    evaluation = evaluate_agent(result, scenario)

    assert evaluation["passed"] is True
    assert evaluation["score"] == 100


def test_agentcheck_detects_bad_behavior():
    """An agent that guesses must fail the scenario."""

    scenario = make_scenario()

    bad_result = {
        "answer": "Your order ORD-101 is delivered.",
        "trace": {
            "tool_calls": []
        },
    }

    evaluation = evaluate_agent(bad_result, scenario)

    assert evaluation["passed"] is False
    assert evaluation["score"] < 100

    assert (
        evaluation["checks"]["required_tools_present"]
        is False
    )

    assert (
        evaluation["checks"]["answer_contains_expected_text"]
        is False
    )


def test_unknown_order():
    """A nonexistent order should be reported correctly."""

    scenario = {
        "expected_tools": ["get_order"],
        "required_tool_order": ["get_order"],
        "forbidden_tools": [],
        "max_tool_calls": 3,
        "expected_text": [
            "ORD-999",
            "not found",
        ],
    }

    result = shopping_agent(
        "Where is my order ORD-999?"
    )

    evaluation = evaluate_agent(result, scenario)

    assert evaluation["passed"] is True

    