# Phase 2 mic strip: exact parts (per strip)

Footprints on the PCB were drawn from these parts' datasheets. If you substitute a part, check that it has the same pin geometry.

| Ref | Function | Manufacturer part number | Qty | One distributor |
|---|---|---|---|---|
| RV1 | GAIN | Alpha RV16AF-41-15R1-C10K-30H4 (16 mm, C = reverse-log, 15 mm knurled shaft) | 1 | [Adafruit 5263](https://www.adafruit.com/product/5263) (also at Jameco) |
| RV2, RV3, RV4, RV8 | MID, HIGH, LOW, PAN | Alpha RV16AF-41-15R1-B10K-30H4 (16 mm, B = linear) | 4 | [Rapid Online 66-0363](https://www.rapidonline.com/taiwan-alpha-rv16af-41-10k-linear-16mm-metal-case-pc-mount-potentiometer-66-0363) (Adafruit 5280 is discontinued) |
| RV5, RV7 | AUX, FX | Alpha RV16AF-41-15R1-A10K-30H4 (16 mm, A = log) | 2 | [Rapid Online 66-0353](https://www.rapidonline.com/taiwan-alpha-rv16af-41-10k-log-16mm-metal-case-pc-mount-potentiometer-66-0353) |
| RV6 | Fader | Bourns PTA6043-2015DPA103 (60 mm travel, 10k audio taper, 15 mm lever) | 1 | [RS 737-7786](https://se.rs-online.com/web/p/potentiometers/7377786) |
| SW1, SW2, SW3 | 48V, PAD, 80Hz | C&K PVA2 EE H2 1.7N V2 (push-push latching DPDT, 23 mm total height) | 3 | [DigiKey 108-PVA2EEH21.7NV2-ND](https://www.digikey.com/en/products/detail/c-k/PVA2-EE-H2-1.7N-V2/401-1142-ND/417722) |
| J1 | Mic/line input | Neutrik NCJ6FA-V (combo XLR + 1/4" TRS, vertical PCB) | 1 | [Full Compass](https://www.fullcompass.com/prod/532035-neutrik-ncj6fa-v-xlrf-1-4-trs-combo-jack-with-vertical-pcb-mount) |
| J2, J3 | Power, bus | Würth 61201021621 (WR-BHD 2x5 shrouded box header, 2.54 mm, vertical) | 2 | [RS 121-6784](https://uk.rs-online.com/web/p/pcb-headers/1216784) |

## Notes

- **Pots (RV16AF-41):** the pins are bent back, so the shaft points straight up out of the PCB. There are 3 pins on a 5 mm pitch, 16 mm from the shaft, in 1.3 mm holes. The pot stands on its legs with the body about 3.5 mm above the board, and only the legs and the panel nut hold it, so tighten the nut. There is an anti-rotation lug 7.8 mm from the shaft on the panel side: drill a 3 mm hole in the panel for it, or snap it off. Leave room for the 17 mm body when spacing knobs.
- **Centre detents:** Alpha's ordering code has a centre-click option, but I found no stocked centre-detent version of the RV16AF-41 B10K at a US distributor. HIGH, MID, LOW and PAN therefore use the plain B10K. StompBoxParts sells a "16 mm short PCB leg, centre detent" pot (SKU POT-41-C), but they don't list its resistance; check that it's 10k linear with the RV16AF-41 pin layout before using it.
- **Switches (PVA2 EE):** this is the push-push (latching) version. OA is the momentary version, so don't order that. Each pole has a middle common pin "0", plus pin "1", closed when the button is out, and pin "2", closed when it's latched in. The module fits into the board either way round. Line up the "1" moulded on the housing with the silkscreen "1" next to each switch. Wired that way: PAD latched = −20 dB pad on, 48V latched = phantom on, 80Hz latched = filter in. H2 is 23 mm tall (made for F-buttons); H1 (17.5 mm) has the same footprint if your panel height suits it better.
- **Fader:** PTA6043-2015DP**A**103 is the audio taper. DP**B**103 is linear, so don't mix them up. Lead times vary a lot between distributors, so check stock first.
- **Jack:** NCJ6FA-V is the plain version. NCJ6FA-V-0 adds a retention spring and has the same footprint.
- Everything else (resistors, caps, ICs, sockets, diodes, LED) is in mixer_strip_bom.csv.
