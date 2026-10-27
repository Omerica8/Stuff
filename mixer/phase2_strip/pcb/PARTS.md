# Phase 2 mic strip: exact parts (per strip)

Footprints on the PCB were drawn from these parts' datasheets. If you substitute a part, check that it has the same pin geometry.

| Ref | Function | Manufacturer part number | Qty | One distributor |
|---|---|---|---|---|
| RV1 | GAIN | Alpha RD901F-40-15R1-C10K (9 mm vertical, C = reverse-log, 6.35 mm round shaft, M7 bushing) | 1 | [Tayda](https://www.taydaelectronics.com/c10k-ohm-taper-potentiometer-round-shaft-pcb-9mm.html) (698 in stock on 2026-10-26) |
| RV2, RV3, RV4, RV8 | MID, HIGH, LOW, PAN | Alpha RD901F-40-15R1-B10K-0CD (9 mm vertical, B = linear, **centre detent**) | 4 | [Tayda A-8401](https://www.taydaelectronics.com/b10k-ohm-taper-potentiometer-round-shaft-pcb-9mm-with-center-detent.html) (721 in stock) |
| RV5, RV7 | AUX, FX | Alpha RD901F-40-15R1-A10K (9 mm vertical, A = log) | 2 | [Tayda A-1856](https://www.taydaelectronics.com/10k-ohm-logarithmic-taper-potentiometer-round-shaft-pcb-9mm.html) (1766 in stock) |
| RV6 | Fader | Bourns PTA6043-2015DPA103 (60 mm travel, 10k audio taper, 15 mm lever) | 1 | [RS 737-7786](https://se.rs-online.com/web/p/potentiometers/7377786) |
| SW1, SW2, SW3 | 48V, PAD, 80Hz | C&K PVA2 EE H2 1.7N V2 (push-push latching DPDT, 23 mm total height) | 3 | [DigiKey 108-PVA2EEH21.7NV2-ND](https://www.digikey.com/en/products/detail/c-k/PVA2-EE-H2-1.7N-V2/401-1142-ND/417722) |
| J1 | Mic/line input | Neutrik NCJ6FA-V (combo XLR + 1/4" TRS, vertical PCB) | 1 | [Full Compass](https://www.fullcompass.com/prod/532035-neutrik-ncj6fa-v-xlrf-1-4-trs-combo-jack-with-vertical-pcb-mount) |
| J2, J3 | Power, bus | Würth 61201021621 (WR-BHD 2x5 shrouded box header, 2.54 mm, vertical) | 2 | [RS 121-6784](https://uk.rs-online.com/web/p/pcb-headers/1216784) |

## Notes

- **Pots (RD901F-40):** these are 9 mm vertical pots. The shaft points straight up out of the PCB and the body sits on the board. The 3 pins are on a 2.5 mm pitch, 7.5 mm from the shaft, with 2 support lugs; the footprint is KiCad's Potentiometer_Alpha_RD901F-40-00D_Single_Vertical. The M7 bushing takes the supplied nut, so the panel needs 7.5 mm holes. Use knobs for a 6.35 mm (1/4") round shaft, about 12–15 mm across; the pots are spaced 18–19 mm apart. The pot comparison and the reasons for choosing these are in POT_OPTIONS.md.
- **Centre detents:** HIGH, MID, LOW and PAN use the centre-detent B10K (-0CD). Alpha's plain RD901F-40-15R1-B10K (Tayda A-1847) has the same footprint if you'd rather have no click.
- **Switches (PVA2 EE):** this is the push-push (latching) version. OA is the momentary version, so don't order that. Each pole has a middle common pin "0", plus pin "1", closed when the button is out, and pin "2", closed when it's latched in. The module fits into the board either way round. Line up the "1" moulded on the housing with the silkscreen "1" next to each switch. Wired that way: PAD latched = −20 dB pad on, 48V latched = phantom on, 80Hz latched = filter in. H2 is 23 mm tall (made for F-buttons); H1 (17.5 mm) has the same footprint if your panel height suits it better.
- **Fader:** PTA6043-2015DP**A**103 is the audio taper. DP**B**103 is linear, so don't mix them up. Lead times vary a lot between distributors, so check stock first.
- **Jack:** NCJ6FA-V is the plain version. NCJ6FA-V-0 adds a retention spring and has the same footprint.
- **Fader meter ICs (U6 TL072, U7 LM339):** their footprints have no socket outline because the lane beside the fader is only 10 mm wide. Solder them directly or use turned-pin sockets, which still fit. The fader uses a local copy of the Bourns footprint (mixer_strip.pretty) with a 0.25 mm courtyard; pads are unchanged.
- Everything else (resistors, caps, ICs, sockets, diodes, LED) is in mixer_strip_bom.csv.
