# Figures — what each one is, and what it is NOT

The rule applied here: **a figure's evidence grade depends on who drew it.** A solver's own
structure view / field / data export is solver evidence; a matplotlib figure is a human
re-projection and is *not* equivalent. Every matplotlib figure therefore has to say so, **on the
figure** and in its PNG metadata.

| figure | what it is | channel | channel label present? |
|---|---|---|---|
| `colsum_and_conversion_vs_modes.png` | matplotlib **re-plot of tabulated EME results** (column sums + conversion at 4 and 6 port modes) | `external` | ✅ yes — on-figure footer **and** PNG `tEXt` chunk `External-Plot` |
| `device_topview.png` | matplotlib **re-draw from the solver model** — two z-slices of the whole device (partial-etch slab layer and waveguide layer) | `external` | ⚠️ **no** — see "Known gap" below |
| `device_cross_section.png` | matplotlib **re-draw from the solver model** — cross-section at the adiabatic coupler | `external` | ⚠️ **no** — see "Known gap" below |

**None of these three is a solver export.** Do not quote any of them as "the solver's own view".
For the two referenceable numbers (`98.35%`, `99.233%`), cite §3 and §6 of the README — never a figure.

## Known gap (stated rather than hidden)

The two device figures were produced before the channel-labelling convention was wired into the
generator that draws them, so they carry the matplotlib software tag but **not** the channel label.
They are kept because they show the actual two-layer structure, which the schematic generator does
not.

What is in place now:

- `tools/make_structure_fig.py` **labels every figure it writes** (on-figure footer + PNG `tEXt`
  chunk) if `fig_channel` is importable — and falls back to a plain save if it is not, so it never
  breaks;
- so **any structure figure you regenerate carries its channel label**:

  ```bash
  python tools/make_structure_fig.py --list
  python tools/make_structure_fig.py --device psr_rotator --out figures
  ```

  (Note: the regenerated top view is a **schematic** — x compressed, no layer split — so it is not a
  drop-in replacement for the two z-slice figures above.)

- Removing or relabelling those two figures is a one-line decision for the repository owner; it is
  left open rather than silently done, because relabelling would mean re-drawing them and the
  original drawing script is not part of this repository.

## One inconsistency to be aware of

`device_topview.png` states a **total length of ≈ 523 µm** in its own title, while the sum of the
segment lengths in the README is **≈ 537.8 µm**. The two numbers come from the same work at
different times; **this repository does not resolve the discrepancy.** Use the segment lengths
(they appear individually in §2 and in the scripts) and re-derive the total if you need it.

## Verify the labels yourself

```bash
# fig_index depends on fig_channel, so put both on PYTHONPATH
PYTHONPATH=tools python /path/to/fig_index.py --figs figures --index figs_index.json
```

`fig_index` reports each figure's channel, bytes, pixels and md5, and flags any `external`-channel
figure whose label chunk is missing. With the current contents it will flag exactly the two figures
listed in "Known gap" — which is the honest state of this repository.
