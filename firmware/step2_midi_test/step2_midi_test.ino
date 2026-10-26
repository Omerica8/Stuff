// Step 2 test: the board shows up as a USB MIDI device.
// Press the BOOT button: it sends note C4 to FL Studio and lights the RGB LED.
#include <Arduino.h>
#if ARDUINO_USB_MODE
#error Set Tools > USB Mode to "USB-OTG (TinyUSB)"
#else

#include "USB.h"
#include "USBMIDI.h"

USBMIDI MIDI("Omer Controller");

const int BUTTON_PIN = 0;   // the board's BOOT button
const int RGB_PIN = 48;     // built-in RGB LED (some boards use 38)
const int NOTE_C4 = 60;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  MIDI.begin();
  USB.begin();
}

void loop() {
  static bool wasPressed = false;
  bool pressed = digitalRead(BUTTON_PIN) == LOW;
  if (pressed != wasPressed) {
    wasPressed = pressed;
    if (pressed) {
      MIDI.noteOn(NOTE_C4, 100);
      rgbLedWrite(RGB_PIN, 0, 40, 0);
    } else {
      MIDI.noteOff(NOTE_C4, 0);
      rgbLedWrite(RGB_PIN, 0, 0, 0);
    }
  }
  delay(5);  // crude debounce
}
#endif
