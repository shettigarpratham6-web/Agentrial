
import argparse
import sys

from shopping_agent import shopping_agent
from reliability import run_trials
from quality_gate import evaluate_quality_gate
from regression import (
    save_baseline,
    load_baseline,
    compare_with_baseline,
)


def main():
    parser = argparse.ArgumentParser(
        description="Run AgentCheck reliability and regression tests."
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--save-baseline",
        action="store_true",
        help="Save results as the trusted baseline.",
    )

    mode.add_argument(
        "--compare-baseline",
        action="store_true",
        help="Compare results against the saved baseline.",
    )

    args = parser.parse_args()

    question = "Where is my order ORD-101?"

    scenario = {
        "question": question,
        "expected_tools": ["get_order"],
        "required_tool_order": ["get_order"],
        "forbidden_tools": [],
        "max_tool_calls": 3,
        "expected_text": ["ORD-101", "shipped"],
    }

    print("=" * 50)
    print("       AGENTCHECK - RELIABILITY TEST")
    print("=" * 50)
    print(f"\nQuestion: {question}")

    results = run_trials(
        agent_function=shopping_agent,
        question=question,
        scenario=scenario,
        trials=5,
        scenario_name="order_status",
        db_path="agentcheck.db",
        use_llm_judge=True,
    )

    summary = results["summary"]

    print("\n--- Evaluation Summary ---")
    print(f"Pass rate:     {summary['pass_rate']:.1f}%")
    print(f"Average score: {summary['average_score']:.1f}/100")
    print(f"Flaky agent:   {summary['flaky']}")

    # Run the existing quality gate first.
    gate = evaluate_quality_gate(
        summary,
        minimum_pass_rate=90.0,
        minimum_average_score=85.0,
    )

    print("\n--- Quality Gate ---")

    for name, passed in gate["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")

    if not gate["passed"]:
        print("\nQUALITY GATE: FAIL")
        print("Fix the quality issues before proceeding.")
        sys.exit(1)

    print("\nQUALITY GATE: PASS")

    # Save a baseline only when the quality gate passes.
    if args.save_baseline:
        save_baseline(summary)
        print("BASELINE: SAVED")
        return

    # Compare the current evaluation with the saved baseline.
    if args.compare_baseline:
        try:
            baseline = load_baseline()
        except (FileNotFoundError, ValueError) as error:
            print(f"\nBASELINE ERROR: {error}")
            sys.exit(1)

        comparison = compare_with_baseline(
            current_summary=summary,
            baseline=baseline,
            allowed_pass_rate_drop=0.0,
            allowed_average_score_drop=5.0,
        )

        print("\n" + "=" * 50)
        print("          REGRESSION COMPARISON")
        print("=" * 50)

        print(
            f"Baseline pass rate: "
            f"{comparison['baseline_pass_rate']:.1f}%"
        )
        print(
            f"Current pass rate:  "
            f"{comparison['current_pass_rate']:.1f}%"
        )
        print(
            f"Pass-rate drop:     "
            f"{comparison['pass_rate_drop']:.1f} percentage points"
        )

        print(
            f"\nBaseline score:     "
            f"{comparison['baseline_average_score']:.1f}/100"
        )
        print(
            f"Current score:      "
            f"{comparison['current_average_score']:.1f}/100"
        )
        print(
            f"Score drop:         "
            f"{comparison['average_score_drop']:.1f} points"
        )

        for name, passed in comparison["checks"].items():
            status = "PASS" if passed else "FAIL"
            print(f"{name}: {status}")

        if not comparison["passed"]:
            print("\nREGRESSION DETECTED!")
            print("The new evaluation is worse than the baseline.")
            sys.exit(1)

        print("\nREGRESSION CHECK: PASS")
        print("No regression was detected by these thresholds.")


if __name__ == "__main__":
    main()
