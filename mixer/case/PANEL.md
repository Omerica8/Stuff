# Panels and printed case

*2026-10-27. Option 2 (stepped top). Everything is generated from the KiCad boards, so a board change only needs a re-run.*

## Files

| File | What it is |
|---|---|
| `out/plate.dxf` | 2.0 mm aluminium control plate. Layers: `OUTLINE`, `CUT` (send these two to the cutter), `LABELS` (for a printed overlay, not cut) |
| `out/shelf.dxf` | 1.5 mm aluminium raised jack shelf, same layers |
| `out/panels_overview.pdf` | Both pieces on one page each, with labels |
| `out/panels_1to1_letter.pdf` | **1:1 paper print for the fit check**, US Letter tiles (6 plate + 3 shelf) |
| `out/case_preview.png` | Render of the printed parts with the two aluminium pieces |
| `stl/*.stl` | Printed parts (sizes in `stl/sizes.json`; all fit the Ender 3 bed, the left armrest goes on the diagonal) |
| `gen/` | `dump_boards.py` (KiCad python, writes `boards.json`), `panels.py` (DXF + PDFs, self-check), `case.py` (STLs), `render.py` |

Re-run from `case/gen`:
```
"C:\Program Files\KiCad\10.0\bin\python.exe" dump_boards.py C:\Users\pogam\kicad-mcp\kicad-sandbox boards.json
uv run --no-project --with ezdxf --with reportlab --with shapely python panels.py
uv run --no-project --with build123d --with matplotlib python case.py
uv run --no-project --with pyvista --with ezdxf python render.py
```
`panels.py` checks that every cut has at least 1.5 mm of metal to its neighbours and to the edge (`MIN_WEB=2` for a stricter cutter). The one allowed exception is Neutrik's own D cut-out, which leaves 1.3 mm between the Ø22.2 hole and its screw holes.

## Paper fit check (do this before ordering aluminium)

1. Print `panels_1to1_letter.pdf` at **100% / Actual size**. Measure the 100 mm bar on one page. If it's off, fix the printer scaling first.
2. Trim each tile on the dashed line. Overlap it 10 mm on its neighbour, line the solid guide line up with the next tile's edge, and tape it.
3. Lay the strip, stereo and master boards side by side at a 31 mm pitch (1 mm gaps). Put the plate print on top so its holes line up with the pot shafts.
4. Check with real parts:
   - Pot shafts, the PVA2 switch bodies, the 3.5 mm jacks and the LEDs land in their holes.
   - Fader levers run the full length of their slots, and the M2 holes sit over the fader's threaded holes.
   - The controller's EC11 shafts, tact buttons, LEDs and 45 mm faders land in theirs. These are generic parts, so check them closely.
   - The shelf print: the XLR combo, XLR and 1/4" jack noses land in their holes, and the screw holes line up with the jack flanges.
   - The TFT window and its 4 holes, against your real 2.8" display.
5. Mark anything that's off on the paper, and tell me the offset in mm. I'll change the generator, not the DXF.

## Sizes that come from datasheets (to verify)

