import numpy as np
import matplotlib.pyplot as plt

def hist_kde(x, bins=50, ax=None, density=True, bw="scott", label=None):
    """
    一张图：直方图 + KDE（需要 scipy）。
    x: 1D array-like
    bw: "scott" / "silverman" / float
    """
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    # histogram
    ax.hist(x, bins=bins, density=density, alpha=0.35, edgecolor="none",
            label=(label or "hist"))

    # kde (optional)
    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(x, bw_method=bw)
        xs = np.linspace(x.min(), x.max(), 400)
        ax.plot(xs, kde(xs), linewidth=2, label=(label + " kde") if label else "kde")
    except Exception:
        ax.text(0.02, 0.95, "No scipy -> skip KDE", transform=ax.transAxes, va="top")

    ax.set_ylabel("Density" if density else "Count")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.5)
    ax.legend(frameon=False)
    return ax