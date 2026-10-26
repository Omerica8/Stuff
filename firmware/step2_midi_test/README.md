# Step 2: get the board talking to FL Studio

No wiring needed. You only need the board, two USB-C data cables and your PC.

## 1. Install Arduino IDE and ESP32 support

1. Download and install Arduino IDE 2 from arduino.cc/en/software.
2. Open it, go to **File > Preferences**, and paste this into *Additional boards manager URLs*:
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
3. Open **Tools > Board > Boards Manager**, search **esp32**, and install **esp32 by Espressif Systems** (version 3.x).

## 2. Open the sketch

Download `step2_midi_test.ino`, put it in a folder named `step2_midi_test`, and open it in Arduino IDE.

## 3. Set the board options (Tools menu)

| Setting | Value |
| --- | --- |
| Board | ESP32S3 Dev Module |
| USB Mode | USB-OTG (TinyUSB) |
| USB CDC On Boot | Disabled |
| Upload Mode | UART0 / Hardware CDC |
| Flash Size | 16MB (128Mb) |
| PSRAM | OPI PSRAM |

## 4. Plug in and upload

Your board has two USB-C ports. Look at the small print next to them: one says **COM** (or UART), the other **USB**.

1. Plug the **COM** port into the PC. Pick its port under **Tools > Port**.
2. Click **Upload** (the arrow). If it fails with "Failed to connect", hold **BOOT**, tap **RST**, release BOOT, and upload again.
3. Now also plug the **USB** port into the PC. Leaving both plugged in is fine.

## 5. Check it in FL Studio

1. Open **Options > MIDI settings**.
2. Under *Input*, you should see **Omer Controller**. Select it and turn on **Enable**.
3. Press the **BOOT** button on the board. The RGB LED should light green, and FL should play a note on the selected channel (the MIDI icon in FL's top bar also blinks).

**Done when:** the controller appears in FL and the BOOT button plays a note. Tell me in the thread what happened, including any error text.

If the note plays but the LED stays dark, your board's LED is on GPIO38: change `RGB_PIN = 48` to `38` and upload again.
