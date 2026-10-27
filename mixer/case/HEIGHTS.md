# Case step A: part heights and the panel-height conflict

All heights are measured from the **top of the PCB** (component side). "Panel underside" means where the bottom face of the top plate has to be for that part to mount correctly. The top plate is 2.0 mm aluminium unless noted otherwise.

Sources: Neutrik drawings NCJ6FA-V (20004523), NC3MAAV (ST-NC3MAAV), NJ3FD-V (3102 St 07 15), NJ5FD-V (3102 St 07 17), NCJ6FA-H, NC3MAAH; Alpha RD901F-40 drawing (SLH-211-208) and the RD90x series catalogue; Bourns PTA datasheet; C&K PVA V2 spec PS-PVA-346; QingPu/Thonk measurements for the WQP419GR / PJ366ST; KiCad models for the generic controller parts. No PCB was changed.

## 1. Heights of every panel part

| Part (boards, refs) | Seats / body top | Panel underside must be | Above that | Panel hole | Notes |
|---|---|---|---|---|---|
| **NCJ6FA-V** combo (strip J1) | flange face **24.0** | **24.0** | nose to 29.7 (5.7 through the panel) | Ø22 + 2×Ø3.2 | panel max 3 mm, rear-mounted, M3 A-screws |
| **NC3MAAV** XLR-M (master J1, J6) | flange face **21.3** | **21.3** | nose to 24.0 (2.7) | Ø22 + 2×Ø3.2 | 24.0 overall, 2.7 of it is the nose |
| **NJ3FD-V** 1/4" TRS (master J7–J10) | shoulder **24.0** | **24.0** | quick-fix cap/nut | ≥Ø12 | **panel must be 1.2–1.5 mm**, not 2 mm |
| **NJ5FD-V** 1/4" switched (stereo J8, J9) | shoulder **24.0** | **24.0** | quick-fix cap/nut | ≥Ø12 | **panel 1.2–1.5 mm** |
| WQP419GR / PJ366ST 3.5 mm (master J11, stereo J10) | body **10.4** | **10.4** (Ø7.8 hole, panel on body) or 11.4 (Ø6 hole, panel on collar) | M6 bushing to ≈14.6 | Ø7.8 or Ø6 | Thonk/QingPu figures; check one real part |
| **RD901F-40-15R1** 9 mm pot (strip ×7, stereo ×3, master ×2) | body face **10.0** | **10.0–10.5** | M7×0.75 bushing to 15.0; shaft to 25.0 | Ø7.5 | nut 2.0 mm thick: 2 mm panel at 10.5 leaves 2.5 mm thread |
| **RD902F-40-15R1** dual (stereo RV1/RV2, master RV3) | body face **10.0** | **10.0–10.5** | same as RD901F | Ø7.5 | same body height as the single |
| **PTA6043-2015DP** fader (strip RV6) | housing top **6.5** | **6.5 or higher on spacers** | lever top ≈21.5 (L = 15 above housing) | 60 mm travel slot + 2×M2 | M2 screws go into the housing top |
| **PTA6044-2015DP** dual fader (stereo RV4, master RV4) | housing top **6.5** | same | lever top ≈21.5 | as above | same heights as the single |
| **PVA2 EE H1** (strip SW1–3, master SW1) | body top **11.0** (9.2 × 9.8 mm); plunger (3.3 mm square) 17.54 at rest, 15.99 latched, 15.34 end stop | body pokes 0.5 mm into a 10.5 mm plate: **rectangular cut-out ≈9.8 × 10.4** | button cap (PE/PV) on the plunger | ≈9.8 × 10.4 | corrected 2026-10-27, see STATUS.md |
| 3 mm LED (master D1–D20, strip D5, stereo D1) | 5.3 (soldered flush) | — | — | Ø3.1 | lift on a spacer so the dome reaches the panel |
| **Controller** EC11 encoder, generic (ENC1–4) | mounting face ≈6.5–7 | ≈7 to ≈10 | M7 bushing ≈7 long, 20 mm shaft | Ø7.5 | generic part: **measure** |
| Controller 6 mm tact H13 (SW1–4) | plunger top 13.0 | — | — | cap hole | H17 version has the same footprint |
| Controller 45 mm slide pots, generic (RV1–4) | ? | ? | ? | slot | generic part: **measure** |
| Controller 5 mm LEDs (D1–D4) | 8.6 | — | — | Ø5.1 | lift on spacers |
| Controller ESP32-S3 devkit on 1×22 sockets (J1, J2) | ≈16 (socket 8.5 + header 2.5 + board 1.6 + USB-C 3.3) | must stay below the panel | — | none | the TFT on its 1×6 socket is about as tall |

The conflict: on the strip, the stereo strip and the master, the jacks need the panel **24.0 mm** above the PCB (21.3 for the XLR-M), but the pots need it at **10.0–10.5 mm**. That's a **13.5 mm** gap on the same PCB. Pot shafts and fader levers can't make up 13.5 mm: a fader lever ends at ≈21.5, under a 24 mm panel.

Every jack is at the rear end of its board (y = 30–95 mm on the 343 mm boards), which both fixes below rely on.

## 2. Common baseline for the control area

- Control plate: 2.0 mm aluminium, **underside 10.5 mm** above the PCB, top surface at 12.5.
  - Pots: 0.5 mm air under the panel, 2.5 mm of thread above it for the 2.0 mm nut, shaft 12.5 mm proud.
  - 3.5 mm jacks: Ø7.8 hole, 0.1 mm clearance over the body.
  - Faders: **4.0 mm spacers** between the housing top and the panel, M2×8 screws, lever 9.0 mm proud.
  - PVA2 H2: plunger 10.5 mm proud before the cap. **H1** would be 5.0 mm proud (same footprint, no PCB change); I suggest H1.
  - 3 mm LEDs: mount them **7.2 mm** off the board (7 mm LED spacer) so the dome sits flush with the panel top.
- Controller board: it has its own standoffs, so its panel height is set separately once the generic encoder and fader are measured. With the panel at ≈10.5, plug the ESP32 and TFT straight in on their male headers, without the socket strips (≈7.4 mm instead of ≈16 mm). That's an assembly change, not a PCB change.

## 3. Fix option 1: jacks on a rear panel, horizontal footprints

Swap to horizontal-PCB parts at the board's rear edge: NCJ6FA-H, NC3MAAH, and horizontal 1/4" TRS / switched TRS jacks.

Numbers:
- NCJ6FA-H: flange 25×25 mm, from 0 to 25.0 mm above the PCB (axis at 12.5); body 24.5 mm deep behind the panel. NC3MAAH: flange 25.3 mm tall, axis at 12.5; body 18.5 mm deep.
- With the top plate at 12.5 mm, a horizontal jack on the top side sticks **12.5 mm above the top plate**. So you would need one of these:
  - (a) Mount the jacks upside down on the **bottom** side. The jack then spans 1.6 to 26.6 mm below the PCB top, the rear cut-outs are centred 14.1 mm below the PCB top, and the case needs ≥28 mm of clear depth under every strip's rear end.
  - (b) A raised rear hump whose top is ≥27 mm above the PCB.
- Width: rear-panel jacks have to sit side by side. The stereo strip (30 mm wide) needs two 1/4" jacks, at ≥16–20 mm each, so 32–40 mm. The master (60 mm) needs 2 XLR + 4 TRS, at 2×25 + 4×16 = **114 mm**. They don't fit on their own board edges, so the stereo and master jacks would have to move to **new rear jack boards** joined by cables.
- The phones jacks (J10 1/4", J11 3.5 mm) belong on the top. J10 is an NJ3FD-V, which needs 24.0, so the conflict stays for it anyway.

PCB changes: strip (J1 to NCJ6FA-H, moved to the edge, rerouted), stereo (J8/J9 off the board, header added), master (J1, J6–J10 off the board, header added, J10 handled separately), plus 1–3 new jack boards. **3 boards changed + new boards.**

## 4. Fix option 2: jacks stay on top, on a raised rear jack shelf

No part moves. The top becomes two levels:

- **Control plate:** 2.0 mm aluminium, underside at 10.5 (section 2).
- **Jack shelf** over the rear of each board: 1.5 mm aluminium, cut in the same order from the same US service. Underside **24.0 mm** above the PCB, top at 25.5. The step up from the control plate is **13.0 mm**. 1.5 mm is what the NJ3FD-V/NJ5FD-V quick-fix caps take, and the NCJ6FA-V takes up to 3 mm.
- **Master XLRs (J1, J6):** flange at 21.3, so fit a **2.7 mm spacer** (printed ring or two M3 washers' worth) between each flange and the shelf, with M3×10 screws.
- **Where the shelf ends** (PCB y coordinates, rear edge = 30):
  - Mono strips: shelf to **y = 58**. The NCJ6FA-V flange ends at 57.0 and the PVA2 bodies start at ≈61, so a 2 mm riser wall fits at y 58–60.
  - Stereo strips: shelf to **y = 59**. The NJ5FD-V square ends at 58.3 and the 3.5 mm jack J10 starts at ≈66, so the riser goes at 59–61.
  - Master: **L-shaped**. Full width to y = 78 (J7–J9 end at 70.8, the 3.5 mm J11 starts at ≈79). On the left part (x ≤ 131, where the phones jack J10 is) it runs on to y = 90 (J10 ends at 88.4). J11 at x 137–147 / y 79–92 stays on the low plate; a riser between J10 and J11 has 11 mm of room.
  - Controller and the empty strips: no shelf needed. It can carry straight across for looks.
- The shelf is ≈28–60 mm deep front to back and sits behind the controls, so it also gives the plugs (XLR, 1/4") a lip to stand behind. The rear printed frame carries it on M3 heat-set inserts. The riser walls are printed.
- **Cost:** the top is no longer one flat plate. It's a flat 2 mm plate plus a raised 1.5 mm rear strip. The wedge feet and the rest of the plan don't change.

PCB changes: **none.**

## 5. Which one

**Option 2 needs fewer PCB changes (zero, against three boards changed plus new jack boards for option 1).** It keeps every jack where the boards already put it and works with all the existing outputs. The only part change I'd suggest with either option is PVA2 H2 → H1 (same footprint).

Things to check with real parts before the panel DXF (step B):
1. One WQP419GR: body height (10.4 assumed).
2. One PTA fader: lever top above the housing (15.0 assumed, from the DP drawing).
3. The controller's generic EC11 and 45 mm faders: mounting-face height, bushing length, lever top.
4. NC3MAAV flange height (21.3, read off the drawing as 24.0 − 2.7).
