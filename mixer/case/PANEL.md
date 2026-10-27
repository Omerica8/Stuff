# Top panels and printed case

*2026-10-27. Option 2 (stepped top), now **3D-printed instead of aluminium** (Omer's choice, saves about $105). Everything is generated from the KiCad boards, so a board change only needs a re-run.*

## Files

| File | What it is |
|---|---|
| `stl/top_plate_*.stl` (5) | Printed control plate tiles: `rear_left`, `front_left`, `rear_master`, `front_master`, `right` |
| `stl/top_shelf_*.stl` (3) | Printed jack shelf tiles: `left`, `middle`, `right` |
| `stl/tray_*`, `riser_*`, `armrest_*`, `esp32_lid`, `rear_foot_x2` | Printed case (see below) |
| `out/panels_1to1_letter.pdf` | **1:1 paper print for the fit check**, US Letter tiles. Dashed lines are the glued joints between printed tiles |
| `out/panels_overview.pdf` | Both pieces with labels, one page each |
| `out/plate.dxf`, `out/shelf.dxf` | 2D outlines and holes (layers `OUTLINE`, `CUT`, `LABELS`). Kept for reference, or for laser-cut acrylic or aluminium later |
| `out/render_hero.png`, `out/render_top.png`, `out/mixer_assembled.blend` | Render of the assembled mixer |
| `out/render_boards_hero.png`, `out/render_boards_top.png`, `out/mixer_boards.blend` | The boards only, as they sit inside: KiCad 3D models, ribbon cables, ESP32, FV-1 module, display |
| `glb/*.glb` | Each board with its 3D models (`kicad-cli pcb export glb`), used by the boards render |
| `gen/` | `dump_boards.py` (KiCad python), `panels.py` (outlines, holes, tiles, PDFs, self-check), `printed_top.py` (top STLs), `case.py` (case STLs), `render_blender.py`, `render.py` (quick pyvista preview) |

Re-run from `case/gen`:
```
"C:\Program Files\KiCad\10.0\bin\python.exe" dump_boards.py C:\Users\pogam\kicad-mcp\kicad-sandbox boards.json
uv run --no-project --with ezdxf --with reportlab --with shapely python panels.py
uv run --no-project --with build123d --with matplotlib python case.py
uv run --no-project --with build123d --with shapely python printed_top.py
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P render_blender.py            (CASE=0 for the boards-only render)
```
`panels.py` checks that there's at least 1.5 mm of material between holes and to every edge, and that no hole is within lap + 1.5 mm of a tile joint. It also checks that every tile fits a 215 mm square. The one allowed exception is Neutrik's own D cut-out (1.3 mm between the Ø22.2 hole and its screw holes).

## Printed top: what changed from aluminium

| | Aluminium plan | Printed |
|---|---|---|
| Control plate | 2.0 mm | **2.5 mm**, underside unchanged (10.5 mm above the strip PCBs, 7.5 above the controller) |
| Pot / encoder nut seat | 2.0 mm panel, 2.5 mm thread above it | **Ø13 × 1.0 mm recess** from the top, so the web is 1.5 mm and **3.0 mm of M7 thread** is left for the 2 mm nut. That's more than a flat 2 mm plate gives |
| 3.5 mm jacks | Ø8.0, washer | Ø8.0 plus a Ø11 × 1.0 recess: 2.6 mm of M6 thread for the nut |
| Fader spacers | loose 4 mm spacers | **Printed bosses** (Ø6) under the plate: 4 mm for the 60 mm PTA faders, 1 mm for the controller faders. M2 × 8 screws go straight into the fader housings |
| 3 mm LEDs | 7.2 mm spacer | **7.7 mm** spacer (the plate top is 0.5 mm higher), or leave them 0.5 mm below the surface |
| Jack shelf | 1.5 mm | **3 mm**, underside unchanged (24.0 mm above the PCB) |
| NJ3FD-V / NJ5FD-V (1/4") | needs a 1.2–1.5 mm panel | **Ø18 × 1.5 mm recess** from the top around each one, leaving a 1.5 mm web for the quick-fix cap. On the master's 19.5 mm jack pitch, Ø18 leaves 1.5 mm between recesses |
| NCJ6FA-V combo | ≤ 3 mm panel | 3 mm, fine |
| NC3MAAV XLR (master) | 2.7 mm loose spacer | **Printed 24 × 24 × 2.7 mm pad** under the shelf. The nose ends at the shelf's underside, recessed 3 mm, and the plug's sleeve still mates |

**Tiles and joints.** The plate splits into 5 tiles and the shelf into 3. All are ≤ 195 mm, so they fit the Ender 3. Neighbouring tiles overlap in a half-lap joint, 3.5 mm either side of the dashed line and half the thickness each, for gluing (CA or epoxy). The joint lines run through hole-free bands: the mono strips at y 142, the stereo strips at y 193 (with a step between them), the master at y 226, the columns at x 191.5 and 253, and the shelf at x 190 and 254. Every tile is also screwed down through the board standoffs, so joints only have to stay flush.

**Printing.** Print each top tile **face down** on the bed for a smooth surface. The nut recesses then face the bed with no overhang, and the fader bosses and XLR pads point up. PETG or PLA, 4 walls, 30 % infill. The STLs are in assembly position, so flip them in the slicer.

**Labels.** These aren't printed into the part, because 2.4 mm text doesn't come out cleanly on a 0.4 mm nozzle. Use the `LABELS` layer as a sticker sheet, or a paint pen.

## Paper fit check (before printing the top)

1. Print `panels_1to1_letter.pdf` at **100% / Actual size**. Measure the 100 mm bar on one page.
2. Trim each tile on the dashed frame. Overlap it 10 mm on its neighbour (solid guide line on the next tile's edge) and tape it.
3. Lay the strip, stereo and master boards side by side at a 31 mm pitch. Put the plate print on top with its holes over the pot shafts.
4. Check that every shaft, switch, jack, LED and fader slot lands in its hole, including the controller's generic encoders and 45 mm faders. On the shelf print, check the jack noses and screw holes, and the display window against your real 2.8" TFT.
5. Mark anything that's off and tell me the offset in mm. I fix the generator, not the files.

## Sizes that come from datasheets (to verify)

| Part | Hole used | Source / what to check |
|---|---|---|
| Alpha RD901F / RD902F pots | Ø7.5 | M7 bushing. No hole for the anti-rotation tab: snip it off or ask for a Ø2.5 hole |
| Bourns PTA6043 / 6044 faders (60 mm) | slot 5 × 65, Ø2.4 holes 71 mm apart | Bourns PTA datasheet, B = 71 |
| Controller "45 mm" slide pots (generic) | slot 5 × 35, holes 41 mm apart | Treated as a PTA3043 outline (45 mm body, 30 mm travel). **If yours have 45 mm of travel, the controller footprint is wrong too** |
| EC11 encoder (generic) | Ø7.5 | Alps EC11E |
| C&K PVA2 H1 | body + 0.5 mm | Mono PAD and 48V share one opening that runs into the plate's rear edge |
| QingPu WQP419GR 3.5 mm | Ø8.0 | Plate rests on the jack body |
| 3 / 5 mm LEDs, tact, 7 × 7 latch | Ø3.2 / Ø5.1 / Ø4.5 / Ø5.0 | |
| Neutrik NCJ6FA-V / NC3MAAV | Ø22.2 + 2 × Ø3.2 on the diagonal (±9.9) | Neutrik drawings |
| Neutrik NJ3FD-V / NJ5FD-V | Ø12.2, Ø18 recess | Check the quick-fix cap fits inside Ø18 |
| 2.8" SPI TFT (ILI9341, generic) | window 60 × 45, 4 × Ø3.2 at 80 × 44 | **Measure your display** |
| Rear wall: MIDI DIN, USB-B, USB-C, DC jack | from datasheet heights | Printed wall: file to fit |

## Layout notes (changes from STATUS.md)

1. **Riser positions:** the KiCad Fab layer put the stereo NJ5 and master NJ3 jacks deeper than HEIGHTS.md said. New riser faces (case y, rear/front): mono 33.9/35.5, stereo 39.4/41.4, master left 69.5/71.5, master right 51.9/53.9, right region 178/180.
2. **The risers hang from the shelf**, screwed up into it through bosses between the jacks.
3. **How the plate is held:** M3 F-F standoffs from each audio board's H1/H2 (10.5 mm) and from controller H1/H2 (7.5 mm), plus the pot and jack nuts, 3 posts in the right region (x 262, 300 and 402.5 at y 185), and the armrest's lip.
4. **Display** under the shelf over the digital board, on a cable to controller J4. **Reverb carrier** at x 320–394, y 177–227.

## Printed case parts

`tray_*` ×4 (posts with M3 heat-set inserts, shelf bosses, rear openings, vents, seam ribs with M3 bolts across), `riser_left/middle/right`, `armrest_left` (254 × 31, goes diagonally on the bed) and `armrest_right`, `esp32_lid`, `rear_foot_x2` (≈10° tilt).

Hardware: about 30 M3 heat-set inserts, M3 × 8 cap screws, M3 × 10 countersunk screws for the shelf, 10.5 mm and 7.5 mm M3 F-F standoffs, M2 × 8 screws for the faders, M3 nuts and bolts for the seams, CA glue or epoxy for the top joints.
