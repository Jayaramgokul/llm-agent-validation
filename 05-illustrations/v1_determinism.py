"""V1. Determinism and reproducibility.

Research: Sclar et al. (2024), on how small prompt changes move LLM outputs; Miller (2024).
Document: 03-research/consistency-and-change.md

Question: a fixed panel of 50 client profiles is put to the agent ten times
each. How often does the recommended portfolio change for the same client,
and are some clients much less stable than others?

Simulated outcomes: no language model is called.

    python 05-illustrations/v1_determinism.py
"""

import numpy as np

PROFILES, RUNS, BUCKETS = 50, 10, 5


def main():
    rng = np.random.default_rng(0)
    # Each profile has a 'true' bucket; profiles near a boundary have a real chance of the next one.
    position = rng.uniform(0, BUCKETS, PROFILES)                     # where the profile sits on the risk scale
    distance = np.abs(position - np.round(position))                # 0 = right on a boundary
    p_flip = np.clip(0.4 - 1.6 * distance, 0.0, 0.4)           # zero once a quarter-bucket from a boundary
    base = np.floor(position).astype(int).clip(0, BUCKETS - 1)
    runs = np.where(rng.random((PROFILES, RUNS)) < p_flip[:, None],
                    np.clip(base[:, None] + rng.choice([-1, 1], (PROFILES, RUNS)), 0, BUCKETS - 1), base[:, None])
    modal_share = np.array([np.bincount(r, minlength=BUCKETS).max() / RUNS for r in runs])
    unstable = modal_share < 1
    print(f"{PROFILES} profiles x {RUNS} runs each (simulated)\n")
    print(f"Profiles that always get the same portfolio: {np.mean(~unstable):.0%}")
    print(f"Profiles that get more than one portfolio:   {np.mean(unstable):.0%}")
    print(f"  of which the most common answer appears in fewer than 8 of 10 runs: {np.mean(modal_share < 0.8):.0%}")
    near = distance < 0.2
    print(f"Instability among profiles near a bucket boundary: {np.mean(unstable[near]):.0%}; "
          f"elsewhere: {np.mean(unstable[~near]):.0%}")
    print("\nWhat this shows: if a client could have received a different portfolio by asking again, the\n"
          "recommendation is hard to defend to the client or an examiner. Either remove the variation\n"
          "(fixed settings, deterministic post-processing) or document and disclose the band, and route\n"
          "boundary cases to the same treatment every time.")


if __name__ == "__main__":
    main()
