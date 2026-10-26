# Phase 4 stereo strip: exact parts (per board)

Build it twice:
- **Stereo line strip:** fit everything. JP1 and JP2 stay open.
- **USB-return strip:** leave out J8, J9 and J10, and put jumper caps on JP1 and JP2. J7 is fed from the digital board's J7.

Stock was checked on 2026-10-26; "check" means I couldn't read a live count.

| Ref | Function | Manufacturer part number | Qty | One US distributor |
|---|---|---|---|---|
| J8, J9 | IN L / IN R | Neutrik NJ5FD-V (1/4" stereo, vertical PCB, switches on tip and ring) | 2 | [Mouser](https://www.mouser.com/ProductDetail/Neutrik/NJ5FD-V) (check) |
| J10 | AUX 3.5 mm | Thonkiconn stereo WQP419GR (sold as PJ366ST) | 1 | [Synthrotek](https://store.synthrotek.com/35mm-Stereo-PCB-Mount-Jacks_p_761.html) |
| RV1, RV2 | HIGH, LOW | Alpha RD902F-40-15R1-B10K (9 mm vertical **dual**, linear; **no centre detent**, none stocked) | 2 | [Tayda A-6433](https://www.taydaelectronics.com/10k-ohm-linear-dual-taper-potentiometer-round-shaft-pcb-9mm.html) (561 in stock) |
| RV3, RV5 | AUX, FX | Alpha RD901F-40-15R1-A10K | 2 | [Tayda A-1856](https://www.taydaelectronics.com/10k-ohm-logarithmic-taper-potentiometer-round-shaft-pcb-9mm.html) (1766) |
| RV6 | BAL | Alpha RD901F-40-15R1-B10K-0CD (centre detent) | 1 | [Tayda A-8401](https://www.taydaelectronics.com/b10k-ohm-taper-potentiometer-round-shaft-pcb-9mm-with-center-detent.html) (721) |
| RV4 | Fader | Bourns PTA6044-2015DPA103 (60 mm, dual gang, 10k audio) | 1 | [Mouser](https://www.mouser.com/ProductDetail/Bourns/PTA6044-2015DPA103?qs=U/acTlguYxZvBk/zeZBsew%3D%3D) (check; DigiKey shows a 21-week lead time) |
| U1–U4 | Receivers, EQ, averagers, fader buffers | TI NE5532P | 4 | [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/NE5532P) |
| U5, U6 | PEAK windows | LM393P / LM393N | 2 | [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/LM393P) |
| J2, J3 | Power, bus | Würth 61201021621 | 2 | [Mouser](https://www.mouser.com/ProductDetail/Wurth-Elektronik/61201021621) |
| J7, JP1, JP2 | USB in, USB-build jumpers | 2.54 mm headers 1x3, 1x2 (+2 jumper caps for the USB build) | — | any |

Everything else is in mixer_stereo_bom.csv. The dual-fader footprint is the same one as on the master, drawn from the PTA datasheet, so give it the same 1:1-print check against the real part.
