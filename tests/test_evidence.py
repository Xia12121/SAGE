import pytest

from sage.evidence import PairedLedger, build_paired_ledger


def test_build_paired_ledger_counts_wins_losses_and_ties():
    current = {"a": 1, "b": 0, "c": 1, "d": 0, "e": 1}
    candidate = {"a": 1, "b": 1, "c": 0, "d": 0, "e": 1}

    ledger = build_paired_ledger(candidate, current)

    assert ledger.n == 5
    assert ledger.wins == 1
    assert ledger.losses == 1
    assert ledger.ties == 3
    assert ledger.incumbent_correct == 3
    assert ledger.common_ids == ("a", "b", "c", "d", "e")


def test_discounted_gain_and_regression_rate_are_asymmetric():
    ledger = PairedLedger(
        n=10,
        wins=4,
        losses=2,
        ties=4,
        incumbent_correct=5,
        common_ids=tuple(str(i) for i in range(10)),
    )

    assert ledger.discounted_gain(lam=1.0) == 2
    assert ledger.discounted_gain(lam=2.0) == 0
    assert ledger.regression_rate == pytest.approx(0.4)


def test_empty_intersection_is_allowed_and_rejectable():
    ledger = build_paired_ledger({"a": 1}, {"b": 1})

    assert ledger.n == 0
    assert ledger.wins == 0
    assert ledger.losses == 0
    assert ledger.ties == 0
    assert ledger.regression_rate == 0.0
