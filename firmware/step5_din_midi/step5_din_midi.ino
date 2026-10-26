// Step 5: step 4b plus a 5-pin DIN MIDI bridge for the mixer's digital board.
// Faders -> CC 20-23, encoders -> CC 30-33 (0-127), encoder pushes -> notes 60-63, button -> note 70.
// DIN MIDI IN (GPIO44) -> USB, USB -> DIN MIDI OUT (GPIO43), both directions, all channels.
#include <Arduino.h>
#if ARDUINO_USB_MODE
#error Set Tools > USB Mode to "USB-OTG (TinyUSB)"
#else

#include "USB.h"
#include "USBMIDI.h"

USBMIDI MIDI("Omer Controller");

const int FADER_PINS[4] = {1, 2, 4, 5};
// Encoder n: A, B, push.
const int ENC_PINS[4][3] = {{11, 12, 13}, {14, 21, 38}, {39, 40, 41}, {42, 47, 15}};
const int BUTTON_PIN = 9;
const int LED_PIN = 6;
const int MIDI_RX_PIN = 44;  // from the 6N138 on the digital board
const int MIDI_TX_PIN = 43;  // to DIN OUT pin 5 through 10 ohms

const int CC_FADER_FIRST = 20;  // fader n sends CC 20 + n
const int CC_ENCODER_FIRST = 30;  // encoder n sends CC 30 + n
const int NOTE_ENC_PUSH_FIRST = 60;  // encoder n push sends note 60 + n
const int NOTE_BUTTON = 70;  // moved off 61, which encoder 2's push now uses

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

// Bytes in a USB MIDI packet, by its code index number (low 4 bits of the header).
const uint8_t CIN_LENGTH[16] = {0, 0, 2, 3, 3, 1, 2, 3, 3, 3, 3, 3, 2, 2, 3, 1};

// Bytes in a DIN channel message, by status byte; 0 = not a channel message.
int channelMessageLength(uint8_t status) {
  if (status >= 0x80 && status < 0xC0) return 3;
  if (status >= 0xC0 && status < 0xE0) return 2;
  if (status >= 0xE0 && status < 0xF0) return 3;
  return 0;
}

// USB -> DIN: copy every packet's bytes out unchanged (SysEx passes through too).
void usbToDin() {
  midiEventPacket_t p;
  while (MIDI.readPacket(&p)) {
    uint8_t bytes[3] = {p.byte1, p.byte2, p.byte3};
    Serial0.write(bytes, CIN_LENGTH[p.header & 0x0F]);
  }
}

// DIN -> USB: rebuild channel messages (with running status) and pass real-time bytes.
// shortcut: SysEx and other system common messages from DIN are dropped; add them if a device needs them.
void dinToUsb() {
  static uint8_t status = 0, data[2];
  static int have = 0;
  while (Serial0.available()) {
    uint8_t b = Serial0.read();
    if (b >= 0xF8) {  // real-time (clock, start, stop) can arrive mid-message
      midiEventPacket_t p = {0x0F, b, 0, 0};
      MIDI.writePacket(&p);
      continue;
    }
    if (b & 0x80) {
      status = channelMessageLength(b) ? b : 0;
      have = 0;
      continue;
    }
    if (!status) continue;
    data[have++] = b;
    if (have == channelMessageLength(status) - 1) {
      midiEventPacket_t p = {(uint8_t)(status >> 4), status, data[0], have == 2 ? data[1] : (uint8_t)0};
      MIDI.writePacket(&p);
      have = 0;  // keep status for running status
    }
  }
}

Button encPush[4] = {{ENC_PINS[0][2], NOTE_ENC_PUSH_FIRST}, {ENC_PINS[1][2], NOTE_ENC_PUSH_FIRST + 1},
                     {ENC_PINS[2][2], NOTE_ENC_PUSH_FIRST + 2}, {ENC_PINS[3][2], NOTE_ENC_PUSH_FIRST + 3}};
Button button{BUTTON_PIN, NOTE_BUTTON};

void pollButton(Button &b) {
  bool down = digitalRead(b.pin) == LOW;
  if (down == b.down || millis() - b.changedAt < 15) return;  // 15 ms debounce
  b.down = down;
  b.changedAt = millis();
  if (down) MIDI.noteOn(b.note, 100);
  else MIDI.noteOff(b.note, 0);
}

uint8_t readAB(int e) {
  return (digitalRead(ENC_PINS[e][0]) << 1) | digitalRead(ENC_PINS[e][1]);
}

void setup() {
  for (int e = 0; e < 4; e++)
    for (int p = 0; p < 3; p++) pinMode(ENC_PINS[e][p], INPUT_PULLUP);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  analogReadResolution(12);
  Serial0.begin(31250, SERIAL_8N1, MIDI_RX_PIN, MIDI_TX_PIN);
  MIDI.begin();
  USB.begin();
}

void loop() {
  usbToDin();
  dinToUsb();

  // Faders: average 16 reads; ignore wobble smaller than RAW_HYST so the value doesn't flicker.
  const int RAW_HYST = 20;
  static int lastRaw[4] = {-1000, -1000, -1000, -1000};
  static int lastFader[4] = {-1, -1, -1, -1};
  for (int f = 0; f < 4; f++) {
    long sum = 0;
    for (int i = 0; i < 16; i++) sum += analogRead(FADER_PINS[f]);
    int raw = sum / 16;
    int fader = faderToMidi(raw);
    if (fader != lastFader[f] && (abs(raw - lastRaw[f]) > RAW_HYST || fader == 0 || fader == 127)) {
      lastRaw[f] = raw;
      lastFader[f] = fader;
      MIDI.controlChange(CC_FADER_FIRST + f, fader);
    }
  }

  // Encoders: count quadrature steps, one value per detent.
  static uint8_t prevAB[4] = {readAB(0), readAB(1), readAB(2), readAB(3)};
  static int steps[4] = {0, 0, 0, 0};
  static int encValue[4] = {64, 64, 64, 64};
  for (int e = 0; e < 4; e++) {
    uint8_t ab = readAB(e);
    if (ab == prevAB[e]) continue;
    steps[e] += encoderStep(prevAB[e], ab);
    prevAB[e] = ab;
    if (abs(steps[e]) >= STEPS_PER_DETENT) {
      encValue[e] = constrain(encValue[e] + (steps[e] > 0 ? 1 : -1), 0, 127);
      steps[e] = 0;
      MIDI.controlChange(CC_ENCODER_FIRST + e, encValue[e]);
    }
  }

  bool anyDown = false;
  for (int e = 0; e < 4; e++) {
    pollButton(encPush[e]);
    anyDown |= encPush[e].down;
  }
  pollButton(button);
  digitalWrite(LED_PIN, button.down || anyDown ? HIGH : LOW);
}
#endif
