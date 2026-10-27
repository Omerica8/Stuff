<!-- sources: firmware/ -->
# Firmware

Arduino IDE 2 + ESP32 core, **Tools > USB Mode: USB-OTG (TinyUSB)**. Each step is a folder with a `.ino` and a README with wiring, upload and a "done when" test. Claude writes the code; Omer wires, uploads and tests.

| Step | Folder | Adds |
|---|---|---|
| 2 | [step2_midi_test](../firmware/step2_midi_test/README.md) | Board shows up in FL Studio as a USB MIDI device |
| 3a | [step3a_fader](../firmware/step3a_fader/README.md) | One fader |
| 3 | [step3_one_of_each](../firmware/step3_one_of_each/README.md) | One fader, encoder, button, LED (with `wiring.png`) |
| 4a | [step4a_four_faders](../firmware/step4a_four_faders/README.md) | Four faders |
| 4b | [step4b_four_encoders](../firmware/step4b_four_encoders/README.md) | Four encoders with push |
| 5 | [step5_din_midi](../firmware/step5_din_midi/README.md) | DIN MIDI ↔ USB MIDI bridge for the digital board. Parser tested off-hardware only; SysEx DIN→USB not passed yet |

## Pin map (as used in step 4b/5)

| Function | GPIO |
|---|---|
| Faders 1–4 (ADC) | 1, 2, 4, 5 |
| Encoders A/B/push | 11/12/13, 14/21/38, 39/40/41, 42/47/15 |
| Button | 9 |
| LED | 6 |
| DIN MIDI RX / TX (Serial0, 31250 baud) | 44 / 43 |
| Reserved: USB D−/D+ | 19 / 20 |

The draft full-core map (plan v2) also has TFT CLK 16, MOSI 17, DC 18 (CS1 to GND, RES to RST, BLK to 3V3, no touch), buttons 0, 3, 45, 46, 9 (strapping pins used as inputs only), LEDs 6, 7, 8, 10. Don't lock the pinout until the exact board and TFT labels are confirmed.

## MIDI map

| Control | Message |
|---|---|
| Fader n (0–3) | CC 20+n |
| Encoder n | CC 30+n (absolute 0–127, 4 steps per detent) |
| Encoder n push | Note 60+n |
| Button | Note 70 |

Fader ADC range is calibrated as RAW_MIN 40 / RAW_MAX 4000, 16-sample average with hysteresis 20.

## FL Studio scripting limits (checked against API stubs v37.0.1)

- `plugins.getParamValue` / `setParamValue` are normalised 0–1 and work on VST and native plugins.
- No callback names which parameter changed (only `OnRefresh` with `HW_Dirty_ControlValues`), so the script has to diff mapped params.
- Focus: `ui.getFocusedFormID`, `mixer.getActiveEffectIndex`.
- Feedback to the controller needs output port = input port.
- Scripts can't load or remove plugins.

Remaining plan steps: 5 FL script, 6 TFT + plugin maps.
