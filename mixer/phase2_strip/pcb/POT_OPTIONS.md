# Pot options for a shorter strip

*2026-10-26. Goal: replace the Alpha RV16AF-41, whose legs put the pins 16 mm from the shaft and make the strip 416 mm long. The replacement needs: shaft square to the PCB, panel-mount threaded bushing, and US stock in C10K (GAIN), B10K with centre detent (HIGH/MID/LOW/PAN) and A10K (AUX/FX).*

## Why 16 mm pots stay long

On this strip the PCB sits parallel to the front panel, so the shaft has to stand straight up from the board. Every 16–17 mm pot built that way brings its terminals out at the edge of the body and bends them toward the PCB. That puts the pin row a long way from the shaft:

| Pot | Pin style | Pin row from shaft | Notes |
|---|---|---|---|
| Alpha RV16AF-41 (current) | legs bent back | **16.0 mm** | pot stands on its legs |
| Bourns PDB181-**P** | legs bent back | **16.5 mm** | same idea |
| TT P160KN**PD**, Bourns PDB181-**D**, Alpha RV16AF-**30** | pins bent forward | 10.9–11.7 mm | the pot hangs **behind** the PCB and its bushing goes through a 7.5 mm hole in the board (plus a 3 mm lug hole). The PCB then sits only ~4 mm behind the panel, which doesn't fit the vertical combo jack, the fader or the switches. Rejected. |
| Bourns PDB181-K/A/B, TT P160KN/KN2, Alps RK163 | "vertical"/"side adjust" | — | shaft is **parallel** to the PCB (front-panel-edge mounting). Wrong orientation. |

TT P160 and Bourns PDB18 do offer all three tapers with a centre detent, but only in the long or behind-the-board styles above.

## 9 mm pots: the short option

| Family | Mount | Pins | C10K | B10K centre detent | A10K | Bushing | US stock |
|---|---|---|---|---|---|---|---|
| **Alpha RD901F-40** | vertical (shaft up), pins straight down | 3 × 2.5 mm pitch, row **7.5 mm** from shaft; 2 support lugs 9.6 mm apart | RD901F-40-15R1-C10K | **RD901F-40-15R1-B10K-0CD** | RD901F-40-15R1-A10K | M7 threaded, nut + washer | Tayda: C10K 698, B10K-0CD 721, A10K 1766 (also plain B10K 2423) |
| Bourns PTV09A-4 / -1 / -6 | vertical ("horizontal/rear mount"), same idea | 3 × 2.5 mm, row 7.0 mm from shaft; lugs 8.8 mm apart | C taper in catalogue, none found stocked | PTV09A-**4225F**-B103 (Mouser 145 pcs, DigiKey) | A taper available | **-4 is bushingless** (no panel nut); the threaded -6 / sleeve -1 aren't stocked in 10k | partial |
| Alps RK09K | vertical | 3 × 2.5 mm, row ~7 mm | no C10K found | not found | RK09K1130BGM (Newark) | threaded | partial, some NLM |

Bourns PTV09 and Alps RK09K each miss one taper, or the panel bushing, at US stock. Alpha RD901F-40 is the only family with all three tapers, the centre detent and a threaded bushing, all in stock at one shop. KiCad also ships its exact footprint (Potentiometer_Alpha_RD901F-40-00D_Single_Vertical).

## Recommendation: Alpha RD901F-40 (9 mm), one footprint for all seven pots

- GAIN: RD901F-40-15R1-C10K (Tayda)
- HIGH, MID, LOW, PAN: RD901F-40-15R1-B10K-0CD (centre detent, Tayda SKU A-8401)
- AUX, FX: RD901F-40-15R1-A10K (Tayda SKU A-1856)
- All 15 mm round 6.35 mm shafts with an M7 bushing. A 9 mm pot needs a knob of about 12–15 mm. The pots sit at an 18–19 mm pitch.

**Estimated strip length: about 340 mm** (from 416). The pot footprint shrinks from 26 × 17 mm to 14 × 13 mm, so the pots are limited only by knob spacing, and the side lanes widen to about 8 mm. What's left of the length is the combo jack (28 mm), the fader (75 mm), the five DIP sockets and the headers.

Trade-offs: 9 mm pots feel lighter, and the carbon track is rated 0.05 W (fine here, since every pot carries line-level signal). It's a common choice on compact mixers.

Sources: Alpha RV16AF and RD901F catalogue; Bourns PDB18, PTV09, PTV111 datasheets; TT Electronics P160 datasheet; Tayda, Mouser and DigiKey listings checked 2026-10-26.
