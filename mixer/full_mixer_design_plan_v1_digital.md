# Full-size mixer: design plan v1 (draft for Omer)

*2026-10-26. Status: proposal, nothing ordered or locked. Prices and specs are from memory, not checked against shops today; I'll verify before any order.*

## 1. What we're building

A real audio mixer, styled after modern Yamaha desks: microphones in on XLR, line and phone/laptop in on 1/4" and 3.5 mm, faders and knobs on top, stereo out to speakers, headphone out, and USB to the PC so it also works as an audio interface for FL Studio. The MIDI controller you already built stays useful: its faders, encoders and screen become the mixer's control surface.

## 2. What the comparable mixers have

| Mixer | Type | Inputs | Outputs | USB | Notable |
|---|---|---|---|---|---|
| Yamaha AG06 | small analog + DSP | 2 mic (1 XLR combo), line, 3.5 mm | stereo, headphone | 2 in / 2 out, loopback | streaming mixer, very simple |
| Yamaha MG10XU | analog | 4 mic/line XLR combo, 3 stereo line pairs | main L/R (XLR + TRS), monitor, headphone | 2 in / 2 out | built-in FX, 48 V phantom, compressor knob |
| Yamaha MG16XU | analog | 10 mic, stereo pairs | main, 4 aux/group | 2 in / 2 out | the "classic" Yamaha look |
| Behringer XR18 / Soundcraft Ui24 | digital rack | 16 to 20 mic | 6 to 10 outs | 18 to 32 channels | no faders, controlled from a tablet |
| Yamaha DM3 | digital desk | 16 mic | 8 outs | 18 in / 18 out | motorized faders, touchscreen, scenes |
| Zoom LiveTrak L-8 | digital | 6 mic + 2 phone | main, 4 headphone | 12 in / 4 out | records to SD card |

The pattern: an analog front end (mic preamps with 48 V phantom), then either analog knobs-and-wires mixing (MG series) or conversion to digital with all mixing done in a chip (DM3, XR18, L-8). "Modern Yamaha" today means the digital approach: faders and screens are just controls, the sound is processed in software.

## 3. Recommended architecture: small digital mixer

```
 XLR/TRS combo x4 ─► mic preamp x4 ─┐
 1/4" L/R + 3.5 mm ─► line buffer ──┼─► 6-ch ADC ┐
                                    │            │  TDM/I2S
                                    │       ┌────▼─────┐   USB (audio + MIDI) ─► PC / FL Studio
 ESP32-S3 control surface ── UART ──┼──────►│ Teensy 4.1│
 (your faders, encoders, TFT)       │       │ mix, EQ,  │
                                    │       │ comp, FX  │
                                    │       └────┬─────┘
 main L/R (XLR) ◄─ line driver ◄────┴─ 8-ch DAC ◄┘
 monitor L/R (1/4") ◄────────────────────┤
 headphones (1/4" + 3.5 mm) ◄─ HP amp ◄──┘
```

| Block | Part (proposed) | Why |
|---|---|---|
| Audio brain | **Teensy 4.1** (~$32) | Programmed in Arduino like your ESP32. Its Audio Library already has mixers, EQ, filters, delay/reverb and USB audio, so the code is mostly wiring blocks together. |
| Converters | **Cirrus CS42448** codec (6 in / 8 out, 24-bit) | One chip for all I/O; the Teensy Audio Library supports it. |
| Mic preamps | **THAT1512** or **SSM2019** preamp IC, one per mic channel | Pro-grade preamp in one chip with a gain pot; far easier and quieter than discrete transistors. |
| Phantom power | small 48 V boost module + 6.8 kΩ resistor pair per channel, switch per channel | Needed for condenser mics. |
| Outputs | DRV134 (balanced XLR main), NE5532 op-amps, headphone amp (e.g. TPA6120 or NE5532) | Standard, cheap, well documented. |
| Power | **12 V DC wall adapter** → DC-DC to ±12 V (analog) and 5 V/3.3 V (digital) | Keeps mains voltage out of the box entirely. |
| Controls | Your **ESP32-S3** + existing core PCB + side modules | Reuses everything built so far; sends fader/knob values to the Teensy and MIDI to FL. |

**Why not the ESP32 alone?** It has no good audio converters, its USB is too slow for many audio channels, and it's already busy with controls.

