#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Writes the finished front page to the output directory the harness
provides. The image is pre-rendered (see compose.py, the build script that
made it from the vignettes and the Natural Earth map data) and this program
only copies it, which is the pattern the competition rules name as the
simplest entry: "a repository holding the image and a one-line program that
copies it there". Standard library only, no network, fully deterministic:
the same bytes are written on every run.
"""
import hashlib
import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB, the competition's file limit
MAX_SIDE = 1024  # pixels, the competition's dimension limit


def die(message):
    """Print an error and exit non-zero."""
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def load_source():
    """Read entry.png from this repository and check it against the
    competition's limits: PNG signature, size, and dimensions. The
    dimensions come straight from the PNG IHDR chunk (width and height
    are big-endian uint32 at bytes 16 and 20), so no image library is
    needed."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_MAGIC):
        raise ValueError("entry.png does not start with the PNG signature")
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit")
    if len(data) < 24:
        raise ValueError("entry.png is too short to hold a PNG header")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"entry.png is {width}x{height}, over the "
            f"{MAX_SIDE}x{MAX_SIDE} limit")
    return data


def write_output(data):
    """Write the bytes to <output dir>/entry.png and verify the copy."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(data).digest():
        raise ValueError("written file differs from the source bytes")
    return target, len(written)


def main():
    try:
        data = load_source()
        target, size = write_output(data)
    except (OSError, ValueError) as exc:
        return die(str(exc))
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({size} bytes, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
