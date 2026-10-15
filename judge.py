
import json
import urllib.request
import urllib.error


def judge_answer(
    question,
    expected_facts,
    agent_answer,
    model="llama3.2:latest",
):
    """
    Evaluate an agent's answer using an LLM judge.
    """

  
    prompt = f"""
You are an impartial evaluator for an AI agent testing framework.

Evaluate the agent's answer against the expected facts.

Question:
{question}

Expected facts:
{json.dumps(expected_facts)}

Agent answer:
{agent_answer}

Evaluation rules:
1. Evaluate the meaning, not exact wording.
2. Accept reasonable paraphrases and equivalent expressions.
3. For an order status, "on its way" or "in transit" can indicate
   "Shipped" when the context supports that interpretation.
4. Do not require every expected fact to appear word-for-word.
5. Penalize missing, incorrect, contradictory, or unsupported claims.
6. If all important facts are communicated correctly, use a high score.
7. Set correct to true when the answer is sufficiently correct
   and complete; otherwise set it to false.
8. Do not invent facts that are absent from the answer.

Return ONLY valid JSON in this format:
{{
    "correct": true,
    "score": 90,
    "reason": "The answer communicates the expected facts."
}}

The score must be an integer from 0 to 100.
The correct field must be a boolean.
The reason must be a string.
"""


    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        evaluation = json.loads(result["response"])

        # Validate the model's response before trusting it.
        if not isinstance(evaluation.get("correct"), bool):
            raise ValueError("The judge must return a boolean 'correct' field.")

        score = evaluation.get("score")
        if type(score) is not int or not 0 <= score <= 100:
            raise ValueError("The judge score must be an integer from 0 to 100.")

        if not isinstance(evaluation.get("reason"), str):
            raise ValueError("The judge must return a text 'reason' field.")

        return evaluation

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Could not connect to Ollama. Check that Ollama is running "
            "and the selected model is installed."
        ) from error
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise RuntimeError(
            "Ollama returned an invalid evaluation response."
        ) from error
