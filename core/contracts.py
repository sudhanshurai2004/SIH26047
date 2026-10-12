"""Local contract loading and validation helpers.

The helpers deliberately use only repository files and ``yaml.safe_load``.
They are the single validation path that later upload endpoints will use.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any, Literal

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ContractName = Literal["scenario", "event", "doctrine"]

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = REPOSITORY_ROOT / "contracts"
SCHEMA_PATHS: dict[ContractName, Path] = {
    "scenario": CONTRACTS_DIR / "scenario.schema.json",
    "event": CONTRACTS_DIR / "event.schema.json",
    "doctrine": CONTRACTS_DIR / "doctrine.schema.json",
}


class ContractValidationError(ValueError):
    """Raised when a payload does not satisfy a frozen contract."""


def load_json_file(path: Path) -> Any:
    """Load a UTF-8 JSON fixture without performing validation."""
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def load_yaml_file(path: Path) -> Any:
    """Load YAML safely; object construction tags are never executed."""
    with path.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


@cache
def validator_for(contract: ContractName) -> Draft202012Validator:
    """Return a checked Draft 2020-12 validator for one local contract."""
    schema = load_json_file(SCHEMA_PATHS[contract])
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_payload(contract: ContractName, payload: Any) -> None:
    """Validate *payload* or raise one deterministic, readable error."""
    errors = sorted(
        validator_for(contract).iter_errors(payload),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ContractValidationError(f"{contract} contract invalid at {location}: {error.message}")


def load_and_validate(contract: ContractName, path: Path) -> Any:
    """Load a local JSON/YAML payload and validate it against its contract."""
    payload = load_yaml_file(path) if path.suffix in {".yaml", ".yml"} else load_json_file(path)
    validate_payload(contract, payload)
    return payload
