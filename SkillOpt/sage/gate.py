"""Full SAGE acceptance gate."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from sage.denoise import denoise_decision
from sage.evidence import PairedLedger, build_paired_ledger


class GateAction(str, Enum):
    COMMIT = "commit"
    ABSTAIN = "abstain"


@dataclass(frozen=True)
class SageGateResult:
    action: GateAction
    ledger: PairedLedger
    p_value: float
    discounted_gain: float
    regression_rate: float
    alpha: float
    lam: float
    tau: float


def sage_accept(
    candidate_items: Mapping[str, float],
    incumbent_items: Mapping[str, float],
    *,
    lam: float = 1.0,
    tau: float = 1.0,
    alpha: float = 0.05,
) -> SageGateResult:
    """Return SAGE commit/abstain decision for candidate vs incumbent.

    With lam=1, tau=1, alpha=1, this recovers the strict aggregate SkillOpt gate
    on paired binary outcomes because wins > losses iff the candidate has a
    higher mean score on the shared validation set.
    """
    ledger = build_paired_ledger(candidate_items, incumbent_items)
    discounted_gain = ledger.discounted_gain(lam=lam)
    regression_rate = ledger.regression_rate
    denoised = denoise_decision(wins=ledger.wins, losses=ledger.losses, alpha=alpha)
    cap_ok = regression_rate <= float(tau)
    gain_ok = discounted_gain > 0
    action = GateAction.COMMIT if denoised.accept and cap_ok and gain_ok else GateAction.ABSTAIN
    return SageGateResult(
        action=action,
        ledger=ledger,
        p_value=denoised.p_value,
        discounted_gain=discounted_gain,
        regression_rate=regression_rate,
        alpha=float(alpha),
        lam=float(lam),
        tau=float(tau),
    )
