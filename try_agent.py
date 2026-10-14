
from shopping_agent import shopping_agent
from reliability import run_trials


def main():
    # Define the customer's question.
    question = "Where is my order ORD-101?"

    # Define the expected agent behavior.
    scenario = {
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

    # Run the agent multiple times.
    # run_trials handles evaluation and SQLite storage.
    results = run_trials(
        agent_function=shopping_agent,
        question=question,
        scenario=scenario,
        trials=5,
        scenario_name="order_status",
        db_path="agentcheck.db",
    )

    # Display the overall reliability results.
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

    print("\nAll trial results saved to agentcheck.db")

    # Determine whether the agent meets our reliability target.
    minimum_pass_rate = 90.0

    if summary["pass_rate"] >= minimum_pass_rate:
        print("\nSTATUS: PASS - Reliability target met.")
    else:
        print("\nSTATUS: FAIL - Reliability target not met.")


if __name__ == "__main__":
    main()

