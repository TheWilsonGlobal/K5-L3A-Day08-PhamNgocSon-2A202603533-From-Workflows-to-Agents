"""Bonus B3 tests: verifier overrides the swarm weakness and keeps ledger clean."""

from lab8.db import connect, init_store
from lab8.metrics import trial_pass
from lab8.schemas import Budget
from bonus.swarm_verified import run_claim as verified_run, verify_quote
from tests.conftest import BY_ID, CLAIMS, WORLD


def test_verify_quote_keeps_matching_facts():
    row = {"delay_days": 4, "status": "delivered_late", "damage_verified": False}
    q = {"amount_vnd": 35000}
    out, overridden = verify_quote(None, row, dict(row), q, Budget())
    assert out is q and overridden is False


def test_verified_swarm_fixes_t02_on_seed_55(tmp_path):
    for seed in (11, 55):
        store = tmp_path / f"v-{seed}.sqlite"
        init_store(store, WORLD, CLAIMS).close()
        result = verified_run("C-002", seed=seed, store_path=str(store))
        conn = connect(store)
        try:
            passed, reason = trial_pass(result.as_dict(), BY_ID["C-002"]["expected"], conn)
        finally:
            conn.close()
        assert passed, f"seed {seed}: {reason}"
