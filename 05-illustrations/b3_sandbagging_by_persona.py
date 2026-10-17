"""B3. Sandbagging by stated sophistication.

Research: Perez et al. (2023), who tested whether models give less accurate answers to users who
appear less educated ("sandbagging"); Poole-Dayan et al. (2024) on targeted underperformance.
Document: 03-research/behaviour-when-the-user-changes.md

Question: the same factual questions (fees, tax wrappers, how diversification
works) are asked by a persona presenting as a novice and one presenting as an
expert. Are the novice's answers less accurate?

Simulated outcomes: no language model is called.

    python 05-illustrations/b3_sandbagging_by_persona.py
"""

import numpy as np

from common import cluster_interval, paired_interval

QUESTIONS, RUNS = 200, 5


def main():
    rng = np.random.default_rng(0)
    difficulty = rng.normal(1.6, 1.0, QUESTIONS)                      # logit of answering correctly
    expert = [rng.random(RUNS) < 1 / (1 + np.exp(-d)) for d in difficulty]
    novice = [rng.random(RUNS) < 1 / (1 + np.exp(-(d - 0.5))) for d in difficulty]
    for name, res in (("expert persona", expert), ("novice persona", novice)):
        p, lo, hi = cluster_interval(res)
        print(f"{name:15s} accuracy {p:.1%} (95% CI {lo:.1%} to {hi:.1%})")
    diff = np.array([n.mean() - e.mean() for n, e in zip(novice, expert)])
    d, lo, hi = paired_interval(diff)
    print(f"\nNovice minus expert, paired by question: {d:+.1%} (95% CI {lo:+.1%} to {hi:+.1%})")
    if hi < 0:
        print("The paired interval excludes zero: novice personas get less accurate answers.")
    else:
        print("The paired interval includes zero: this sample cannot show a gap. Report it as inconclusive\n"
              "and say how many questions would be needed, rather than as a pass.")
    print("\nWhat this shows: separate accuracy intervals for each persona overlap and suggest little.\n"
          "Pairing by question removes question difficulty from the comparison and sharpens it. Clients\n"
          "who present as less experienced are often the ones who most need accurate answers.")


if __name__ == "__main__":
    main()
