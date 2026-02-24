import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor("#0d0d0d")
ax.set_facecolor("#0d0d0d")
ax.set_xlim(0, 10)
ax.set_ylim(4.1, 9.5)
ax.axis("off")

MONO = "monospace"
WHITE = "#f0f0f0"
DIM = "#555555"
GREEN = "#4ade80"
ARROW = "#444444"

# --- Agent box ---
agent_box = FancyBboxPatch((3.5, 8.0), 3, 0.95,
    boxstyle="round,pad=0.15",
    linewidth=1.2, edgecolor="#444444", facecolor="#1a1a1a")
ax.add_patch(agent_box)
ax.text(5, 8.49, "agent", ha="center", va="center",
        fontsize=14, color=WHITE, fontfamily=MONO, fontweight="bold")

# --- Arrow down to workspace ---
ax.annotate("", xy=(5, 7.15), xytext=(5, 8.0),
    arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.5))

# --- Root folder ---
ax.text(5, 6.82, "/workspace/", ha="center", va="center",
        fontsize=13, color=GREEN, fontfamily=MONO, fontweight="bold")

# --- Trunk: from workspace down to last entry ---
trunk_x = 3.5
ax.plot([trunk_x, trunk_x], [4.55, 6.55], color=DIM, lw=1.2)

# --- Connecting line from /workspace/ down to trunk ---
ax.plot([trunk_x, 5.0], [6.55, 6.55], color=DIM, lw=1.2)

entries = [
    ("/emails/unread",     "#a78bfa"),
    ("/users/123/orders",  "#38bdf8"),
    ("/context/notes",     "#fb923c"),
]

y_positions = [6.1, 5.4, 4.7]

for (label, color), y in zip(entries, y_positions):
    ax.plot([trunk_x, trunk_x + 0.55], [y, y], color=DIM, lw=1.2)
    ax.text(trunk_x + 0.7, y, "▸", ha="left", va="center",
            fontsize=9, color=DIM, fontfamily=MONO)
    ax.text(trunk_x + 1.1, y, label, ha="left", va="center",
            fontsize=12, color=color, fontfamily=MONO)

plt.tight_layout(pad=0)
plt.savefig("hero.png", dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved hero.png")
