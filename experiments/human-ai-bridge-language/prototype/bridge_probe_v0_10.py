#!/usr/bin/env python3
"""Typed JSON semantic probe for Bridge-0 v0.10."""

from __future__ import annotations

import json


def main() -> int:
    payload = {
        "result": 42,
        "state": {
            "ready": True,
            "values": [2, 3, 5, 7],
        },
        "summary": "stable",
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
