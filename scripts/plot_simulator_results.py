"""Reproduce six statistical-simulation success/regret figures.

Run from repository root: python scripts/plot_simulator_results.py
Reads the archived 50-seed simulator trials; no IBM hardware is accessed.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "simulator_raw.csv.gz"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, compression="gzip")
required = {
    "delta", "seed", "qpa", "method", "kR", "supported",
    "total_queries_used", "total_queries_requested",
    "success", "simple_regret",
}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

# Underfunded trials are not counted as supported configurations.
rows = df[(df["supported"] == 1) & (df["qpa"] >= 200)].copy()
n_arms = int((rows["total_queries_requested"] / rows["qpa"]).median())
if n_arms != 1000:
    raise ValueError(f"Unexpected arm count: {n_arms}")

summary = (
    rows.groupby(["delta", "method", "kR", "qpa"], as_index=False)
    .agg(
        trials=("seed", "nunique"),
        success_rate=("success", "mean"),
        mean_simple_regret=("simple_regret", "mean"),
        mean_total_queries_used=("total_queries_used", "mean"),
    )
)
summary["mean_queries_per_arm_used"] = (
    summary["mean_total_queries_used"] / n_arms
)
summary.to_csv(OUT / "aggregated_simulation_results.csv", index=False)

for delta in [0.01, 0.05, 0.10]:
    data = summary[np.isclose(summary["delta"], delta)]
    for metric, kind, ylabel in [
        ("success_rate", "success", "Exact best-arm success rate"),
        ("mean_simple_regret", "regret", "Mean simple regret"),
    ]:
        fig, ax = plt.subplots(figsize=(9, 5.3))
        for kr in range(11):
            q = data[
                (data["method"] == "theory_stream_dswap")
                & (data["kR"] == kr)
            ].sort_values("qpa")
            if not q.empty:
                ax.plot(
                    q["mean_queries_per_arm_used"], q[metric],
                    "-o", color=plt.cm.viridis(.07 + .87 * kr / 10),
                    ms=3.5, lw=1.6, label=rf"$k_R={kr}$",
                )
        for method, label, color, linestyle, marker in [
            ("sequential_halving", "Sequential Halving", "#b52e25", "--", "D"),
            ("uniform_sampling", "Uniform Sampling", "#262626", ":", "s"),
        ]:
            q = data[data["method"] == method].sort_values("qpa")
            if not q.empty:
                ax.plot(
                    q["mean_queries_per_arm_used"], q[metric],
                    linestyle=linestyle, marker=marker, color=color,
                    lw=2.3, ms=5, label=label,
                )
        ax.set_xscale("log")
        ax.set_xlabel("Mean realized logical oracle queries per arm")
        ax.set_ylabel(ylabel)
        if metric == "success_rate":
            ax.set_ylim(-.03, 1.03)
        else:
            ax.set_ylim(bottom=0)
        ax.set_title(
            rf"Statistical simulation | $\Delta_{{[2]}}={delta:.2f}$ | "
            rf"$n=1000$ | 50 seeds"
        )
        ax.grid(alpha=.22, which="both")
        ax.legend(ncol=2, fontsize=7)
        fig.tight_layout()
        tag = {0.01: "0p01", 0.05: "0p05", 0.10: "0p1"}[delta]
        for ext in ["pdf", "png"]:
            fig.savefig(
                OUT / f"sim_{kind}_delta_{tag}.{ext}",
                dpi=180, bbox_inches="tight",
            )
        plt.close(fig)
        print(f"Saved sim_{kind}_delta_{tag}.pdf")

print("Saved six figures to:", OUT)
