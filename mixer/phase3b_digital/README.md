# Phase 3b: digital board (design v1)

*2026-10-26. Status: spec. Nothing ordered.*

A small board under the panel that gives the mixer **one USB cable** to the PC carrying audio + MIDI, plus 5-pin DIN MIDI IN/OUT. Everything is through-hole or a ready-made module, so there's no fine SMD soldering.

## Blocks

| Block | How | Why |
|---|---|---|
| USB to PC | USB-B (or USB-C) socket → **USB 2.0 hub module** (FE1.1s-based, 4 port, solder pads) | one cable to the PC |
| USB audio | **PCM2902 USB audio module** (stereo line in/out, class-compliant, no drivers) on hub port 1 | records the main mix, plays PC audio back into the mixer |
| MIDI + controls | your **ESP32-S3 controller board** (4 faders, 4 encoders, TFT) on hub port 2 via its USB-C | USB MIDI, as built in the controller steps |
| DIN MIDI | MIDI IN + MIDI OUT circuits on this board, wired to ESP32 **GPIO44 (RX) / GPIO43 (TX)**: the pins kept free in the controller pin map | hardware synths and keyboards |
| 5 V | hub's USB 5 V, plus a second **USB-C power-only** input for use without a PC, joined by two Schottky diodes (1N5817) | meters, reverb module and USB parts keep working standalone |

## Circuits

**MIDI IN (MIDI 1.0 spec, 3.3 V side):** DIN-5 pin 4 → 220 Ω → 6N138 pin 2 (anode); DIN pin 5 → 6N138 pin 3 (cathode); 1N4148 across pins 2–3 (reverse). 6N138: pin 8 = 3.3 V, pin 5 = GND, pin 7 → 10 kΩ to GND (speeds turn-off), pin 6 = output → 1 kΩ pull-up to 3.3 V → ESP32 GPIO44. 100 nF at pin 8. DIN shield/pin 2 not connected (spec: no ground at the input).

**MIDI OUT (MIDI 3.3 V spec):** 3.3 V → 33 Ω → DIN pin 4; ESP32 GPIO43 → 10 Ω → DIN pin 5; DIN pin 2 → GND.

**Audio:** PCM2902 module line-in L/R ← master J4 pins 1/3 (USB_REC, already scaled by the master board's 10k/2.2k). Module line-out L/R → 10 µF → header J7 to the **USB-return stereo strip** (Phase 4).

**Headers:**
- J4 (2×5 IDC, to master J4): 1 USB_REC_L, 3 USB_REC_R, 5 +5V, 7 +5V, evens GND.
- J5b (1×4): +5V/GND for the reverb module (or take it from the master's J5).
- J6 (1×4) to the ESP32 controller: GPIO43 (MIDI TX), GPIO44 (MIDI RX), 3.3 V, GND.
- J7 (1×3) USB playback out: L, R, GND.

## Firmware
One addition to the controller sketch: `Serial0.begin(31250)` on GPIO44/43 bridging DIN MIDI ↔ USB MIDI in both directions. I'll write it as a new firmware step when the board exists.

## Ground
USB ground (PC) and audio ground meet at one point: this board's GND to master J4 GND. If hum appears with the PC connected, the fix is a USB isolator (ADuM3160 module) between the PC and the hub.
