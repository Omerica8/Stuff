<!-- sources: mixer/phase2_strip/pcb/PARTS.md mixer/phase3_master/pcb/PARTS.md mixer/phase3b_digital/pcb/PARTS.md mixer/phase4_stereo/pcb/PARTS.md mixer/phase5_reverb/pcb/PARTS.md shopping/ controller/controller_bom.csv -->
# Parts and sourcing

Omer is in the US (120 V / 60 Hz), so use US distributors (DigiKey, Mouser, Tayda, Jameco). Take part sizes from datasheets rather than asking Omer to measure, and check fit with a 1:1 paper print. Stock and prices in the PARTS.md files weren't read live, so confirm before ordering.

## Where the lists are

| List | File |
|---|---|
| Exact parts per mixer board | `mixer/phase*/pcb/PARTS.md` |
| BOM csv per board | `mixer/phase*/pcb/*_bom.csv` |
| Controller BOM | `controller/controller_bom.csv`, `controller_bom_pcbway.csv` |
| Controller soldering supplies (AliExpress) | [shopping/aliexpress_pcb_shopping_list.md](../shopping/aliexpress_pcb_shopping_list.md) |

## Already owned (controller)

ESP32-S3 N16R8 DevKitC-style clone (2 USB-C), 2.8" ILI9341 240×320 SPI TFT with touch (11-pin), 10× 45 mm B10K faders (30 mm travel), 10× EC11 encoders (15 mm half shaft), tact buttons (16 mm tall), LEDs, resistor kit, M3 screws and heat-set inserts.

## Key mixer parts

| Part | Use |
|---|---|
| THAT1512 (genuine, Mouser/DigiKey) | Mic preamp, one per mono strip |
| NE5532, TL072, NJM4556AD, LM393 | Op-amps, phones driver, peak detector |
| DRV134PA | Balanced main outs |
| Bourns PTA6043-2015DPA103 | 60 mm A10K mono strip fader |
| Bourns PTA6044-2015DPA103 | 60 mm dual A10K, master and stereo strips |
| Alpha RD901F-40-15R1 / RD902F | 9 mm pots (C10K gain, B10K centre detent EQ/pan via Tayda A-8401, A10K sends via Tayda A-1856) |
| C&K PVA2 EE H1 1.7N V2 latching | Strip switches (needs a ~9.8 × 10.4 mm rectangular panel hole) |
| Neutrik NCJ6FA-V, NJ5FD-V, NC3MAAV | Combo inputs, stereo inputs, XLR outs |
| NTE1509 | LM3915 replacement (LM3915N-1 is obsolete) |
| PCM2902 module, FE1.1s hub module (Amazon JESSINIE B0GTVPVPV9) | Digital board |
| Akizuki AE-FV-1-DIP | Reverb (may need ZenMarket proxy for US) |
| Jameco ReliaPro ADU150150RV0650 | 15 VAC 1.5 A wall adapter, 2.1 mm (price unchecked) |

## Order first (long lead)

- C&K PVA2 switches: about 15 weeks.
- Bourns PTA6044 dual faders: up to 21 weeks at DigiKey.
- NTE1509.
