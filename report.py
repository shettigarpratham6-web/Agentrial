
import html
from pathlib import Path
from storage import get_all_results


def generate_html_report(
    output_path="agentcheck_report.html",
    db_path="agentcheck.db",
):
    """Generate a light financial-dashboard-style evaluation report."""

    results = get_all_results(db_path)

    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    failed = total - passed

    pass_rate = (passed / total * 100) if total else 0

    average_score = (
        sum(result["score"] for result in results) / total
        if total else 0
    )

    rows = []

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        status_class = "pass" if result["passed"] else "fail"

        checks_html = "".join(
            f'<li class="{"pass" if passed_check else "fail"}">'
            f'{html.escape(str(name))}: '
            f'{"PASS" if passed_check else "FAIL"}</li>'
            for name, passed_check in result["checks"].items()
        )

        judge = result.get("judge")

        if judge:
            judge_html = f"""
                <div class="judge-panel">
                    <p><strong>Judge decision:</strong>
                    {html.escape(str(judge["correct"]))}</p>
                    <p><strong>Judge score:</strong>
                    {html.escape(str(judge["score"]))}/100</p>
                    <p><strong>Reason:</strong>
                    {html.escape(str(judge["reason"]))}</p>
                </div>
            """
        else:
            judge_html = (
                '<p class="muted">No LLM judge result recorded.</p>'
            )

        rows.append(f"""
            <tr>
                <td>{result["id"]}</td>
                <td>{html.escape(str(result["scenario_name"]))}</td>
                <td>
                    <span class="status {status_class}">{status}</span>
                </td>
                <td class="score">{result["score"]:.1f}/100</td>
                <td>
                    <details>
                        <summary>View details</summary>
                        <ul class="checks">{checks_html}</ul>
                        {judge_html}
                    </details>
                </td>
                <td class="timestamp">
                    {html.escape(str(result["created_at"]))}
                </td>
            </tr>
        """)

    table_rows = "\n".join(rows)

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AgentCheck | Evaluation Dashboard</title>

<style>
:root {{
    --page: #f3f4f6;
    --white: #ffffff;
    --header: #f8f9fa;
    --text: #111827;
    --muted: #64748b;
    --border: #e1e5eb;
    --green: #00a63e;
    --green-bg: #effcf3;
    --red: #dc2626;
    --red-bg: #fef1f1;
    --blue-bg: #eff6ff;
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: var(--page);
    color: var(--text);
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.6;
}}

.topbar {{
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
}}

.brand {{
    font-size: 21px;
    font-weight: 700;
    letter-spacing: -0.4px;
}}

.brand span {{
    color: var(--green);
}}

.topbar-label {{
    color: var(--muted);
    font-size: 14px;
}}

.container {{
    max-width: 1600px;
    margin: 0 auto;
    padding: 28px 32px 40px;
}}

.page-heading {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 28px;
}}

h1 {{
    margin: 0;
    font-size: 28px;
    letter-spacing: -0.6px;
}}

.subtitle {{
    color: var(--muted);
    margin: 4px 0 0;
}}

.generated {{
    color: var(--muted);
    font-size: 13px;
    text-align: right;
}}

.section {{
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}}

.section-heading {{
    padding: 20px 24px;
    background: var(--header);
    border-bottom: 1px solid var(--border);
    font-size: 18px;
    font-weight: 700;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 28px;
}}

.card {{
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    min-width: 0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}}

.card-label {{
    color: var(--muted);
    font-size: 14px;
    font-weight: 500;
}}

.value {{
    font-size: 29px;
    font-weight: 700;
    letter-spacing: -0.7px;
    margin-top: 8px;
    overflow-wrap: anywhere;
}}

.value.pass,
.pass {{
    color: var(--green);
}}

.value.fail,
.fail {{
    color: var(--red);
}}

.value.neutral {{
    color: var(--text);
}}

.card-note {{
    color: var(--muted);
    font-size: 12px;
    margin-top: 5px;
}}

.table-wrapper {{
    width: 100%;
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--white);
}}

th,
td {{
    padding: 17px 24px;
    text-align: left;
    border-bottom: 1px solid #edf0f3;
    vertical-align: middle;
}}

th {{
    color: var(--muted);
    font-size: 13px;
    font-weight: 700;
    background: var(--white);
    white-space: nowrap;
}}

