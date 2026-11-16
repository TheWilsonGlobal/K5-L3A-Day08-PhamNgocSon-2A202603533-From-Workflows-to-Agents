"""Bonus B3 — swarm + deterministic verifier (error-amplification guard).

Same peer chatter and same REFERENCE_WEAKNESS as the swarm (seed % 5 == 0 trusts
the ticket delay). Before the host write, a code verifier compares every fact used
for the quote (delay_days) with the structured order row. On mismatch it
re-quotes from the order row (max 1 repair) and traces `verifier_override`.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.handoff import make_handoff
from lab8.mock_llm import complete, parse_delay_days
from lab8.runtime import run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes._commit import commit_quote
from lab8.shapes.common import finish, safe_dump
from lab8.tools import compute_compensation, tool_cost
from lab8.trace import Trace

SHAPE = "swarm_verified"


def run_claim(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def verify_quote(conn: sqlite3.Connection, order_row: dict, proposed_order: dict, quote: dict, budget: Budget):
    """Return (quote, overridden). Re-quote from structured row if facts disagree."""
    facts = ("delay_days", "status", "damage_verified")
    if all(proposed_order.get(k) == order_row.get(k) for k in facts):
        return quote, False
    budget.add_tool(tool_cost())
    return compute_compensation(conn, order_row), True


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))
    budget.add_tool(tool_cost())
    row = conn.execute(
        "SELECT claim_id, principal_id, order_id, ticket FROM claims WHERE claim_id = ?", (claim_id,)
    ).fetchone()
    if row is None:
        trace.add("error", {"reason": "unknown_claim"})
        return finish(conn, shape=SHAPE, claim_id=claim_id, seed=seed, status="failed",
                      proposal_amount=0, budget=budget, trace=trace, error_reason="unknown_claim")

    ticket = row["ticket"]
    complete(budget, seed=seed, purpose="peer", prompt=ticket)
    parsed = parse_delay_days(ticket)
    complete(budget, seed=seed, purpose="parse", prompt=ticket)

    if not row["order_id"]:
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        trace.add("decision", {"status": "needs_info"})
        return finish(conn, shape=SHAPE, claim_id=claim_id, seed=seed, status="needs_info",
                      proposal_amount=0, budget=budget, trace=trace, error_reason="missing_order_id")

    handoff = make_handoff(request_id=f"REQ-{claim_id}", claim_id=claim_id,
                           task="check_applicable_policy", facts={},
                           allowed_tools=["lookup_order", "lookup_policy", "compute_compensation"])
    trace.add("handoff", safe_dump(handoff))
    inv = run_readonly_investigators(conn, budget, handoff, principal_id=row["principal_id"])
    view = inv["tools"].get("lookup_order", {})
    if not view.get("visible"):
        complete(budget, seed=seed, purpose="draft", prompt="escalated")
        return finish(conn, shape=SHAPE, claim_id=claim_id, seed=seed, status="escalated",
                      proposal_amount=0, budget=budget, trace=trace, error_reason=view.get("reason"))

    order_row = dict(view["order"])
    proposed = dict(order_row)
    quote = inv["tools"]["compute_compensation"]
    if parsed is not None and parsed != int(order_row["delay_days"]) and seed % 5 == 0:
        proposed["delay_days"] = parsed  # reference weakness
        budget.add_tool(tool_cost())
        quote = compute_compensation(conn, proposed)

    quote, overridden = verify_quote(conn, order_row, proposed, quote, budget)
    if overridden:
        trace.add("verifier_override", {"from_delay": proposed["delay_days"], "to_delay": order_row["delay_days"]})
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={quote.get('amount_vnd')}")
    return commit_quote(conn, shape=SHAPE, claim_id=claim_id, seed=seed, quote_payload=quote,
                        budget=budget, trace=trace, crash_at=crash_at)
