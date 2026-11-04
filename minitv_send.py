"""Stream your screen (or part of it) to the ESP32 mini TV over Wi-Fi.

Install:  pip install mss pillow numpy
Run:      python minitv_send.py 192.168.1.50
Options:  --fps 10                      frames per second (try 5-20)
          --monitor 1                   which monitor to capture
          --region X Y WIDTH HEIGHT     capture only this rectangle (e.g. a phone-mirror window)
"""
import argparse
import socket
import time

import numpy as np
from mss import mss
from PIL import Image, ImageOps

W, H, ROWS, PORT = 256, 240, 4, 5005


def to_tv(img):
    """Fit any image onto the 4:3 TV and pack it as grayscale RGB332 bytes (H x W)."""
    # Pad on square pixels at 4:3, then squash to 256 wide: the TV stretches it back.
    img = ImageOps.pad(img.convert("L"), (320, 240)).resize((W, H), Image.BILINEAR)
    v = np.asarray(img, dtype=np.uint8)
    # Same level in R, G and B: no color, so a B/W set shows clean grays.
    return (v & 0xE0) | ((v >> 3) & 0x1C) | (v >> 6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ip", help="IP shown in the ESP32 serial monitor")
    ap.add_argument("--fps", type=float, default=10)
    ap.add_argument("--monitor", type=int, default=1)
    ap.add_argument("--region", type=int, nargs=4, metavar=("X", "Y", "W", "H"))
    a = ap.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with mss() as sct:
        area = sct.monitors[a.monitor]
        if a.region:
            x, y, w, h = a.region
            area = {"left": x, "top": y, "width": w, "height": h}
        print(f"Streaming to {a.ip}:{PORT} at {a.fps} fps. Ctrl+C to stop.")
        while True:
            start = time.time()
            shot = sct.grab(area)
            px = to_tv(Image.frombytes("RGB", shot.size, shot.rgb))
            for r in range(0, H, ROWS):
                sock.sendto(bytes([r]) + px[r:r + ROWS].tobytes(), (a.ip, PORT))
            time.sleep(max(0, 1 / a.fps - (time.time() - start)))


if __name__ == "__main__":
    main()
