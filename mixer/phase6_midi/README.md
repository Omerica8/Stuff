# Phase 6: MIDI hub board (design v1)

*2026-10-27. Status: PCB designed, nothing ordered. Added when Omer moved the mixer's focus from XLR to MIDI (mic strips went from 4 to 2).*

A 200 × 64 mm, 2-layer, through-hole board along the rear panel. It gives the mixer **5 DIN MIDI IN, 3 DIN MIDI OUT (OUT 3 can be THRU) and a USB-A host port** for a USB-MIDI keyboard. A Raspberry Pi Pico (RP2040) does the work. It plugs into two 1×20 sockets and connects to port 3 of the digital board's USB hub, so it shares the one USB cable to the PC. The PC sees it as its own class-compliant USB MIDI device with one port per input, so FL Studio can tell the keyboards apart.

The digital board's own DIN IN/OUT on the ESP32 stay as they are. The mixer has **6 DIN IN, 4 DIN OUT and 1 USB host** in total.

## Blocks

| Block | How | Why |
|---|---|---|
| Brain | Raspberry Pi Pico (RP2040) in sockets J10/J11 | about $4. 2 hardware UARTs, plus PIO for more serial ports and a USB host port |
| To the PC | the Pico's own micro-USB → short cable to **hub USB3** pads on the FE1.1s module | no change to the digital board PCB. The hub's 4th port stays spare |
| MIDI IN 1–5 | 6N138 per input, same circuit as the digital board | the MIDI spec needs an opto at every input |
| MIDI OUT 1–3 | 3.3 V MIDI spec: 33 Ω from 3.3 V to pin 4, 10 Ω from TX to pin 5 | same as the digital board |
| USB host | USB-A J9, 22 Ω series on D+/D−, 500 mA polyfuse F1 from the Pico VBUS | PIO-USB host (the Pico-PIO-USB library, as used by rppicomidi's usb_midi_host) |

## Pico pins

| Pico pin | GPIO | Use |
|---|---|---|
| 1 / 2 | GP0 / GP1 | UART0 TX → OUT 1, RX ← IN 1 |
| 6 / 7 | GP4 / GP5 | UART1 TX → OUT 2, RX ← IN 2 |
| 9 / 10 / 11 | GP6 / GP7 / GP8 | PIO UART RX ← IN 3 / 4 / 5 |
| 12 | GP9 | PIO UART TX → OUT 3 (firmware option: THRU of IN 1) |
| 21 / 22 | GP16 / GP17 | PIO-USB host D+ / D− (through 22 Ω) |
| 36 | 3V3 OUT | opto pull-ups, MIDI OUT source |
| 40 | VBUS | 5 V for the 6N138s and the USB-A port (through F1) |
| 3, 8, 13, 18, 23, 28, 33, 38 | GND | |

## Circuits

**MIDI IN (×5):** DIN pin 4 → 220 Ω → 6N138 pin 2. DIN pin 5 → 6N138 pin 3. 1N4148 reversed across pins 2–3. 6N138 pin 8 = +5 V (Pico VBUS, 100 nF each), pin 5 = GND, pin 7 → 10 kΩ to GND, pin 6 → 1 kΩ pull-up to 3.3 V → Pico RX. DIN pin 2 and the shell stay open.

**MIDI OUT (×3):** 3.3 V → 33 Ω → DIN pin 4. TX → 10 Ω → DIN pin 5. DIN pin 2 → GND.

**USB host:** Pico VBUS → MF-R050 polyfuse → USB-A VBUS, with 100 µF + 100 nF. GP16 → 22 Ω → D+, GP17 → 22 Ω → D−. Pico-PIO-USB uses the RP2040's internal pull-downs for host mode.

## Power

Everything runs from the Pico's micro-USB, which is hub port 3. On a PC, the whole USB side shares the PC port's 500 mA: PCM2902, ESP32 + TFT, hub, Pico and a typical keyboard (about 100 mA) fit. If a keyboard draws more, plug a phone charger into the digital board's USB-C power input, which feeds the hub directly. The polyfuse stops a faulty device from dropping the hub.

## Firmware (to write when the board exists)

Arduino IDE with the Earle Philhower RP2040 core, CPU at 120 or 240 MHz (PIO-USB needs a multiple of 12 MHz), **Tools > USB Stack: Adafruit TinyUSB**. Native USB is the device, with 6 virtual cables (DIN IN 1–5 and the USB keyboard). Pico-PIO-USB on GP16/17 is the host. Serial1/Serial2 serve UART0/1, and SerialPIO serves IN 3–5 and OUT 3, all at 31250 baud. The plan is a firmware step next to `firmware/step5_din_midi`.

## Files

KiCad sources: `C:\Users\pogam\kicad-mcp\kicad-sandbox\mixer_midi` (generator scripts in `tools/`, the same flow as the other boards). Outputs are in `pcb/`.
