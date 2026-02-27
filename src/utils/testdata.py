from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

DEFAULT_DATA_DIR = "src/data"


def repo_root() -> Path:
    """Resolve repository root reliably."""
    env = os.getenv("QA_REPO_ROOT")
    if env:
        return Path(env).resolve()

    here = Path(__file__).resolve()
    markers = {".git", "pyproject.toml", "requirements.txt"}
    for parent in [here, *here.parents]:
        if any((parent / marker).exists() for marker in markers):
            return parent

    return here.parents[2]


@lru_cache(maxsize=128)
def load_json(name: str, base_dir: str = DEFAULT_DATA_DIR) -> Any:
    """Load JSON by filename from ``base_dir`` and cache the result."""
    path = repo_root() / base_dir / name
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get(path: str, *, file: str, base_dir: str = DEFAULT_DATA_DIR, default: Any = None) -> Any:
    """Get nested value from JSON using dotted path syntax."""
    data = load_json(file, base_dir=base_dir)
    current: Any = data
    for key in path.split("."):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
