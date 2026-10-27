<!-- sources: mixer/case/ -->
# Case

The case thread owns `mixer/case/`. Read [HEIGHTS.md](../mixer/case/HEIGHTS.md) and [STATUS.md](../mixer/case/STATUS.md) for the current numbers; this page is only a summary.

- **Size:** about 407 × 353 mm. Printed pieces must be ≤ 210 mm to fit the Ender 3 (≈220 × 220 × 250, exact variant unverified).
- **Top:** stepped. 2 mm aluminium control plate, underside 10.5 mm above the strip PCBs, plus a raised 1.5 mm aluminium jack strip, underside 24 mm up. No PCB changes needed.
- **Under the plate:** PVA2 H1 switches in rectangular cut-outs, 4 mm fader spacers, LEDs raised 7.2 mm, 7 mm low-profile or laid-flat electrolytics, ESP32/TFT soldered without sockets.
- **Front:** the plate ends after the faders (local y 322), and a printed armrest covers the ribbon plugs.
- **Inside:** audio boards on 18 mm posts so the 35 mm power heatsinks fit under the raised rear shelf.
- **Feet:** separate wedge feet (about 10–15°), flat deck.
- **Tools:** OpenSCAD isn't on Omer's PC, so CAD runs in the cloud container. Check every panel with a 1:1 paper print before cutting or printing full parts.
- **Next:** panel DXF/PDF with labels and the rear panel, then the OpenSCAD frame, tray and feet with STLs and renders.
