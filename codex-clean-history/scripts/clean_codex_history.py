#!/usr/bin/env python3
"""Preview or clean local Codex history artifacts while preserving memories."""

from __future__ import annotations

import argparse
import fnmatch
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path


DEFAULT_INCLUDE = {
    "history": ["history.jsonl"],
    "sessions": ["sessions"],
    "logs": ["log", "logs_*.sqlite", "logs_*.sqlite-shm", "logs_*.sqlite-wal"],
    "snapshots": ["shell_snapshots"],
    "tmp": [".tmp", "tmp"],
}

PROTECTED_PATTERNS = [
    "auth.json",
    "config.toml",
    "installation_id",
    "version.json",
    "models_cache.json",
    "memories",
    "memories_*",
    "rules",
    "skills",
    "plugins",
    "cache",
    "goals_*.sqlite*",
    "state_*.sqlite*",
]


@dataclass(frozen=True)
class Target:
    path: Path
    category: str
    size: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean Codex logs, sessions, input history, and shell snapshots without touching memories."
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"),
        help="Codex home directory. Defaults to $CODEX_HOME or ~/.codex.",
    )
    parser.add_argument("--apply", action="store_true", help="Delete files. Omit for dry-run.")
    parser.add_argument(
        "--days",
        type=float,
        default=None,
        help="Only remove targets whose newest mtime is older than this many days.",
    )
    parser.add_argument(
        "--categories",
        default="history,sessions,logs,snapshots,tmp",
        help="Comma-separated categories: history,sessions,logs,snapshots,tmp",
    )
    return parser.parse_args()


def is_protected(path: Path, codex_home: Path) -> bool:
    try:
        rel = path.relative_to(codex_home)
    except ValueError:
        return True
    if rel.parts and rel.parts[0] in {"memories", "rules", "skills", "plugins", "cache"}:
        return True
    name = rel.as_posix()
    base = rel.parts[0] if rel.parts else ""
    return any(fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(base, pat) for pat in PROTECTED_PATTERNS)


def tree_size(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file() or path.is_symlink():
        return path.stat().st_size
    total = 0
    for child in path.rglob("*"):
        if child.is_file() or child.is_symlink():
            try:
                total += child.stat().st_size
            except FileNotFoundError:
                pass
    return total


def newest_mtime(path: Path) -> float:
    if path.is_file() or path.is_symlink():
        return path.stat().st_mtime
    newest = path.stat().st_mtime
    for child in path.rglob("*"):
        try:
            newest = max(newest, child.stat().st_mtime)
        except FileNotFoundError:
            pass
    return newest


def collect_targets(codex_home: Path, categories: list[str], days: float | None) -> list[Target]:
    cutoff = None if days is None else time.time() - (days * 86400)
    targets: list[Target] = []
    seen: set[Path] = set()

    for category in categories:
        patterns = DEFAULT_INCLUDE.get(category)
        if patterns is None:
            raise ValueError(f"unknown category: {category}")
        for pattern in patterns:
            matches = list(codex_home.glob(pattern))
            for path in matches:
                path = path.resolve()
                if path in seen or not path.exists():
                    continue
                if is_protected(path, codex_home):
                    raise RuntimeError(f"refusing protected target: {path}")
                if cutoff is not None and newest_mtime(path) >= cutoff:
                    continue
                seen.add(path)
                targets.append(Target(path=path, category=category, size=tree_size(path)))

    return sorted(targets, key=lambda t: str(t.path))


def delete_target(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def format_size(num: int) -> str:
    value = float(num)
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if value < 1024 or unit == "GiB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{num} B"
        value /= 1024
    return f"{num} B"


def main() -> int:
    args = parse_args()
    codex_home = Path(args.codex_home).expanduser().resolve()
    if not codex_home.is_dir():
        print(f"Codex home not found: {codex_home}", file=sys.stderr)
        return 2

    categories = [item.strip() for item in args.categories.split(",") if item.strip()]
    targets = collect_targets(codex_home, categories, args.days)
    action = "DELETE" if args.apply else "DRY-RUN"
    total = sum(target.size for target in targets)

    print(f"{action}: {len(targets)} target(s), {format_size(total)}")
    for target in targets:
        rel = target.path.relative_to(codex_home)
        print(f"{target.category:9} {format_size(target.size):>10} {rel}")

    if not args.apply:
        print("No files deleted. Re-run with --apply to clean these targets.")
        return 0

    for target in targets:
        delete_target(target.path)
    print("Cleanup complete. Memories and protected Codex files were not targeted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
