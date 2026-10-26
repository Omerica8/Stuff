# Step 4a: four faders

Keep everything from step 3 where it is and add three more faders. Unplug USB while you wire.

## Wiring

Wire each new fader the same way as the first one, with socket-ended jumpers. "Column of pin X" means a free hole in the same column as the ESP32 pin **labelled** X.

| Fader | Pin 1 | Pin 2 (slider) | Pin 3 |
| --- | --- | --- | --- |
| 1 (already wired) | − rail | column of **1** | + rail (through its 330 Ω, as before) |
| 2 | − rail | column of **2** | + rail |
| 3 | − rail | column of **4** | + rail |
| 4 | − rail | column of **5** | + rail |

- Pins **1** and **2** are next to each other on one side of the ESP32. Pins **4** and **5** are on the other side, next to RST.
- The new faders go straight to the + rail; no resistor needed.
- Push every jumper all the way in and give it a gentle tug. Loose wires were the problem last time.

## Upload

Open `step4a_four_faders.ino` (in a folder named `step4a_four_faders`), same Tools settings, upload.

## Test in FL Studio

| Fader | Sends |
| --- | --- |
| 1 | CC 20 |
| 2 | CC 21 |
| 3 | CC 22 |
| 4 | CC 23 |

Link each one to a mixer track's volume (right-click the volume fader, **Link to controller**, move your fader).

The encoder now sends **CC 30** instead of 21, so re-link the pan knob if you had it linked. The encoder push and button work as before.

**Done when:** all four faders move their own FL fader, and none of them moves another one.

## If something's off

- **One fader does nothing:** reseat its three wires, then check its slider wire is in the column of the right label.
- **Moving one fader moves two in FL:** two slider wires are in the same column. Move one.
- **A fader works backwards:** swap the wires on its pins 1 and 3.
