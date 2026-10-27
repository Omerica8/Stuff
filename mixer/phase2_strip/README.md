# Phase 2: mono mic channel strip (design v1)

*2026-10-26. Status: circuit designed and the filters checked in ngspice (ideal op-amps). PCB next. Nothing ordered.*

One strip = one mic/line channel, like a Yamaha MG10XU mono channel. Two identical strips make channels 1 and 2 (four until 2026-10-27, when the MIDI hub took the space).

## Controls, top to bottom

| Control | What it does | Part |
|---|---|---|
| XLR/TRS combo jack | mic (XLR) or line (1/4") in | vertical PCB combo jack (Neutrik NCJ6FA-V or equal) |
| 48V switch | phantom power for condenser mics | SPST toggle/push |
| PAD switch | −20 dB for loud line sources | DPDT push |
| GAIN | +4 to +60 dB | C10K (reverse-log) pot |
| 80 Hz switch | cuts rumble and pops | SPDT push |
| HIGH | ±14 dB shelf at 10 kHz | B10K pot, centre detent |
| MID | ±14.5 dB peak at 2.5 kHz | B10K pot, centre detent |
| LOW | ±15 dB shelf at 100 Hz | B10K pot, centre detent |
| AUX | monitor send, **pre-fader** | A10K pot |
| FX | reverb send, **post-fader** | A10K pot |
| PAN | left/right | B10K pot, centre detent |
| Fader meter | 5 LEDs beside the fader: −20, −10, 0, +6 (green ×3, yellow), PEAK on top | 3 mm LEDs, TL072 + LM339 (added 2026-10-27) |
| Fader | channel level | **Bourns PTA6043, 60 mm travel, A10K (audio taper)**, new part (Omer chose bigger faders 2026-10-26) |

## Signal path

```
XLR 2/3 ∥ TRS tip/ring ─ 47µF ─┬─ [91k pad, shorted by PAD sw] ─┬─ 10k to GND, 1N4004 clamps to ±12 ─► THAT1512 ─ 22µF NP ─┐
P48 ─ 48V sw ─ 6.81k (×2) ─────┘                                                        (RG = 4.7Ω + C10K)      │
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
 └─► 80 Hz HPF (U2A, switch bypass) ─► MID cell (U3A + gyrator U3B) ─► HIGH/LOW stage (U2B, inverting) ─► EQ_OUT
EQ_OUT ─► AUX pot ─ 10k ─► AUX bus                                            (pre-fader)
EQ_OUT ─► PEAK detector (LM393 window ±8 V) ─► LED (top of the fader meter)
EQ_OUT ─► peak detector U6A ─► LM339 ladder ─► 4 meter LEDs (pre-fader)
EQ_OUT ─► 60 mm A10K fader ─► U4A buffer ×2.5 (+8 dB) ─► BUF
BUF ─► FX pot ─ 10k ─► FX bus                                                 (post-fader)
BUF ─ 10k ─► PAN_L ┐  pan pot between PAN_L and PAN_R, wiper to GND
BUF ─ 10k ─► PAN_R ┘  PAN_L ─ 10k ─► MAIN L bus,  PAN_R ─ 10k ─► MAIN R bus
```

Buses are "virtual earth": the master board's summing amps hold them at 0 V and add up the currents from every strip.

## Component values (netlist-level)

**Input + phantom**
- J1 combo jack: XLR pin 1 = GND (chassis via 100Ω ∥ 10nF later at the case), XLR 2 ∥ TRS tip = HOT, XLR 3 ∥ TRS ring = COLD, TRS sleeve = GND.
- C1, C2 470 pF HOT/COLD to GND (RF filter).
- SW1 (48V): P48 → SW1 → node PH. R1, R2 6.81 kΩ 0.1 % from PH to HOT and COLD.
- C3, C4 47 µF 63 V electrolytic, + side at HOT/COLD (jack side), − side at nodes H1/C1.
- Pad: R3, R4 91 kΩ in series H1→H2 and C1→C2, SW2 (DPDT) shorts each when PAD is off.
- R5, R6 10 kΩ H2/C2 to GND. D1–D4 1N4004: H2 and C2 each clamped to +12 (cathode to +12) and −12 (anode to −12).

**Preamp U1 THAT1512 (DIP-8):** pin 1 RG1, 2 −IN, 3 +IN, 4 V−, 5 REF, 6 OUT, 7 V+, 8 RG2 (confirm against the datasheet). +IN = H2, −IN = C2, REF = GND. RG between pins 1 and 8: R7 4.7 Ω in series with RV1 C10K wired as a rheostat (gain rises clockwise). Gain = 1 + 5 kΩ/RG: 4 dB (CCW) … 16 dB (½) … 26 dB (¾) … 60 dB (CW). 100 nF + 22 µF on each rail pin.
- C5 22 µF non-polar from OUT → node PRE; R8 100 kΩ PRE to GND.

**80 Hz HPF, U2A (NE5532):** unity Sallen-Key: C6, C7 100 nF film in series from PRE; R9 14 kΩ from the C6/C7 junction to U2A output; R10 28 kΩ (+IN to GND, use 27k + 1k or 28k 1 %). U2A −IN tied to its output. SW3 (SPDT) selects HPF output or PRE → node HPF_OUT. Simulated −3 dB at 80.7 Hz, −12.4 dB at 40 Hz.

**MID cell, U3A (NE5532), non-inverting:** R11 2.2 kΩ HPF_OUT → +IN (node P). R12 2.2 kΩ U3A output → −IN (node N). RV2 B10K: one end P, other end N, wiper → R13 390 Ω → C8 47 nF film → node L. Gyrator at L: C9 8.2 nF from L to U3B +IN, R14 100 kΩ U3B +IN to GND, U3B as follower (out → −IN), R15 100 Ω from U3B output to L. (L ≈ 82 mH.) Wiper toward N = boost. Output MID_OUT.

**HIGH/LOW stage, U2B (NE5532), inverting unity:** R16 10 kΩ MID_OUT → −IN, R17 10 kΩ output → −IN, +IN to GND. Output = EQ_OUT.
- HIGH: RV3 B10K between MID_OUT and EQ_OUT, wiper → R18 1.5 kΩ → C10 22 nF → U2B −IN. Wiper toward MID_OUT = boost.
- LOW: RV4 B10K between MID_OUT and EQ_OUT, wiper → R19 1 kΩ → node X; C11 1 µF film X to GND; R20 1 kΩ X → U2B −IN. Wiper toward MID_OUT = boost.

**Sends, fader, pan**
- AUX: RV5 A10K, top EQ_OUT, bottom GND, wiper → R21 10 kΩ → AUX bus.
- Fader RV6 (Bourns PTA6043 60 mm, A10K audio taper): top EQ_OUT, bottom GND, wiper → U4A +IN. (No law resistor needed; R22 removed.) U4A gain 2.5: R23 15 kΩ out→−IN, R24 10 kΩ −IN→GND. Output BUF.
- FX: RV7 A10K, top BUF, bottom GND, wiper → R25 10 kΩ → FX bus.
- PAN: R26 10 kΩ BUF→PAN_L, R27 10 kΩ BUF→PAN_R, RV8 B10K ends PAN_L/PAN_R, wiper GND. R28 10 kΩ PAN_L→MAIN_L, R29 10 kΩ PAN_R→MAIN_R.
- U4B unused: +IN to GND, output to −IN.

**PEAK, U5 LM393:** supply +12 / −12 (GND pin to −12). Refs: R30 4.7k/R31 10k from +12 to GND gives +8.2 V; R32 4.7k/R33 10k from −12 gives −8.2 V. U5A: +IN = +8.2 V, −IN = EQ_OUT. U5B: +IN = EQ_OUT, −IN = −8.2 V. Outputs tied together → LED D5 cathode; D5 anode → R34 4.7 kΩ → +12. (No hold circuit: short peaks give a short flash. A hold can be added later.)

**Fader meter (added 2026-10-27), pre-fader, like the MG10XU's channel meters:**
- Peak detector U6A (TL072, not the spare NE5532 half: the NE5532's input clamp diodes would dump the hold cap into EQ_OUT): +IN = EQ_OUT, output → D6 1N4148 → node MTRK, which is also −IN (ideal diode). MTRK → R38 220 Ω → MTR; C27 1 µF film and R39 1 MΩ from MTR to GND (≈1 s fall). U6B unused (follower to GND). Positive half-cycles only, which is fine for a meter.
- Ladder from +12: R40 18k → REF4 → R41 3.6k → REF3 → R42 2.4k → REF2 → R43 750 → REF1 → R44 360 → GND gives 3.40 / 1.68 / 0.53 / 0.17 V = sine peaks at +9.8 / +3.7 / −6.3 / −16.1 dBu, marked **+6, 0, −10, −20** (0 = +4 dBu, the same 0 as the master meter).
- U7 LM339 (+12 / GND; MTR never goes below 0 V): comparator n has +IN = REFn, −IN = MTR, open-collector out → LED cathode; anode → 4.7 kΩ (R45–R48) → +12, about 2 mA like PEAK. D7 −20, D8 −10, D9 0 green, D10 +6 yellow. The existing red PEAK LED D5 sits on top of the column.
- 100 nF per rail at U6 and U7 (C28–C30). No comparator hysteresis: the hold cap keeps the LEDs steady enough.

**Power:** J2 2×5 IDC, same pinout as the power board (1–2 +12, 3–6 and 10 GND, 7–8 −12, 9 P48). Each rail: 10 Ω + 47 µF filter at the header; 100 nF at every op-amp.
**Bus:** J3 2×5 IDC: 1 MAIN_L, 2 GND, 3 MAIN_R, 4 GND, 5 AUX, 6 GND, 7 FX, 8 GND, 9 NC, 10 GND.

## Levels and polarity
- Unity gain (preamp output to main bus, pan centre, assuming the master sums with 39 kΩ feedback) is at fader ≈ −8 dB, about ¾ travel. That leaves +8 dB above it, like a real desk.
- The strip inverts once (HIGH/LOW stage). The master's summing amp inverts again, so polarity is correct at the outputs. The stereo strips will be designed to invert once too.

## Simulated results (`eq.py`, `mid.py`, `hpf.cir`)

| Band | Full boost | Full cut | Centre |
|---|---|---|---|
| HIGH | +14.3 dB @ 10 kHz, +15.8 @ 15 kHz | mirror | 0.0 dB |
| MID | +14.5 dB @ 2.5 kHz (−6 dB points 1.7–3.8 kHz) | mirror | 0.0 dB |
| LOW | +14.7 dB @ 100 Hz, +15.3 @ 50 Hz | mirror | 0.0 dB |

Pan law −2.5 dB at centre with full separation at the ends. The A10K fader reads about −20 dB at half travel and −10 dB at ¾ travel (typical audio taper), so unity sits a little above ¾ travel.

## Parts per strip

1 THAT1512, 3 NE5532, 1 LM393, 1 TL072, 1 LM339, 1 combo jack, 3 switches (48V, PAD, 80Hz), 7 pots (1 C10K gain; 4 B10K centre-detent for HIGH, MID, LOW, PAN; 2 A10K for AUX, FX), 1 fader (PTA6043 60 mm A10K, new), 4 1N4004, 1 1N4148, 5 LEDs (3 green, 1 yellow, 1 red), 2× 6.81k 0.1 %, film caps (2× 100n, 47n, 22n, 8.2n, 1µF), 2× 47µF 63V, 22µF NP, ~35 resistors, 2 IDC headers, IC sockets.

## Phase 2 test rig (breadboard, no master board yet)

One NE5532 as the MAIN L/R summing amps: −IN = bus, +IN = GND, 39 kΩ feedback, output → 100 Ω → headphone jack. Power from the Phase 1 board. Use 80 Ω+ headphones and keep the level modest; it's a test, not the final headphone amp.
