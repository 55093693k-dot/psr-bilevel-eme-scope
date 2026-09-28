# make_fig_cross_sections.py -- fig 2 of the manuscript: the two cross-sections of the device,
# drawn in the clean "plane plot" style asked for on 2026-09-28 (µm axes with ticks, a panel
# frame, ports marked with arrows, and NO dimension text on the figure -- every dimension is
# stated in the manuscript caption).
#
# Geometry: DEVICES["psr_rotator"] of make_structure_fig.py (slab 1.55 µm wide, 90 nm partial
# etch, 220 nm Si, 200 nm edge-to-edge gap, w2 = 550 nm at mid-taper, w5/w6 = 650/500 nm at the
# coupler end).
#
# Saved through fig_channel's metadata convention but WITHOUT the on-figure footer (author's
# request: the footer blocked the drawing); the statement still goes into the PNG tEXt chunk.
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                          # noqa: E402
from matplotlib.patches import Polygon, Rectangle                        # noqa: E402
from matplotlib.ticker import AutoMinorLocator                           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fig_channel as FC                                                 # noqa: E402

OUT = os.path.join(HERE, "..", "figures", "device_cross_section.png")
PROV = ("cross-sections re-drawn from the DEVICES['psr_rotator'] geometry "
        "(not a solver export)")

T_PES, T_SI = 0.090, 0.220            # partial-etch slab and Si thickness (µm)
W_PES = 1.550                         # slab width (µm)
GAP = 0.200                           # edge-to-edge gap between the two arms (µm)
W2 = 0.550                            # rib width at x = 50 µm (mid-taper)
W5, W6 = 0.650, 0.500                 # coupler arms (µm)

SI = "#b5432a"                        # silicon
PES = "#f3c9a8"                       # partial-etch slab
PORT = "#e8862f"                      # port arrows (same language as the reference figure)

PANELS = (
    ("x = 50 µm (mid-taper)", [(0.0, W2)]),
    ("x = 405 µm (coupler end)", [(+(GAP + W5) / 2, W5), (-(GAP + W6) / 2, W6)]),
)

fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.4), dpi=200)
for ax, (title, ribs) in zip(axs, PANELS):
    ax.add_patch(Rectangle((-W_PES / 2, 0.0), W_PES, T_PES, fc=PES, ec="#8a6a4a",
                           lw=0.6, zorder=2))
    for yc, w in ribs:
        ax.add_patch(Rectangle((yc - w / 2, T_PES), w, T_SI, fc=SI, ec="#7a2f1c",
                               lw=0.7, zorder=3))
        # 端口不画三角形：横截面看不出传播方向，图上只留几何（端口在图注里用文字说明）
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-0.18, 0.68)
    ax.set_xlabel("y (µm)", fontsize=10)
    ax.set_ylabel("z (µm)", fontsize=10)
    ax.set_title(title, fontsize=11)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(which="both", direction="out", top=False, right=False)
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", metadata={FC.CHUNK: FC.statement("external", PROV)})
plt.close(fig)
print("wrote:", OUT, os.path.getsize(OUT), "bytes")
