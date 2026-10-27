# Phase 5: FV-1 reverb carrier

A 74 × 50 mm, 2-layer, through-hole board. It carries a ready-made Spin FV-1 module (Akizuki AE-FV-1-DIP) and connects to the master's J5 with one 4-wire cable. It mounts inside the case on three M3 holes.

```
master J5 ──1 FX_SEND──► 10k + IN LEVEL trim (max -6 dB) ─┬─► 4.7u ─ 1k ─┬─► FV-1 LIN
                                                           │              1n C0G
                                                           └─► 4.7u ─ 1k ─┬─► FV-1 RIN
                                                                          1n C0G
FV-1 LOUT ─ 4.7u ─ 10k ─┬─► MCP6002, gain x1–x3 (OUT LEVEL trim), on +5 V, biased at 2.5 V
FV-1 ROUT ─ 4.7u ─ 10k ─┘          └─► 10u ─ 100R ─► master J5 2 FX_RET (100k to GND)
master J5 3 +5V ─► MCP1700 3.3 V ─► module DVDD; 10R + 10u + 100n ─► AVDD
SW1 (3-way DIP) ─► S0–S2 (module has pull-ups; all off = program 7 Reverb 2)
JP1 fitted = internal ROM; open = programs from the 24LC32A in U2
RV2–RV4 trims ─► POT0–POT2 (reverb time, HF, LF on programs 6/7)
```

- **J1 pinout = master J5:** 1 FX_SEND, 2 FX_RET, 3 +5V, 4 GND.
- **Polarity:** the carrier doesn't invert (passive average, then a non-inverting buffer), so the master's FX RETURN stage keeps the reverb in the same polarity as the dry signal, as the phase 3 README describes.
- **Levels:** FV-1 full scale is about 2.6–3.0 V p-p. The input path can only attenuate (10k fixed + 10k trim), which is enough for the master's 0 dBu FX send, with peaks up to about +20 dBu. The 1k series resistor limits clamp current to under 10 mA at the worst case. The output buffer swings about 4.5 V p-p on 5 V. Set OUT LEVEL so it never clips.
- The datasheet's application notes were followed: inputs AC-coupled (the FV-1 biases them internally to VDD/2), with 1k + 1 nF C0G at the pins. The outputs see more than 10k, with a coupling time constant of about 47 ms.

Files are in kicad-sandbox/mixer_reverb (generator scripts in tools/, the same flow as the other boards). Outputs are in pcb/. ERC: 0. DRC with schematic parity: 0 violations, 0 unconnected.
