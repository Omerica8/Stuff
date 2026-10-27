# Phase 5 reverb carrier: exact parts

Stock and shipping weren't checked live on 2026-10-27, so confirm before ordering.

| Ref | Function | Manufacturer part number | Qty | One distributor |
|---|---|---|---|---|
| M1 | FV-1 reverb module | Akizuki Denshi **AE-FV-1-DIP** (Spin FV-1 with crystal, pull-ups and clip LED on a 25.5 × 19 mm board, 2 × 9 pins, 600 mil rows) | 1 | [Akizuki K-15566](https://akizukidenshi.com/catalog/g/g115566/). It's a Japanese shop, so order through a proxy (ZenMarket, Buyee) if they won't ship to the US. |
| M1 socket | Lets the module plug in | 2 × 1×9 female header strips, 2.54 mm (e.g. Samtec SSW-109-01-T-S, or any) | 2 | any |
| U1 | 3.3 V regulator | Microchip MCP1700-3302E/TO (TO-92) | 1 | [DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/MCP1700-3302E-TO/652677) |
| U3 | Output buffer | Microchip MCP6002-I/P (rail-to-rail dual op-amp, DIP-8) | 1 | [DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/MCP6002-I-P/500446) |
| U2 | Custom programs (optional) | Microchip 24LC32A-I/P (DIP-8) | 0–1 | [DigiKey](https://www.digikey.com/en/products/detail/microchip-technology/24LC32A-I-P/273432) |
| U2, U3 sockets | | DIP-8 sockets | 2 | any |
| RV1 | IN LEVEL | Bourns 3296W-1-103LF (10k multi-turn trimmer) | 1 | DigiKey / Mouser |
| RV2, RV3, RV4 | POT0 / POT1 / POT2 (reverb time, HF, LF on programs 6/7) | Bourns 3296W-1-103LF | 3 | DigiKey / Mouser |
| RV5 | OUT LEVEL | Bourns 3296W-1-203LF (20k) | 1 | DigiKey / Mouser |
| SW1 | Program select | 3-position DIP switch, 2.54 mm (e.g. CTS 206-3) | 1 | any |
| JP1 | ROM / EEPROM | 1×2 pin header + jumper cap | 1 | any |
| J1 | To the master J5 | 1×4 pin header, 2.54 mm, plus a 4-wire female–female cable | 1 | any |
| C10, C12 | Input RF filter | 1 nF **C0G/NP0** ceramic, 2.5 mm | 2 | any |

Everything else (resistors, the other caps) is in mixer_reverb_bom.csv.

## Notes

- **Module pinout (check it on the real board before you solder the socket strips).** I took it from Akizuki's PDF and numbered it like a DIP. The left row, from the top, is 1 LIN, 2 RIN, 3 MID, 4 GND, 5 AVDD, 6 DVDD, 7 T0, 8 SCL, 9 SDA. The right row, from the bottom, is 10 S0, 11 S1, 12 S2, 13 DVDD, 14 POT0, 15 POT1, 16 POT2, 17 ROUT, 18 LOUT. The square pad on the carrier is pin 1.
- **Programs.** With JP1 fitted, the FV-1 runs its 8 internal programs. SW1 picks the program: a switch ON pulls its bit to 0, and all three OFF is program 7, "Reverb 2" (made for consoles). Program 6 is "Reverb 1". Programs 0–2 are chorus, flange and tremolo with reverb, and 3–4 are pitch shift. To run your own programs, fit a programmed 24LC32A in U2 and pull the JP1 jumper.
- **Setting the trims.** Start with IN LEVEL at about half way. Send a loud mic through the FX knob and turn IN LEVEL up until the module's clip LED just flickers on peaks, then back it off a little. Then set OUT LEVEL so the reverb return is as loud as you want at FX RETURN "12 o'clock". POT0–2 set the reverb time and tone; set them by ear.
- **Power.** The carrier runs from the +5 V on the master's J5. That's the USB side, so it keeps working without the wall adapter. It draws about 20 mA.
