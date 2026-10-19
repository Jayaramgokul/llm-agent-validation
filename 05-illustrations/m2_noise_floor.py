"""M2. Know the noise first.

Research: Miller (2024), Adding Error Bars to Evals; Efron (1979).
Document: 03-research/measuring-honestly.md

Question: a new prompt version is compared with the current one on a
300-question evaluation. Is the difference a real change, or the model's
normal run-to-run variation?

Simulated outcomes: no language model is called.

    python 05-illustrations/m2_noise_floor.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import paired_interval, save  # noqa: E402

QUESTIONS, BASELINE_RUNS = 300, 10


def run(p, rng):
    return rng.random(len(p)) < p


def main():
    rng = np.random.default_rng(0)
    p_current = 1 / (1 + np.exp(-rng.normal(1.2, 1.3, QUESTIONS)))   # per-question chance of a correct answer
    p_new = np.clip(p_current + rng.normal(0.0, 0.03, QUESTIONS), 0, 1)
    baseline = np.array([run(p_current, rng).mean() for _ in range(BASELINE_RUNS)])
    floor = np.quantile(np.abs(baseline[:, None] - baseline[None, :])[np.triu_indices(BASELINE_RUNS, 1)], 0.95)
    current, new = run(p_current, rng), run(p_new, rng)
    print(f"Current version run {BASELINE_RUNS} times, unchanged: scores from {baseline.min():.1%} to {baseline.max():.1%}")
    print(f"Noise floor (95th percentile of differences between identical runs): {floor:.1%}\n")
    single = new.mean() - current.mean()
    print(f"One run each: current {current.mean():.1%}, new {new.mean():.1%}, difference {single:+.1%}"
          f"{'  (inside the noise floor)' if abs(single) < floor else ''}")
    reps = 5
    cur_rep = np.array([run(p_current, rng) for _ in range(reps)]).mean(0)
    new_rep = np.array([run(p_new, rng) for _ in range(reps)]).mean(0)
    d, lo, hi = paired_interval(new_rep - cur_rep)
    print(f"Five runs each, paired by question: difference {d:+.1%} (95% CI {lo:+.1%} to {hi:+.1%})")
    verdict = "a real change" if lo > 0 or hi < 0 else "not distinguishable from noise"
    print(f"Verdict: {verdict}.")
    print("\nWhat this shows: an unchanged model does not score the same twice. Measure that first, then\n"
          "report only differences beyond it, using several runs and pairing by question, so that a\n"
          "lucky run is not reported as an improvement, or an unlucky one as a regression.")
    fig, ax = plt.subplots(figsize=(6, 2.2))
    ax.axvspan(baseline.min(), baseline.max(), color="#eeeeee")
    ax.plot(baseline, np.full(BASELINE_RUNS, 2), "o", color="#3182bd")
    ax.plot(current.mean(), 1, "o", color="#3182bd")
    ax.plot(new.mean(), 0, "o", color="#d8543b")
    ax.set_yticks([2, 1, 0], [f"current version, {BASELINE_RUNS} identical runs", "current version, one run",
                              "new version, one run"])
    ax.set_ylim(-0.6, 2.6)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Score; grey band = range of the identical runs")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'm2_noise_floor')}")


if __name__ == "__main__":
    main()
