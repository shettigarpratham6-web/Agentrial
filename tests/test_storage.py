
from storage import save_evaluation, get_all_results


def test_save_and_read_evaluation(tmp_path):
    # pytest provides a temporary directory for this test.
    db_path = tmp_path / "test_agentcheck.db"

    evaluation = {
        "passed": True,
        "score": 100.0,
        "checks": {
            "required_tools_present": True,
            "answer_contains_expected_text": True,
        },
    }

    trace = {
        "tool_calls": [
            {
                "name": "get_order",
                "arguments": {"order_id": "ORD-101"},
            }
        ]
    }

    # Save the evaluation.
    run_id = save_evaluation(
        scenario_name="order_status",
        evaluation=evaluation,
        trace=trace,
        db_path=str(db_path),
    )

    # Confirm that SQLite assigned an ID.
    assert run_id == 1

    # Read the evaluation back.
    results = get_all_results(db_path=str(db_path))

    assert len(results) == 1
    assert results[0]["scenario_name"] == "order_status"
    assert results[0]["passed"] is True
    assert results[0]["score"] == 100.0
    assert results[0]["checks"] == evaluation["checks"]
    assert results[0]["trace"] == trace
