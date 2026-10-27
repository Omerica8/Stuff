<!-- sources: mixer/case/ -->
# Case

The case thread owns `mixer/case/`. Read [PANEL.md](../mixer/case/PANEL.md) (files, paper fit check, to-verify list), [HEIGHTS.md](../mixer/case/HEIGHTS.md) and [STATUS.md](../mixer/case/STATUS.md) for the numbers; this page is only a summary.

- **Size:** 407 × 353 mm, kept after the cut to 2 mic strips so the MIDI hub fits along the back wall. The digital board's ports moved to the right wall (layout option 1, Omer's pick; board positions in `case/gen/layout.py`). The tray prints in 4 quarters (203.5 × 176.5); the left armrest (254 × 31) goes diagonally on the Ender 3 bed.
- **Top:** stepped and **3D-printed** (was aluminium). 2.5 mm control plate, underside 10.5 mm above the strip PCBs, with Ø13 nut recesses (3 mm of pot thread). A raised 3 mm jack shelf, underside 24 mm up, with Ø18 × 1.5 mm recesses so the NJ3/NJ5 caps get their 1.5 mm panel. 5 plate tiles and 3 shelf tiles joined by glued half-lap joints. Draft: printing is on hold, at Omer's request. No PCB changes needed.
- **Generated:** `case/gen/panels.py` places every cut-out from the KiCad footprints and checks ≥1.5 mm of material between cuts and around the tile joints. `printed_top.py` and `case.py` (build123d via uv, not OpenSCAD) make the STLs. `render_blender.py` renders the assembled mixer, or with CASE=0 just the boards with their KiCad 3D models.
- **Risers:** printed, hung from the shelf on bosses between the jacks, and placed from the KiCad Fab extents (the old HEIGHTS numbers for the NJ3/NJ5 jacks were short).
- **Holding the plate:** M3 standoffs from the board H1/H2 holes (10.5 mm audio, 7.5 mm controller), plus the pot nuts, 3 posts in the right region and the armrest lip.
- **Display:** the 2.8" TFT hangs under the shelf over the digital board, cabled to controller J4.
- **Under the plate:** PVA2 H1 switches in rectangular cut-outs (mono PAD/48V share one notch), 4 mm fader spacers, LEDs raised 7.2 mm, 7 mm low-profile or laid-flat electrolytics, ESP32 soldered without sockets under a printed lid.
- **Feet:** printed rear wedges for about 10°, rubber feet at the front.
- **Next:** on hold. When printing resumes: the 1:1 paper check (`out/panels_1to1_letter.pdf`), then print the tiles face down.
