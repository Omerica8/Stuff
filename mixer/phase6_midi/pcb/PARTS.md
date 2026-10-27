# Phase 6 MIDI hub: exact parts

Links are DigiKey keyword searches. I didn't read live stock counts or prices, so check them before ordering.

| Ref | Function | Part | Qty | Link |
|---|---|---|---|---|
| — | MCU module | Raspberry Pi Pico (RP2040), SC0915, **without** pre-soldered headers, plus 2× male 1×20 header strips soldered to it | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=SC0915) |
| J10, J11 | Pico sockets | Female 1×20, 2.54 mm (Samtec SSW-120-01-T-S or any) | 2 | [DigiKey](https://www.digikey.com/en/products/result?keywords=SSW-120-01-T-S) |
| J1–J8 | MIDI IN 1–5, OUT 1–3 | CUI / Same Sky SDS-50J (5-pin 180° DIN, right-angle PCB) | 8 | [DigiKey](https://www.digikey.com/en/products/result?keywords=SDS-50J) |
| U1–U5 | MIDI IN optos | 6N138 (Vishay or Lite-On), DIP-8, plus DIP-8 sockets | 5 | [DigiKey](https://www.digikey.com/en/products/result?keywords=6N138) |
| J9 | USB host port | Molex 67643-2910 (USB-A, through-hole) | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=0676432910) |
| F1 | Host port fuse | Bourns MF-R050 (0.5 A hold PTC, radial, 5.1 mm leads) | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=MF-R050) |
| D1–D5 | MIDI IN reverse protection | 1N4148 | 5 | any |
| R1–R5 | Opto LED | 220 Ω | 5 | any |
| R11–R15, R21–R25 | Opto speed-up / pull-up | 10 kΩ, 1 kΩ | 5 + 5 | any |
| R31–R33, R41–R43 | MIDI OUT | 33 Ω, 10 Ω | 3 + 3 | any |
| R51, R52 | USB host series | 22 Ω | 2 | any |
| C1–C5, C11, C14 | Decoupling | 100 nF ceramic, 2.5 mm | 7 | any |
| C12 | Pico VBUS bulk | 10 µF 25 V, 5 mm radial | 1 | any |
| C13 | Host VBUS bulk | 100 µF 10 V, 8 mm radial | 1 | any |
| — | Link to the hub | Short USB-A-to-micro-B cable: cut the A end off and solder its 4 wires to the hub module's USB3 pads (red 5V, white D−, green D+, black GND) | 1 | any |

## Notes

- The Pico sits in sockets so it can be swapped or reflashed out of the board. With sockets it's about 11 mm tall.
- The micro-USB end of the Pico faces left (toward MIDI IN 1). Leave room for the cable plug in the case.
- **DIN shell:** the shell pins are mechanical only. The OUTs ground pin 2. The INs leave pin 2 and the shell open, as the MIDI spec requires.
