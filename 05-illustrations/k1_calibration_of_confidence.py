"""K1. Calibration of confidence statements.

Research: Kadavath et al. (2022), Language Models (Mostly) Know What They Know; Guo et al. (2017),
On Calibration of Modern Neural Networks.
Document: 03-research/honest-confidence.md

Question: the agent describes outcomes with phrases such as "very likely" or
"unlikely". When it says "very likely", does the outcome happen about as
often as a client would take that phrase to mean?

Simulated outcomes: no language model is called.

    python 05-illustrations/k1_calibration_of_confidence.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import expected_calibration_error, save, wilson  # noqa: E402

# What each phrase is taken to mean (agreed with compliance), and how often it is used.
PHRASES = {"almost certain": 0.95, "very likely": 0.85, "likely": 0.70, "possible": 0.40, "unlikely": 0.15}
USE = [0.10, 0.25, 0.30, 0.20, 0.15]
TRUE_RATE = {"almost certain": 0.80, "very likely": 0.72, "likely": 0.66, "possible": 0.42, "unlikely": 0.17}


def main():
    rng = np.random.default_rng(0)
    n = 2000
    phrase = rng.choice(list(PHRASES), n, p=USE)
    happened = rng.random(n) < np.array([TRUE_RATE[p] for p in phrase])
    stated = np.array([PHRASES[p] for p in phrase])
    print(f"{n} statements with a confidence phrase, checked against what happened (simulated)\n")
    rows = []
    for p, meaning in PHRASES.items():
        m = phrase == p
        k, total = int(happened[m].sum()), int(m.sum())
        lo, hi = wilson(k, total)
        rows.append((meaning, k / total, lo, hi))
        flag = "   overstated" if hi < meaning else ""
        print(f"{p:15s} means {meaning:4.0%}   happened {k / total:4.0%} (95% CI {lo:.0%} to {hi:.0%}){flag}")
    print(f"\nExpected calibration error: {expected_calibration_error(stated, happened):.1%}")
    print("\nWhat this shows: the agent is roughly right about doubtful outcomes and overconfident about\n"
          "the ones it is surest of, which is where clients rely on it most. Agree what each phrase means,\n"
          "then check the record against it, phrase by phrase.")

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot([0, 1], [0, 1], color="#bbb", lw=1)
    for meaning, rate, lo, hi in rows:
        ax.errorbar(meaning, rate, yerr=[[rate - lo], [hi - rate]], fmt="o", color="#3182bd", capsize=3)
    ax.set_xlabel("What the phrase means")
    ax.set_ylabel("How often it happened")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'k1_reliability')}")


if __name__ == "__main__":
    main()
