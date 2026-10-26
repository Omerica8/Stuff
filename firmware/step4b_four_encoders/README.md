# Step 4b: four encoders

Keep everything from step 4a where it is and add three more encoders. Unplug USB while you wire.

## Wiring

Wire each new encoder exactly like the first one. "Column of pin X" means a free hole in the same column as the ESP32 pin **labelled** X.

Each encoder has 5 pins: A, C (middle) and B on the 3-pin side, and two push pins on the 2-pin side.

| Encoder | A | B | C (middle) | Push pin 1 | Push pin 2 |
| --- | --- | --- | --- | --- | --- |
| 1 (already wired) | column of **11** | column of **12** | − rail | column of **13** | − rail |
| 2 | column of **14** | column of **21** | − rail | column of **38** | − rail |
| 3 | column of **39** | column of **40** | − rail | column of **41** | − rail |
| 4 | column of **42** | column of **47** | − rail | column of **15** | − rail |

- Each encoder needs its own spot on the breadboard, with its pins in columns nothing else uses.
- Pins 14 and 15 are on the same side as 11, 12 and 13. Pins 21, 38, 39, 40, 41, 42 and 47 are on the other side, with 1 and 2.
- No resistors. Push every jumper all the way in and give it a gentle tug.

## Upload

Open `step4b_four_encoders.ino` (in a folder named `step4b_four_encoders`), same Tools settings, upload.

## Test in FL Studio

| Encoder | Turn sends | Push sends |
| --- | --- | --- |
| 1 | CC 30 | note 60 |
| 2 | CC 31 | note 61 |
| 3 | CC 32 | note 62 |
| 4 | CC 33 | note 63 |

Link each encoder to a mixer track's pan knob. Every push lights your LED while held. The faders still send CC 20-23.

The button now sends **note 70** instead of 61.

**Done when:** each encoder turns its own pan knob, one step per click, and each push lights the LED.

## If something's off

- **An encoder does nothing:** reseat its five wires, then check A and B are in the right columns.
- **An encoder turns the wrong way:** swap its A and B wires.
- **Turning one encoder moves another knob in FL:** two wires are in the same column. Move one.
- **The LED stays on:** a push wire is touching the − rail side, or two push pins share a column.
