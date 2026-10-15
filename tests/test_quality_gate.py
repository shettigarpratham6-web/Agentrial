
from quality_gate import evaluate_quality_gate


def test_quality_gate_passes_when_thresholds_are_met():
    summary = {
        "pass_rate": 100.0,
        "average_score": 95.0,
    }

    result = evaluate_quality_gate(summary)

    assert result["passed"] is True
    assert all(result["checks"].values())


def test_quality_gate_fails_when_pass_rate_is_too_low():
    summary = {
        "pass_rate": 80.0,
        "average_score": 95.0,
    }

    result = evaluate_quality_gate(summary)

    assert result["passed"] is False
    assert result["checks"]["pass_rate_met"] is False


def test_quality_gate_fails_when_average_score_is_too_low():
    summary = {
        "pass_rate": 100.0,
        "average_score": 70.0,
    }

    result = evaluate_quality_gate(summary)

    assert result["passed"] is False
    assert result["checks"]["average_score_met"] is False


def test_quality_gate_fails_when_both_thresholds_are_missed():
    summary = {
        "pass_rate": 60.0,
        "average_score": 70.0,
    }

    result = evaluate_quality_gate(summary)

    assert result["passed"] is False
    assert not any(result["checks"].values())


def test_quality_gate_accepts_exact_thresholds():
    summary = {
        "pass_rate": 90.0,
        "average_score": 85.0,
    }

    result = evaluate_quality_gate(summary)

    assert result["passed"] is True
