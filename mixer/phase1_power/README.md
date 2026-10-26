# Phase 1: power board (design v1)

*2026-10-26. Status: circuit designed and checked in simulation (ngspice). PCB not drawn yet, nothing ordered. Prices are estimates, not checked against shops today.*

## What it does

It takes one **AC-to-AC wall adapter** and makes everything the audio side needs:

| Output | Voltage | Current (design) | Feeds |
|---|---|---|---|
| +12 V | regulated | 300 mA | op-amps, preamps (positive side) |
| −12 V | regulated | 300 mA | op-amps, preamps (negative side) |
| P48 | ~50 V, filtered | 30 mA | phantom power for 4 condenser mics |
| GND | star point | — | everything |

**Not on this board:** the 5 V digital side (ESP32, USB hub, USB audio chip, LED meters, reverb module). It runs from USB, either the PC or any phone charger plugged into a second power-only USB-C socket. That keeps noisy digital currents off the audio rails and keeps the wall adapter small.

I changed the audio rails from ±15 V in the plan to **±12 V**. With a single 15 V AC adapter, ±15 V doesn't have enough headroom when the mains voltage dips, and that would cause hum. NE5532 and THAT1512 run fine on ±12 V.

## Circuit

```
                 2 A slow fuse
 15 V AC adapter ──╫──┬───────────────► AC node "a"
 (barrel jack)        │
 other wire ──────────┼─────────────── GND (star point)
                      │
 +12 V:  a ─►|─ 1N5401 ─┬─ 6800µF 35V ─ GND ─► 7812 ─┬─ 100µF ─► +12 V   (LED + 2.2k to GND)
 −12 V:  a ─|◄─ 1N5401 ─┴─ 6800µF 35V ─ GND ─► 7912 ─┴─ 100µF ─► −12 V   (LED + 2.2k to GND)
         (each regulator: 0.33µF in, 0.1µF out, 1N4007 out→in, 1N4007 rail→GND reversed)

 P48: voltage quadrupler off "a" (4× 1N4007, 4× 1000µF 63V) ─► raw ~55–66 V
      raw ─ 3.3k 1W ─┬─ 1N4757A 51 V zener (1 W) ∥ 47µF 63V ─ GND
                     └─ base MJE340 (emitter follower), collector = raw
      emitter (~50 V) ─ 47 Ω ─┬─ 220µF 63V ─ GND ─► P48   (LED + 10k 0.5W to GND)
```

The ±12 V rails use the classic "half-wave pair" that many mixers use with an AC adapter: one diode charges the positive cap on the positive half of the AC wave, the other charges the negative cap on the negative half. The 48 V phantom comes from a voltage quadrupler (a ladder of diodes and caps that stacks up the AC peaks), then a zener + transistor regulator. The zener's 47µF cap and the output 47 Ω/220µF filter remove the remaining hum from it. Each mic channel's own 6.81 kΩ resistor pair (on the strip board) limits current, so a shorted mic cable can't hurt the regulator.

## Simulation results (ngspice, file `power_sim.cir`)

Adapter modelled as a 15 V AC source with 1.5 Ω internal resistance, 50 Hz. "Low mains" is −10 %.

| Case | Lowest + raw | Lowest − raw | P48 raw (min) | Adapter current (RMS) |
|---|---|---|---|---|
| 15 V AC, phantom 20 mA | 16.3 V | −16.3 V | 65.3 V | 1.17 A |
| 15 V AC, phantom 30 mA | 16.3 V | −16.2 V | 63.5 V | 1.20 A |
| 13.5 V AC (low mains), 30 mA | **14.3 V** | **−14.2 V** | 55.5 V | 1.18 A |
| **US 60 Hz:** 15 V AC, 30 mA | 16.3 V | −16.2 V | 63.8 V | 1.21 A |
| **US 60 Hz:** 13.5 V AC, 30 mA | 14.3 V | −14.3 V | 55.9 V | 1.19 A |

Omer is in the US (120 V, 60 Hz). 60 Hz is slightly kinder than 50 Hz, and US mains normally stays within ±5 %, so the −10 % row is a safe worst case.

The 7812/7912 need about 14 V in to give a clean 12 V, so the worst case just passes. The phantom regulator needs about 52 V in and gets 55 V or more. The earlier try with 100 µF multiplier caps failed (P48 fell below 20 V), which is why those caps are 1000 µF now.

**What this means for the adapter:** buy **15 V AC (not DC!), 1.5 A or more (about 24 VA)**. If the label says "DC" or "15V ⎓", it's the wrong kind. 16 V AC also works and gives more headroom. Its regulators then run a bit warmer, and the heatsinks cover that.

## Parts list, Phase 1

