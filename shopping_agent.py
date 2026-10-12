
import re


ORDERS = {
    "ORD-101": "Shipped",
    "ORD-102": "Delivered",
    "ORD-103": "Processing",
}


def get_order(order_id):
    """Look up an order in our database."""
    return ORDERS.get(order_id)


def shopping_agent(question):
    """Answer a customer's question about an order."""


    trace = {"tool_calls": []}


    match = re.search(r"ORD-\d+", question.upper())

    if not match:
        return {
            "answer": "Please provide a valid order ID.",
            "trace": trace,
        }

    order_id = match.group()

   
    trace["tool_calls"].append({
        "name": "get_order",
        "arguments": {"order_id": order_id},
    })

    
    status = get_order(order_id)

   
    if status is None:
        answer = f"Order {order_id} was not found."
    else:
        answer = f"Order {order_id} is {status}."

   
    return {
        "answer": answer,
        "trace": trace,
    }
