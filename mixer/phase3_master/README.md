# Phase 3: master section (design v1)

*2026-10-26. Status: circuit spec, being drawn in KiCad. Nothing ordered.*

The master section is a strip-shaped board the same height as the channel strips (343 mm) and about **60 mm wide**, sitting to the right of the channels. Like the channel strips, its jacks are on top (outputs) and its controls are on the panel. The USB audio chip, USB hub and MIDI go on a separate small **digital board** (Phase 3b), so digital noise stays off the audio board.

## Controls and jacks, top to bottom

| Item | What it does | Part |
|---|---|---|
| MAIN OUT L/R (XLR male) | balanced outputs to speakers | Neutrik NC3MAAV-style vertical PCB XLR ×2 |
| MAIN OUT L/R (1/4" TRS) | balanced, same signal | vertical PCB 1/4" TRS ×2 |
| MONITOR OUT (1/4" TRS) | aux bus (mono), impedance-balanced | 1/4" TRS ×1 |
| PHONES (1/4" + 3.5 mm) | headphones, both usable at once | 1/4" TRS + 3.5 mm TRS |
| FX RETURN | reverb level into the main mix | A10K 9 mm pot |
| MONITOR | monitor output level | A10K 9 mm pot |
| PHONES | headphone level | **dual** A10K 9 mm pot |
| PHONES SOURCE switch | headphones hear MAIN or MONITOR | latching DPDT (same C&K PVA2 EE as the strips) |
| L/R meters | two 10-LED bars, 3 dB steps | LM3915 ×2 |
| MASTER fader | main L/R level | **dual-gang** 60 mm A10K (Bourns PTA60 family, dual) |

Change from the plan: the monitor output is **mono** (one TRS), because the aux bus is mono.

## Circuit (values)

**Bus summing (U1, U2 NE5532), all inverting virtual-earth, +IN to GND, 47 pF across each feedback resistor:**
- MAIN_L sum: Rf 39 kΩ. MAIN_R sum: Rf 39 kΩ. (Each strip feeds the bus through 10 kΩ; 39k recovers the 12 dB pan-network loss.)
- AUX sum: Rf 10 kΩ. FX sum: Rf 10 kΩ.
- Bus inputs come from J3 (2×5 IDC: 1 MAIN_L, 3 MAIN_R, 5 AUX, 7 FX, even pins GND, 9 NC), same pinout as the strips, so one ribbon daisy-chains all boards.

**FX return:** FX_SUM output → J5 (to the reverb module input). Module output (J5) → FX RETURN pot (A10K, top = module out, bottom GND) → U3A inverting unity (10k/10k) → 10 kΩ into MAIN_L bus and 10 kΩ into MAIN_R bus (mono reverb into both sides). The extra inversion keeps the reverb in the same polarity as the dry signal.

**Master:** MAIN_L/R sum outputs → master fader (dual A10K, each gang: top = sum out, bottom GND) → U4A/U4B non-inverting ×3.16 (+10 dB: Rf 21.5 kΩ, Rg 10 kΩ) → MAIN_OUT_L / MAIN_OUT_R. Unity sits at about ¾ fader travel, like the channel faders.

**Main outputs:** MAIN_OUT_L → DRV134PA (DIP-8, U5) → XLR L pins 2(+)/3(−), pin 1 GND, and the 1/4" TRS L tip/ring in parallel. Same for R (U6). Follow the DRV134 datasheet's basic connection (sense pins tied to outputs at the IC), 100 nF + 10 µF per rail pin.

**Monitor:** AUX_SUM → MONITOR pot (A10K) → U3B buffer ×1 → 47 Ω → TRS tip; ring → 47 Ω → GND (impedance-balanced).

**Headphones:** PHONES SOURCE switch (DPDT): released = MAIN_OUT_L/R, latched = MONITOR (U3B output to both sides). → PHONES dual pot (A10K) → U7 NJM4556AD (DIP-8 dual, high current) each side non-inverting ×2 (10k/10k) → 10 Ω series → both phones jacks (tip L, ring R) in parallel. 100 nF + 47 µF per rail pin on U7.

**Meters:** MAIN_OUT_L/R → precision half-wave peak detectors (U8 TL072: diode + 1 µF hold, 1 MΩ release ≈ 1 s) → LM3915 inputs (U9, U10), bar mode, LED current about 5 mA (set by the RLO/RHI resistors per the datasheet). Calibrate so the top LED = +16 dBu (≈ 3 dB below clip), the 0 dB LED (4th from top) = +4 dBu. LM3915s and LEDs run from the **5 V** supply from the digital board (J4), the detectors from ±12 V; clamp the detector output to 0–5 V.

**Power:** J2 2×5 IDC same pinout as everywhere (1–2 +12, 3–6/10 GND, 7–8 −12, 9 P48 unused here), 10 Ω + 47 µF filter per rail. 100 nF at every IC.

**Headers to the other boards:**
- J4 to the digital board (2×5 IDC): 1 USB_REC_L (= MAIN_OUT_L through 10k/2.2k divider for the USB codec's input range), 3 USB_REC_R, 5 +5V in, 7 +5V in, even pins GND. (The USB playback stereo comes back into its own stereo strip, Phase 4, not here.)
- J5 to the reverb module (1×4): FX_SEND, FX_RETURN, +5V, GND.

## Parts to buy (master)
2 NE5532, 1 NE5532 or TL072 for FX/monitor buffers, 1 NE5532 for master gain, 2 DRV134PA, 1 NJM4556AD, 1 TL072, 2 LM3915, 20 LEDs (10 per side: 7 green, 2 yellow, 1 red), 2 XLR male vertical, 3 TRS 1/4" vertical, 1 TRS 1/4" + 1 TRS 3.5 mm (phones), 2 A10K 9 mm pots, 1 dual A10K 9 mm pot, 1 dual-gang 60 mm A10K fader, 1 latching DPDT, IDC headers, sockets, resistors and caps.
