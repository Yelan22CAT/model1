#!/usr/bin/env python3
"""Typed JSON semantic comparator for Bridge-0 v0.10."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import sys
from typing import Any


class TypedObservableError(ValueError):
    pass


def reject_constant(value: str):
    raise TypedObservableError(f"non-finite JSON number is forbidden: {value}")


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise TypedObservableError("non-finite number")
        if value.is_integer():
            return int(value)
        return value
    return value


def load_semantic(path: pathlib.Path) -> Any:
    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, TypedObservableError) as exc:
        raise TypedObservableError(f"{path}: invalid json_value observable: {exc}") from exc
    return normalize(raw)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        normalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def compare(paths: list[pathlib.Path]) -> tuple[bool, str]:
    if len(paths) < 2:
        raise TypedObservableError("at least two observables are required")
    values = [load_semantic(path) for path in paths]
    baseline = values[0]
    if any(value != baseline for value in values[1:]):
        detail = " ".join(
            f"{path.name}={digest(value)}"
            for path, value in zip(paths, values)
        )
        return False, detail
    return True, digest(baseline)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    paths = [pathlib.Path(item) for item in args.paths]
    try:
        equal, detail = compare(paths)
    except TypedObservableError as exc:
        print(f"TYPED_OBSERVABLE_ERROR {exc}", file=sys.stderr)
        return 2

    if not equal:
        print(f"HETEROGENEOUS_BACKEND_DRIFT {detail}", file=sys.stderr)
        return 1

    print(f"BRIDGE_TYPED_EQUIVALENT sha256={detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
