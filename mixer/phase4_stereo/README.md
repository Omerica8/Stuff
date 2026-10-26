# Phase 4: stereo strip (design v1)

*2026-10-26. Status: spec. Nothing ordered.*

One PCB design, built twice:
- **Stereo line strip** (channels 5/6): 1/4" L and R jacks plus a 3.5 mm aux jack (phone/laptop).
- **USB return strip** (channels 7/8): PC playback from the digital board's J7 header. Jacks left off.

Same width (30 mm) and height (343 mm) as the mono strip, with the same J2 power / J3 bus positions so the ribbons run straight across.

## Controls, top to bottom
| Item | Part |
|---|---|
| 1/4" L, 1/4" R (balanced or unbalanced), switched | vertical PCB TRS jacks with normalling switch contact |
| 3.5 mm aux (stereo) | vertical PCB 3.5 mm stereo jack; it feeds L/R only when the 1/4" jacks are empty (normalled through their switch contacts) |
| HIGH (±14 dB @ 10 kHz) | **dual** B10K 9 mm, centre detent if stocked |
| LOW (±15 dB @ 100 Hz) | **dual** B10K 9 mm, centre detent if stocked |
| AUX (pre-fader, mono L+R) | A10K 9 mm |
| FX (post-fader, mono L+R) | A10K 9 mm |
| BAL (balance) | B10K 9 mm centre detent (same as mono strip PAN) |
| PEAK LED | red LED |
| Fader | **dual-gang** 60 mm A10K, Bourns PTA6044-2015DPA103 (same as master) |

## Circuit (per side L and R unless noted)
- **Input:** J7 header (1×3: L, R, GND) in parallel with the jack inputs (USB build: no jacks fitted). Balanced line receiver NE5532 half: 10k/10k/10k/10k differential amp, gain 0 dB, tip → +, ring → −, 100 pF across feedback. 3.5 mm tip (L) / ring (R) normalled into the 1/4" L/R tip switch contacts; 1/4" ring is grounded through 10 kΩ when unbalanced plugs short it.
- **EQ:** the same bridged-pot inverting HIGH/LOW stage as the mono strip (Rin = Rf = 10k; HIGH wiper → 1.5k → 22n → −IN; LOW wiper → 1k → node → 1k → −IN, 1 µF node to GND), one dual pot gang per side. Output EQ_L / EQ_R. (One inversion, the same as the mono strip.)
- **AUX (pre):** EQ_L and EQ_R → 20k each → inverting summer (10k feedback, gives (L+R)/2), then an inverting unity stage to restore polarity → AUX pot → 10 kΩ → AUX bus. (Two op-amp halves; alternatively one non-inverting averager with 10k/10k into +IN, unity buffer; RC's choice, keep polarity equal to EQ out.)
- **Fader:** dual A10K: top EQ_L/EQ_R, bottom GND, wipers → NE5532 non-inverting ×2.5 (15k/10k) → BUF_L / BUF_R.
- **FX (post):** BUF_L + BUF_R averaged (10k/10k into a buffer) → FX pot → 10 kΩ → FX bus.
- **BAL:** BUF_L → 10k → node BL; BUF_R → 10k → node BR; BAL pot between BL and BR, wiper GND; BL → 10k → MAIN_L, BR → 10k → MAIN_R. (Same network and centre level as the mono strip pan, so the master's 39k summing gives the same unity point.)
- **PEAK:** two LM393s, ±8.2 V window on EQ_L and on EQ_R, all four outputs wired-OR to one LED (4.7k from +12), same values as the mono strip.
- **Power / bus:** J2 and J3 identical to the mono strip. 10 Ω + 47 µF per rail, 100 nF per IC.
