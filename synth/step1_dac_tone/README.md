# Step 1: make sound

The ESP32-S3 plays up to 8 saw-wave notes from USB MIDI through a PCM5102A DAC. The BOOT button plays A4 (440 Hz) so you can test the sound before MIDI.

## Wiring

Pins are provisional (see [../README.md](../README.md)).

| PCM5102A board | ESP32-S3 |
|---|---|
| VIN | 5V (or 3V3) |
| GND | GND |
| BCK | GPIO16 |
| LCK (LRCK) | GPIO17 |
| DIN | GPIO18 |
| SCK | GND (uses the DAC's own clock) |

On the purple boards, check the four solder bridges on the back: 1 (FLT), 2 (DEMP) and 4 (FMT) to **L**, 3 (XSMT) to **H**. If XSMT is low the DAC stays muted. Many boards ship bridged this way; some have no SCK pin and ground it on the board.

Plug headphones (through an amp, or at low volume) or a mixer line input into the 3.5 mm jack. Start quiet.

## Upload

Same Arduino IDE settings as the controller (see [firmware/step2_midi_test](../../firmware/step2_midi_test/README.md)): ESP32S3 Dev Module, **USB Mode: USB-OTG (TinyUSB)**, USB CDC On Boot: Disabled. Upload over the COM port, then also plug in the USB port.

## Test

1. Press **BOOT**: you should hear a 440 Hz buzz while it's held, fading out over about 50 ms when you let go.
2. In FL Studio, **Options > MIDI settings**: enable **Omer Synth** as an *Output* device, give it a port number, and on a MIDI Out channel set the same port. Play notes or chords from the piano roll or a keyboard: up to 8 at once, the oldest note is dropped after that.

**Done when:** BOOT plays a tone and FL plays chords on it. Tell me what happened, including any compile error text.

If it's silent: check XSMT is high and SCK is grounded first. High notes sound a bit harsh on purpose: the saw isn't band-limited yet (step 2 fixes that).
