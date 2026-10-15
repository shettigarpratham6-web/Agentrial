
def evaluate_quality_gate(
    summary,
    minimum_pass_rate=90.0,
    minimum_average_score=85.0,
):
    """Check whether an agent meets the required quality thresholds."""

    checks = {
        "pass_rate_met": (
            summary["pass_rate"] >= minimum_pass_rate
        ),
        "average_score_met": (
            summary["average_score"] >= minimum_average_score
        ),
    }

    return {
        "passed": all(checks.values()),
        "checks": checks,
        "thresholds": {
            "minimum_pass_rate": minimum_pass_rate,
            "minimum_average_score": minimum_average_score,
        },
    }
