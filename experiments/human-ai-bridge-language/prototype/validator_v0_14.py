#!/usr/bin/env python3
"""Bridge-0 Unicode text identity semantic validator v0.14."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
CODEPOINT_SEQUENCE = re.compile(r"^[0-9A-F]{4,6}(?:\+[0-9A-F]{4,6})*$")
ALLOWED_TARGETS = {"python312", "node20"}
REQUIRED_VECTORS = {
    "00E9",
    "0065+0301",
    "00C5",
    "0041+030A",
    "212B",
    "AC00",
    "1100+1161",
    "0065+0323+0301",
    "0065+0301+0323",
}


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def decode_codepoints(token: str) -> list[int] | None:
    if not CODEPOINT_SEQUENCE.fullmatch(token):
        return None
    points = [int(part, 16) for part in token.split("+")]
    for point in points:
        if point > 0x10FFFF or 0xD800 <= point <= 0xDFFF:
            return None
    return points


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors = []
    warnings = []
    conflicts = []

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V089", "statements must be a list"))
        return {"valid": False, "errors": errors, "warnings": warnings, "conflicts": conflicts}

    programs = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "program"
    ]
    computes = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "semantic_compute"
    ]
    others = [
        s for s in statements
        if isinstance(s, dict)
        and s.get("kind") not in {"program", "semantic_compute"}
    ]

    if others:
        errors.append(issue("V089", "v0.14 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V089", "v0.14 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V089", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V090", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V090",
                    "v0.14 Unicode test requires exactly python312,node20",
                    sid,
                )
            )

    if len(computes) != 1:
        errors.append(issue("V091", "v0.14 requires exactly one semantic compute task"))
    else:
        task = computes[0]
        sid = str(task.get("id"))

        if task.get("op") != "text_profile":
            errors.append(issue("V091", "v0.14 supports only op=text_profile", sid))
        if task.get("text_model") != "unicode_scalar":
            errors.append(issue("V092", "v0.14 requires text_model=unicode_scalar", sid))
        if task.get("normalization") != "NFC":
            errors.append(issue("V092", "v0.14 requires normalization=NFC", sid))
        if task.get("identity") != "normalized_scalar_sequence":
            errors.append(
                issue(
                    "V092",
                    "v0.14 requires identity=normalized_scalar_sequence",
                    sid,
                )
            )
        if task.get("observe") != "json_value":
            errors.append(issue("V092", "v0.14 requires observe=json_value", sid))

        values = csv_values(task.get("values"))
        if not values:
            errors.append(issue("V093", "Unicode conformance values must be non-empty", sid))
        else:
            if len(values) != len(set(values)):
                errors.append(issue("V093", "Unicode conformance tokens must be unique", sid))
            invalid = [value for value in values if decode_codepoints(value) is None]
            if invalid:
                errors.append(
                    issue(
                        "V093",
                        "invalid Unicode scalar token(s): " + ", ".join(invalid),
                        sid,
                    )
                )
            missing = sorted(REQUIRED_VECTORS - set(values))
            if missing:
                errors.append(
                    issue(
                        "V093",
                        "conformance vector missing: " + ", ".join(missing),
                        sid,
                    )
                )

        allowed = {
            "id",
            "kind",
            "op",
            "text_model",
            "normalization",
            "identity",
            "values",
            "observe",
        }
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V093", "semantic compute contains unsupported fields", sid))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
    }


def main() -> int:
    try:
        doc = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "errors": [{"rule": "V000", "message": str(exc)}]}))
        return 2
    result = validate_document(doc)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
