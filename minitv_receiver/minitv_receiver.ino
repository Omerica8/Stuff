// Mini TV receiver: shows frames streamed over Wi-Fi (UDP) on a TV via composite out.
// Board: classic ESP32 (ESP32 Dev Module). Video out: GPIO25 -> RCA center, GND -> RCA shell.
// Library: ESP_8_BIT_composite (Arduino Library Manager).
#include <WiFi.h>
#include <AsyncUDP.h>
#include <ESP_8_BIT_composite.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const uint16_t PORT = 5005;
const int W = 256, H = 240, ROWS = 4;  // each packet: 1 byte start row + ROWS*W pixels (RGB332)

ESP_8_BIT_composite video(true);  // true = NTSC
AsyncUDP udp;
uint8_t* frame;  // latest image from the sender; copied into the video buffer every frame

void setup() {
  Serial.begin(115200);
  video.begin();
  frame = (uint8_t*)calloc(W * H, 1);
  if (!frame) { Serial.println("Out of memory"); while (true) delay(1000); }

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(250);
  WiFi.setSleep(false);  // power save adds big latency to incoming packets
  Serial.print("Mini TV ready at IP: ");
  Serial.println(WiFi.localIP());

  udp.listen(PORT);
  udp.onPacket([](AsyncUDPPacket p) {
    if (p.length() != 1 + ROWS * W) return;  // ignore anything that isn't our format
    uint8_t row = p.data()[0];
    if (row > H - ROWS) return;
    memcpy(frame + row * W, p.data() + 1, ROWS * W);
  });
}

void loop() {
  video.waitForFrame();
  uint8_t** lines = video.getFrameBufferLines();  // must re-fetch: buffers swap each frame
  for (int y = 0; y < H; y++) memcpy(lines[y], frame + y * W, W);
}
