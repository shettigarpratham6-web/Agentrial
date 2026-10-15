
import sqlite3
import json
from datetime import datetime, timezone


def init_db(db_path="agentcheck.db"):
    """Create the evaluation history table if it does not exist."""

    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_name TEXT NOT NULL,
                passed INTEGER NOT NULL,
                score REAL NOT NULL,
                checks_json TEXT NOT NULL,
                trace_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_evaluation(
    scenario_name,
    evaluation,
    trace,
    db_path="agentcheck.db",
):
    """Save an evaluation, including LLM judge details, to SQLite."""

    init_db(db_path)

    checks_json = json.dumps({
        "checks": evaluation["checks"],
        "judge": evaluation.get("judge"),
    })

    trace_json = json.dumps(trace)

    created_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute("""
            INSERT INTO evaluation_runs (
                scenario_name,
                passed,
                score,
                checks_json,
                trace_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            scenario_name,
            int(evaluation["passed"]),
            float(evaluation["score"]),
            checks_json,
            trace_json,
            created_at,
        ))

        return cursor.lastrowid


def get_all_results(db_path="agentcheck.db"):
    """Retrieve saved evaluations, including judge details."""

    init_db(db_path)

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT *
            FROM evaluation_runs
            ORDER BY id DESC
        """).fetchall()

    results = []

    for row in rows:
        stored_data = json.loads(row["checks_json"])

        # Support records saved by the older storage implementation.
        if "checks" in stored_data:
            checks = stored_data["checks"]
            judge = stored_data.get("judge")
        else:
            checks = stored_data
            judge = None

        results.append({
            "id": row["id"],
            "scenario_name": row["scenario_name"],
            "passed": bool(row["passed"]),
            "score": row["score"],
            "checks": checks,
            "judge": judge,
            "trace": json.loads(row["trace_json"]),
            "created_at": row["created_at"],
        })

    return results
