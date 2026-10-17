"""Shared helpers for the illustration scripts: small statistics and plotting.

No script here calls a language model. Each one simulates the *outcomes* of
an evaluation (pass or fail, a recommended allocation, a judge's verdict) so
that the statistical method can be seen working. The point is how to test
and how to read the result, not the behaviour of any real model.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for k events in n independent trials."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def upper_bound(k: int, n: int, level: float = 0.95) -> float:
    """Exact (Clopper-Pearson) one-sided upper bound on a failure rate."""
    if k >= n:
        return 1.0
    return float(stats.beta.ppf(level, k + 1, n - k))


def prompts_needed(max_rate: float, level: float = 0.95) -> int:
    """Failure-free trials needed to show the true rate is below max_rate."""
    return math.ceil(math.log(1 - level) / math.log(1 - max_rate))


def cluster_interval(values_by_cluster: list[np.ndarray], n: int = 4000, seed: int = 0,
                     level: float = 0.95) -> tuple[float, float, float]:
    """Mean over all observations, with an interval from resampling whole clusters.

    Repeated replies to one prompt (or one question) are not independent
    evidence, so the prompt is the unit that is resampled.
    """
    sums = np.array([v.sum() for v in values_by_cluster], float)
    sizes = np.array([len(v) for v in values_by_cluster], float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(sums), (n, len(sums)))
    boots = sums[idx].sum(1) / sizes[idx].sum(1)
    lo, hi = np.quantile(boots, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(sums.sum() / sizes.sum()), float(lo), float(hi)


def paired_interval(diff: np.ndarray, n: int = 4000, seed: int = 0, level: float = 0.95):
    """Mean of paired differences, with a bootstrap interval over pairs."""
    rng = np.random.default_rng(seed)
    boots = diff[rng.integers(0, len(diff), (n, len(diff)))].mean(1)
    lo, hi = np.quantile(boots, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(diff.mean()), float(lo), float(hi)


def cohen_kappa(a, b) -> float:
    """Agreement between two raters beyond chance (1 = perfect, 0 = chance)."""
    a, b = np.asarray(a), np.asarray(b)
    labels = np.union1d(a, b)
    po = np.mean(a == b)
    pe = sum(np.mean(a == lab) * np.mean(b == lab) for lab in labels)
    return 1.0 if pe == 1 else float((po - pe) / (1 - pe))


def bh(p) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values."""
    p = np.asarray(p, float)
    order = np.argsort(p)
    ranked = p[order] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty_like(q)
    out[order] = np.minimum(q, 1.0)
    return out


def expected_calibration_error(stated, outcome, bins=None) -> float:
    """Average gap between stated probability and observed frequency, weighted by bin size."""
    stated, outcome = np.asarray(stated, float), np.asarray(outcome, float)
    keys = np.unique(stated) if bins is None else np.digitize(stated, bins)
    groups = [stated == k for k in keys] if bins is None else [keys == k for k in np.unique(keys)]
    return float(sum(g.mean() * abs(stated[g].mean() - outcome[g].mean()) for g in groups))


def save(fig, name: str) -> Path:
    path = OUT / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return path
