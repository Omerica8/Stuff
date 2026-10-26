# Full-size mixer: design plan v2, classic analog

*2026-10-26. Status: Omer chose classic analog (MG10XU style). Nothing ordered or locked. The earlier digital version is kept in full_mixer_design_plan_v1_digital.md. Prices and specs are from memory, not checked against shops today; I'll verify before any order.*

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

## 3. Architecture: classic analog, built from channel-strip boards

Audio stays analog from jack to jack, like the Yamaha MG10XU. Knobs and faders sit in the audio path. The mixer is split into **one small PCB per channel strip** plus a **master board**, joined by a ribbon-cable bus. You build and test one strip, then copy it, so a mistake costs one cheap board, not the whole mixer. A strip board (about 35 × 200 mm) also fits the Ender 3 bed for its own printed frame.

```
 MONO STRIP (x4)
 XLR/TRS combo ─► mic preamp ─► 80 Hz cut ─► 3-band EQ ─┬─► AUX knob (pre-fader) ──────► AUX bus
   (48 V switch)   (gain knob,    (switch)    (hi/mid/lo)│
                    pad switch)                          ├─► FX knob ───────────────────► FX bus
                                                         └─► fader ─► pan ─► L/R ───────► MAIN L/R bus
                                                              peak LED

 STEREO STRIP (x1, +1 for USB return)
 1/4" L+R, 3.5 mm aux ─► line buffer ─► 2-band EQ ─► aux/FX knobs ─► dual fader ─► balance ─► buses

 MASTER BOARD
 MAIN L/R bus ─► summing amps ─► master fader (dual) ─┬─► main out XLR + 1/4" TRS
                                                      ├─► USB codec (PCM2902) ─► PC / FL Studio
                                                      └─► LED meters
 ESP32-S3 (your core board) ─► MIDI IN / OUT (5-pin DIN) + USB MIDI ─┐
 PCM2902 USB audio ───────────────────────────────────────────────────┴─► USB hub ─► one cable to PC
 AUX bus ─► summing amp ─► monitor knob ─► monitor out 1/4" TRS
 FX bus ─► reverb/delay module ─► FX return knob ─► MAIN bus
 PC playback (USB) ─► USB-return stereo strip
 phones knob + source switch (main / monitor) ─► headphone amp ─► 1/4" + 3.5 mm

 POWER BOARD: AC wall adapter (15 V AC) ─► rectifier ─► ±12 V regulators (audio) + 48 V phantom (5 V digital side runs from USB; see phase1_power/README.md)
```

| Block | Part (proposed) | Why |
|---|---|---|
| Mic preamp | **THAT1512** or **SSM2019**, one per mono channel | Pro-grade, low-noise preamp in one chip, with a single gain pot. |
| EQ, buffers, summing | **NE5532** / **TL072** op-amps | The classic mixer op-amps: cheap, through-hole, well documented. |
| Channel faders | your **B10K faders** + one "law-faking" resistor each | The fader you own is linear, which sounds wrong for volume. One resistor from the wiper to ground makes it feel close to a proper audio (log) fader, so the 10 you bought still get used. |
| Master fader | one **dual-gang 10 kΩ audio-taper (A10K) fader** | Stereo master needs two tracks in one fader. A new part to buy. |
| Knobs | about 40 pots (gain, EQ, aux, FX, pan) | A new part to buy, mostly 10 kΩ and 50 kΩ, linear and audio taper, some with a centre detent. |
| USB audio | **PCM2902** USB codec (stereo in/out, plug and play) | The same chip many budget mixers use. It needs no code or drivers. It's SMD, so either JLCPCB assembles it or we use a ready-made module (~$5). |
| FX | **Belton BTDR** or **Spin FV-1** reverb/delay module | Gives the "built-in FX" of the MG series without writing DSP code. |
| Meters | **LM3915** LED bar driver ×2 | Gives classic LED level meters with no code. |
| Phantom power | 48 V from a small boost circuit, 6.8 kΩ resistor pair + switch per channel | Needed for condenser mics. |
| Main out | XLR out, impedance-balanced (simple) or **DRV134** (true balanced) | Standard way to connect PA speakers. |
| Headphones | NE5532 or **NJM4556** headphone driver | Can drive 32 to 300 Ω headphones. |
| Power | **AC-to-AC wall adapter** + 7812/7912 linear regulators (±12 V) | Quieter than switching DC-DC converters, and mains voltage never enters the box. |

### MIDI in and out (added 2026-10-26 at Omer's request)

Your **ESP32-S3 core board moves into the mixer** as its MIDI section, sitting next to the master section like the controller panel on a DAW-style desk.

