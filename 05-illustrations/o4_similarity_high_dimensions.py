"""O4. Similarity in high dimensions.

Research: Beyer et al. (1999), When Is "Nearest Neighbor" Meaningful?; Hastie et al. (2009),
section 2.5.
Document: 03-research/the-agent-in-operation.md

Question: the agent retrieves "clients like you" or "similar past questions"
by nearest-neighbour search over embeddings. Is the nearest item meaningfully
nearer than the farthest?

Simulated embeddings: no language model is called.

    python 05-illustrations/o4_similarity_high_dimensions.py
"""

import numpy as np


def relative_contrast(E, rng, queries=200):
    """(farthest - nearest) / nearest distance, averaged over queries (Beyer et al., 1999)."""
    q = rng.choice(len(E), queries, replace=False)
    d = np.sqrt(((E[q, None, :] - E[None, :, :]) ** 2).sum(-1))
    d[np.arange(queries), q] = np.nan
    return float(np.nanmean((np.nanmax(d, 1) - np.nanmin(d, 1)) / np.nanmin(d, 1)))


def main():
    rng = np.random.default_rng(0)
    n = 2000
    print("Relative contrast: how much farther the farthest item is than the nearest (simulated)\n")
    for d in (2, 8, 64, 768):
        print(f"no structure, {d:3d} dimensions          {relative_contrast(rng.normal(size=(n, d)), rng):6.2f}")
    centres = rng.normal(size=(30, 768)) * 1.5
    E = centres[rng.integers(0, 30, n)] + rng.normal(size=(n, 768))
    print(f"30 real client types, 768 dimensions  {relative_contrast(E, rng):6.2f}")
    print("\nWhat this shows: as dimensions grow, with no real structure, every item ends up about equally\n"
          "far from every other, so 'nearest' means little. Real structure restores the contrast. A\n"
          "retrieval component should be shown to have that structure, by comparing its neighbours with\n"
          "random pairs, before 'similar clients' are used to shape advice.")


if __name__ == "__main__":
    main()
