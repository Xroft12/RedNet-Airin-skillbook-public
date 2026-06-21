#!/usr/bin/env python3
"""Validate REDNET public schemas and example files.

This validator intentionally implements only the JSON Schema subset used by
the public REDNET schema files. It avoids external dependencies so cycle-close
can run on a clean Windows workstation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


EXAMPLE_SCHEMA_PAIRS = [
    (
        ROOT / "examples" / "hermes-next-gen" / "profile-passport.example.json",
        ROOT / "schemas" / "hermes-profile-passport.schema.json",
    ),
    (
        ROOT / "examples" / "hermes-next-gen" / "hook-registry.example.json",
        ROOT / "schemas" / "hook-registry.schema.json",
    ),
    (
        ROOT / "examples" / "hermes-next-gen" / "plugin-capabilities.example.json",
        ROOT / "schemas" / "plugin-capability.schema.json",
    ),
]

JSONL_SCHEMA_PAIRS = [
    (
        ROOT
        / "packages"
        / "agents"
        / "rednet-science-coordinator"
        / "examples"
        / "task-ledger.example.jsonl",
        ROOT / "schemas" / "science-flow.schema.json",
    )
]


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_type(value: Any, expected: str, path: str) -> None:
    checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "boolean": lambda item: isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
    }
    check = checks.get(expected)
    if check is None:
        return
    if not check(value):
        raise ValidationError(f"{path}: expected {expected}, got {type(value).__name__}")


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected_type = schema.get("type")
    if isinstance(expected_type, str):
        validate_type(value, expected_type, path)

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationError(f"{path}: value {value!r} is not allowed")

    if "const" in schema and value != schema["const"]:
        raise ValidationError(f"{path}: expected constant {schema['const']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            raise ValidationError(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(str(schema["pattern"]), value):
            raise ValidationError(f"{path}: value {value!r} does not match pattern")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise ValidationError(f"{path}: missing required field {key!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                joined = ", ".join(sorted(extra))
                raise ValidationError(f"{path}: additional properties: {joined}")

        for key, item in value.items():
            if key in properties:
                validate_schema(item, properties[key], f"{path}.{key}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            raise ValidationError(f"{path}: too few items")
        if schema.get("uniqueItems") is True:
            normalized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(normalized)) != len(normalized):
                raise ValidationError(f"{path}: duplicate array items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{index}]")


def validate_json_pair(example_path: Path, schema_path: Path) -> str:
    example = load_json(example_path)
    schema = load_json(schema_path)
    validate_schema(example, schema)
    return f"OK {example_path.relative_to(ROOT)}"


def validate_jsonl_pair(example_path: Path, schema_path: Path) -> str:
    schema = load_json(schema_path)
    count = 0
    with example_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            validate_schema(item, schema, f"$[{line_number}]")
            count += 1
    if count == 0:
        raise ValidationError(f"{example_path}: empty JSONL")
    return f"OK {example_path.relative_to(ROOT)} ({count} rows)"


def main() -> int:
    results: list[str] = []
    try:
        for schema_path in sorted((ROOT / "schemas").glob("*.json")):
            load_json(schema_path)
            results.append(f"OK {schema_path.relative_to(ROOT)}")
        for example_path, schema_path in EXAMPLE_SCHEMA_PAIRS:
            results.append(validate_json_pair(example_path, schema_path))
        for example_path, schema_path in JSONL_SCHEMA_PAIRS:
            results.append(validate_jsonl_pair(example_path, schema_path))
    except Exception as exc:
        print(f"schema validation failed: {exc}", file=sys.stderr)
        return 1

    print("\n".join(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
