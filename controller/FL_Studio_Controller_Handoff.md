# Handoff: Modular FL Studio MIDI Controller / Mixer + FX Controller

**Handoff date:** 2026-10-17  
**Purpose:** Resume the controller design and 3D-printable enclosure work without losing decisions, files, or open questions.

## Project goal

Design and build a bespoke, modular MIDI controller for FL Studio, with mixer/fader controls, rotary encoders, buttons, LEDs, a display, transport controls, and future expansion capability. The enclosure should be irregular/industrial in style, ergonomic, serviceable, and practical to print on a Creality Ender 3.

## Current hardware / context

- **3D printer:** Creality Ender 3. Typical build volume for the classic family is about 220 × 220 × 250 mm; verify the exact printer variant before finalizing print dimensions.
- **Microcontroller:** ESP32-S3 board ordered; exact board variant and dimensions still need verification.
- **Controls ordered:** 10 × B10K linear slide potentiometers, 10 × EC11 rotary encoders with push switches, tactile buttons, assorted LEDs and resistors.
- **Display:** 2.8-inch SPI TFT; exact display controller, PCB dimensions, active area, and mounting-hole positions are not yet verified.
- **Other parts:** solderless breadboard/jumper wires and USB-C data cable.
- **DAW:** FL Studio on a Windows PC.
- **Longer-term plan:** prototype first; later consider motorized faders, custom PCB, and additional modules.

## Agreed design direction

- Ten channels/controls total, matching the ordered quantity of 10 faders and 10 encoders.
- Modular layout: a central core plus left/right expansion sections, with each printable part kept within the Ender 3's usable build area.
- Current conceptual allocation in the CAD: **core = 4 faders + 4 encoders; each side module = 3 faders + 3 encoders**, for 10 total.
- Central TFT, transport/navigation controls, per-channel buttons, LED feedback, rear cable routing, and future module connections.
- Use a flat printable control deck with separate tilt/wedge rails or angled supports if an ergonomic angle is desired. The concept image suggested roughly 15° tilt, but the current CAD does not yet implement this angle.
- Make modules mechanically separable and allow the core to work standalone. Keep room for additional FX/transport modules and future motorized faders.
- ESP32-S3 native USB is preferred. Reserve GPIO19/GPIO20 for USB D-/D+ unless the exact board design requires otherwise.
- **Do not lock the GPIO pinout until the exact ESP32-S3 board and TFT pin labels are confirmed.**

## Software/communication target

- ESP32 communicates with FL Studio using USB MIDI where supported.
- A custom FL Studio MIDI scripting layer should support two-way behavior where the API permits it: update controller LEDs/display and map controls to the selected mixer/plugin context.
- Example dynamic mappings:
  - Fruity Parametric EQ 2: frequency, gain, Q, and related parameters.
  - Fruity Limiter: threshold, ratio, attack, release, gain, and related parameters.
- Verify exact capabilities and limitations of the current FL Studio MIDI scripting API before promising arbitrary plugin-state inspection or fully bidirectional parameter discovery.

## Existing CAD and deliverables

The following files were created in `/mnt/data` during the conversation:

- `fl_controller_modular.scad` — parametric concept model.
- `fl_controller_modular_fast.scad` — faster preview/render variant using lower polygon count.
- `fl_controller_core.scad` — wrapper to render the core.
- `fl_controller_side.scad` — wrapper to render a side module.
- `fl_controller_cheek.scad` — wrapper to render a side cheek.
- `fl_controller_side_fast.scad` and `fl_controller_cheek_fast.scad` — fast wrappers.
- `fl_controller_core.stl` — core printable part.
- `fl_controller_side.stl` — side-module printable part.
- `fl_controller_cheek.stl` — side cheek printable part.
- `FL_Studio_Modular_Ender3_Prototype.zip` — package of CAD files and STLs.

Previously shared package link:

` sandbox:/mnt/data/FL_Studio_Modular_Ender3_Prototype.zip `

The OpenSCAD preview PNG failed in the environment and was empty; do not treat it as a valid preview.

## Current CAD dimensions and limitations

The initial parametric model uses approximately:

- Wall thickness: 3 mm
- Base height: 24 mm
- Top/deck thickness: 4 mm
- Module depth: 190 mm
- Core width: 210 mm
- Side module width: 165 mm
- Fader slot length parameter: 60 mm
- Fader slot width parameter: 8 mm
- Fader pitch: 35 mm
- Encoder/button hole parameter: 7.2 mm
- Generic TFT opening parameters: 78 × 52 mm

These are **provisional concept dimensions, not verified fit dimensions**. In particular, the actual fader length/slot and mounting tabs, EC11 body clearance, TFT PCB/cutout, button diameter, and ESP32 board mounting holes must be measured before printing a final fit-critical enclosure.

## Next steps (recommended order)

1. **Inventory and measure actual components.** Take photos of the front/back and measure:
   - each fader body, full travel, slot length/width, mounting tabs/hole spacing, and connector clearance;
   - EC11 body diameter/depth, shaft diameter, anti-rotation tab, and pin spacing;
   - TFT PCB width/height/thickness, active area, mounting holes, and connector location;
   - ESP32-S3 board dimensions, mounting holes, USB-C position, and labeled GPIOs;
   - tactile button body/hole size and LED dimensions.
2. **Confirm the exact printer variant and usable print area.** Leave margin for clips/brims and avoid relying on the full nominal bed dimensions.
3. **Revise the CAD around measured parts.** Add exact fader slots and mounting features, encoder clearance, display opening/standoffs, M3 screw bosses or heat-set insert bosses, USB-C access, rear ports, ventilation, and cable channels.
4. **Finish the modular interface.** Add repeatable alignment features and fastener locations between the core and side modules. Choose a practical internal electrical connector/bus only after the electronics layout is known.
5. **Add the ergonomic tilt.** Prefer separate printable wedge rails or angled supports so the top deck remains easy to print flat.
6. **Print fit tests before full parts.** Print small sections for one fader, one encoder, one button, and the TFT opening; test with the real components before printing all modules.
7. **Prototype electronics safely.** Verify ESP32-S3 board pinout and ADC availability; plan GPIO expansion if needed. Keep USB pins reserved where applicable.
8. **Build the firmware and FL Studio script incrementally.** First prove USB MIDI input/output, then fader/encoder input, then LEDs/display, then selected-track/plugin mapping.
9. **Plan motorized faders as a later revision.** They require motor drivers, position feedback, mechanical depth, power budgeting, and additional wiring clearance; do not assume the current shell supports them without redesign.

## Design constraints / cautions

- The existing model is an early prototype, not production-ready.
- Do not print all parts before testing fit with the physical components.
- Do not finalize GPIO assignments until board markings/pinout are known.
- Check current FL Studio scripting API capabilities for plugin parameter names/values and selection events.
- Keep the enclosure serviceable: removable deck, accessible fasteners, strain relief, and enough clearance for connectors and wiring.
- Ensure each individual print part fits the exact printer's usable build volume, including any brim/support requirements.

## Conversation outcome

The user requested research into MIDI controller/mixer/FX control-surface layouts, then asked for a more irregular, modular enclosure with room for future expansion and efficient Ender 3 printing. A conceptual image was generated, and an initial OpenSCAD/STL package was created and shared. The next valuable action is to refine the existing CAD using exact measurements from the user's ordered physical components.
