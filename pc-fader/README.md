# PC fader: master volume + 4 macro buttons

A standalone ESP32-S3 on perfboard: one fader sets the Windows master volume (absolute, so fader at the bottom = 0 %, top = 100 %), and four buttons run whatever you put in a text file. State: code written, not yet tested on the hardware.

How it works: the ESP32 only reports what it sees over Bluetooth LE or USB (`F 73` = fader at 73 %, `B 2 1` = button 2 pressed). A small Python program on the PC, the helper, turns that into volume changes and macros. So changing what a button does is editing [helper/buttons.toml](helper/buttons.toml), never reflashing.

| Folder | What's in it |
|---|---|
| [pc_fader/](pc_fader/pc_fader.ino) | Arduino sketch for the ESP32-S3 |
| [helper/](helper/) | `pc_fader.py` (the helper), `buttons.toml` (your button settings), `start.bat` (double-click to run) |

## Wiring (already soldered)

| Part | ESP32-S3 pin |
|---|---|
| Fader wiper (middle pin) | GPIO1 |
| Fader ends | 3V3 and GND (if the volume goes the wrong way, swap these two) |
| Buttons 1–4 | GPIO4, 5, 6, 17, other leg of each to GND (no resistors, the sketch turns on pull-ups) |

GPIO19/20 are the USB lines; leave them free.

## 1. Flash the ESP32 (once)

1. Install **Arduino IDE 2** from arduino.cc if you don't have it. In **Tools > Board > Boards Manager**, install **esp32 by Espressif Systems** (version 3.x).
2. Open `pc_fader/pc_fader.ino`.
3. Plug a cable into the devkit's USB-C port labelled **USB** (the native one).
4. In **Tools**, set:
   - Board: **ESP32S3 Dev Module**
   - USB Mode: **Hardware CDC and JTAG** (the controller sketches used TinyUSB; this one doesn't need it)
   - USB CDC On Boot: **Enabled**
   - Port: the COM port that appeared when you plugged it in
5. Click **Upload** (the → arrow). If it says it can't connect, hold **BOOT**, tap **RST**, let go of BOOT, and upload again. After uploading, tap **RST** once.
6. Check it: **Tools > Serial Monitor**, 115200 baud. You should see `F 42` lines once a second and every time you move the fader, and `B 1 1` / `B 1 0` when you press and release button 1. The onboard LED glows green while a button is held. Close the Serial Monitor afterwards, or the helper can't use the port.

(Using the **COM** port instead also works: set USB CDC On Boot to **Disabled**.)

## 2. Set up the helper on the PC (once)

**Easiest, no Python needed:** download `pc-fader-windows.zip` from the latest [PC fader release](https://github.com/Omerica8/Stuff/releases/latest), unzip it anywhere, and double-click `PCFader.exe`. `PCFader-hidden.exe` does the same with no window (put a shortcut to it in `shell:startup`). Edit the `buttons.toml` next to them. Windows SmartScreen may warn on first run because the file isn't signed: click **More info > Run anyway**.

**Or run it from Python:**

1. Install **Python 3.11 or newer** from python.org. On the first installer screen, tick **Add python.exe to PATH**.
2. Open the `helper` folder in File Explorer, click the address bar, type `cmd` and press Enter. In the black window, type:
   ```
   py -m pip install -r requirements.txt
   ```
3. Double-click **start.bat**. It finds the fader by itself and prints `Connected over Bluetooth` (or `Connected on COM5` in USB mode). Move the fader: the Windows volume follows. Press the buttons: with the example settings, 1 = play/pause, 2 = mute, 3 = opens YouTube, 4 = opens Notepad and types a line.

To start it with Windows and no window: press **Win+R**, type `shell:startup`, Enter, and put a shortcut to `start_hidden.pyw` in that folder (right-click the file > Show more options > Create shortcut, then move the shortcut). To stop it, end **pythonw** in Task Manager. Use `start.bat` when you want to see its messages.

## Bluetooth or USB

The sketch talks over both at once; `connection` at the top of `buttons.toml` picks which one the helper listens to (`"bluetooth"` by default, `"usb"` for the cable). Restart the helper after changing it.

- **Don't pair it in Windows Bluetooth settings.** The helper connects to the device named `PC Fader` by itself. Your PC just needs Bluetooth switched on.
- The onboard LED glows dim blue while Bluetooth is connected.
- Bluetooth only carries the data. The board still needs power: a USB phone charger, a power bank, or the built-in battery in [BATTERY.md](BATTERY.md).
- Volume over Bluetooth can lag a few tens of milliseconds behind the fader; use USB if that bothers you.

## 3. Change what the buttons do

Open `helper/buttons.toml` in Notepad, change it, save. The next button press uses the new setting. The file explains each kind of action; a few examples:

```toml
[button1]
keys = "ctrl+shift+m"                  # a keyboard shortcut

[button2]
run = "C:\\Program Files\\Image-Line\\FL Studio 2024\\FL64.exe"   # open a program (double the backslashes)

[button3]
type = "my email signature"            # type text

[button4]
steps = [ {keys = "ctrl+a"}, {keys = "ctrl+c"}, {wait = 0.2}, {run = "notepad.exe"}, {wait = 1}, {keys = "ctrl+v"} ]
```

A button can also do something different on a double tap: add `double = {keys = "previous track"}` under it. Single taps on that button then wait about a third of a second before firing, to see if a second tap is coming.

If you make a typo, the helper prints what's wrong and keeps the last good settings.

## FL Studio

While FL Studio is the window in front, the fader and all four buttons send MIDI (fader CC 7, buttons CC 102–105: 127 while held, 0 on release), so you can link each one to anything in FL. Click any other window and it goes back to Windows volume and your normal buttons. Under `[fl.buttonN]` in `buttons.toml`, `keys = "space"` instead of `cc = ...` makes that button an FL keyboard shortcut; `mode = "always"` or `"off"` under `[fl]` changes when FL mode applies.

One-time setup:

1. Install **loopMIDI** (free, from tobias-erichsen.de). Open it, type `PC Fader` in the "New port-name" box and click **+**. Let it start with Windows (its tray icon > Autostart).
2. Restart the helper.
3. In FL Studio, open **Options > MIDI settings**. In the Input list, click **PC Fader** and turn on **Enable**.
4. Right-click FL's master fader (or any knob) > **Link to controller...**, then move your fader. FL learns it; close the window. Do the same for each button: right-click an FL control (play, record, a mute button, a plugin knob...) > **Link to controller...**, then press the button.

If the helper prints `MIDI port "PC Fader" not found`, loopMIDI isn't running or the port name differs from `midi_port` in `buttons.toml`.

## Things to know

- Shortcuts don't reach programs running as Administrator unless the helper is also run as Administrator.
- In USB mode, if auto-detect picks the wrong device, set `port = "COM5"` (your number, from Device Manager or the Arduino IDE port list) in `buttons.toml` and restart the helper.
- Volume follows whatever Windows has as the default output device, including after you switch to headphones.
- Self-check of the message parser and config: `py pc_fader.py --test` prints `ok`.
