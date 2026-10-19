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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import save  # noqa: E402


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
    contrast = {}
    for d in (2, 8, 64, 768):
        contrast[d] = relative_contrast(rng.normal(size=(n, d)), rng)
        print(f"no structure, {d:3d} dimensions          {contrast[d]:6.2f}")
    centres = rng.normal(size=(30, 768)) * 1.5
    E = centres[rng.integers(0, 30, n)] + rng.normal(size=(n, 768))
    structured = relative_contrast(E, rng)
    print(f"30 real client types, 768 dimensions  {structured:6.2f}")
    print("\nWhat this shows: as dimensions grow, with no real structure, every item ends up about equally\n"
          "far from every other, so 'nearest' means little. Real structure restores the contrast. A\n"
          "retrieval component should be shown to have that structure, by comparing its neighbours with\n"
          "random pairs, before 'similar clients' are used to shape advice.")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(list(contrast), list(contrast.values()), "o-", color="#3182bd", label="no structure")
    ax.plot(768, structured, "s", color="#d8543b", label="30 real client types")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(list(contrast), [str(d) for d in contrast])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Dimensions")
    ax.set_ylabel("Relative contrast (log scale)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'o4_contrast_by_dimension')}")


if __name__ == "__main__":
    main()