**Why not fully analog like the MG10XU?** Every EQ band, aux send and the bus becomes dozens of op-amps and pots on a big board, your faders would need to carry audio (your B10K faders are fine for control, not ideal for audio), and noise problems get much harder to debug. Digital means fewer analog parts and fixes in code instead of re-soldering.

### Known limits of this design
- **USB audio is stereo (2 in / 2 out) at 44.1 kHz/16-bit** with the stock Teensy library, the same as MG10XU/AG06. True multitrack (each mic as its own track in FL) needs an XMOS-type USB chip, which is a much harder design; I'd park that for v2.
- No Bluetooth audio (ESP32-S3 has BLE only, not the classic Bluetooth audio phones use). A cheap Bluetooth receiver module could feed the 3.5 mm input later.
- Size: a 7-to-10-fader desk is roughly 350–450 mm wide, bigger than the Ender 3 bed (220 mm), so the case is printed in panels and bolted together, or the top is a sheet of aluminium/plywood with printed sides.

## 4. Proposed channel list (v1)

| # | Strip | Connector | Controls |
|---|---|---|---|
| 1–4 | Mono mic/line | XLR/1/4" combo (Neutrik-style) | gain knob, 48 V switch, pad, fader, EQ/comp on screen |
| 5/6 | Stereo line | 1/4" L + R, plus 3.5 mm aux (phone/laptop) | fader, EQ |
| 7/8 | USB return (PC playback) | USB-C | fader |
| — | FX return (reverb/delay) | internal | fader |
| — | Monitor send master | — | fader |
| M | Main L/R | 2× XLR out + 2× 1/4" TRS out | master fader |
| — | Monitor L/R | 2× 1/4" TRS out | knob |
| — | Headphones | 1/4" + 3.5 mm | knob |

That's **8 faders in use plus 2 spare**, matching the 10 faders you already own. Each mono channel gets a peak/clip LED.

## 5. Build phases

Each phase works on its own before the next starts, like the controller steps did.

1. **Audio proof on breadboard (~$50).** Teensy 4.1 + the standard Teensy Audio Shield (stereo in/out). Goal: audio in → EQ → out, USB audio to the PC, and one ESP32 fader changing the volume over a UART wire. Proves the whole chain cheaply.
2. **One mic channel (~$30).** One XLR combo jack, one THAT1512 preamp, phantom power, on a small PCB from JLCPCB. Goal: a real mic sounds clean through the Teensy.
3. **Main audio PCB (~$120–200 with parts).** 4 preamps, line inputs, CS42448, outputs, headphone amp, power. Likely a 4-layer board for low noise; I do the KiCad work, you solder (through-hole where possible; the codec is SMD, so I'd have JLCPCB pre-assemble that part).
4. **Firmware.** Mixer, EQ, compressor, FX, meters on the TFT, scenes saved to flash.
5. **Enclosure.** Printed panels + metal or wood top plate, jack panel at the back.

**Rough total: $250–400**, depending on connectors and whether JLCPCB assembles the SMD parts. Honest note: a Yamaha MG10XU costs about $250, so this is a learning build, not a money-saving one.

## 6. Difficulty for you

| Part of the job | Difficulty | Who does it |
|---|---|---|
| Schematic, PCB, firmware, CAD | hard | Claude |
| Soldering through-hole parts, jacks, wiring | medium (matches your 2/3) | Omer |
| SMD codec and small parts | hard by hand | JLCPCB assembly |
| Testing and finding hum/noise | medium, needs patience | together, step by step |
| Safety | low risk: 12 V adapter outside, nothing touches mains. 48 V phantom is low current but don't touch the pins while on. | — |

## 7. Decisions I need from you

1. **Architecture:** digital (Teensy, recommended) or classic analog (MG10XU style)?
2. **Size:** 4 mic channels (v1 above) or 8 mic channels (needs a second codec, ~+$100 and a bigger board)?
3. **USB:** is stereo USB audio to FL enough for now, or is multitrack recording a must?
4. **Budget ceiling** for the whole thing?
5. **Look:** printed case only, or a metal/wood top plate for a more "real desk" feel?
6. **Extras:** built-in reverb/delay FX, recording to SD card, Bluetooth input — which ones matter?

Once 1 and 2 are answered I'll write the Phase 1 shopping list and the first breadboard step.
