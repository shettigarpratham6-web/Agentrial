
from judge import judge_answer


def main():
    result = judge_answer(
        question="Where is my order ORD-101?",
        expected_facts=[
            "The order ID is ORD-101.",
            "The order status is Shipped.",
        ],
        agent_answer="Good news! Your parcel ORD-101 is on its way.",
    )

    print("Judge Evaluation:")
    print(result)


if __name__ == "__main__":
    main()
