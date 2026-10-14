
import pytest

from reliability import summarize_trials, run_trials
from shopping_agent import shopping_agent


def test_perfect_reliability():
    evaluations = [
        {"passed": True, "score": 100.0},
        {"passed": True, "score": 100.0},
        {"passed": True, "score": 100.0},
    ]

    summary = summarize_trials(evaluations)

    assert summary["total_runs"] == 3
    assert summary["passed_runs"] == 3
    assert summary["failed_runs"] == 0
    assert summary["pass_rate"] == 100.0
    assert summary["average_score"] == 100.0
    assert summary["flaky"] is False


def test_flaky_behavior():
    evaluations = [
        {"passed": True, "score": 100.0},
        {"passed": False, "score": 40.0},
        {"passed": True, "score": 100.0},
        {"passed": False, "score": 40.0},
        {"passed": True, "score": 100.0},
    ]

    summary = summarize_trials(evaluations)

    assert summary["total_runs"] == 5
    assert summary["passed_runs"] == 3
    assert summary["failed_runs"] == 2
    assert summary["pass_rate"] == 60.0
    assert summary["average_score"] == 76.0
    assert summary["flaky"] is True


def test_empty_trials():
    summary = summarize_trials([])

    assert summary["total_runs"] == 0
    assert summary["pass_rate"] == 0.0
    assert summary["flaky"] is False


def test_run_trials_and_save(tmp_path):
    scenario = {
        "expected_tools": ["get_order"],
        "required_tool_order": ["get_order"],
        "forbidden_tools": [],
        "max_tool_calls": 3,
        "expected_text": ["ORD-101", "shipped"],
    }

    db_path = str(tmp_path / "test_agentcheck.db")

    result = run_trials(
        agent_function=shopping_agent,
        question="Where is my order ORD-101?",
        scenario=scenario,
        trials=3,
        scenario_name="order_status",
        db_path=db_path,
    )

    assert result["summary"]["total_runs"] == 3
    assert result["summary"]["passed_runs"] == 3
    assert result["summary"]["pass_rate"] == 100.0
    assert result["summary"]["flaky"] is False
