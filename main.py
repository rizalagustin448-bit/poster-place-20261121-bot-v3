#!/usr/bin/env python3
"""Write the AURMARA v3 travel poster to /output/entry.png.

The poster image is drawn at build time (draw_poster.py, Pillow) and
shipped as poster.png; this program only copies it into the output
directory the harness provides, so it runs with the standard library
alone and no network.
"""
import os
import shutil
from pathlib import Path

MAX_BYTES = 1_048_576


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "poster.png"
    if not src.is_file():
        raise FileNotFoundError(f"poster asset missing: {src}")
    if src.stat().st_size > MAX_BYTES:
        raise ValueError(f"poster asset too large: {src.stat().st_size} bytes")
    shutil.copyfile(src, out_dir / "entry.png")
    # Confirm the copy so a silent failure can never pass unnoticed.
    dest = out_dir / "entry.png"
    assert dest.is_file() and dest.stat().st_size == src.stat().st_size
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
