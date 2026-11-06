// PC fader: one fader (GPIO1) + four buttons (GPIO4-7) talk to the PC helper over USB serial
// and Bluetooth LE at the same time (the helper picks which one in buttons.toml).
// Sends lines like "F 73" (fader, 0-100) and "B 2 1" / "B 2 0" (button 2 pressed / released).
// All the meaning (volume, macros) lives in the PC helper, so you never reflash to change a button.
#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#if !CONFIG_NIMBLE_ENABLED
#include <BLE2902.h>
#endif

const int FADER_PIN = 1;
const int BUTTON_PINS[4] = {4, 5, 6, 7};  // wired to GND, internal pull-ups
const int RAW_MIN = 40, RAW_MAX = 4000;     // fader ends, same calibration as the controller steps
const int RGB_PIN = 48;                     // on-board RGB LED (38 on some boards)

// Nordic UART Service: a common "serial over BLE" layout; the helper listens on TX.
#define NUS_SERVICE "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
#define NUS_TX      "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

BLECharacteristic *bleTx;
volatile bool bleConnected = false;

class ServerEvents : public BLEServerCallbacks {
  void onConnect(BLEServer *) override { bleConnected = true; }
  void onDisconnect(BLEServer *server) override {
    bleConnected = false;
    server->startAdvertising();  // so the PC can reconnect
  }
};

int lastPercent = -1;
float smooth = -1;
bool lastDown[4];
unsigned long lastChange[4], lastHeartbeat;

void send(const char *line) {
  Serial.print(line);
  if (bleConnected) {
    bleTx->setValue((uint8_t *)line, strlen(line));
    bleTx->notify();
  }
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  for (int i = 0; i < 4; i++) pinMode(BUTTON_PINS[i], INPUT_PULLUP);

  BLEDevice::init("PC Fader");
  BLEServer *server = BLEDevice::createServer();
  server->setCallbacks(new ServerEvents());
  BLEService *service = server->createService(NUS_SERVICE);
  bleTx = service->createCharacteristic(NUS_TX, BLECharacteristic::PROPERTY_NOTIFY);
#if !CONFIG_NIMBLE_ENABLED
  bleTx->addDescriptor(new BLE2902());  // NimBLE (core 3.3+ on the S3) adds this itself; a second copy breaks Windows service discovery
#endif
  service->start();
  BLEDevice::getAdvertising()->addServiceUUID(NUS_SERVICE);
  BLEDevice::startAdvertising();

  rgbLedWrite(RGB_PIN, 0, 0, 40);  // blue for 1 s: the sketch is running
  delay(1000);
  rgbLedWrite(RGB_PIN, 0, 0, 0);
}

void loop() {
  char line[16];
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
    snprintf(line, sizeof line, "F %d\n", lastPercent);
    send(line);
    lastHeartbeat = millis();
  }

  for (int i = 0; i < 4; i++) {
    bool down = digitalRead(BUTTON_PINS[i]) == LOW;
    if (down != lastDown[i] && millis() - lastChange[i] > 25) {  // 25 ms debounce
      lastDown[i] = down;
      lastChange[i] = millis();
      snprintf(line, sizeof line, "B %d %d\n", i + 1, down);
      send(line);
      rgbLedWrite(RGB_PIN, 0, down ? 40 : 0, bleConnected ? 10 : 0);  // green while held
    }
  }
  static bool shownConnected = false;  // dim blue LED = Bluetooth connected
  if (bleConnected != shownConnected) {
    shownConnected = bleConnected;
    rgbLedWrite(RGB_PIN, 0, 0, bleConnected ? 10 : 0);
  }
  delay(5);
}
