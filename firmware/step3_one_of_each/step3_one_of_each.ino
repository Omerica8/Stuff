// Step 3: one fader, one encoder (with push), one button, one LED.
// Fader -> CC 20, encoder -> CC 21 (0-127), encoder push -> note 60, button -> note 61.
#include <Arduino.h>
#if ARDUINO_USB_MODE
#error Set Tools > USB Mode to "USB-OTG (TinyUSB)"
#else

#include "USB.h"
#include "USBMIDI.h"

USBMIDI MIDI("Omer Controller");

const int FADER_PIN = 1;
const int ENC_A_PIN = 11;
const int ENC_B_PIN = 12;
const int ENC_PUSH_PIN = 13;
const int BUTTON_PIN = 9;
const int LED_PIN = 6;

const int CC_FADER = 20;
const int CC_ENCODER = 21;
const int NOTE_ENC_PUSH = 60;
const int NOTE_BUTTON = 61;

// shortcut: fixed ADC ends, fine-tune if the fader can't reach 0 or 127
const int RAW_MIN = 40;
const int RAW_MAX = 4000;
const int STEPS_PER_DETENT = 4;  // most EC11s; set to 2 if one click moves 2 values

// Defined before any function: the Arduino IDE puts its auto-generated prototypes above the first function.
struct Button {
  int pin;
  int note;
  bool down = false;
  uint32_t changedAt = 0;
};

// Fader raw ADC (0-4095) to 0-127, clamped to the calibrated ends.
int faderToMidi(int raw) {
  long v = (long)(raw - RAW_MIN) * 127 / (RAW_MAX - RAW_MIN);
  return constrain(v, 0, 127);
}

// Quadrature step from previous and current AB state: +1, -1 or 0.
int encoderStep(uint8_t prevAB, uint8_t ab) {
  static const int8_t table[16] = {0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};
  return table[(prevAB << 2) | ab];
}

Button encPush{ENC_PUSH_PIN, NOTE_ENC_PUSH};
Button button{BUTTON_PIN, NOTE_BUTTON};

void pollButton(Button &b) {
  bool down = digitalRead(b.pin) == LOW;
  if (down == b.down || millis() - b.changedAt < 15) return;  // 15 ms debounce
  b.down = down;
  b.changedAt = millis();
  if (down) MIDI.noteOn(b.note, 100);
  else MIDI.noteOff(b.note, 0);
}

uint8_t readAB() {
  return (digitalRead(ENC_A_PIN) << 1) | digitalRead(ENC_B_PIN);
}

void setup() {
  pinMode(ENC_A_PIN, INPUT_PULLUP);
  pinMode(ENC_B_PIN, INPUT_PULLUP);
  pinMode(ENC_PUSH_PIN, INPUT_PULLUP);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  analogReadResolution(12);
  MIDI.begin();
  USB.begin();
}

void loop() {
  // Fader: average 16 reads; ignore wobble smaller than RAW_HYST so the value doesn't flicker.
  const int RAW_HYST = 20;
  static int lastRaw = -1000;
  static int lastFader = -1;
  long sum = 0;
  for (int i = 0; i < 16; i++) sum += analogRead(FADER_PIN);
  int raw = sum / 16;
  int fader = faderToMidi(raw);
  if (fader != lastFader && (abs(raw - lastRaw) > RAW_HYST || fader == 0 || fader == 127)) {
    lastRaw = raw;
    lastFader = fader;
    MIDI.controlChange(CC_FADER, fader);
  }

  // Encoder: count quadrature steps, one value per detent.
  static uint8_t prevAB = readAB();
  static int steps = 0;
  static int encValue = 64;
  uint8_t ab = readAB();
  if (ab != prevAB) {
    steps += encoderStep(prevAB, ab);
    prevAB = ab;
    if (abs(steps) >= STEPS_PER_DETENT) {
      encValue = constrain(encValue + (steps > 0 ? 1 : -1), 0, 127);
      steps = 0;
      MIDI.controlChange(CC_ENCODER, encValue);
    }
  }

  pollButton(encPush);
  pollButton(button);
  digitalWrite(LED_PIN, button.down || encPush.down ? HIGH : LOW);
}
#endif
