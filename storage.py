
import json
import sqlite3

from datetime import datetime, timezone


def init_db(db_path="agentcheck.db"):
    """Create the database and evaluation table if needed."""

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
    """Save one evaluation result in SQLite."""

    init_db(db_path)

    created_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO evaluation_runs (
                scenario_name,
                passed,
                score,
                checks_json,
                trace_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                scenario_name,
                int(evaluation["passed"]),
                evaluation["score"],
                json.dumps(evaluation["checks"]),
                json.dumps(trace),
                created_at,
            ),
        )

        return cursor.lastrowid


def get_all_results(db_path="agentcheck.db"):
    """Retrieve saved evaluations, newest first."""

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
        item = dict(row)

        # Convert stored JSON text back into Python dictionaries.
        item["passed"] = bool(item["passed"])
        item["checks"] = json.loads(item.pop("checks_json"))
        item["trace"] = json.loads(item.pop("trace_json"))

        results.append(item)

    return results
