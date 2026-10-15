
import sys

from shopping_agent import shopping_agent
from reliability import run_trials
from quality_gate import evaluate_quality_gate


def main():
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

    # Run repeated trials and save results to SQLite.
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

    print("\n" + "=" * 50)
    print("             FINAL RESULTS")
    print("=" * 50)

    print(f"Total Trials  : {summary['total_runs']}")
    print(f"Passed Trials : {summary['passed_runs']}")
    print(f"Failed Trials : {summary['failed_runs']}")
    print(f"Pass Rate     : {summary['pass_rate']:.1f}%")
    print(f"Average Score : {summary['average_score']:.1f}/100")
    print(f"Flaky Agent   : {summary['flaky']}")

    # Configure and evaluate quality thresholds.
    gate = evaluate_quality_gate(
        summary,
        minimum_pass_rate=90.0,
        minimum_average_score=85.0,
    )

    print("\n" + "=" * 50)
    print("             QUALITY GATE")
    print("=" * 50)

    for name, passed in gate["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")

    print(
        f"\nRequired Pass Rate: "
        f"{gate['thresholds']['minimum_pass_rate']:.1f}%"
    )
    print(
        f"Required Average Score: "
        f"{gate['thresholds']['minimum_average_score']:.1f}/100"
    )

    if gate["passed"]:
        print("\nQUALITY GATE: PASS")
        print("The agent meets all quality requirements.")
    else:
        print("\nQUALITY GATE: FAIL")
        print("The agent does not meet all quality requirements.")

    print("\nEvaluation history saved to agentcheck.db")

    # Return a nonzero exit code if the quality gate fails.
    if not gate["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
