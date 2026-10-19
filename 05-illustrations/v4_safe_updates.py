"""V4. Safe model updates.

Research: Saria & Subbaswamy (2019), safe updating; Benjamini & Hochberg (1995).
Document: 03-research/consistency-and-change.md

Question: a new model version has a lower overall failure rate. Is it worse
for any client persona or attack category, once the number of comparisons is
accounted for?

Simulated outcomes: no language model is called.

    python 05-illustrations/v4_safe_updates.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

from common import bh, save  # noqa: E402

PERSONAS = ["retiree", "first-time investor", "high earner", "student", "small business owner", "non-native speaker"]
CATEGORIES = ["risk override", "guarantees", "fees", "vulnerable customer"]
N = 400


def main():
    rng = np.random.default_rng(3)
    rows = []
    for persona in PERSONAS:
        for cat in CATEGORIES:
            old_rate = rng.uniform(0.04, 0.10)
            new_rate = old_rate * 0.7
            if persona == "non-native speaker" and cat == "vulnerable customer":
                new_rate = old_rate + 0.10                      # the update broke this cell
            old, new = rng.binomial(N, old_rate), rng.binomial(N, new_rate)
            p = stats.fisher_exact([[new, N - new], [old, N - old]], alternative="greater")[1]
            rows.append((persona, cat, old / N, new / N, p))
    old_all = np.mean([r[2] for r in rows])
    new_all = np.mean([r[3] for r in rows])
    print(f"Failure rate overall: old {old_all:.1%}, new {new_all:.1%} (simulated)\n")
    q = bh([r[4] for r in rows])
    for (persona, cat, o, n, p), qi in zip(rows, q):
        if qi < 0.10:
            print(f"Regression: {persona} / {cat}: {o:.1%} -> {n:.1%} (corrected q = {qi:.3f})")
    print("\nWhat this shows: the new version is better on average and worse for one group of clients in\n"
          "one situation. A release decision based on the average would ship the regression. Compare\n"
          "old and new cell by cell, correct for the number of cells, and block or mitigate any regression.")
    change = 100 * np.array([r[3] - r[2] for r in rows]).reshape(len(PERSONAS), len(CATEGORIES))
    flagged = (q < 0.10).reshape(change.shape)
    lim = np.abs(change).max()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    im = ax.imshow(change, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
    for i in range(len(PERSONAS)):
        for j in range(len(CATEGORIES)):
            ax.text(j, i, f"{change[i, j]:+.1f}", ha="center", va="center", fontsize=8,
                    color="white" if abs(change[i, j]) > 0.6 * lim else "black")
            if flagged[i, j]:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec="black", lw=2))
    ax.set_xticks(range(len(CATEGORIES)), [c.replace(" ", "\n") for c in CATEGORIES])
    ax.set_yticks(range(len(PERSONAS)), PERSONAS)
    fig.colorbar(im, ax=ax, label="New minus old failure rate (points)")
    print(f"\nChart: {save(fig, 'v4_regression_by_cell')}")


if __name__ == "__main__":
    main()
