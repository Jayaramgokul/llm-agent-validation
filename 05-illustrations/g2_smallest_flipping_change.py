"""G2. Adversarial robustness: the smallest change that flips the outcome.

Research: red-teaming literature (Perez et al., 2022; Ganguli et al., 2022), applied to the
structured inputs an agent collects.
Document: 03-research/guardrails-under-attack.md

Question: the agent collects eight risk-questionnaire answers (1 to 5) and
offers the highest-risk band (Band 5) to clients scoring 75 or more. How many
clients could unlock it by changing one or two answers, and would a
consistency check catch them?

Simulated data: no language model is called.

    python 05-illustrations/g2_smallest_flipping_change.py
"""

import numpy as np

ITEMS, CUT = 8, 75


def score(a):
    return (a - 1).mean(axis=-1) / 4 * 100


def main():
    rng = np.random.default_rng(0)
    n = 5000
    latent = rng.normal(0, 1, n)
    answers = np.clip(np.round(3 + latent[:, None] + rng.normal(0, 0.6, (n, ITEMS))), 1, 5)
    eligible = score(answers) >= CUT
    # Raise the lowest answers to 5: the cheapest way to cross the cut-off.
    order = np.sort(answers, axis=1)
    needed = np.full(n, 99)
    for k in range(1, ITEMS + 1):
        gamed = order.copy()
        gamed[:, :k] = 5
        newly = (score(gamed) >= CUT) & (needed == 99) & ~eligible
        needed[newly] = k
    within1, within2 = np.mean(~eligible & (needed <= 1)), np.mean(~eligible & (needed <= 2))
    print(f"Clients not eligible for Band 5: {np.mean(~eligible):.0%} (simulated)\n")
    print(f"Could become eligible by changing one answer:   {within1:.1%} of all clients")
    print(f"Could become eligible by changing two answers:  {within2:.1%} of all clients")
    # A simple consistency check: flag answer sets whose spread is unusually wide.
    spread_ok = np.percentile(answers.std(axis=1), 95)
    gamed2 = order.copy()
    gamed2[:, :2] = 5
    caught = gamed2.std(axis=1) > spread_ok
    two = ~eligible & (needed == 2)
    print(f"Of the two-answer cases, a spread-based consistency check would flag: {caught[two].mean():.0%}")
    if caught[two].mean() < 0.5:
        print("A simple spread check misses most of them, so it is not an adequate control on its own.")
    print("\nWhat this shows: a hard cut-off on a short questionnaire is easy to game, often by changing one\n"
          "or two answers, whether by a client or by an agent steered into 'helping'. The test measures how\n"
          "close clients sit to each threshold and whether consistency checks catch implausible changes.")


if __name__ == "__main__":
    main()