| Qty | Part | Notes | ~Price |
|---|---|---|---|
| 1 | 15 V AC wall adapter, 1.5 A, US plug: **Jameco ReliaPro ADU150150RV0650** (15 VAC, 1.5 A, 2.1 mm plug) | found at jameco.com, price/stock not checked | $12–20 |
| 1 | barrel jack, PCB mount, **2.1 mm** pin | matches the Jameco adapter | $1 |
| 1 | 2 A slow-blow fuse + PCB holder | | $1 |
| 2 | 1N5401 diode (3 A) | main rails | $0.50 |
| 8 | 1N4007 diode | 4 multiplier + 4 regulator protection | $0.50 |
| 2 | 6800 µF 35 V electrolytic | main rail reservoirs | $3 |
| 4 | 1000 µF 63 V electrolytic | multiplier | $4 |
| 1 | 220 µF 63 V electrolytic | P48 output | $0.50 |
| 1 | 47 µF 63 V electrolytic | zener filter | $0.30 |
| 2 | 100 µF 25 V electrolytic | regulator outputs | $0.30 |
| 2 | 0.33 µF film cap | regulator inputs | $0.50 |
| 2 | 0.1 µF film/ceramic cap | regulator outputs | $0.20 |
| 1 | L7812CV (TO-220) | genuine ST or onsemi | $0.60 |
| 1 | L7912CV (TO-220) | **pinout differs from 7812**, PCB handles it | $0.60 |
| 2 | TO-220 heatsink (~15 °C/W) + thermal pad | | $2 |
| 1 | MJE340 NPN (TO-126) | phantom pass transistor | $0.50 |
| 1 | 1N4757A 51 V 1 W zener | | $0.30 |
| 1 | 3.3 kΩ 1 W resistor | | $0.20 |
| 1 | 47 Ω ¼ W, 2× 2.2 kΩ ¼ W, 1× 10 kΩ ½ W | | $0.20 |
| 3 | LED 3 mm (power indicators) | | $0.30 |
| 1 | 4-pin output header + screw terminals for testing | | $1 |
| 1 | PCB, 2-layer, JLCPCB (5 pcs) | I'll design it | $5 + shipping |

**Phase 1 total: about $35–45** with the adapter.

## Parts list, Phase 2 (preliminary)

For one mono channel strip and a simple headphone output. I'll finalize it with the Phase 2 schematic, so values may still change. No need to order yet unless you want to combine shipping.

| Qty | Part | Notes |
|---|---|---|
| 2 | **THAT1512** mic preamp (DIP-8), from Mouser/DigiKey, not AliExpress | 1 + 1 spare; fakes are common elsewhere |
| 6 | NE5532 dual op-amp (DIP-8), genuine TI | EQ, buffers, headphone; includes spares |
| 1 | XLR/1/4" combo jack (PCB mount) | |
| 2 | 6.81 kΩ 0.1 % resistor | phantom feed, must match |
| 2 | 47 µF 63 V cap | phantom blocking |
| ~8 | pots: gain, hi/mid/lo EQ (centre detent), aux, FX, pan (centre detent) | exact values with schematic |
| 3 | switches: 48 V, pad, 80 Hz cut | |
| 1 | NJM4556 headphone driver + 1/4" and 3.5 mm stereo jacks + volume pot | test headphone output |
| — | resistors, film caps, IC sockets, knobs | |
| 1 | B10K fader | **already owned** |

**Phase 2 estimate: about $35–50.**

## Testing plan (when it's built)

With a multimeter, adapter plugged in, nothing else connected: +12 V and −12 V within ±0.5 V, P48 between 46 and 52 V, all three LEDs on, regulators warm but touchable after 10 minutes. I'll write the full step-by-step with a picture of the test points when the PCB is designed.

**Safety:** nothing on this board touches mains. The multiplier caps can hold about 60 V for a while after unplugging, so wait a minute or touch the P48 pin to GND through a 1 kΩ resistor before handling the board. Electrolytic caps must go in the right way round, because they can burst if reversed.

## Next

1. Draw this in KiCad and make the PCB + JLCPCB files. This uses your PC (the KiCad setup from the controller).
2. Phase 2 schematic: the mono channel strip.

## PCB (done 2026-10-26)

Files on Omer's PC in `C:\Users\pogam\kicad-mcp\mixer_power_outputs\`: `mixer_power_jlcpcb.zip` (upload to JLCPCB), schematic PDF, top render PNG, BOM CSV, ERC/DRC reports. The project is in `kicad-sandbox\mixer_power`.

- 100 × 85 mm, 2 layers, through-hole only, 4 M3 holes. ERC and DRC are clean.
- **When buying, check:** the barrel jack matches KiCad's generic 2.1 mm horizontal footprint; the 6800 µF caps are 22 mm wide with 10 mm lead spacing; the 1000 µF 63 V caps are 18 mm wide with 7.5 mm spacing. The heatsinks are Fischer SK104 (35 mm).
- **U2 (7912) is mounted insulated:** use the TO-220 insulator kit (BOM line HW1) **and** the nylon shoulder washer on the screw. Without the washer, the screw connects the tab (at about −21 V) to the heatsink.
- Output header J2 (2×5): pins 1–2 +12 V, 3–6 and 10 GND, 7–8 −12 V, 9 P48. This is not Eurorack order.
- With no mics connected, the 48 V multiplier rises to about 80 V before the regulator. All parts are rated for it. It's another reason to discharge the board before touching it.
