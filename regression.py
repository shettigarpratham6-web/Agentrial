
import json
from datetime import datetime, timezone
from pathlib import Path


BASELINE_PATH = Path("baselines/order_status.json")


def save_baseline(
    summary,
    path=BASELINE_PATH,
):
    """Save a trusted evaluation summary as a baseline."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    baseline = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)

    print(f"Baseline saved to: {path}")


def load_baseline(path=BASELINE_PATH):
    """Load a previously saved baseline."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline not found: {path}. "
            "Run with --save-baseline first."
        )

    with path.open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    if not isinstance(baseline.get("summary"), dict):
        raise ValueError("Baseline file has an invalid format.")

    return baseline


def compare_with_baseline(
    current_summary,
    baseline,
    allowed_pass_rate_drop=0.0,
    allowed_average_score_drop=5.0,
):
    """Compare current metrics against the saved baseline."""

    previous = baseline["summary"]

    pass_rate_drop = (
        previous["pass_rate"] - current_summary["pass_rate"]
    )

    score_drop = (
        previous["average_score"] - current_summary["average_score"]
    )

    checks = {
        "pass_rate_stable": (
            pass_rate_drop <= allowed_pass_rate_drop
        ),
        "average_score_stable": (
            score_drop <= allowed_average_score_drop
        ),
    }

    return {
        "passed": all(checks.values()),
        "baseline_pass_rate": previous["pass_rate"],
        "current_pass_rate": current_summary["pass_rate"],
        "pass_rate_drop": pass_rate_drop,
        "baseline_average_score": previous["average_score"],
        "current_average_score": current_summary["average_score"],
        "average_score_drop": score_drop,
        "checks": checks,
    }
