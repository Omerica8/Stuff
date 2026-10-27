<!-- sources: mixer/README.md mixer/phase1_power/README.md mixer/phase3_master/README.md mixer/phase3b_digital/README.md mixer/phase6_midi/README.md -->
# Architecture

## The mixer (classic analog)

Audio stays analog from jack to jack. Each channel is its own PCB, so a mistake costs one cheap board. Boards join through a 2×5 ribbon bus.

```
2× MONO STRIP   XLR/TRS ─► THAT1512 preamp ─► 80 Hz HPF ─► 3-band EQ ─┬─► AUX (pre-fader) ─► AUX bus
                                                                      ├─► fader ─► FX (post) ─► FX bus
                                                                      └─► fader ─► pan ─► MAIN L/R bus
2× STEREO STRIP 1/4" L/R + 3.5 mm (line build) or USB playback (USB-return build) ─► same buses
MASTER          sums the buses ─► dual master fader ─► DRV134 balanced XLR + TRS outs, LM3915 meters,
                mono monitor out, NJM4556 phones (MAIN/MON switch), FX send/return
REVERB          FX bus ─► Spin FV-1 module ─► FX RETURN pot ─► MAIN L/R
DIGITAL         USB-B ─► FE1.1s hub ─┬─► PCM2902 USB audio (records MAIN, plays into USB-return strip)
                                     ├─► ESP32-S3 controller (USB MIDI + DIN MIDI IN/OUT)
                                     └─► MIDI HUB: Raspberry Pi Pico, 5 DIN IN, 3 DIN OUT/THRU, USB-A host for a USB keyboard
POWER           15 VAC wall adapter ─► ±12 V linear (7812/7912) + 48 V phantom (quadrupler + zener/MJE340)
```

- **Buses are virtual earth.** Each strip feeds a bus through 10 kΩ. The master's inverting summing amps hold the bus at 0 V: MAIN L/R Rf 39 kΩ (recovers the 12 dB pan-network loss), AUX/FX Rf 10 kΩ.
- **Bus ribbon (J3, 2×5):** 1 MAIN_L, 3 MAIN_R, 5 AUX, 7 FX, evens GND, 9 NC. Same pinout on every board, so one ribbon daisy-chains them.
- **Power ribbon (J2, 2×5):** 1–2 +12 V, 3–6 and 10 GND, 7–8 −12 V, 9 P48. Not the Eurorack order.
- **Two power domains.** The AC adapter feeds only the audio rails (±12 V, P48). The 5 V side (ESP32, hub, PCM2902, meters, reverb) runs from USB (PC or a phone charger in a second power-only USB-C), so digital currents stay off the audio rails and mains never enters the box.
- **Grounding:** star ground on the power board. USB ground meets audio ground at one point (digital board GND to master J4). If hum shows up with the PC connected, add an ADuM3160 USB isolator.
- **MIDI-first since 2026-10-27:** 6 DIN IN, 4 DIN OUT and 1 USB host port in total. The MIDI hub shows up as its own multi-port USB MIDI device, so FL Studio sees each input separately.
- **USB is stereo only** (2 in / 2 out, 16-bit), like the MG10XU. FL Studio records the main mix, not each mic.

Full detail: [mixer/README.md](../mixer/README.md).

## The controller

ESP32-S3 N16R8 DevKitC-style board, native USB MIDI (TinyUSB, shows as "Omer Controller"). Core = 4 faders + 4 EC11 encoders + TFT + buttons and LEDs. In the mixer it sits right of the master as the MIDI section, on digital-board hub port 2, with DIN MIDI on GPIO44 (RX) / GPIO43 (TX). See [firmware.md](firmware.md).

The original plan for side modules (3+3 each, 10 channels total) is on hold: 10 channels need about 45 pins, more than the board has.
