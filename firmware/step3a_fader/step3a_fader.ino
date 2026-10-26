// Step 3a: just the fader. Sends CC 20 and sets the on-board RGB LED brightness,
// so you can see it working without FL Studio.
#include <Arduino.h>
#if ARDUINO_USB_MODE
#error Set Tools > USB Mode to "USB-OTG (TinyUSB)"
#else

#include "USB.h"
#include "USBMIDI.h"

USBMIDI MIDI("Omer Controller");

const int FADER_PIN = 1;
const int RGB_PIN = 48;  // on-board RGB LED (38 on some boards)
const int CC_FADER = 20;

void setup() {
  analogReadResolution(12);
  MIDI.begin();
  USB.begin();
  rgbLedWrite(RGB_PIN, 0, 0, 40);  // blue for 1 s: the sketch is running
  delay(1000);
}

void loop() {
  long sum = 0;
  for (int i = 0; i < 16; i++) sum += analogRead(FADER_PIN);
  int value = constrain((sum / 16) * 128 / 4096, 0, 127);
  static int last = -1;
  if (abs(value - last) > 1 || (value != last && (value == 0 || value == 127))) {
    last = value;
    MIDI.controlChange(CC_FADER, value);
    rgbLedWrite(RGB_PIN, 0, value, 0);  // green: brighter as the fader goes up
  }
}
#endif
