"""Helpers for making the current clawteam executable available to spawned agents."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def resolve_clawteam_executable() -> str:
    """Resolve the current clawteam executable.

    Prefer the current process entrypoint when running from a venv or editable
    install via an absolute path. Fall back to `shutil.which("clawteam")`, then
    the bare command name.
    """

    argv0 = (sys.argv[0] or "").strip()
    if argv0:
        candidate = Path(argv0).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())

    resolved = shutil.which("clawteam")
    return resolved or "clawteam"


def build_spawn_path(base_path: str | None = None) -> str:
    """Ensure the current clawteam executable directory is on PATH."""

    path_value = base_path if base_path is not None else os.environ.get("PATH", "")
    executable = resolve_clawteam_executable()
    if not os.path.isabs(executable):
        return path_value

    bin_dir = str(Path(executable).resolve().parent)
    path_parts = [part for part in path_value.split(os.pathsep) if part] if path_value else []
    if bin_dir in path_parts:
        return path_value
    if not path_parts:
        return bin_dir
    return os.pathsep.join([bin_dir, *path_parts])
