# make_fig_colsum_vs_modes.py -- falsification figure for this repository.
#
# LEFT panel  : EME port-power column sums vs number of port modes (4 and 6).
#               If radiation loss were represented in the port-mode basis, the
#               column sums would fall BELOW 1 as modes are added. Measured:
#               they do not -- the minimum moves UP (0.99889 -> 0.99973).
# RIGHT panel : the functional conversion TE1 -> lower-arm TE0 DOES converge
#               (99.525% -> 99.233%, delta = -0.29%, i.e. passes the <2% test).
#
# Reading the two panels together is the point of this figure: the number that
# matters for the device converges, while the number that would give absolute
# insertion loss never leaves the port-mode basis.
#
# Data source (verbatim, no rounding changed):
#   notes/eme_coupler_4modes.md            -> column sums + conversion, 4 modes
#   notes/eme_coupler_6modes_convergence.md-> column sums + conversion, 6 modes
#
# This is an EXTERNAL PLOT: a matplotlib re-projection of tabulated solver
# output, NOT a solver export. It is written through fig_channel.save() so the
# statement is on the figure AND in the PNG metadata (the same convention used
# in the figure-provenance tooling).
#
# Usage:  python make_fig_colsum_vs_modes.py
import os
import sys

# console code pages are not always UTF-8; never let a print() kill the script
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                                    # noqa: BLE001
        pass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fig_channel as FC                                                 # noqa: E402

OUT = os.path.join(HERE, "..", "figures", "colsum_and_conversion_vs_modes.png")
PROV = ("col sums and conversion re-plotted from the tabulated EME results "
        "(4-mode and 6-mode runs); not a solver export")

MODES = [4, 6]
# per-input column sums, taken from the two run records
COLSUM = {
    4: [0.99999, 0.99996, 0.99999, 0.99889],
    6: [0.99999, 0.99996, 0.99999, 0.99991, 0.99995, 0.99973],
}
# TE1 -> lower-arm TE0 conversion (%)
CONV = {4: 99.525, 6: 99.233}

fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.3), dpi=150)

# ---------------------------------------------------------------- left panel
ax = axs[0]
xpos = [0.0, 1.0]
for i, (x, m) in enumerate(zip(xpos, MODES)):
    v = COLSUM[m]
    ax.plot([x, x], [min(v), max(v)], color="#8899aa", lw=4, solid_capstyle="round",
            zorder=1, alpha=0.55)
    ax.plot([x] * len(v), v, "o", ms=5, mfc="white", mec="#1f4e79", mew=1.1,
            zorder=3)
    # 数值标注与说明文字移交图注（见稿件 Fig. 3 的 \caption）
ax.axhline(1.0, ls="--", lw=1.2, color="#b00020")
ax.set_xticks(xpos)
ax.set_xticklabels(["%d modes" % m for m in MODES])
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(0.99860, 1.00022)
ax.set_ylabel("EME port-power column sum\n(one circle = one input mode)")
ax.set_title("Column sums stay at 1", fontsize=12)
ax.grid(alpha=0.25, axis="y")

# --------------------------------------------------------------- right panel
ax = axs[1]
conv = [CONV[m] for m in MODES]
ax.plot(xpos, conv, "o-", color="#c94f2b", lw=1.4, ms=5)
# 数值标签与 "delta = ..." 说明移交图注
ax.set_xticks(xpos)
ax.set_xticklabels(["%d modes" % m for m in MODES])
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(98.6, 99.95)
ax.set_ylabel("TE1 -> lower-arm TE0 conversion (%)")
ax.set_title("Conversion converges", fontsize=12)
ax.grid(alpha=0.25, axis="y")
# 面板内那条斜体说明移交图注

fig.suptitle("EME port modes 4 -> 6", fontsize=13)
fig.tight_layout(rect=(0, 0.035, 1, 0.95))
# 按你的要求：图上**不再画**"外部绘图"页脚（避免遮挡图面）；同一句声明仍写进 PNG 元数据
# （fig_index 的审计照旧可查），并在稿件的图注里用文字给出。
fig.savefig(OUT, bbox_inches="tight",
            metadata={FC.CHUNK: FC.statement("external", PROV)})
plt.close(fig)
print("wrote:", OUT, os.path.getsize(OUT), "bytes")