| Port | What it does | Parts |
|---|---|---|
| **MIDI IN** (5-pin DIN) | Keyboards, drum machines, etc. play into FL Studio through the mixer | DIN socket, **6N138** or **H11L1** optocoupler (the MIDI standard requires one, so ground loops can't add hum), 220 Ω resistor, diode |
| **MIDI OUT** (5-pin DIN) | FL Studio (or the mixer's own controls) drives synths and hardware | DIN socket, two resistors (3.3 V MIDI version of the spec: 33 Ω + 10 Ω) |
| **MIDI THRU** (optional) | Passes MIDI IN straight on to another device | one more DIN + a buffer gate |
| **USB MIDI** | FL Studio sees the mixer as a MIDI device: DIN ports + the controls below | ESP32-S3 native USB (already working in your Step 2 test) |

The ESP32 also keeps your **4 faders + 4 encoders + TFT** as a MIDI control section for FL, separate from the audio faders. It can light the clip LEDs or show meters on the TFT later.

**One USB cable:** the PCM2902 (audio) and the ESP32 (MIDI) are two USB devices. A small USB hub chip (**FE1.1s**, or a ready-made hub module) joins them, so the PC sees one cable carrying both audio and MIDI, like a commercial mixer.

The MIDI circuits are small and use parts you can solder easily. They go on the master board, or on their own small board if we want to test them early. Each test goes alongside the controller steps you already know.

### Known limits of this design
- USB is stereo (2 in / 2 out, 16-bit), the same as the MG10XU. FL Studio records the main mix as one stereo track, not each mic separately.
- No Bluetooth audio built in. A ~$5 Bluetooth receiver module could feed the 3.5 mm input later.
- Noise and hum are the main risk. Grounding layout matters a lot; I'll design for it (star ground, separate audio and LED returns), and the build order lets us catch problems on one strip.
- Size: about 350–450 mm wide, so the case is printed in panels or uses a metal/wood top plate.

## 4. Proposed channel list (v1)

| # | Strip | Connector | Controls |
|---|---|---|---|
| 1–4 | Mono mic/line | XLR/1/4" combo | gain, pad, 48 V, 80 Hz cut, hi/mid/lo EQ, aux, FX, pan, fader, peak LED |
| 5/6 | Stereo line | 1/4" L + R, 3.5 mm aux | hi/lo EQ, aux, FX, balance, dual fader* |
| 7/8 | USB return | USB-B or USB-C | level, fader* |
| — | FX return | internal | level knob |
| M | Main L/R | 2× XLR + 2× 1/4" TRS | dual master fader, LED meters |
| — | Monitor (aux) | 2× 1/4" TRS | knob |
| — | Headphones | 1/4" + 3.5 mm | knob, main/monitor switch |
| — | MIDI | DIN IN, OUT (+ THRU), USB | 4 faders, 4 encoders, TFT (your core board) |

*Stereo strips need dual-gang faders, so they'd use new parts too. The other option is a dual-gang knob for level, with your B10K faders only on the 4 mono strips.

That uses 8 of your 10 B10K faders: 4 on the mono strips and 4 on the MIDI section. The other 2 are spares.

## 5. Build phases

1. **Power board (~$30).** AC adapter, ±12 V and 48 V. Designed: see phase1_power/README.md. Everything else plugs into this, so it's built and measured first with a multimeter. I'll give you safe test points.
2. **One mono strip + simple headphone out (~$40).** Preamp, EQ, fader, pan into a basic headphone amp. Goal: a mic plugged into XLR comes out of headphones cleanly. This is the big milestone.
3. **Master board (~$70).** Summing, master fader, main/monitor outputs, headphones, USB codec, meters, plus MIDI IN/OUT and the USB hub.
4. **Copy the strips (~$25 each).** Three more mono strips and the stereo strips. These are the same boards, so soldering gets faster each time.
5. **FX module.**
6. **Enclosure.** Printed frame/panels, top plate, jack panel.

**Rough total: $250–400**, depending on pots, connectors and how much JLCPCB pre-assembles. That's similar to buying an MG10XU, so this is a learning build.

## 6. Difficulty for you

| Part of the job | Difficulty | Who does it |
|---|---|---|
| Schematics, PCBs, CAD | hard | Claude |
| Soldering | medium: mostly through-hole, but a lot of it (~300 joints per mixer) | Omer |
| SMD (USB codec only) | avoided: module or JLCPCB assembly | — |
| Testing, finding hum | medium, needs patience | together, one strip at a time |
| Safety | low risk: AC adapter is outside, ~15 V inside. 48 V phantom is low current but don't touch it while on. | — |

## 7. Decisions still open

1. ~~Architecture~~: **classic analog** (decided 2026-10-26).
2. ~~Size~~: **4 mic channels** (decided 2026-10-26).
3. **Budget ceiling** for the whole thing?
4. **Look:** printed case only, or a metal/wood top plate?
5. **Extras:** reverb/delay FX module, LED meters, Bluetooth input: keep, drop, or later?
6. **Stereo strip level:** buy dual-gang faders, or use dual-gang knobs to save money?

Next step from me: the Phase 1 power board is designed (phase1_power/README.md); next is its PCB.

## Status (2026-10-26)

| Board | Folder | Size | State |
|---|---|---|---|
| Power (±12 V, 48 V) | phase1_power/ | 100 × 85 mm | PCB done, checks clean, not ordered |
| Mono mic strip ×4 | phase2_strip/ | 30 × 343 mm | PCB done, exact parts in pcb/PARTS.md |
| Master | phase3_master/ | 60 × 343 mm | PCB done, check dual-fader + 3.5 mm jack footprints with a 1:1 print |
| Digital (USB audio, hub, DIN MIDI) | phase3b_digital/ | 100 × 75 mm | PCB done, modules wired to pads |
| Stereo strip ×2 (line, USB return) | phase4_stereo/ | 30 × 343 mm | PCB done |
| Firmware step 5 (DIN MIDI bridge) | ../firmware/step5_din_midi/ | — | written, logic tested off-hardware |
| Reverb module, enclosure | — | — | not started |

Long-lead parts to order first: C&K PVA2 EE switches (~15 weeks), Bourns PTA6044 dual faders (up to 21 weeks), NTE1509 (LM3915 replacement).
