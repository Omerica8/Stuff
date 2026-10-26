# AliExpress shopping list: controller PCB

Checked against `controller_bom.csv` and the latest schematic (`controller_schematic.pdf`). The schematic has the same parts as the BOM, so nothing new was added after it. The TFT screen is left out because it's on hold.

Prices are rough AliExpress prices in USD, before shipping. They change a lot between sellers.

## Need to buy

| # | Item | Search term | Qty | Rough price | Why |
|---|------|-------------|-----|-------------|-----|
| 1 | Female pin header strips, 2.54 mm, single row, 40 pin | `2.54mm female header 1x40 single row` | 1 pack of 10 | $1–2 | Cut two 1x22 pieces (J1, J2) so the ESP32 DevKit plugs into the board instead of being soldered in. Also cut one 1x6 piece (J4) for the TFT header so it's ready later. Cutting strips loses one pin per cut, so 10 strips leaves plenty spare. |
| 2 | Solder wire, 63/37 rosin core, 0.6–0.8 mm | `63/37 solder wire 0.8mm rosin core 100g` | 1 roll (50–100 g) | $3–6 | Every part on the board is through-hole. Leaded 63/37 is the easiest to work with. |
| 3 | Flux pen or no-clean flux paste | `no clean flux pen` or `RMA-223 flux` | 1 | $2–4 | Helps the solder flow on the ground pads and makes fixing mistakes easier. |
| 4 | Desoldering wick, 2–2.5 mm | `desoldering wick 2.5mm` | 1 | $1–2 | To remove solder when you need to fix a joint. |

**Total for the must-haves: about $7–14.**

## Worth buying if you don't already have them

| # | Item | Search term | Qty | Rough price | Why |
|---|------|-------------|-----|-------------|-----|
| 5 | Soldering iron, temperature controlled | `TS101 soldering iron` (or `T12 soldering station`) | 1 | $15–45 | Only if your current iron has no temperature control. |
| 6 | Flush cutters | `170 flush cutter` | 1 | $2–3 | To trim leads after soldering, and to cut the header strips. |
| 7 | Fader knobs for 45 mm slide pots, 4 mm T-shaft | `slide potentiometer knob 4mm` | 10 | $2–4 | Your faders probably don't come with caps. Check the shaft on yours before ordering, since some are 3 mm. |
| 8 | Encoder knobs, 6 mm D-shaft | `6mm D shaft knob aluminum` | 10 | $3–6 | For the EC11 encoders, which have a 15 mm D shaft. |
| 9 | M3 nylon standoffs kit | `M3 nylon standoff kit` | 1 kit | $3–5 | To lift the PCB off the case floor. You already have the M3 screws and inserts. |
| 10 | Isopropyl alcohol 99% + small brush | (buy locally) | 1 | $3–5 | Cleans flux residue off the board. Cheaper at a local shop than shipped. |

## Already owned (don't buy)

| Item | Board parts it covers |
|------|----------------------|
| ESP32-S3 N16R8 DevKit | plugs into J1 and J2 |
| 10x B10K 45 mm slide pots | RV1–RV4 (4 used, 6 spare for side modules) |
| 10x EC11 encoders with push | ENC1–ENC4 (4 used) |
| Tact switch kit (6x6 and 7x7) | SW1–SW4 (6x6) and SW5 power latch (7x7). The board is drawn for 13 mm tall 6x6 buttons. Your 16 mm ones fit the same holes and just sit 3 mm taller. |
| LED kit | D1–D4 (5 mm) |
| 1/4 W resistor kit | R1–R8, all 330 Ω |
| M3 screws and heat-set inserts | case mounting |
| Breadboards and jumpers | testing before soldering |

## Not from AliExpress

The PCB itself comes from JLCPCB using `controller_jlcpcb.zip` (the newest upload). 5 boards cost about $2–5 plus shipping. You can order it together with this list so everything shows up around the same time.
