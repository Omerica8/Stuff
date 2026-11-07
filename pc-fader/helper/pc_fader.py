# PC fader helper (Windows): fader -> master volume, buttons -> actions from buttons.toml.
# Edit buttons.toml and save; the change applies on the next button press, no restart needed.
import asyncio, os, queue, subprocess, sys, threading, time, tomllib
from pathlib import Path

import keyboard
import serial
from serial.tools import list_ports

# Next to the .exe when packaged (PyInstaller unpacks the script to a temp folder), else next to this file.
HERE = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
CONFIG = HERE / "buttons.toml"


def set_volume(percent):
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import POINTER, cast
    dev = AudioUtilities.GetSpeakers()  # looked up each time so it follows headphones/speaker switches
    vol = getattr(dev, "EndpointVolume", None)  # newer pycaw
    if vol is None:  # older pycaw
        vol = cast(dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
    vol.SetMasterVolumeLevelScalar(percent / 100, None)


def foreground_exe():
    """File name of the program in front, e.g. "FL64.exe" ("" if unknown or not on Windows)."""
    try:
        import ctypes
        from ctypes import wintypes
        user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ctypes.byref(pid))
        handle = kernel32.OpenProcess(0x1000, False, pid.value)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return ""
        try:
            buf, size = ctypes.create_unicode_buffer(260), wintypes.DWORD(260)
            kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size))
            return Path(buf.value).name
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        return ""


def fl_active(config, exe):
    """True when the [fl] settings apply: FL Studio is in front (mode "auto") or mode is "always"."""
    fl = config.get("fl")
    if not fl:
        return False
    mode = fl.get("mode", "auto")
    return mode == "always" or (mode == "auto" and exe.lower() == fl.get("app", "FL64.exe").lower())


def active(config, fl_on):
    """The settings to use now: [fl.buttonN] replace [buttonN] while FL is active."""
    if not fl_on:
        return config
    return {**config, **{k: v for k, v in config["fl"].items() if k.startswith("button")}}


midi_out, midi_retry = None, 0.0


def send_cc(fl, percent):
    """Fader -> MIDI CC on a loopMIDI port, for FL Studio's "Link to controller"."""
    global midi_out, midi_retry
    import mido
    if midi_out is None:
        if time.monotonic() < midi_retry:
            return
        name = fl.get("midi_port", "PC Fader")
        found = [n for n in mido.get_output_names() if n.startswith(name)]
        if not found:
            print(f'MIDI port "{name}" not found: is loopMIDI running with a port of that name?')
            midi_retry = time.monotonic() + 5
            return
        midi_out = mido.open_output(found[0])
    midi_out.send(mido.Message("control_change", channel=fl.get("channel", 1) - 1,
                               control=fl.get("fader_cc", 7), value=round(percent * 127 / 100)))


def do_step(step):
    if "keys" in step:
        keyboard.send(step["keys"])
    if "type" in step:
        keyboard.write(step["type"])
    if "run" in step:
        os.startfile(step["run"])  # a program, file, folder or https:// link
    if "command" in step:
        subprocess.Popen(step["command"], shell=True)
    if "wait" in step:
        time.sleep(step["wait"])


def press(n, config, double=False):
    action = config.get(f"button{n}")
    if action and double:
        action = action.get("double")
    if not action:
        print(f"button {n}: nothing set in buttons.toml")
        return
    print(f"button {n}{' double tap' if double else ''}: {action}")
    for step in action.get("steps", [action]):
        try:
            do_step(step)
        except Exception as e:  # a bad macro must not stop the fader
            print(f"  failed: {e}")


DOUBLE_TAP = 0.35  # seconds between taps that count as a double tap


def tap(pending, n, now, has_double):
    """Returns "single", "double" or None (wait for a possible second tap). pending = {button: first tap time}."""
    if n in pending:
        del pending[n]
        return "double"
    if has_double:
        pending[n] = now
        return None
    return "single"


def expired(pending, now):
    """Buttons whose double-tap window ran out: fire their single action."""
    done = [n for n, t in pending.items() if now - t > DOUBLE_TAP]
    for n in done:
        del pending[n]
    return done


def load_config():
    try:
        return tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"buttons.toml has a mistake, keeping the old settings: {e}")
        return None


def parse(line):
    """'F 73' -> ('F', 73); 'B 2 1' -> ('B', 2, True); anything else -> None."""
    parts = line.split()
    try:
        if parts[0] == "F" and len(parts) == 2:
            return "F", max(0, min(100, int(parts[1])))
        if parts[0] == "B" and len(parts) == 3:
            return "B", int(parts[1]), parts[2] == "1"
    except (IndexError, ValueError):
        pass
    return None


def find_port(config):
    port = config.get("port", "auto")
    if port != "auto":
        return port
    for p in list_ports.comports():  # the fader sends "F nn" every second, so listen for it
        try:
            with serial.Serial(p.device, 115200, timeout=1.5) as s:
                if parse(s.readline().decode(errors="ignore")) or parse(s.readline().decode(errors="ignore")):
                    return p.device
        except serial.SerialException:
            pass
    return None


