"""M1. Validating the judge.

Research: Zheng et al. (2023), Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena; Wang et
al. (2024), Large Language Models are not Fair Evaluators.
Document: 03-research/measuring-honestly.md

Question: an LLM judge grades the agent's replies. Before its verdicts are
trusted, how well does it agree with human reviewers, how many real failures
does it miss, and does it favour the first answer shown or longer answers?

Simulated outcomes: no language model is called.

    python 05-illustrations/m1_validating_the_judge.py
"""

import numpy as np
import statsmodels.api as sm

from common import cohen_kappa, wilson


def main():
    rng = np.random.default_rng(0)
    n = 400
    human = rng.random(n) < 0.12                                     # True = reviewer says the reply fails policy
    judge = np.where(human, rng.random(n) < 0.78, rng.random(n) < 0.03)
    k = int((judge & human).sum())
    lo, hi = wilson(k, int(human.sum()))
    boots = []
    for _ in range(2000):
        s = rng.integers(0, n, n)
        boots.append(cohen_kappa(human[s], judge[s]))
    print(f"{n} replies labelled by a human reviewer and by the judge (simulated)\n")
    print(f"Agreement (kappa)              {cohen_kappa(human, judge):.2f} "
          f"(95% CI {np.quantile(boots, .025):.2f} to {np.quantile(boots, .975):.2f})")
    print(f"Real failures the judge caught {k} of {int(human.sum())} = {k / human.sum():.0%} "
          f"(95% CI {lo:.0%} to {hi:.0%})")

    # Position bias: the same pair of answers shown in both orders.
    pairs = 300
    quality_gap = rng.normal(0, 1, pairs)
    first_bias = 0.6
    pick_a_first = rng.random(pairs) < 1 / (1 + np.exp(-(quality_gap + first_bias)))
    pick_a_second = rng.random(pairs) < 1 / (1 + np.exp(-(quality_gap - first_bias)))
    consistent = np.mean(pick_a_first == pick_a_second)
    print(f"\nSame pair, order swapped: the judge's choice holds in {consistent:.0%} of pairs")
    print(f"Answer A chosen when shown first: {pick_a_first.mean():.0%}; when shown second: {pick_a_second.mean():.0%}")

    # Length bias: score against length for answers of equal human-rated quality.
    length = rng.uniform(80, 600, 500)
    quality = rng.normal(0, 1, 500)
    score = 6 + 1.0 * quality + 0.003 * length + rng.normal(0, 0.8, 500)
    fit = sm.OLS(score, sm.add_constant(np.column_stack([quality, length / 100]))).fit()
    lo_l, hi_l = fit.conf_int()[2]
    print(f"Holding quality fixed, each extra 100 words adds {fit.params[2]:+.2f} points "
          f"(95% CI {lo_l:+.2f} to {hi_l:+.2f}) on a 10-point scale")
    print("\nWhat this shows: the judge is itself a model under validation. Good overall agreement still\n"
          f"leaves it missing {1 - k / human.sum():.0%} of real failures, so the failure rate it reports understates\n"
          "the truth unless corrected or checked against a human sample. Swapping the order and\n"
          "controlling for length expose biases that would otherwise be read as differences in quality.")


if __name__ == "__main__":
    main()
