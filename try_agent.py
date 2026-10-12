
from shopping_agent import shopping_agent


def main():
    question = "Where is my order ORD-101?"

    result = shopping_agent(question)

    print("Customer question:", question)
    print("Agent answer:", result["answer"])
    print("Execution trace:", result["trace"])


if __name__ == "__main__":
    main()
