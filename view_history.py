
from storage import get_all_results


def main():
    results = get_all_results()

    if not results:
        print("No evaluation history found.")
        return

    print("=" * 60)
    print("             AGENTCHECK HISTORY")
    print("=" * 60)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(f"\nRun ID      : {result['id']}")
        print(f"Scenario    : {result['scenario_name']}")
        print(f"Status      : {status}")
        print(f"Overall Score: {result['score']:.1f}/100")
        print(f"Created At  : {result['created_at']}")

        print("\nChecks:")
        for name, passed in result["checks"].items():
            check_status = "PASS" if passed else "FAIL"
            print(f"  {name}: {check_status}")

        judgment = result.get("judge")

        if judgment:
            print("\nLLM Judge:")
            print(f"  Correct: {judgment['correct']}")
            print(f"  Score  : {judgment['score']}/100")
            print(f"  Reason : {judgment['reason']}")

        print("-" * 60)


if __name__ == "__main__":
    main()
