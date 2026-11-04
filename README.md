# GPX mini TV as a Wi-Fi screen

PC or phone → Wi-Fi → classic ESP32 → composite (GPIO25) → RF modulator (CH3) → TV antenna input

## Parts (about $20)
- A classic ESP32 DevKit (ESP32-WROOM-32). An S3, C3 or C6 won't work because they have no DAC.
- The AliExpress AV-to-RF modulator (NTSC CH3, 5V USB)
- A coax lead to reach the TV's antenna input

## Wiring
- ESP32 **GPIO25** → the center pin of the modulator's **yellow** plug. ESP32 **GND** → the plug's outer shell.
- Modulator **RF OUT** → the TV's antenna input
- Power both the ESP32 and the modulator from USB.
- On the TV, set the band to **V-L** and tune to **channel 3**.

## 1. ESP32
1. In the Arduino IDE, install the "esp32" board package and the **ESP_8_BIT_composite** library.
   If the sketch fails to compile on board package 3.x, install esp32 version **2.0.17** from the Boards Manager instead.
2. Open `minitv_receiver/minitv_receiver.ino` and put your Wi-Fi name and password in it.
3. Select **ESP32 Dev Module**, then upload.
4. Open the Serial Monitor at 115200 baud and note the IP address it prints.

## 2. Computer (Windows or Linux)
```
pip install mss pillow numpy
python minitv_send.py 192.168.1.50            # use your ESP32's IP
python minitv_send.py 192.168.1.50 --fps 15   # more fps if it stays stable
python minitv_send.py 192.168.1.50 --monitor 2
```
On Linux, this needs an X11 session. On Wayland, log in with "Ubuntu on Xorg" or the equivalent for your distro.

## 3. Phone (Android)
Mirror the phone to the computer with **scrcpy** (free) and send just that window to the TV.
- Windows: download it from https://github.com/Genymobile/scrcpy/releases. Linux: `sudo apt install scrcpy`.
- On the phone, turn on Developer options and then USB debugging. Plug the phone in and run `scrcpy`.
- Note where the scrcpy window sits on screen, then run:
  `python minitv_send.py 192.168.1.50 --region X Y WIDTH HEIGHT`
  (WIDTH and HEIGHT are the window size, with X Y as its top-left corner.)

## Tips
- Rows that tear or stay stale usually mean dropped packets. Lower `--fps` or move the ESP32 closer to the router.
- Text gets hard to read at 256×240. Large fonts, video and visualizers look best.
