# ESP32 synth

A polyphonic digital synth on an ESP32-S3, played over USB MIDI (FL Studio) or DIN MIDI (keyboards, the mixer's MIDI hub), with line out from a PCM5102A I2S DAC.

**State:** concept agreed 2026-11-11, step 1 firmware written, nothing tested on hardware yet.

## Concept

| Part | Plan |
|---|---|
| Brain | ESP32-S3 devkit. Core 0 renders audio only, core 1 reads MIDI, controls and the screen. GPIO19/20 stay free for USB MIDI. |
| Audio out | PCM5102A I2S DAC board (the purple "GY-PCM5102" type, about $4-8), 44.1 kHz 16-bit, line level on its 3.5 mm jack. |
| Voices | 8-voice poly, plus a mono mode (one voice, glide, optional unison detune). Chosen by Omer 2026-11-11. |
| Per voice | 2 oscillators (saw, square/PWM, triangle, sine, noise), resonant low-pass filter, amp + filter ADSR envelopes, 1 LFO. |
| Controls | B10K slide pots as ADSR faders, EC11 encoders for cutoff, resonance, detune and menus, tact buttons for wave select and presets, LEDs for gate/LFO. Same parts as the controller. |
| Screen | The 2.8" SPI TFT: patch name, envelope and waveform. |
| MIDI in | USB MIDI (device name "Omer Synth") and a DIN MIDI IN through an optocoupler, like [firmware/step5_din_midi](../firmware/step5_din_midi/). |

Not decided yet: sound focus (bass, pads, leads, all-round) and whether it needs to play standalone without a keyboard (note buttons, sequencer). The default is an all-rounder played from MIDI.

## Pins (provisional)

Not locked until the exact board and TFT labels are confirmed.

| Signal | GPIO |
|---|---|
| I2S BCK | 16 |
| I2S LRCK (LCK) | 17 |
| I2S DATA (DIN) | 18 |
| USB D-/D+ | 19 / 20 (reserved) |
| Test button | 0 (BOOT) |

## Build steps

| Step | What | State |
|---|---|---|
| [1](step1_dac_tone/) | DAC + 8 saw voices from USB MIDI notes | Written, untested |
| 2 | Band-limited oscillators, second oscillator, waveforms, mono mode with glide | |
| 3 | Resonant filter + ADSR envelopes + LFO | |
| 4 | Faders and encoders on the parameters | |
| 5 | DIN MIDI IN | |
| 6 | TFT, presets saved to flash | |
| 7 | PCB / perfboard and a printed case | |

## To buy

- PCM5102A I2S DAC board (Amazon/AliExpress, "PCM5102A I2S DAC"). Everything else for steps 1-6 is already on hand.
