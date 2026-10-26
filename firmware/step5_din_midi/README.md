# Step 5: DIN MIDI in and out

Everything from step 4b, plus a bridge between the mixer's 5-pin MIDI sockets and USB. Notes, CCs, pitch bend, program changes and clock from a keyboard on **MIDI IN** reach FL Studio. Anything FL sends to the controller's MIDI output comes out of **MIDI OUT** to a synth.

## When
Do this step once the **digital board** (Phase 3b) is built. The bridge uses two pins the controller left free:

| ESP32 pin label | Digital board J6 |
| --- | --- |
| **44** | MIDI RX (from the 6N138) |
| **43** | MIDI TX (to DIN OUT) |
| **3V3** | 3.3 V |
| **GND** | GND |

## Upload
Open `step5_din_midi.ino` (in a folder named `step5_din_midi`), same Tools settings as before (USB Mode: USB-OTG (TinyUSB)), upload.

## Test
1. **IN:** plug a MIDI keyboard's MIDI OUT into the mixer's MIDI IN. In FL Studio, enable the "Omer Controller" input, play a key, and the MIDI activity light should blink and the note play.
2. **OUT:** plug the mixer's MIDI OUT into a synth's MIDI IN. In FL, set "Omer Controller" as a MIDI output with a port number, point a MIDI Out channel at that port, and play notes: the synth should play.

**Done when:** both work, and the faders and encoders still send CC 20-23 and 30-33.

Not passed from DIN to USB yet: SysEx (patch dumps). Tell me if a device needs it.
