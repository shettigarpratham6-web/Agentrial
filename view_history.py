
from storage import get_all_results


def main():
    results = get_all_results()

    if not results:
        print("No evaluation results found.")
        return

    print("\nAGENTCHECK - EVALUATION HISTORY")
    print("-" * 65)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(f"Run ID:    {result['id']}")
        print(f"Scenario:  {result['scenario_name']}")
        print(f"Status:    {status}")
        print(f"Score:     {result['score']:.1f}/100")
        print(f"Time:      {result['created_at']}")
        print("Checks:")

        for name, passed in result["checks"].items():
            mark = "PASS" if passed else "FAIL"
            print(f"  {name}: {mark}")

        print("-" * 65)


if __name__ == "__main__":
    main()
