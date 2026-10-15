
from agentcheck import evaluate_agent
from storage import save_evaluation


def summarize_trials(evaluations):
    """Calculate reliability statistics from evaluation results."""

    total = len(evaluations)

    if total == 0:
        return {
            "total_runs": 0,
            "passed_runs": 0,
            "failed_runs": 0,
            "pass_rate": 0.0,
            "average_score": 0.0,
            "flaky": False,
        }

    passed = sum(
        1 for result in evaluations
        if result["passed"]
    )

    failed = total - passed

    average_score = sum(
        result["score"] for result in evaluations
    ) / total

    pass_rate = (passed / total) * 100

    return {
        "total_runs": total,
        "passed_runs": passed,
        "failed_runs": failed,
        "pass_rate": pass_rate,
        "average_score": average_score,
        "flaky": passed > 0 and failed > 0,
    }


def run_trials(
    agent_function,
    question,
    scenario,
    trials=5,
    scenario_name="manual_test",
    db_path="agentcheck.db",
    use_llm_judge=False,
):
    """
    Run an agent repeatedly, evaluate its behavior,
    optionally use an LLM judge, and save each result.
    """

    if trials < 1:
        raise ValueError("trials must be at least 1")

    evaluations = []

    for trial_number in range(1, trials + 1):

        # Execute the agent.
        result = agent_function(question)

        # Evaluate tool usage and answer correctness.
        # Optionally enable the LLM judge.
        evaluation = evaluate_agent(
            result,
            scenario,
            use_llm_judge=use_llm_judge,
        )

        # Save this individual trial to SQLite.
        save_evaluation(
            scenario_name=scenario_name,
            evaluation=evaluation,
            trace=result["trace"],
            db_path=db_path,
        )

        evaluations.append(evaluation)

        status = "PASS" if evaluation["passed"] else "FAIL"

        print(
            f"Trial {trial_number}/{trials}: "
            f"{status} | Score: {evaluation['score']:.1f}/100"
        )

        # Display LLM judge details when enabled.
        if use_llm_judge and evaluation.get("judge"):
            judgment = evaluation["judge"]

            print(
                f"  Judge score: {judgment['score']}/100"
            )
            print(
                f"  Judge reason: {judgment['reason']}"
            )

    # Summarize all trials.
    summary = summarize_trials(evaluations)

    print("\n--- Reliability Summary ---")
    print(f"Total runs:    {summary['total_runs']}")
    print(f"Passed:        {summary['passed_runs']}")
    print(f"Failed:        {summary['failed_runs']}")
    print(f"Pass rate:     {summary['pass_rate']:.1f}%")
    print(f"Average score: {summary['average_score']:.1f}/100")
    print(f"Flaky:         {summary['flaky']}")

    return {
        "evaluations": evaluations,
        "summary": summary,
    }
