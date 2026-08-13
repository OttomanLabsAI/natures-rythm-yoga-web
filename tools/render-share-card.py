#!/usr/bin/env python3
"""Render tools/share-card.html to public/assets/img/share-card.png (1200x630).

Headless Chromium here renders a viewport shorter than the requested window
height, which silently crops the bottom of the card. So the page is captured
into a deliberately taller window and the result is cropped back to exactly
1200x630. Standard library only — no image dependencies.

Usage:  python3 tools/render-share-card.py [path/to/chromium]
"""

import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

WIDTH, HEIGHT = 1200, 630
CAPTURE_PAD = 220  # extra window height to absorb the viewport shortfall

ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
SOURCE = os.path.join(ROOT, "tools", "share-card.html")
TARGET = os.path.join(ROOT, "public", "assets", "img", "share-card.png")

CANDIDATES = [
    "/opt/pw-browsers/chromium",
    "chromium",
    "chromium-browser",
    "google-chrome",
]


def find_chromium(explicit=None):
    for name in ([explicit] if explicit else []) + CANDIDATES:
        path = shutil.which(name) or (name if os.path.exists(name) else None)
        if path:
            return path
    sys.exit("Could not find Chromium. Pass its path as the first argument.")


def read_png(path):
    """Return (width, height, channels, list-of-unfiltered-rows)."""
    data = open(path, "rb").read()
    pos, idat = 8, b""
    width = height = colour = None
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        if kind == b"IHDR":
            width, height, depth, colour = struct.unpack(">IIBB", data[pos + 8:pos + 18])
            if depth != 8 or colour not in (2, 6):
                sys.exit("Unexpected PNG format from Chromium (depth %d, colour %d)" % (depth, colour))
        elif kind == b"IDAT":
            idat += data[pos + 8:pos + 8 + length]
        pos += 12 + length

    channels = 3 if colour == 2 else 4
    raw = zlib.decompress(idat)
    stride = width * channels
    rows, prev, offset = [], bytearray(stride), 0

    for _ in range(height):
        filt = raw[offset]
        offset += 1
        line = bytearray(raw[offset:offset + stride])
        offset += stride
        if filt == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 255
        elif filt == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif filt == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 255
        elif filt == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line
        if len(rows) >= HEIGHT:  # everything below the crop is discarded anyway
            break

    return width, height, channels, rows


def write_png(path, width, rows, channels):
    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    stride = width * channels
    body = b"".join(b"\x00" + row[:stride] for row in rows)
    colour = 2 if channels == 3 else 6
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, len(rows), 8, colour, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(body, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def main():
    chromium = find_chromium(sys.argv[1] if len(sys.argv) > 1 else None)
    with tempfile.TemporaryDirectory() as tmp:
        shot = os.path.join(tmp, "capture.png")
        subprocess.run([
            chromium, "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            "--virtual-time-budget=10000",
            "--window-size=%d,%d" % (WIDTH, HEIGHT + CAPTURE_PAD),
            "--screenshot=" + shot, SOURCE,
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        width, height, channels, rows = read_png(shot)
        if width != WIDTH or len(rows) < HEIGHT:
            sys.exit("Capture was %dx%d; expected at least %dx%d" % (width, len(rows), WIDTH, HEIGHT))

        os.makedirs(os.path.dirname(TARGET), exist_ok=True)
        write_png(TARGET, WIDTH, rows[:HEIGHT], channels)

    print("wrote %s (%dx%d, %.0f KiB)" % (
        os.path.relpath(TARGET, ROOT), WIDTH, HEIGHT, os.path.getsize(TARGET) / 1024))


if __name__ == "__main__":
    main()
