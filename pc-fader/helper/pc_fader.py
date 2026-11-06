# PC fader helper (Windows): fader -> master volume, buttons -> actions from buttons.toml.
# Edit buttons.toml and save; the change applies on the next button press, no restart needed.
import asyncio, os, queue, subprocess, sys, threading, time, tomllib
from pathlib import Path

import keyboard
import serial
from serial.tools import list_ports

CONFIG = Path(__file__).with_name("buttons.toml")


def set_volume(percent):
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import POINTER, cast
    dev = AudioUtilities.GetSpeakers()  # looked up each time so it follows headphones/speaker switches
    vol = getattr(dev, "EndpointVolume", None)  # newer pycaw
    if vol is None:  # older pycaw
        vol = cast(dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
    vol.SetMasterVolumeLevelScalar(percent / 100, None)


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
            press(n, config)
        try:  # short timeout while a double tap may follow; the timeout also keeps Ctrl+C working
            msg = parse(lines.get(timeout=0.05 if pending else 0.5))
        except queue.Empty:
            continue
        if not msg:
            continue
        if msg[0] == "F" and config.get("volume", True) and msg[1] != last:
            last = msg[1]
            set_volume(last)
        elif msg[0] == "B" and msg[2]:
            if CONFIG.stat().st_mtime != mtime:
                mtime = CONFIG.stat().st_mtime
                config = load_config() or config
            has_double = "double" in config.get(f"button{msg[1]}", {})
            kind = tap(pending, msg[1], time.monotonic(), has_double)
            if kind:
                press(msg[1], config, double=kind == "double")


if __name__ == "__main__":
    if "--test" in sys.argv:
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
        print("ok")
    else:
        try:
            main()
        except KeyboardInterrupt:
            pass
