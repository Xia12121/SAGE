import pytest

from sage.denoise import denoise_decision
from sage.metrics import exact_sign_test_p_value


def test_exact_sign_test_known_values():
    assert exact_sign_test_p_value(0, 0) == 1.0
    assert exact_sign_test_p_value(5, 0) == pytest.approx(1 / 32)
    assert exact_sign_test_p_value(4, 1) == pytest.approx(6 / 32)
    assert exact_sign_test_p_value(1, 1) == pytest.approx(3 / 4)


def test_denoise_accepts_only_significant_positive_evidence():
    assert denoise_decision(wins=8, losses=0, alpha=0.05).accept is True
    assert denoise_decision(wins=5, losses=3, alpha=0.05).accept is False
    assert denoise_decision(wins=0, losses=8, alpha=1.0).accept is False
