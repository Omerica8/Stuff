# Battery power for the synth

Runs the synth from Omer's salvaged toy-quadcopter cells (1S LiPo, 3.7 V, about 350 mAh each). Only useful away from the PC: when the synth plays from FL over USB, the USB cable powers it anyway.

## Check the cells first

Toy-drone cells usually have **no protection circuit** and may have sat flat for months. For each cell, with a multimeter:

| Cell voltage / look | What to do |
|---|---|
| 3.0-4.2 V, flat and undamaged | OK to use |
| 2.5-3.0 V | Charge it slowly (below) and watch it the first time; bin it if it gets warm or won't pass 4.1 V |
| Below 2.5 V, puffy, dented, torn wrap or cut wires | Don't use. Tape the leads and take it to a battery drop-off (Home Depot, Lowe's, Best Buy) |

Charge and use them on a non-flammable surface the first few times, never unattended.

## Parts (about $3-5)

| Qty | Part | Note |
|---|---|---|
| 1 | **TP4056 charger board with protection** (has a DW01A chip and 6 pads: IN+, IN-, B+, B-, OUT+, OUT-) | The protection cuts off below about 2.5 V and on a short, which the bare cells don't have. Not the 4-pad version without DW01 |
| 1 | **MT3608 boost module** | Set it to 5.0 V with a multimeter **before** connecting the ESP32 |
| 1 | Small SPDT slide switch | On/off |

**Change the TP4056's charge resistor.** It ships set to 1 A, which is about 3x too much for a 350 mAh cell. Replace the resistor marked R3 (or "PROG", usually 122 = 1.2 kΩ) with **4.7 kΩ** for about 250 mA, which is safe. (Charge current ≈ 1200 / R.)

The [PC fader's PowerBoost 1000C](../pc-fader/BATTERY.md) is not a good fit here: it charges at 1 A with no easy way to lower it.

## Wiring

```
cell + ──> TP4056 B+        TP4056 OUT+ ──> switch ──> MT3608 VIN+
cell - ──> TP4056 B-        TP4056 OUT- ─────────────> MT3608 VIN-
                            MT3608 VOUT+ (5.0 V) ────> ESP32 devkit 5V pin
                            MT3608 VOUT-  ───────────> ESP32 devkit GND
```

The PCM5102A board keeps taking its power from the devkit's 5V pin as in [step 1](step1_dac_tone/README.md). Charge through the TP4056's own USB socket with the switch off: the red LED means charging, blue/green means full.

**Switch the battery off before plugging USB into the devkit** (for flashing or FL). Otherwise the PC's 5 V and the boost's 5 V fight.

Two cells can go in parallel for twice the runtime, but only if they're the same type and within 0.05 V of each other when you join them.

## Runtime

Rough estimate, current at 3.3 V: ESP32-S3 running audio on both cores about 80-100 mA (no Wi-Fi), PCM5102A about 20 mA, TFT backlight about 50 mA once the screen is added. Boost and the devkit's 3.3 V regulator lose about 45% on the way.

| Setup | One 350 mAh cell | Two in parallel |
|---|---|---|
| Step 1 (ESP32 + DAC) | about 1.5 h | about 3 h |
| With TFT | about 1 h | about 2 h |

Measure the real draw with a multimeter in series once it's built; these are estimates, not measurements.

## Noise

The MT3608 switches at about 1.2 MHz, which can leak into the audio as hiss or a whine. The PCM5102A has its own regulators, so it's usually fine. If you hear it, add a 100 µF electrolytic + 0.1 µF ceramic across the devkit's 5V and GND pins.
