# Case (steps B and C): status

*2026-10-27. This work moved to a new thread before any drawing or CAD file was made. Below are the decisions and the numbers I had worked out, so the next session can start drawing straight away.*

## Done
- Step A: HEIGHTS.md (part heights, the jack/pot conflict, options 1 and 2).
- Omer picked **option 2**: a stepped top (2 mm control plate, underside 10.5 mm above the strip PCBs, plus a raised 1.5 mm jack shelf, underside 24.0 mm up), **PVA2 H1** switches, 4 mm fader spacers, LEDs raised 7.2 mm, ESP32/TFT soldered without sockets.
- Step D (reverb carrier) is done: phase5_reverb/.

## Not started
- B: control plate DXF, jack shelf DXF, rear panel DXF, labelled PDF, 1:1 tiled PDF for the paper fit test.
- C: OpenSCAD case, STLs, renders. **OpenSCAD isn't installed on Omer's PC.** Install it from openscad.org, or ask Omer first.

## New findings since HEIGHTS.md (fold these in)
1. **PVA2 H1 body is 11.0 mm tall** (9.2 × 9.8 mm body, 3.3 mm square plunger, C&K drawing). That's above the 10.5 mm plate underside, so each switch needs a **rectangular cut-out ≈ 9.8 × 10.4 mm**. The body top then sits 0.5 mm inside the plate, and a PVA button (PE/PV, ordered separately) goes on the plunger. HEIGHTS.md's "anything below ≈19" for the PVA2 is wrong.
2. **Electrolytic caps under the plate are 11–12 mm tall** and would hit the plate at 10.5. Affected: strip C3, C4, C12, C13, C14, C17, C18, C5; stereo C19, C20; master C6, C8, C10, C12, C16, C18, C19, C21, C22, C32, C34. Fix without PCB changes: buy **7 mm low-profile** types where they exist (5×7, 6.3×7). Otherwise bend the cap over flat. The 47 µF 63 V 8 mm parts (strip C3, C4, C14) probably need laying over.
3. **Ribbon headers J2–J4 (and master J5)** are at local y ≈ 325, on every board's front end. Header plus plug plus cable is about 13 mm tall, which is too tall for the plate. Plan: the **control plate stops at local y 322** (all fader screw holes are at ≤ 317) and a **printed front armrest** covers y 327–350, underside ≥ 37 mm above the floor (see the Z table), top about 40.
4. **Power board heatsinks (Fischer SK104, 35 mm)** set the internal height. They have to sit under the raised rear shelf, so the strip PCBs ride on **18 mm posts** (Z table below).
5. **Controller (generic parts, from datasheets):**
   - EC11: Alps EC11E drawing gives the mounting face 4.5 mm above the PCB, M7 bushing 7 mm, shaft 20 mm above the face. Generic clones may be up to 6.5 mm.
   - 45 mm faders: PTA3043 outline, assumed to match the Bourns PTA (housing 6.5, lever top 21.5).
   - Omer's tact buttons are 16 mm tall. 5 mm LEDs are 8.6 mm.
   - ESP32-S3 devkit soldered straight on is ≈7.4 mm tall.
   - So the **controller PCB sits 7.5 mm below the plate underside**. That leaves an exact nut fit on a 4.5 mm EC11 face (more on 6.5), 1.0 mm fader spacers, LEDs 1.1 mm into a Ø5.1 hole, tact buttons 6.5 mm proud. Cut a **window ≈ 30 × 70 mm over the ESP32** (it's only 0.1 mm under the plate, and the BOOT/RESET buttons become reachable) with a printed lid. The ESP32's USB-C points to the board's front edge, so the cable runs under the armrest.
   - All controller values come from generic parts. **The check is the 1:1 paper fit test:** print the plate 1:1, lay it on the real boards, and push the real parts through.
6. 3.5 mm jacks (Thonkiconn PJ366ST / WQP419GR): body 10.4 → panel hole **Ø8.0** (the panel sits around the collar). PTA lever top 21.5 (from the DP lever drawing, L = 15 above the 6.5 housing).

## Layout I'd worked out (case coordinates in mm: x from the left outer face, y from the rear outer face, z from the bottom)
- Walls 3 mm. Boards at a 31 mm pitch, rear edges at y = 5:
  - mono strips: x = 6, 37, 68, 99
  - stereo strips: x = 130, 161
  - master: x = 192 (to 252)
  - controller: x 256–401, **y 230–330** (moved back so its faders end before the armrest)
- Case outside: **407 × 353**. The tray is split 2 × 2 so every part is ≤ 204 × 177 for the Ender 3, joined with M3 + heat-set inserts.
- **Z table:**

  | Item | z (mm) |
  |---|---|
  | Floor | 0–3 |
  | Strip / stereo / master PCB top (18 mm posts) | 22.6 |
  | Control plate | 33.1–35.1 |
  | Jack shelf | 46.6–48.1 |
  | Controller PCB top | 25.6 (plate − 7.5) |
  | Digital board on 6 mm posts | PCB top 10.6 |
  | Power board on 5 mm posts | PCB top 9.6 (heatsink top ≈ 44.6, under the shelf) |
  | Reverb carrier on 5 mm posts | top ≈ 23.6 (fits under the plate) |
  | Front armrest | ≈ 37–40 |

- **Riser walls** (printed, z 35.1 → 46.6, 2 mm thick, along the shelf's front edge):
  - mono + stereo: y 34–36
  - master, left part (x 192–223): y 64–66
  - master, right part (x 223–252): y 47–49. This keeps clear of the J11 3.5 mm hole and the NJ3 squares.
  - right region (x 253–404): y 178–180
  - jogs at x ≈ 191.5 and ≈ 253 (both checked clear of parts)
- **Under the rear shelf, right region:**
  - digital board: y 5–80, x ≈ 278–378, connectors through the rear wall
  - power board: y 88–173, fed from a panel-mount 2.1 mm DC jack on the rear wall with a short plug pigtail into its barrel jack
  - reverb carrier: under the plate, y ≈ 180–230
- **Cut-out sizes:**

  | Part | Cut-out |
  |---|---|
  | Pots | Ø7.5 |
  | Faders | slot 5 wide × (travel + 5), plus 2 × Ø2.4 at B = 71 (60 mm) / 41 (45 mm). Centre = midpoint of the footprint's two Fab circles (PTA6043, controller) or the Fab box centre (PTA6044 custom) |
  | 3 mm LEDs | Ø3.2 |
  | 5 mm LEDs | Ø5.1 |
  | PVA2 | ≈ 9.8 × 10.4 |
  | 3.5 mm jacks | Ø8.0 |
  | EC11 | Ø7.5 |
  | Tact | Ø4.5 |
  | 7×7 latch | Ø5.0 |
  | NJ3/NJ5 (shelf) | Ø12.2 |
  | NCJ6FA-V / NC3MAAV (shelf) | Ø22.2 + 2 × Ø3.2 at (−9.9, −9.9) and (+9.9, +9.9) from the centre, as seen from above (KiCad Fab layer) |

  Where each centre sits relative to its footprint origin (from the Fab layer, already rotated):
  - pots: the Fab circle
  - NJ3/NJ5: (0, 5.72)
  - WQP419GR: (0, 6.48)
  - NCJ6: (−7.62, 0)
  - NC3MAAV: (3.81, 0)
  - EC11: (7.5, 2.5)
  - tact: (3.25, 2.25)
  - LEDs: (1.27, 0)

  The scratch script that prints these is fab.py, described in the next section.
- **Labels:** take them from each footprint's Value with the taper prefix dropped (C10K/B10K/A10K, "(dual)"). They go on a separate non-cut DXF layer, for a printed overlay.

## Next steps
1. Fold findings 1–6 into HEIGHTS.md. Write the panel generator (Python + ezdxf via `uv run --with ezdxf`) that reads the KiCad boards and places every cut-out from the footprints. Output the plate, shelf and rear wall DXFs, a labelled PDF and a 1:1 tiled PDF.
2. OpenSCAD case from the same numbers: tray quarters, risers, armrest, wedge feet (~10°), ESP32 lid, posts with heat-set inserts. Then STLs and renders.

Scratch scripts on Omer's PC (not in the repo): C:\Users\pogam\AppData\Local\Temp\fab.py prints Fab-layer centres per footprint; pos.py prints board edges and part positions.
