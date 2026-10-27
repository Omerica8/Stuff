<!-- sources: mixer/README.md mixer/case/STATUS.md mixer/case/HEIGHTS.md -->
# Decisions

Newest last. "Why" is given where it was recorded.

| Date | Decision | Why |
|---|---|---|
| 2026-10-17 | Controller: modular core (4+4) plus two 3+3 side modules, flat deck with separate wedge rails, core works standalone | Fits the Ender 3 bed and the 10+10 parts bought |
| 2026-10-17 | Reserve GPIO19/20 for USB; don't lock the pinout until board and TFT labels are confirmed | Native USB on the S3 |
| 2026-10-19 | Controller v1 uses only parts already bought, function over looks; Claude writes all code and CAD | Omer's interview answers |
| 2026-10-26 | Mixer is **classic analog** (MG10XU style), not the Teensy digital design | Kept as `mixer/full_mixer_design_plan_v1_digital.md` |
| 2026-10-26 | 4 mic channels | |
| 2026-10-26 | Standard budget (~$300): genuine THAT1512, dual faders on stereo strips, FV-1 reverb, LM3915 meters, aluminium top | Bluetooth input left for later |
| 2026-10-26 | Audio rails ±12 V, not ±15 V | A 15 VAC adapter lacks headroom at low mains |
| 2026-10-26 | 5 V digital side runs from USB, not the AC adapter | Keeps digital noise off the audio rails |
| 2026-10-26 | 60 mm Bourns PTA faders on the strips instead of the owned 45 mm B10K | Omer chose bigger faders; law-faking resistor dropped |
| 2026-10-26 | Monitor out is mono | The aux bus is mono |
| 2026-10-26 | USB audio, hub and MIDI on a separate digital board | Keeps digital noise off the master board |
| 2026-10-26 | ESP32 controller moves into the mixer as its MIDI section, with DIN IN/OUT | Omer asked for MIDI I/O |
| 2026-10-26 | All project files live on the `mixer` branch of Omerica8/Stuff, not a new repo | Omer's choice |
| 2026-10-27 | Stepped top (2 mm control plate + raised 1.5 mm jack strip) instead of moving jacks to a rear panel | No PCB changes |
| 2026-10-27 | PVA2 H1 switches, 4 mm fader spacers, LEDs raised 7.2 mm, ESP32/TFT without sockets | From the height study |
| 2026-10-27 | Take part sizes from datasheets, not Omer's measurements; verify with a 1:1 paper print | Omer's instruction |
| 2026-10-27 | Case CAD in Python (build123d + ezdxf via uv), generated from the KiCad boards, instead of OpenSCAD | Nothing to install on the PC, and one re-run follows any board change |
| 2026-10-27 | Display under the raised shelf (meter-bridge style); risers hang from the shelf | Free space over the digital board; risers can't stand on the plate behind the mono combo jacks |

## Still open

- Bluetooth input (later).
- Firmware: FL Studio script (step 5 of the controller plan) and TFT + plugin maps.
- Nothing has been ordered. Verify prices and stock first.
