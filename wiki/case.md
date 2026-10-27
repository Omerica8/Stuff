<!-- sources: mixer/case/ -->
# Case

The case thread owns `mixer/case/`. Read [PANEL.md](../mixer/case/PANEL.md) (files, paper fit check, to-verify list), [HEIGHTS.md](../mixer/case/HEIGHTS.md) and [STATUS.md](../mixer/case/STATUS.md) for the numbers; this page is only a summary.

- **Size:** 407 × 353 mm. The tray prints in 4 quarters (203.5 × 176.5); the left armrest (254 × 31) goes diagonally on the Ender 3 bed.
- **Top:** stepped. 2 mm aluminium control plate (`out/plate.dxf`), underside 10.5 mm above the strip PCBs, plus a raised 1.5 mm aluminium jack shelf (`out/shelf.dxf`), underside 24 mm up. No PCB changes needed.
- **Generated:** `case/gen/panels.py` places every cut-out from the KiCad footprints and checks ≥1.5 mm of metal between cuts. `case/gen/case.py` (build123d via uv, not OpenSCAD) makes the STLs.
- **Risers:** printed, hung from the shelf on bosses between the jacks, and placed from the KiCad Fab extents (the old HEIGHTS numbers for the NJ3/NJ5 jacks were short).
- **Holding the plate:** M3 standoffs from the board H1/H2 holes (10.5 mm audio, 7.5 mm controller), plus the pot nuts, 3 posts in the right region and the armrest lip.
- **Display:** the 2.8" TFT hangs under the shelf over the digital board, cabled to controller J4.
- **Under the plate:** PVA2 H1 switches in rectangular cut-outs (mono PAD/48V share one notch), 4 mm fader spacers, LEDs raised 7.2 mm, 7 mm low-profile or laid-flat electrolytics, ESP32 soldered without sockets under a printed lid.
- **Feet:** printed rear wedges for about 10°, rubber feet at the front.
- **Next:** Omer prints `out/panels_1to1_letter.pdf` at 100% and checks it against the real parts. Then aluminium order (DXF) and printing.
