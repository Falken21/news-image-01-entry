#!/usr/bin/env python3
"""Entry for make.fun news-image-01 ("The Daily Byte").

Copies the front-page image entry.png to the output directory.
The image is a newspaper front page drawn with PIL from researched
headlines of Friday 13 November 2026: Nvidia chief Jensen Huang
resigns, Europe joins the Ukraine peace talks, and England beat
Croatia to reach the Nations League quarter-finals.

Before copying, the program validates the image against the
competition gate: a PNG signature, at most 1 MiB, at most
1024 by 1024 pixels. Deterministic: the same image on every run,
no network, stdlib only.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct

IMAGE = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB
MAX_DIMENSION = 1024


def validate_png(path: str) -> None:
    """Check the gate rules: PNG signature, size, dimensions."""
    with open(path, "rb") as f:
        data = f.read()
    assert data[:8] == PNG_SIGNATURE, "entry.png is not a PNG file"
    assert len(data) <= MAX_BYTES, "entry.png exceeds 1 MiB"
    # IHDR chunk: width and height are the first 8 bytes after the
    # 8-byte signature, 4-byte length and 4-byte "IHDR" type.
    assert data[12:16] == b"IHDR", "entry.png has no IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    assert width <= MAX_DIMENSION, "entry.png wider than 1024 px"
    assert height <= MAX_DIMENSION, "entry.png taller than 1024 px"


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE)
    validate_png(source)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(output_dir, IMAGE))


if __name__ == "__main__":
    main()
