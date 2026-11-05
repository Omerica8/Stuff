// PC fader: one fader (GPIO1) + four buttons (GPIO4-7) talk to the PC helper over USB serial.
// Sends lines like "F 73" (fader, 0-100) and "B 2 1" / "B 2 0" (button 2 pressed / released).
// All the meaning (volume, macros) lives in the PC helper, so you never reflash to change a button.
#include <Arduino.h>

const int FADER_PIN = 1;
const int BUTTON_PINS[4] = {4, 5, 6, 7};  // wired to GND, internal pull-ups
const int RAW_MIN = 40, RAW_MAX = 4000;     // fader ends, same calibration as the controller steps
const int RGB_PIN = 48;                     // on-board RGB LED (38 on some boards)

int lastPercent = -1;
float smooth = -1;
bool lastDown[4];
unsigned long lastChange[4], lastHeartbeat;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) pinMode(BUTTON_PINS[i], INPUT_PULLUP);
  rgbLedWrite(RGB_PIN, 0, 0, 40);  // blue for 1 s: the sketch is running
  delay(1000);
  rgbLedWrite(RGB_PIN, 0, 0, 0);
}

void loop() {
  long sum = 0;
  for (int i = 0; i < 16; i++) sum += analogRead(FADER_PIN);
  float raw = sum / 16.0;
  smooth = smooth < 0 ? raw : smooth * 0.8 + raw * 0.2;
  int percent = constrain(map((long)smooth, RAW_MIN, RAW_MAX, 0, 100), 0, 100);
  // Hysteresis: ignore 1-step jitter, except to land exactly on 0 or 100.
  bool moved = abs(percent - lastPercent) > 1 || (percent != lastPercent && (percent == 0 || percent == 100));
  // Heartbeat once a second so the helper finds the port and gets the position after it starts.
  if (moved || millis() - lastHeartbeat > 1000) {
    if (moved) lastPercent = percent;
    Serial.printf("F %d\n", lastPercent);
    lastHeartbeat = millis();
  }

  for (int i = 0; i < 4; i++) {
    bool down = digitalRead(BUTTON_PINS[i]) == LOW;
    if (down != lastDown[i] && millis() - lastChange[i] > 25) {  // 25 ms debounce
      lastDown[i] = down;
      lastChange[i] = millis();
      Serial.printf("B %d %d\n", i + 1, down);
      rgbLedWrite(RGB_PIN, 0, down ? 40 : 0, 0);  // green while a button is held
    }
  }
  delay(5);
}
