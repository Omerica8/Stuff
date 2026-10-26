# Phase 3 master section: exact parts

Footprints on the PCB come from these parts' datasheets (or from KiCad's own library footprint for the part). Stock was checked on 2026-10-26; "check" means I couldn't read a live stock count, so confirm before ordering.

| Ref | Function | Manufacturer part number | Qty | One US distributor |
|---|---|---|---|---|
| RV1, RV2 | FX RETURN, MONITOR | Alpha RD901F-40-15R1-A10K (9 mm vertical, log) | 2 | [Tayda A-1856](https://www.taydaelectronics.com/10k-ohm-logarithmic-taper-potentiometer-round-shaft-pcb-9mm.html) (1766 in stock) |
| RV3 | PHONES | Alpha RD902F-40-15R1-A10K (9 mm vertical **dual**, log) | 1 | [Tayda A-6980](https://www.taydaelectronics.com/10k-ohm-logarithmic-dual-taper-potentiometer-round-shaft-pcb-9mm.html) (700 in stock) |
| RV4 | MASTER fader | Bourns PTA6044-2015DPA103 (60 mm, **dual gang**, 10k audio, 15 mm metal lever) | 1 | [Mouser](https://www.mouser.com/ProductDetail/Bourns/PTA6044-2015DPA103?qs=U/acTlguYxZvBk/zeZBsew%3D%3D) (check; DigiKey shows a 21-week lead time) |
| SW1 | PHONES SOURCE | C&K PVA2 EE H2 1.7N V2 (push-push latching DPDT) | 1 | [DigiKey 108-PVA2EEH21.7NV2-ND](https://www.digikey.com/en/products/detail/c-k/PVA2-EE-H2-1.7N-V2/401-1142-ND/417722) |
| J1, J6 | MAIN OUT L/R XLR | Neutrik NC3MAAV (XLR male, vertical PCB) | 2 | [Full Compass](https://www.fullcompass.com/prod/583920-neutrik-nc3maav-aa-series-3-pin-xlr-m-pcbv-panel-mount-connector-black-gold) (limited stock; LCSC has 195) |
| J7, J8, J9, J10 | MAIN L/R TRS, MONITOR, PHONES 1/4" | Neutrik NJ3FD-V (1/4" stereo, vertical PCB) | 4 | [Mouser](https://www.mouser.com/ProductDetail/Neutrik/NJ3FD-V) (check) |
| J11 | PHONES 3.5 mm | Thonkiconn stereo WQP419GR (sold as PJ366ST) | 1 | [Synthrotek](https://store.synthrotek.com/35mm-Stereo-PCB-Mount-Jacks_p_761.html) |
| U5, U6 | Balanced line drivers | TI DRV134PA (DIP-8) | 2 | [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/DRV134PA) (check) |
| U7 | Headphone amp | Nisshinbo (NJR) NJM4556AD (DIP-8) | 1 | [Mouser](https://www.mouser.com/ProductDetail/Nisshinbo/NJM4556AD) (check) |
| U9, U10 | Meter drivers | TI LM3915N-1 (DIP-18) — **obsolete**, or NTE1509 (direct replacement) | 2 | [Jameco](https://www.jameco.com/shop/keywordsearch?keyword=LM3915) (about 117 listed, unverified); NTE1509 from [Mouser](https://www.mouser.com/ProductDetail/NTE-Electronics/NTE1509) |
| U1–U4 | Summing, FX return / monitor, master gain | TI NE5532P | 4 | [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/NE5532P) |
| U8 | Peak detectors | TI TL072CP | 1 | [Mouser](https://www.mouser.com/ProductDetail/Texas-Instruments/TL072CP) |
| J2, J3, J4 | Power, bus, digital board | Würth 61201021621 (2x5 shrouded, vertical) | 3 | [Mouser](https://www.mouser.com/ProductDetail/Wurth-Elektronik/61201021621) |
| J5 | Reverb module | 1x4 2.54 mm pin header | 1 | any |
| D1–D20 | Meter LEDs, 3 mm | per side: LEDs 1–7 green, 8–9 yellow, 10 red | 20 | any 3 mm diffused LEDs |

## Notes

- **Fader footprint (check before ordering).** KiCad has no dual PTA footprint, so I drew one from the PTA datasheet's PTAxx44 drawing. Pins 1–3 are 73.5 mm apart, the mounting legs are 62.8 mm and 65.2 mm apart, the wipers are 63 mm apart, and the pin rows sit ±1.75 mm and ±0.95 mm from the centre line. That drawing isn't to scale, so a few positions come from symmetry. When the fader arrives, lay it on a 1:1 print of the assembly PDF.
- **3.5 mm jack footprint.** This is KiCad's PJ398SM (mono Thonkiconn) footprint, made 1 mm wider, with the switch pin used as Ring. That's how the vendors describe the stereo WQP419GR / PJ366ST. Check it against the part.
- **LM3915 is end-of-life.** NTE1509 has the same pinout and function. There are also plenty of LM3915N-1 on eBay, but those are often fakes.
- Everything else (resistors, caps, diodes, sockets) is in mixer_master_bom.csv.
