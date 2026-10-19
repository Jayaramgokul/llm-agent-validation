"""G1. Red-team failure rate with honest intervals.

Research: Perez et al. (2022), Red Teaming Language Models with Language Models; Ganguli et al.
(2022), Red Teaming Language Models to Reduce Harms; Clopper & Pearson (1934).
Document: 03-research/guardrails-under-attack.md

Question: 144 hand-written attack prompts (8 categories, 6 scenarios, 3
levels of sophistication) and 36 legitimate control questions are each run
three times. What is the failure rate, and what can the sample prove?

Simulated outcomes: no language model is called.

    python 05-illustrations/g1_red_team_failure_rate.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import cluster_interval, prompts_needed, save, upper_bound, wilson  # noqa: E402

CATEGORIES = ["risk override", "guarantees", "discrimination", "fees and conflicts", "jailbreaks",
              "vulnerable customers", "privacy and leakage", "financial crime"]
LEVELS = {"basic": 0.01, "intermediate": 0.04, "advanced": 0.12}
RUNS = 3


def main():
    rng = np.random.default_rng(0)
    prompts = []
    for c in CATEGORIES:
        for _ in range(6):
            for level, base in LEVELS.items():
                # Most prompts never work; the few that do tend to work on most runs.
                breaks = c != "financial crime" and rng.random() < 1.5 * base
                p = rng.uniform(0.4, 1.0) if breaks else 0.0
                prompts.append((c, level, rng.random(RUNS) < p))
    replies = np.concatenate([f for _, _, f in prompts])
    k, n = int(replies.sum()), len(replies)
    lo_w, hi_w = wilson(k, n)
    p, lo, hi = cluster_interval([f for _, _, f in prompts])
    print(f"{len(prompts)} attack prompts x {RUNS} runs = {n} replies (simulated)\n")
    print(f"Failure rate {p:.1%}")
    print(f"  interval treating every reply as independent: {lo_w:.1%} to {hi_w:.1%}")
    print(f"  interval resampling prompts (honest):          {lo:.1%} to {hi:.1%}\n")
    for level in LEVELS:
        cl = [f for _, lv, f in prompts if lv == level]
        p, lo, hi = cluster_interval(cl)
        if p == 0:
            print(f"  {level:13s} no failures in {len(cl)} prompts; upper bound {upper_bound(0, len(cl)):.1%}")
        else:
            print(f"  {level:13s} {p:5.1%} ({lo:.1%} to {hi:.1%})")
    fc = [f for c, _, f in prompts if c == "financial crime"]
    print(f"\nFinancial crime: 0 failures in {len(fc)} prompts. The true rate could still be up to "
          f"{upper_bound(0, len(fc)):.0%}.")
    print(f"Failure-free prompts needed to show a rate below 5%: {prompts_needed(0.05)}; below 1%: "
          f"{prompts_needed(0.01)}")
    controls = rng.random((36, RUNS)) < 0.06                              # legitimate questions refused
    print(f"Over-refusal on 36 legitimate control questions: {controls.mean():.0%}")
    print("\nWhat this shows: three runs of one prompt are not three independent tests, so resampling\n"
          "prompts gives the honest, wider interval. Zero failures is not proof of safety, and an agent\n"
          "that refuses everything would pass every attack, which is why controls are reported beside it.")
    rows = [("all replies, as if independent", k / n, lo_w, hi_w),
            ("all prompts, resampled", *cluster_interval([f for _, _, f in prompts]))]
    for level in LEVELS:
        rows.append((f"{level} attacks", *cluster_interval([f for _, lv, f in prompts if lv == level])))
    rows.append(("financial crime (no failures)", 0.0, 0.0, upper_bound(0, len(fc))))
    fig, ax = plt.subplots(figsize=(6, 3))
    y = np.arange(len(rows))[::-1]
    for i, (label, p, lo, hi) in enumerate(rows):
        ax.errorbar(p, y[i], xerr=[[p - lo], [hi - p]], fmt="o", capsize=3, color="#bdbdbd" if i == 0 else "#3182bd")
    ax.set_yticks(y, [r[0] for r in rows])
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.05))
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Failure rate (95% interval)")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'g1_failure_rates')}")


if __name__ == "__main__":
    main()
