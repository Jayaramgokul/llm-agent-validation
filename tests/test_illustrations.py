"""Checks that the shared statistics are right and that every illustration runs.

    python -m pytest tests/ -q
"""

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ILLUSTRATIONS = Path(__file__).resolve().parents[1] / "05-illustrations"
sys.path.insert(0, str(ILLUSTRATIONS))

import common  # noqa: E402


def test_upper_bound_matches_rule_of_three():
    assert common.upper_bound(0, 60) == pytest.approx(1 - 0.05 ** (1 / 60))
    assert 0.045 < common.upper_bound(0, 60) < 0.05


def test_prompts_needed():
    assert common.prompts_needed(0.05) == 59
    assert common.prompts_needed(0.01) == 299


def test_wilson_contains_rate():
    lo, hi = common.wilson(12, 100)
    assert lo < 0.12 < hi


def test_cluster_interval_is_wider_when_failures_cluster():
    clustered = [np.array([1, 1, 1])] * 5 + [np.array([0, 0, 0])] * 95
    spread = [np.array([1, 0, 0])] * 15 + [np.array([0, 0, 0])] * 85
    _, lo_c, hi_c = common.cluster_interval(clustered)
    _, lo_s, hi_s = common.cluster_interval(spread)
    assert hi_c - lo_c > hi_s - lo_s


def test_cohen_kappa():
    assert common.cohen_kappa([0, 1, 0, 1], [0, 1, 0, 1]) == 1.0
    assert abs(common.cohen_kappa([0, 1] * 50, [0, 0, 1, 1] * 25)) < 1e-9


def test_bh_matches_hand_calculation():
    assert np.allclose(common.bh([0.01, 0.04, 0.03, 0.20]), [0.04, 0.16 / 3, 0.16 / 3, 0.20])


def test_expected_calibration_error_zero_when_calibrated():
    stated = np.repeat([0.2, 0.8], 10)
    outcome = np.array([1, 1] + [0] * 8 + [1] * 8 + [0, 0])
    assert common.expected_calibration_error(stated, outcome) == pytest.approx(0.0)


@pytest.mark.parametrize("script", sorted(p.name for p in ILLUSTRATIONS.glob("[a-z][0-9]_*.py")))
def test_illustration_runs(script):
    result = subprocess.run([sys.executable, script], cwd=ILLUSTRATIONS, capture_output=True, text=True,
                            timeout=600, env={**os.environ, "MPLBACKEND": "Agg"})
    assert result.returncode == 0, result.stderr
    assert "What this shows" in result.stdout
