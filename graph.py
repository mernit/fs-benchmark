import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

backends = ["Filesystem\n(single file)", "Redis", "PostgreSQL"]
p50  = [0.029, 0.100, 0.251]
p95  = [0.043, 0.174, 0.629]
p99  = [0.058, 0.371, 1.330]

x = np.arange(len(backends))
bar_width = 0.26

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#0f0f0f")
ax.set_facecolor("#0f0f0f")

color_p50 = "#4ade80"
color_p95 = "#facc15"
color_p99 = "#f87171"

bars_p50 = ax.bar(x - bar_width, p50, bar_width, label="p50", color=color_p50, zorder=3)
bars_p95 = ax.bar(x,             p95, bar_width, label="p95", color=color_p95, zorder=3)
bars_p99 = ax.bar(x + bar_width, p99, bar_width, label="p99", color=color_p99, zorder=3)

for bar in [*bars_p50, *bars_p95, *bars_p99]:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.01,
        f"{h:.3f}",
        ha="center", va="bottom",
        fontsize=8, color="#cccccc"
    )

ax.set_ylabel("Latency (ms)", color="#cccccc", fontsize=11)
ax.set_title("Reading 100kb of text: Filesystem vs Redis vs PostgreSQL\n1,000 iterations, Apple M-series, local SSD",
             color="#ffffff", fontsize=12, pad=14)
ax.set_xticks(x)
ax.set_xticklabels(backends, color="#cccccc", fontsize=11)
ax.tick_params(colors="#cccccc")
ax.yaxis.label.set_color("#cccccc")
for spine in ax.spines.values():
    spine.set_edgecolor("#333333")
ax.grid(axis="y", color="#222222", zorder=0)
ax.set_ylim(0, 1.6)

legend = ax.legend(
    handles=[
        mpatches.Patch(color=color_p50, label="p50 (median)"),
        mpatches.Patch(color=color_p95, label="p95"),
        mpatches.Patch(color=color_p99, label="p99"),
    ],
    facecolor="#1a1a1a", edgecolor="#333333", labelcolor="#cccccc", fontsize=10
)

plt.tight_layout()
plt.savefig("benchmark.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved benchmark.png")
