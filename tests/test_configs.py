"""Shape checks for the assignment config files.

The companion app returns an existing file verbatim, so these tests assert
structure and leave the welcome-message text alone.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_NAME = re.compile(r"^[a-z][a-z0-9]*-config\.(json|yml)$")
REQUIRED = ("dev-config.json", "test-config.json", "test-config.yml")


def config_files() -> list[Path]:
    """Return root-level assignment configs in name order."""
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_file() and CONFIG_NAME.fullmatch(path.name)
    )


def load_mapping(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    loaded = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    assert isinstance(loaded, dict), f"{path.name} must be a mapping"
    return loaded


def test_required_configs_are_present() -> None:
    names = {path.name for path in config_files()}
    missing = [name for name in REQUIRED if name not in names]
    assert missing == []


def test_configs_are_only_at_repo_root() -> None:
    nested: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if path.is_file() and path.parent != ROOT and CONFIG_NAME.fullmatch(path.name):
            nested.append(relative.as_posix())
    assert nested == []


@pytest.mark.parametrize("path", config_files(), ids=lambda path: path.name)
def test_welcome_message_is_a_nonempty_string(path: Path) -> None:
    message = load_mapping(path).get("welcome_message")
    assert isinstance(message, str)
    assert message.strip()
