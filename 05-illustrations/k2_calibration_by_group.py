"""K2. Calibration by group.

Research: Kadavath et al. (2022); Barocas et al. (2021) on disaggregated evaluation.
Document: 03-research/honest-confidence.md

Question: the agent's confidence is well calibrated overall. Is it equally
well calibrated for clients who write in plain, informal English and for
those who write formally?

Simulated outcomes: no language model is called.

    python 05-illustrations/k2_calibration_by_group.py
"""

import numpy as np

from common import expected_calibration_error

BINS = np.linspace(0.1, 0.9, 9)


def main():
    rng = np.random.default_rng(0)
    n = 6000
    group = rng.choice(["formal", "informal"], n, p=[0.7, 0.3])
    stated = rng.uniform(0.05, 0.99, n)
    # Informal writers' questions are understood less well: the same stated confidence is right less often.
    true_p = np.where(group == "formal", stated, np.clip(stated - 0.12 * stated, 0, 1))
    happened = rng.random(n) < true_p
    print("Expected calibration error, overall and by how the client writes (simulated)\n")
    for label, m in [("overall", np.ones(n, bool)), ("formal", group == "formal"), ("informal", group == "informal")]:
        ece = expected_calibration_error(stated[m], happened[m], BINS)
        boots = []
        idx = np.flatnonzero(m)
        for _ in range(500):
            s = rng.choice(idx, len(idx))
            boots.append(expected_calibration_error(stated[s], happened[s], BINS))
        lo, hi = np.quantile(boots, [0.025, 0.975])
        gap = stated[m].mean() - happened[m].mean()
        print(f"{label:9s} ECE {ece:5.1%} (95% CI {lo:.1%} to {hi:.1%})   stated minus actual {gap:+.1%}")
    print("\nWhat this shows: an overall calibration figure averages a well-served majority with a minority\n"
          "for whom the agent is consistently overconfident. Calibration should be reported per group, like\n"
          "any other performance measure.")


if __name__ == "__main__":
    main()
