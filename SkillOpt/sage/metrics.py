"""Exact statistical helpers for SAGE."""
from __future__ import annotations

from math import comb


def exact_sign_test_p_value(wins: int, losses: int) -> float:
    """One-sided exact sign-test p-value for candidate better than incumbent."""
    n_disc = int(wins) + int(losses)
    if n_disc <= 0:
        return 1.0
    tail = sum(comb(n_disc, k) for k in range(int(wins), n_disc + 1))
    return tail / (2**n_disc)