NUS_TX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # must match the sketch


def read_usb(config, lines):
    while True:
        port = find_port(config)
        if not port:
            print("Fader not found, is it plugged in? Trying again...")
            time.sleep(2)
            continue
        print(f"Connected on {port}. Ctrl+C to quit.")
        try:
            with serial.Serial(port, 115200, timeout=2) as s:
                while True:
                    lines.put(s.readline().decode(errors="ignore"))
        except serial.SerialException:
            print("Fader unplugged.")
            time.sleep(1)


async def read_bluetooth(name, lines):
    from bleak import BleakClient, BleakScanner
    while True:
        print(f'Looking for Bluetooth device "{name}"...')
        dev = await BleakScanner.find_device_by_name(name, timeout=10)
        if not dev:
            continue
        buf = ""

        def on_data(_, data):
            nonlocal buf
            buf += data.decode(errors="ignore")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                lines.put(line)

        gone = asyncio.Event()
        try:
            # use_cached_services=False: Windows re-reads the services after a reflash
            async with BleakClient(dev, disconnected_callback=lambda _: gone.set(),
                                   winrt={"use_cached_services": False}) as client:
                await client.start_notify(NUS_TX, on_data)
                print("Connected over Bluetooth. Ctrl+C to quit.")
                await gone.wait()
            print("Bluetooth disconnected.")
        except Exception as e:  # out of range, switched off, etc.: just look again
            print(f"Bluetooth connect failed: {e}")
            await asyncio.sleep(2)


def main():
    config = load_config() or {}
    mtime = CONFIG.stat().st_mtime
    lines = queue.Queue()
    # The reader runs in its own thread; volume and macros run here, so Bluetooth and the
    # Windows audio API don't share a COM apartment.
    if config.get("connection", "usb") == "bluetooth":
        reader = lambda: asyncio.run(read_bluetooth(config.get("bluetooth_name", "PC Fader"), lines))
    else:
        reader = lambda: read_usb(config, lines)
    threading.Thread(target=reader, daemon=True).start()
    last = None
    pending = {}
    while True:
        for n in expired(pending, time.monotonic()):
            press(n, active(config, fl_active(config, foreground_exe())))
        try:  # short timeout while a double tap may follow; the timeout also keeps Ctrl+C working
            msg = parse(lines.get(timeout=0.05 if pending else 0.5))
        except queue.Empty:
            continue
        if not msg:
            continue
        if msg[0] == "F" and msg[1] != last:
            last = msg[1]
            if fl_active(config, foreground_exe()):
                send_cc(config["fl"], last)
            elif config.get("volume", True):
                set_volume(last)
        elif msg[0] == "B" and msg[2]:
            if CONFIG.stat().st_mtime != mtime:
                mtime = CONFIG.stat().st_mtime
                config = load_config() or config
            now = active(config, fl_active(config, foreground_exe()))
            has_double = "double" in now.get(f"button{msg[1]}", {})
            kind = tap(pending, msg[1], time.monotonic(), has_double)
            if kind:
                press(msg[1], now, double=kind == "double")


if __name__ == "__main__":
    if "--test" in sys.argv:
        if getattr(sys, "frozen", False):  # the .exe must have bundled the lazily imported parts
            import bleak, comtypes, mido.backends.rtmidi, pycaw.pycaw, rtmidi  # noqa: F401
        assert parse("F 73\n") == ("F", 73)
        assert parse("F 150") == ("F", 100)
        assert parse("B 2 1") == ("B", 2, True)
        assert parse("B 2 0") == ("B", 2, False)
        assert parse("garbage") is None and parse("") is None and parse("F x") is None
        assert tomllib.loads(CONFIG.read_text(encoding="utf-8"))["button4"]["steps"]
        p = {}
        assert tap(p, 1, 0.0, False) == "single" and not p
        assert tap(p, 3, 0.0, True) is None and expired(p, 0.2) == []
        assert tap(p, 3, 0.2, True) == "double" and not p
        assert tap(p, 3, 1.0, True) is None and expired(p, 1.4) == [3] and not p
        c = {"button1": {"keys": "a"}, "button2": {"keys": "b"}, "fl": {"button1": {"keys": "space"}}}
        assert fl_active(c, "FL64.exe") and fl_active(c, "fl64.EXE") and not fl_active(c, "chrome.exe")
        assert not fl_active({}, "FL64.exe") and fl_active({"fl": {"mode": "always"}}, "")
        assert not fl_active({"fl": {"mode": "off"}}, "FL64.exe")
        assert active(c, True)["button1"] == {"keys": "space"} and active(c, True)["button2"] == {"keys": "b"}
        assert active(c, False) is c and foreground_exe() in ("", Path(foreground_exe()).name)
        print("ok")
    else:
        try:
            main()
        except KeyboardInterrupt:
            pass