tbody tr:last-child td {{
    border-bottom: none;
}}

tbody tr:hover {{
    background: #fafbfc;
}}

tbody tr:nth-child(even) {{
    background: #ffffff;
}}

.status {{
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 5px 10px;
    border-radius: 6px;
}}

.status.pass {{
    background: var(--green-bg);
    color: var(--green);
}}

.status.fail {{
    background: var(--red-bg);
    color: var(--red);
}}

.score {{
    font-weight: 700;
    white-space: nowrap;
}}

.timestamp {{
    color: var(--muted);
    font-size: 12px;
    min-width: 180px;
}}

details {{
    min-width: 150px;
}}

summary {{
    cursor: pointer;
    color: #334155;
    font-size: 13px;
    font-weight: 600;
}}

summary:hover {{
    color: var(--green);
}}

.checks {{
    padding-left: 20px;
}}

.checks li {{
    margin: 7px 0;
    overflow-wrap: anywhere;
}}

.judge-panel {{
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    margin-top: 14px;
    overflow-wrap: anywhere;
}}

.judge-panel p {{
    margin: 7px 0;
    font-size: 13px;
}}

.muted {{
    color: var(--muted);
}}

.footer {{
    display: flex;
    justify-content: space-between;
    gap: 12px;
    color: var(--muted);
    font-size: 12px;
    padding: 12px 2px;
}}

@media (max-width: 1050px) {{
    .cards {{
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }}
}}

@media (max-width: 650px) {{
    .topbar {{
        padding: 16px;
    }}

    .container {{
        padding: 20px 14px;
    }}

    .page-heading {{
        align-items: flex-start;
        flex-direction: column;
    }}

    .generated {{
        text-align: left;
    }}

    h1 {{
        font-size: 24px;
    }}

    .cards {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }}

    .card {{
        padding: 15px;
    }}

    .value {{
        font-size: 24px;
    }}

    th,
    td {{
        padding: 13px 15px;
    }}

    .footer {{
        flex-direction: column;
    }}
}}
</style>
</head>

<body>

<div class="topbar">
    <div class="brand">Agent<span>Check</span></div>
    <div class="topbar-label">AI Agent Evaluation Dashboard</div>
</div>

<main class="container">

    <header class="page-heading">
        <div>
            <h1>Evaluation Overview</h1>
            <p class="subtitle">
                Reliability, quality checks and LLM judge results
            </p>
        </div>
        <div class="generated">
            Historical evaluations<br>
            {total} recorded runs
        </div>
    </header>

    <section class="cards">
        <div class="card">
            <div class="card-label">Total Evaluations</div>
            <div class="value neutral">{total}</div>
            <div class="card-note">Recorded runs</div>
        </div>

        <div class="card">
            <div class="card-label">Passed</div>
            <div class="value pass">{passed}</div>
            <div class="card-note">Successful evaluations</div>
        </div>

        <div class="card">
            <div class="card-label">Failed</div>
            <div class="value fail">{failed}</div>
            <div class="card-note">Evaluations requiring review</div>
        </div>

        <div class="card">
            <div class="card-label">Pass Rate</div>
            <div class="value neutral">{pass_rate:.1f}%</div>
            <div class="card-note">Across recorded runs</div>
        </div>

        <div class="card">
            <div class="card-label">Average Score</div>
            <div class="value neutral">{average_score:.1f}<span
                style="font-size:15px;color:#64748b">/100</span></div>
            <div class="card-note">Overall evaluation score</div>
        </div>
    </section>

    <section class="section">
        <div class="section-heading">Evaluation History</div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Scenario</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Details</th>
                        <th>Created At (UTC)</th>
                    </tr>
                </thead>

                <tbody>
                    {table_rows if table_rows else
                    '<tr><td colspan="6">No evaluations found.</td></tr>'}
                </tbody>
            </table>
        </div>
    </section>

    <footer class="footer">
        <span>AgentCheck · AI Agent Evaluation Framework</span>
        <span>Evaluation data from SQLite</span>
    </footer>

</main>

</body>
</html>
"""

    Path(output_path).write_text(document, encoding="utf-8")
    print(f"HTML report generated: {Path(output_path).resolve()}")


if __name__ == "__main__":
    generate_html_report()
