"""O1. Explanations that are faithful.

Research: Jacovi & Goldberg (2020), Towards Faithfully Interpretable NLP Systems.
Document: 03-research/the-agent-in-operation.md

Question: the agent tells each client the three factors that drove their
recommendation. Do those factors actually drive it? If they are neutralised,
does the recommendation move more than if three random factors are?

A stand-in scoring rule plays the model; two ways of producing the stated
reasons are compared.

    python 05-illustrations/o1_faithful_explanations.py
"""

import numpy as np

FACTORS = ["time horizon", "loss tolerance", "income stability", "existing savings", "debt", "experience"]
WEIGHTS = np.array([0.05, 0.45, 0.04, 0.35, -0.25, 0.03])
GENERIC = [0, 1, 5]            # a template that always cites horizon, tolerance and experience


def main():
    rng = np.random.default_rng(0)
    n = 3000
    X = rng.normal(0, 1, (n, len(FACTORS)))
    score = X @ WEIGHTS
    contrib = X * WEIGHTS
    faithful = np.argsort(-np.abs(contrib), axis=1)[:, :3]          # the three largest actual contributions

    def change_when_neutralised(chosen):
        Xn = X.copy()
        Xn[np.arange(n)[:, None], chosen] = 0.0
        return np.abs(Xn @ WEIGHTS - score).mean()

    random = np.array([rng.choice(len(FACTORS), 3, replace=False) for _ in range(n)])
    generic = np.tile(GENERIC, (n, 1))
    base = change_when_neutralised(random)
    print("Average change in the score when the stated reasons are neutralised (simulated)\n")
    for label, chosen in (("three random factors", random), ("template reasons", generic),
                          ("reasons from actual contributions", faithful)):
        c = change_when_neutralised(chosen)
        print(f"{label:34s} {c:.3f}   ({c / base:.1f}x random)")
    print("\nWhat this shows: a plausible explanation is not necessarily a faithful one. Generic reasons\n"
          "read well but barely beat chance at predicting what moves the recommendation. The deletion test\n"
          "checks explanations against the model's actual behaviour.")


if __name__ == "__main__":
    main()
