# Step 3a: just the fader

Unplug USB. Take every other part and wire off the breadboard, so only the ESP32 is left in it.

## Wiring (3 wires, by label)

Use socket-ended (female-to-male) jumpers on the fader. "Column of pin X" means a free hole in the same column as the ESP32 pin labelled X.

1. Fader **pin 1** → column of the pin labelled **GND**.
2. Fader **pin 3** → column of the pin labelled **3V3**. No resistor is needed for this test.
3. Fader **pin 2** (the slider; numbers are printed on the fader) → column of the pin labelled **1**.

## Upload and test

Open `step3a_fader.ino` (in a folder named `step3a_fader`), use the same Tools settings as before, and upload.

- The small LED on the ESP32 shows **blue for 1 second** right after upload or after you press RST. That means the sketch is running.
- Move the fader. The same LED turns **green**, dim at the bottom and bright at the top.
- In FL Studio, right-click a mixer fader, choose **Link to controller**, and move your fader.

## If it's off

- **No blue at start:** the upload didn't finish, or your board's RGB LED is on pin 38. Tell me which.
- **Blue, but no green when you move the fader:** check that wire 3 is in the column labelled **1**, not RX/TX.
- **Green flickers but doesn't follow the fader:** swap the wires on fader pins 1 and 2.
