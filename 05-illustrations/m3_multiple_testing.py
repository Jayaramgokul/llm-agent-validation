"""M3. Multiple testing across the suite.

Research: Benjamini & Hochberg (1995).
Document: 03-research/measuring-honestly.md

Question: a new agent version is compared with the old one on 8 attack
categories x 3 sophistication levels x 6 client personas = 144 slices. Three
slices genuinely regressed. How many alarms are real?

Simulated outcomes: no language model is called.

    python 05-illustrations/m3_multiple_testing.py
"""

import numpy as np
from scipy import stats

from common import bh

SLICES, REAL, N = 144, 3, 400


def main():
    rng = np.random.default_rng(1)
    old_rate = rng.uniform(0.02, 0.08, SLICES)
    new_rate = old_rate.copy()
    new_rate[:REAL] += 0.10
    old = rng.binomial(N, old_rate)
    new = rng.binomial(N, new_rate)
    p = np.array([stats.fisher_exact([[n_, N - n_], [o, N - o]], alternative="greater")[1] for n_, o in zip(new, old)])
    real = np.arange(SLICES) < REAL
    print(f"{SLICES} slices, {N} replies each per version; {REAL} slices genuinely worse (simulated)\n")
    raw = p < 0.05
    for label, flag in (("each slice at p < 0.05", raw), ("false discovery rate 10% (BH)", bh(p) < 0.10)):
        print(f"{label:30s} {flag.sum():2d} alarms: {np.sum(flag & real)} real, {np.sum(flag & ~real)} false")
    print("\nWhat this shows: slicing an LLM evaluation by category, level and persona multiplies the tests.\n"
          f"Without correction, {np.sum(raw & ~real)} of {raw.sum()} alarms are false, and each one costs an investigation or a\n"
          "blocked release. Controlling the false discovery rate across the whole comparison keeps the real\n"
          "regressions and drops the chance ones.")


if __name__ == "__main__":
    main()
