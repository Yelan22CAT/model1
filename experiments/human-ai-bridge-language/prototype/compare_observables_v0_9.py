#!/usr/bin/env python3
"""Compare Bridge-0 v0.9 backend observables."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(normalize(path.read_bytes())).hexdigest()


def equivalent(left: pathlib.Path, right: pathlib.Path) -> bool:
    return normalize(left.read_bytes()) == normalize(right.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left")
    parser.add_argument("right")
    args = parser.parse_args()

    left = pathlib.Path(args.left)
    right = pathlib.Path(args.right)

    if not equivalent(left, right):
        print(
            f"BACKEND_DRIFT left={digest(left)} right={digest(right)}",
            file=sys.stderr,
        )
        return 1

    print(f"BRIDGE_BACKEND_EQUIVALENT sha256={digest(left)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
