"""Hypothesis-test denoising for SAGE."""
from __future__ import annotations

from dataclasses import dataclass

from sage.metrics import exact_sign_test_p_value


@dataclass(frozen=True)
class DenoiseDecision:
    accept: bool
    p_value: float
    alpha: float


def denoise_decision(*, wins: int, losses: int, alpha: float) -> DenoiseDecision:
    """Accept only when wins beat losses and the exact sign test passes."""
    p_value = exact_sign_test_p_value(wins, losses)
    accept = wins > losses and p_value < float(alpha)
    return DenoiseDecision(accept=accept, p_value=p_value, alpha=float(alpha))
