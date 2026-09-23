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
    ax.plot([x, x], [min(v), max(v)], color="#8899aa", lw=6, solid_capstyle="round",
            zorder=1, alpha=0.55)
    ax.plot([x] * len(v), v, "o", ms=7, mfc="white", mec="#1f4e79", mew=1.4,
            zorder=3)
    ax.annotate("min %.5f" % min(v), (x, min(v)), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=8, color="#1f4e79")
ax.axhline(1.0, ls="--", lw=1.2, color="#b00020")
ax.text(0.5, 1.000038, "1.0000 = no loss channel inside the port-mode basis",
        fontsize=7.8, color="#b00020", ha="center", va="bottom")
ax.annotate("", xy=(1.28, 0.99872), xytext=(-0.28, 0.99872),
            arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.2))
ax.text(0.5, 0.99878, "the minimum moves UP, not down  \u2192  "
                      "no radiation-loss channel appeared",
        fontsize=8.2, color="#2e7d32", ha="center", va="bottom")
ax.set_xticks(xpos)
ax.set_xticklabels(["%d modes" % m for m in MODES])
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(0.99860, 1.00022)
ax.set_ylabel("EME port-power column sum\n(one circle = one input mode)")
ax.set_title("Column sums do NOT drop below 1", fontsize=10.5)
ax.grid(alpha=0.25, axis="y")

# --------------------------------------------------------------- right panel
ax = axs[1]
conv = [CONV[m] for m in MODES]
ax.plot(xpos, conv, "o-", color="#c94f2b", lw=1.8, ms=7)
for x, m, c in zip(xpos, MODES, conv):
    ax.annotate("%.3f%%" % c, (x, c), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9, color="#8a3418")
ax.annotate("", xy=(1.0, CONV[6]), xytext=(0.0, CONV[4]),
            arrowprops=dict(arrowstyle="->", color="#666666", lw=1.1, ls="dashed"))
ax.text(0.5, (CONV[4] + CONV[6]) / 2 - 0.20,
        "delta = -0.29%   (convergence test: < 2%)", fontsize=8.6,
        color="#444444", ha="center")
ax.set_xticks(xpos)
ax.set_xticklabels(["%d modes" % m for m in MODES])
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(98.6, 99.95)
ax.set_ylabel("TE1 -> lower-arm TE0 conversion (%)")
ax.set_title("The functional number DOES converge", fontsize=10.5)
ax.grid(alpha=0.25, axis="y")
ax.text(0.5, 99.88, "port-mode-basis conversion  (not device efficiency)",
        fontsize=7.8, color="#555555", ha="center", style="italic")

fig.suptitle("Adding EME port modes 4 -> 6:  conversion converges, "
             "column sums stay at ~1", fontsize=11.5)
fig.tight_layout(rect=(0, 0.035, 1, 0.95))
FC.save(fig, OUT, "external", PROV, bbox_inches="tight")
plt.close(fig)
print("wrote:", OUT, os.path.getsize(OUT), "bytes")
