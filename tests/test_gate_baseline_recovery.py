from sage.gate import GateAction, sage_accept


def test_sage_abstains_when_regression_cap_fails():
    current = {"a": 1, "b": 1, "c": 0, "d": 0}
    candidate = {"a": 0, "b": 1, "c": 1, "d": 1}

    result = sage_accept(candidate, current, lam=1.0, tau=0.25, alpha=1.0)

    assert result.action == GateAction.ABSTAIN
    assert result.ledger.wins == 2
    assert result.ledger.losses == 1


def test_sage_accepts_strong_paired_evidence():
    current = {str(i): 0 for i in range(8)}
    candidate = {str(i): 1 for i in range(8)}

    result = sage_accept(candidate, current, lam=1.0, tau=1.0, alpha=0.05)

    assert result.action == GateAction.COMMIT
    assert result.p_value == 1 / 256


def test_baseline_recovery_matches_strict_aggregate_gate():
    cases = [
        ({"a": 1, "b": 0}, {"a": 1, "b": 1}, True),
        ({"a": 1, "b": 0}, {"a": 0, "b": 1}, False),
        ({"a": 1, "b": 1}, {"a": 1, "b": 0}, False),
    ]
    for current, candidate, expected in cases:
        result = sage_accept(candidate, current, lam=1.0, tau=1.0, alpha=1.0)
        assert (result.action == GateAction.COMMIT) is expected
