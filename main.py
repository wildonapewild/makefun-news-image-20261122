#!/usr/bin/env python3
"""THE MERIDIAN LINE — MakeFun entry carrier for Final 4 (@wildonaped),
NI22 Wave 7.

Wave 7 rebuild from the verified Sunday 22 November 2026 pool (bedah Top 1):
15 cards + 21 briefs = 36 stories, all dated Sunday 22 November 2026, with
per-card certainty/source tags, a UTC timeline, a day-in-numbers strip, a
dotted world map with numbered pins, and a named DATE CHECK. Layout A:
three leads in a row, then 12 minis. Stdlib-only carrier: verifies the PNG
signature, reads the IHDR dimensions and REFUSES to ship an image that
breaks the 1024x1024 gate, copies entry.png byte-for-byte into
MAKEFUN_OUTPUT_DIR (fallback /output), then verifies the copy is
byte-identical.
"""
import hashlib
import os
import shutil
import struct
import sys

CONCEPT = "THE MERIDIAN LINE — Sunday's World in One Picture"
ACCOUNT = "@wildonaped"
ACCOUNT_LABEL = "Final 4"
BOUNTY = "news-image-20261122"
STORIES = 36  # 15 cards + 21 briefs, 7 regions
MAX_SIDE = 1024  # server gate: dimensions must stay within 1x1..1024x1024

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != PNG_SIG:
        raise ValueError("entry.png: bad PNG signature")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png: first chunk is not IHDR")
    return struct.unpack(">II", head[16:24])


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if not os.path.isfile(ENTRY):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    width, height = png_dimensions(ENTRY)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"dimension gate: {width}x{height} exceeds {MAX_SIDE}x{MAX_SIDE}",
              file=sys.stderr)
        return 1
    digest = sha256_of(ENTRY)
    size = os.path.getsize(ENTRY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ENTRY, dest)

    if sha256_of(dest) != digest or os.path.getsize(dest) != size:
        print("copy verification FAILED: output bytes differ", file=sys.stderr)
        return 1

    print(f"Concept : {CONCEPT}")
    print(f"Account : {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty  : {BOUNTY}")
    print(f"File    : entry.png -> {dest}")
    print(f"Size    : {size} bytes")
    print(f"Dim     : {width}x{height} px (gate <= {MAX_SIDE}x{MAX_SIDE}: OK)")
    print(f"SHA256  : {digest}")
    print(f"Stories : {STORIES} (15 cards + 21 briefs, 7 regions)")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