| Part | Cut-out used | Source, what to check |
|---|---|---|
| Alpha RD901F / RD902F pots | Ø7.5 | M7 bushing (Alpha drawing). No hole for the anti-rotation tab: snip the tab off or tell me to add a Ø2.5 hole |
| Bourns PTA6043 / PTA6044 faders (60 mm) | slot 5 × 65, 2 × Ø2.4 holes 71 mm apart | Bourns PTA datasheet, B = 71 for PTA6043. Check one real fader |
| Controller "45 mm" slide pots (generic) | slot 5 × 35, 2 × Ø2.4 holes 41 mm apart | Treated as a PTA3043 outline (45 mm body, 30 mm travel), the same as the controller footprint. **If yours really have 45 mm of travel (a 60 mm body), the controller footprint is wrong too** |
| EC11 encoder (generic) | Ø7.5 | Alps EC11E: M7 bushing. No tab hole |
| C&K PVA2 H1 | body + 0.5 mm (≈9.8 × 10.4) | C&K drawing. On the mono strips, the PAD and 48V switches share one 20 × 10.4 opening that runs into the plate's rear edge, under the riser |
| QingPu WQP419GR 3.5 mm | Ø8.0 | Plate rests on the jack body. Use an M6 washer under the nut |
| 3 mm / 5 mm LEDs | Ø3.2 / Ø5.1 | |
| 6 mm tact | Ø4.5 | |
| 7 × 7 latching switch | Ø5.0 | |
| Neutrik NCJ6FA-V / NC3MAAV | Ø22.2 + 2 × Ø3.2 on the diagonal (±9.9, ±9.9) | Neutrik drawings / KiCad Fab layer |
| Neutrik NJ3FD-V / NJ5FD-V | Ø12.2 | Shelf must be 1.2–1.5 mm for the quick-fix cap |
| 2.8" SPI TFT (ILI9341, generic) | window 60 × 45, 4 × Ø3.2 at 80 × 44 | **Generic module numbers. Measure your display before ordering the shelf** |
| Rear wall: MIDI DIN, USB-B, USB-C, DC jack | rectangles from datasheet heights, Ø8.2 DC jack | CUI SDS-50J, OST USB-B1HS, GCT USB4125, generic M8 panel jack. The wall is printed, so file to fit |

## Changes from STATUS.md

1. **Riser positions changed.** HEIGHTS.md had the stereo NJ5 jacks ending at PCB y 58.3 and the master NJ3 jacks at 70.8. The KiCad Fab layer says 64.1 (stereo J9) and 76.6 (master J7–J9), so the old risers would have sat on the jacks. New riser faces (case y, rear/front): mono 33.9/35.5, stereo 39.4/41.4, master left 69.5/71.5, master right 51.9/53.9, right region 178/180. Jogs are at x 129.5, 191.5, 223 and 253, all clear of parts.
2. **The risers hang from the shelf.** They're screwed up into the shelf through small bosses in the gaps between the jacks, and the plate's rear edge butts against their front face. They can't stand on the plate, because on the mono strips the PVA2 switches start right behind the combo jacks.
3. **How the plate is held:** M3 female-female standoffs, 10.5 mm, from each audio board's H1/H2 holes up to the plate, plus the pot and jack nuts, the way commercial mixers do it. Also 3 posts in the right region, and the armrest's lip over the plate's front edge. On the controller: H1/H2 with 7.5 mm standoffs.
4. **The display goes under the shelf**, over the digital board, as a raised meter-bridge screen. It runs on a ~200 mm cable from the controller's J4.
5. **Reverb carrier position:** x 320–394, y 177–227, on 5 mm posts under the plate's right region.
6. **Controller fader screws are 41 mm apart** (PTA3043 outline). STATUS.md's "B = 41 (45 mm)" was right for the controller footprint, but note the row above.

## Printed parts

- `tray_*` ×4: floor, walls, all board posts (Ø7, M3 heat-set inserts), plate posts, shelf bosses, rear openings, vents under the power heatsinks. 4 mm seam ribs with M3 bolts across join the quarters.
- `riser_left/middle/right`: the stepped wall under the shelf's front edge.
- `armrest_left` (254 × 31, diagonal on the bed) and `armrest_right`: covers the ribbon plugs. Its 5 mm lip clamps the plate's front edge. M3 cap screws go into inserts in the front-wall bosses.
- `esp32_lid`: plugs the ESP32 window, so the BOOT/RESET buttons stay reachable.
- `rear_foot_x2`: wedges for a ≈10° tilt with 8 mm rubber feet at the front. Glue or VHB them on.

Hardware: M3 heat-set inserts (~30), M3 × 8 cap screws, M3 × 10 countersunk screws (shelf), 10.5 mm and 7.5 mm M3 F-F standoffs, M2 × 8 screws plus 4 mm spacers for the faders, M3 nuts and bolts for the seams.
