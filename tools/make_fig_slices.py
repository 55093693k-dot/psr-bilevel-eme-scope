# make_fig_slices.py -- Fig. 1 and Fig. 2 of the manuscript: the two z-slices of the device, drawn
# as **plane plots in the solver's own style** (what the author asked for on 2026-09-28): µm axes
# with ticks, a hatched PML band at the top and bottom of the domain, port bars and arrows, and a
# one-line title.
#
# Geometry: DEVICES["psr_rotator"] of make_structure_fig.py -- input taper L_t = 30 µm
# (w_1 0.45 -> w_pes 1.55 µm), bi-level taper L_blt = 100 µm (rib w_2 0.55 -> w_3 0.85 µm on a
# 1.55 µm partial-etch slab), straight L_s = 5 µm, adiabatic coupler L_ac = 300 µm (two arms,
# R = 300 µm bend over 6 deg, widths -> w_5 0.65 / w_6 0.50 µm, edge-to-edge gap 0.2 µm).
# Domain x = 0...500 µm, y = +-6 µm (the solver domain half-width).  Device length 435 µm;
# ports marked at x = 0 (in) and x = 435 (out).
#
# Assumptions (no solver export of this view exists): the arm separation follows a smooth 6 deg
# arc; the rib starts at the beginning of the bi-level taper and widens linearly to w_2 at
# x = 50 µm and to w_3 at its end.  Same statements as the manuscript caption -- no dimension
# text on the figure.
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                          # noqa: E402
from matplotlib.patches import Polygon, Rectangle                        # noqa: E402
from matplotlib.ticker import AutoMinorLocator, MultipleLocator          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fig_channel as FC                                                 # noqa: E402

FIGDIR = os.path.join(HERE, "..", "..", "05_首篇_BilevelPSR与EME边界", "figures")
PROV = "plane plots re-drawn from the DEVICES['psr_rotator'] geometry (not a solver export)"

RATIO = 1.4                          # canvas proportion, as in the reference plane plot
L_DEV = 435.0                        # 30 + 100 + 5 + 300
XMAX, YMAX, PML = 500.0, 6.0, 0.5

CLAD = "#f6cf85"                     # cladding / background
SI = "#a3a05e"                       # Si (the reference's olive family)
PORT = "#e8862f"                     # port bars
PMLC = "#9a9a8f"
XS = [i * 2.5 for i in range(int(L_DEV / 2.5) + 1)] + [L_DEV]


def prog(x):
    return min(max((x - 130.0) / (L_DEV - 130.0), 0.0), 1.0)


def centre(x):
    """|y| of each arm centre: 0.525 µm out of the bi-level taper, + 1.65 µm over a 6 deg arc."""
    return 0.525 + 1.65 * prog(x)


def width(x, end):
    return 0.85 + (end - 0.85) * prog(x)


def ribw(x):
    if x <= 30.0:
        return 0.0
    if x <= 50.0:
        return 0.55 * (x - 30.0) / 20.0
    return 0.55 + 0.30 * (x - 50.0) / 80.0


def half(x):
    if x <= 30.0:
        return 0.225 + 0.550 * x / 30.0
    if x <= 130.0:
        return 0.775
    return max(centre(x) + width(x, 0.65) / 2, centre(x) + width(x, 0.50) / 2)


def edge(x, sgn, end, use_rib):
    w = (ribw(x) if (use_rib and x <= 130.0) else width(x, end))
    return sgn * centre(x) + w / 2


def draw(ax, layer):
    """layer='slab' -> the partial-etch plate (Fig. 1); layer='rib' -> the two ribs (Fig. 2)."""
    ax.set_facecolor(CLAD)
    for sgn in (+1, -1):                                         # PML bands
        ax.add_patch(Rectangle((0, sgn * (YMAX - PML)), XMAX, sgn * PML, fc=PMLC, ec="none",
                               hatch="xx", lw=0.0, alpha=0.55, zorder=1))
    if layer == "slab":                                          # partial-etch plate silhouette
        top = [(x, half(x)) for x in XS]
        bot = [(x, -half(x)) for x in reversed(XS)]
        ax.add_patch(Polygon(top + bot, closed=True, fc=SI, ec="#8d8a4f", lw=0.6, zorder=3))
    for sgn, end in ((+1, 0.65), (-1, 0.50)):                    # the two waveguides / ribs
        xs = [x for x in XS if x >= 30.0]
        up = [(x, edge(x, sgn, end, True)) for x in xs]
        dn = [(x, edge(x, sgn, end, True) - (ribw(x) if x <= 130.0 else width(x, end)))
              for x in reversed(xs)]
        ax.add_patch(Polygon(up + dn, closed=True,
                             fc=("#8f8c52" if layer == "slab" else SI),
                             ec="#7d7a45", lw=0.5, zorder=4))
    ax.add_patch(Rectangle((-3.0, -0.35), 6.0, 0.70, fc=PORT, ec="none", zorder=5))
    ax.plot([2, 14], [0, 0], color="#1a7f37", lw=1.2, zorder=6)
    ax.plot(16, 0, marker=">", ms=4, color="#1a7f37", zorder=6)
    for sgn, end in ((+1, 0.65), (-1, 0.50)):                    # output ports
        c = sgn * centre(L_DEV)
        ax.add_patch(Rectangle((L_DEV - 3.0, c - end / 2 - 0.25), 6.0, end + 0.5, fc=PORT,
                               ec="none", zorder=5))
        ax.plot([L_DEV - 16, L_DEV - 2], [c, c], color="#c0392b", lw=1.2, zorder=6)
        ax.plot(L_DEV - 19, c, marker=">", ms=4, color="#c0392b", zorder=6)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(-YMAX, YMAX)
    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.xaxis.set_minor_locator(MultipleLocator(20))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.tick_params(which="both", direction="out", top=False, right=False)
    ax.set_xlabel("x (µm)", fontsize=11)
    ax.set_ylabel("y (µm)", fontsize=11)


for layer, z, name in (("slab", "0.045", "device_topview_slab.png"),
                       ("rib", "0.200", "device_topview_waveguide.png")):
    fig, ax = plt.subplots(figsize=(6.6, 6.6 / RATIO), dpi=300)
    draw(ax, layer)
    ax.set_title("cross section at z = %s (µm)" % z, fontsize=12)
    fig.subplots_adjust(left=0.085, right=0.99, top=0.935, bottom=0.105)
    out = os.path.abspath(os.path.join(FIGDIR, name))
    fig.savefig(out, metadata={FC.CHUNK: FC.statement("external", PROV)})
    plt.close(fig)
    print("wrote:", out, os.path.getsize(out), "bytes")
