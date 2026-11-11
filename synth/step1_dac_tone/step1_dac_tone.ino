// Step 1: 8-voice saw synth. USB MIDI notes in, PCM5102A I2S DAC out.
// The BOOT button plays A4 so you can test the DAC without MIDI.
#include <Arduino.h>
#if ARDUINO_USB_MODE
#error Set Tools > USB Mode to "USB-OTG (TinyUSB)"
#else

#include "USB.h"
#include "USBMIDI.h"
#include "ESP_I2S.h"

USBMIDI MIDI("Omer Synth");
I2SClass i2s;

// Provisional pins: not locked until the board labels are confirmed. GPIO19/20 stay free for USB.
const int I2S_BCK_PIN = 16;
const int I2S_LRCK_PIN = 17;
const int I2S_DATA_PIN = 18;
const int BUTTON_PIN = 0;  // BOOT button

const uint32_t SAMPLE_RATE = 44100;
const int VOICES = 8;
const int BLOCK = 64;  // frames per I2S write, about 1.5 ms
const float ATTACK = 0.01f;  // per-sample envelope step toward the target, about 2 ms
const float RELEASE = 0.0005f;  // about 45 ms
const float MIX_GAIN = 1.0f / VOICES;  // 8 full-velocity voices can't clip

// Defined before any function: the Arduino IDE puts its auto-generated prototypes above the first function.
struct Voice {
  uint8_t note;
  bool gate = false;
  float target = 0, level = 0;
  uint32_t phase = 0, inc = 0, startedAt = 0;
};
struct NoteEvent {
  uint8_t note, velocity;  // velocity 0 = note off
};

Voice voices[VOICES];
QueueHandle_t events;
uint32_t noteCounter = 0;

// Phase step per sample for a MIDI note; the 32-bit phase wraps once per cycle.
uint32_t phaseInc(uint8_t note) {
  return (uint32_t)(440.0 * pow(2.0, (note - 69) / 12.0) / SAMPLE_RATE * 4294967296.0);
}

// Same note retriggers its voice, else a silent voice, else steal the oldest.
Voice &pickVoice(uint8_t note) {
  Voice *oldest = &voices[0];
  for (Voice &v : voices) if (v.note == note && v.level > 0) return v;
  for (Voice &v : voices) if (!v.gate && v.level < 0.001f) return v;
  for (Voice &v : voices) if (v.startedAt < oldest->startedAt) oldest = &v;
  return *oldest;
}

void handle(const NoteEvent &e) {
  if (e.velocity) {
    Voice &v = pickVoice(e.note);
    v.note = e.note;
    v.inc = phaseInc(e.note);
    v.gate = true;
    v.target = e.velocity / 127.0f;
    v.startedAt = ++noteCounter;
  } else {
    for (Voice &v : voices) if (v.gate && v.note == e.note) v.gate = false, v.target = 0;
  }
}

// Core 0: drains note events and renders audio. i2s.write blocks until DMA has room, which paces the loop.
void audioTask(void *) {
  static int16_t buf[BLOCK * 2];
  for (;;) {
    NoteEvent e;
    while (xQueueReceive(events, &e, 0)) handle(e);
    for (int i = 0; i < BLOCK; i++) {
      float mix = 0;
      for (Voice &v : voices) {
        v.level += (v.target - v.level) * (v.gate ? ATTACK : RELEASE);
        if (v.level < 0.0001f && !v.gate) continue;
        // shortcut: naive saw aliases on high notes, band-limit it (PolyBLEP) in step 2
        mix += (int32_t)v.phase / 2147483648.0f * v.level;
        v.phase += v.inc;
      }
      int16_t s = (int16_t)(constrain(mix * MIX_GAIN, -1.0f, 1.0f) * 32767);
      buf[2 * i] = buf[2 * i + 1] = s;
    }
    i2s.write((uint8_t *)buf, sizeof buf);
  }
}

void send(uint8_t note, uint8_t velocity) {
  NoteEvent e = {note, velocity};
  xQueueSend(events, &e, 0);
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  events = xQueueCreate(64, sizeof(NoteEvent));
  i2s.setPins(I2S_BCK_PIN, I2S_LRCK_PIN, I2S_DATA_PIN);
  i2s.setTimeout(1000);
  if (!i2s.begin(I2S_MODE_STD, SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO)) {
    for (;;) delay(1000);  // I2S failed to start: check the pins above
  }
  xTaskCreatePinnedToCore(audioTask, "audio", 4096, nullptr, configMAX_PRIORITIES - 1, nullptr, 0);
  MIDI.begin();
  USB.begin();
}

// Core 1: USB MIDI notes on any channel, plus the BOOT test button.
void loop() {
  midiEventPacket_t p;
  while (MIDI.readPacket(&p)) {
    uint8_t type = p.byte1 & 0xF0;
    if (type == 0x90) send(p.byte2, p.byte3);  // note on with velocity 0 is a note off
    if (type == 0x80) send(p.byte2, 0);
  }
  static bool wasPressed = false;
  bool pressed = digitalRead(BUTTON_PIN) == LOW;
  if (pressed != wasPressed) {
    wasPressed = pressed;
    send(69, pressed ? 100 : 0);
  }
  delay(1);
}
#endif
