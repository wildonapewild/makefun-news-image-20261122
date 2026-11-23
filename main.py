"""THE MERIDIAN LINE milik @wildonaped (Akun Final 4) — NI22 Wave 7.

Garis meridian pada kanvas ini hanya jujur kalau berkasnya juga jujur.
Skrip ini membaca kepala PNG, menolak kanvas yang kebesaran, kemudian
menyalin gambar ke tujuan keluaran dan mencocokkan ulang hasilnya.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

CONCEPT = "THE MERIDIAN LINE"
ACCOUNT = "@wildonaped"
ACCOUNT_LABEL = "Akun Final 4"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

EXPECTED_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def fingerprint(path):
    """Kembalikan pasangan (sha256, ukuran) dari sebuah berkas."""
    sha = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(32768), b""):
            sha.update(chunk)
            size += len(chunk)
    return sha.hexdigest(), size


def read_dimensions(path):
    """Ambil lebar dan tinggi dari 33 byte pertama sebuah PNG."""
    with path.open("rb") as stream:
        prefix = stream.read(33)
    if len(prefix) != 33:
        raise ValueError("prefix PNG kependekan")
    if prefix[0:8] != EXPECTED_MAGIC:
        raise ValueError("bukan berkas PNG")
    if prefix[12:16] != b"IHDR":
        raise ValueError("IHDR hilang")
    return struct.unpack(">II", prefix[16:24])


def main():
    folder = Path(__file__).resolve().parent
    picture = folder / "entry.png"
    if not picture.exists():
        print("entry.png tidak ditemukan.", file=sys.stderr)
        return 1

    # Kepala berkas dibaca lebih dulu; salinan tidak dibuat sebelum lolos.
    try:
        w, h = read_dimensions(picture)
    except ValueError as problem:
        print(f"Berkas ditolak: {problem}", file=sys.stderr)
        return 1
    if w > MAX_SIDE or h > MAX_SIDE:
        print(f"Ukuran {w}x{h} melebihi pagu {MAX_SIDE} piksel.", file=sys.stderr)
        return 1

    before = fingerprint(picture)

    destination_dir = Path(os.getenv("MAKEFUN_OUTPUT_DIR") or "/output")
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    destination.write_bytes(picture.read_bytes())

    after = fingerprint(destination)
    if after != before:
        print("Hasil salinan berbeda dari aslinya.", file=sys.stderr)
        return 1

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {before[1]}")
    print(f"Dim: {w}x{h}")
    print(f"SHA256: {before[0]}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
