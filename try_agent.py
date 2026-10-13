
from shopping_agent import shopping_agent
from agentcheck import evaluate_agent
from storage import save_evaluation


def main():
    question = "Where is my order ORD-101?"

    scenario = {
        "expected_tools": ["get_order"],
        "required_tool_order": ["get_order"],
        "forbidden_tools": [],
        "max_tool_calls": 3,
        "expected_text": ["ORD-101", "shipped"],
    }

    # Step 1: Run the shopping agent.
    result = shopping_agent(question)

    # Step 2: Evaluate the agent's behavior.
    evaluation = evaluate_agent(result, scenario)

    # Step 3: Print the evaluation.
    print("Question:", question)
    print("Answer:", result["answer"])
    print("Evaluation:", evaluation)

    # Step 4: Save the evaluation in SQLite.
    run_id = save_evaluation(
        scenario_name="order_status",
        evaluation=evaluation,
        trace=result["trace"],
    )

    print("Saved evaluation ID:", run_id)
    print("Database: agentcheck.db")


if __name__ == "__main__":
    main()
