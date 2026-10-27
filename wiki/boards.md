<!-- sources: mixer/README.md mixer/phase1_power/ mixer/phase2_strip/ mixer/phase3_master/ mixer/phase3b_digital/ mixer/phase4_stereo/ mixer/phase5_reverb/ mixer/phase6_midi/ controller/ -->
# Boards

Every mixer board is 2-layer, through-hole where possible, ERC/DRC clean, and **not ordered yet**. Each folder has a README (circuit), `pcb/PARTS.md` (exact parts), and `pcb/` outputs: BOM csv, schematic PDF, assembly PDF, renders, ERC/DRC reports and a JLCPCB gerber zip. KiCad sources live on Omer's PC in `C:\Users\pogam\kicad-mcp\kicad-sandbox\<board>` (generator scripts in `tools/`).

| Board | Folder | Size (mm) | Count | Notes |
|---|---|---|---|---|
| Power (±12 V, P48) | [phase1_power](../mixer/phase1_power/README.md) | 100 × 85 | 1 | 7912 insulated; Fischer SK104 heatsinks (35 mm tall, they set the case height). Sim in `power_sim.cir`. |
| Mono mic strip | [phase2_strip](../mixer/phase2_strip/README.md) | 30 × 343 | 2 | THAT1512, HPF, MID gyrator EQ, PTA6043 60 mm A10K fader, LM393 peak LED. EQ math in `eq.py`, `mid.py`, `hpf.cir`. Pot options in `pcb/POT_OPTIONS.md`. |
| Master | [phase3_master](../mixer/phase3_master/README.md) | 60 × 343 | 1 | Summing, dual PTA6044 master, DRV134 outs, LM3915 meters, phones. **Check the dual-fader and 3.5 mm jack footprints with a 1:1 print before ordering.** |
| Digital | [phase3b_digital](../mixer/phase3b_digital/README.md) | 100 × 75 | 1 | Hub module + PCM2902 module on labelled pads, 6N138 MIDI IN, MIDI OUT, USB-C power-only input. |
| Stereo strip | [phase4_stereo](../mixer/phase4_stereo/README.md) | 30 × 343 | 2 | Line build: fit J8–J10, JP1/JP2 open. USB-return build: omit J8–J10, fit JP1/JP2. Dual HIGH/LOW pots have no detent. |
| Reverb carrier | [phase5_reverb](../mixer/phase5_reverb/README.md) | 74 × 50 | 1 | Akizuki AE-FV-1-DIP module, 3-way DIP program select, ROM jumper, trims. |
| MIDI hub | [phase6_midi](../mixer/phase6_midi/README.md) | 200 × 64 | 1 | Raspberry Pi Pico in sockets on hub USB3 (micro-USB cable). 5× 6N138 DIN IN, 3 DIN OUT (OUT 3 = THRU option), USB-A host via PIO-USB with 500 mA polyfuse. ERC 0, DRC 0; outputs in pcb/. |
| MIDI controller | [controller/](../controller/) | — | 1 | Earlier standalone board: schematic, gerbers, BOM (incl. PCBWay), assembly guide HTML. |

## Inter-board connectors

| Connector | Pins |
|---|---|
| J2 power (all audio boards) | 1–2 +12 V, 3–6 & 10 GND, 7–8 −12 V, 9 P48 |
| J3 bus (strips ↔ master) | 1 MAIN_L, 3 MAIN_R, 5 AUX, 7 FX, evens GND, 9 NC |
| Master J4 ↔ digital J4 | 1 USB_REC_L, 3 USB_REC_R, 5 & 7 +5 V, evens GND |
| Master J5 ↔ reverb J1 | 1 FX_SEND, 2 FX_RET, 3 +5 V, 4 GND |
| Digital J6 → ESP32 | GPIO43 MIDI TX, GPIO44 MIDI RX, 3.3 V, GND |
| Digital J7 → USB-return strip J7 | L, R, GND |
| Hub module USB3 → MIDI hub Pico | cut micro-USB cable: 5V, D−, D+, GND |

Ribbon headers J2–J4 (and master J5) sit at local y ≈ 325, at each board's front end.
