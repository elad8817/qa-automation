from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    """
    Resolve repository root reliably.
    Priority:
      1) env var QA_REPO_ROOT
      2) git root (if available)
      3) walk up from this file until we find pyproject.toml / .git / requirements.txt
    """
    # 1) explicit override
    env = os.getenv("QA_REPO_ROOT")
    if env:
        return Path(env).resolve()

    here = Path(__file__).resolve()

    # 2) heuristic walk up
    markers = {".git", "pyproject.toml", "requirements.txt"}
    for p in [here, *here.parents]:
        if any((p / m).exists() for m in markers):
            return p

    # fallback: project might be packaged differently
    return here.parents[2]


@lru_cache(maxsize=128)
def load_json(name: str, base_dir: str = "tests/data") -> Any:
    """
    Load JSON by filename from tests/data (default), cached.
    Usage: data = load_json("testdata.json")
    """
    path = repo_root() / base_dir / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get(path: str, *, file: str = "testdata.json", base_dir: str = "tests/data", default: Any = None) -> Any:
    """
    Get nested value by dotted path.
    Example: get("login.valid.username")
    """
    data = load_json(file, base_dir=base_dir)
    cur: Any = data
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur