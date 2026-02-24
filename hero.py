import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# 690x290 @ 100dpi — use inches as coordinate units
DPI = 100
W, H = 6.9, 2.9

fig, ax = plt.subplots(figsize=(W, H))
fig.patch.set_facecolor("#0d0d0d")
ax.set_facecolor("#0d0d0d")
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

MONO   = "monospace"
WHITE  = "#f0f0f0"
DIM    = "#555555"
GREEN  = "#4ade80"
ARROW  = "#444444"

cx = W / 2  # horizontal center = 3.45

# --- Agent box ---
bw, bh = 2.2, 0.52
agent_box = FancyBboxPatch((cx - bw/2, 2.2), bw, bh,
    boxstyle="round,pad=0.08",
    linewidth=1.0, edgecolor="#444444", facecolor="#1a1a1a")
ax.add_patch(agent_box)
ax.text(cx, 2.46, "agent", ha="center", va="center",
        fontsize=13, color=WHITE, fontfamily=MONO, fontweight="bold")

# --- Arrow ---
ax.annotate("", xy=(cx, 1.78), xytext=(cx, 2.2),
    arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.3))

# --- /workspace/ ---
ax.text(cx, 1.60, "/workspace/", ha="center", va="center",
        fontsize=11, color=GREEN, fontfamily=MONO, fontweight="bold")

# --- Tree ---
trunk_x = cx - 0.9
ax.plot([trunk_x, cx],        [1.44, 1.44], color=DIM, lw=1.0)  # connector to workspace
ax.plot([trunk_x, trunk_x],   [0.22, 1.44], color=DIM, lw=1.0)  # vertical trunk

entries = [
    ("/emails/unread",    "#a78bfa"),
    ("/users/123/orders", "#38bdf8"),
    ("/orders/pending",   "#fb923c"),
]
y_positions = [1.18, 0.72, 0.26]

for (label, color), y in zip(entries, y_positions):
    ax.plot([trunk_x, trunk_x + 0.28], [y, y], color=DIM, lw=1.0)
    ax.text(trunk_x + 0.36, y, "▸", ha="left", va="center",
            fontsize=8, color=DIM, fontfamily=MONO)
    ax.text(trunk_x + 0.58, y, label, ha="left", va="center",
            fontsize=11, color=color, fontfamily=MONO)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("hero.png", dpi=DPI, bbox_inches=None,
            facecolor=fig.get_facecolor())
print("Saved hero.png")
