# Phase 3b digital board: exact parts

Links are DigiKey keyword searches unless noted. I didn't read live stock counts, so check before ordering.

| Ref | Function | Part | Qty | Link |
|---|---|---|---|---|
| — | USB 2.0 hub | FE1.1s 4-port hub module, ~29.5 x 18.9 mm, pads VCC / GND / D+ / D- in, USB1–USB4 out (JESSINIE, 5-pack) | 1 | [Amazon B0GTVPVPV9](https://www.amazon.com/JESSINIE-FE1-1S-USB-2-0-Module/dp/B0GTVPVPV9) |
| — | USB audio | PCM2902 USB audio module with line-in / line-out pads (any seller), **or** TI PCM2902CEVM-U eval board (distributor-stocked) | 1 | [TI PCM2902CEVM-U](https://www.ti.com/tool/PCM2902CEVM-U) |
| J1 | USB to PC | On Shore USB-B1HSW6 (USB-B, through-hole) | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=USB-B1HSW6) |
| J8 | 5 V in (no PC) | GCT USB4125-GF-A (USB-C power-only; 6 SMD pins at 1 mm pitch + through-hole shell legs) | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=USB4125-GF-A) |
| J13 | To the ESP32 controller | Molex 67643-2910 (USB-A, through-hole) | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=0676432910) |
| J2, J3 | MIDI IN / OUT | CUI / Same Sky SDS-50J (5-pin 180° DIN, right-angle PCB) | 2 | [DigiKey](https://www.digikey.com/en/products/result?keywords=SDS-50J) |
| U1 | MIDI IN opto | 6N138 (Vishay or Lite-On), DIP-8 + socket | 1 | [DigiKey](https://www.digikey.com/en/products/result?keywords=6N138) |
| D1, D2 | 5 V OR | 1N5817 Schottky | 2 | [DigiKey](https://www.digikey.com/en/products/result?keywords=1N5817) |
| D3 | MIDI IN reverse protection | 1N4148 | 1 | any |
| J4 | To master J4 | Würth 61201021621 (2x5 shrouded, vertical) | 1 | [Mouser](https://www.mouser.com/ProductDetail/Wurth-Elektronik/61201021621) |
| J5, J6, J7, J9–J12, J14 | Headers / wire pads | 2.54 mm pin headers (1x3, 1x4, 1x6) or just wires | — | any |

## Notes

- **Modules are wired, not plugged in.** Neither listing publishes exact pad positions, so the board gives each module a marked area plus a row of labelled 2.54 mm wire pads:
  - **HUB IN:** 5V, D−, D+, GND. The 5 V is the diode-OR rail, so the hub and its ports also work on the USB-C supply.
  - **HUB USB1 → PCM USB:** connected on the PCB.
  - **HUB USB2:** goes to the USB-A socket J13 for the controller's USB-C cable.
  - **PCM LINE IN/OUT:** L-in, R-in, GND, L-out, R-out, GND.

  Mount the modules with foam tape or nylon standoffs. Keep the USB wires short and twist each D+/D− pair.
- **USB-C:** the GCT USB4125 isn't fully through-hole. Its 6 signal pins are SMD pads on a 1 mm pitch, which are fine with a normal iron. The two 5.1 kΩ resistors on CC1/CC2 are required, or a USB-C charger won't supply 5 V.
- **DIN shell:** the shell pins are mechanical only. MIDI OUT grounds pin 2; MIDI IN leaves pin 2 and the shell open, as the MIDI spec requires.
