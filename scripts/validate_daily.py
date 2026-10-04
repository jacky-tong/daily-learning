#!/usr/bin/env python3
"""Validate the small, repeatable contract for daily learning notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "daily"
DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")
REQUIRED_SECTIONS = (
    "## 今天学什么",
    "## 核心理解",
    "## 亲手验证",
    "## 自测",
    "## 资料",
    "## 一句话复盘",
)


def validate_note(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not DATE_PREFIX.match(path.name):
        errors.append(f"{path}: filename must start with YYYY-MM-DD-")
    if not text.startswith("# "):
        errors.append(f"{path}: note must start with one H1 title")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path}: missing section {section}")
    if len(text.strip()) < 500:
        errors.append(f"{path}: note is too short to be a useful learning record")
    return errors


def main() -> int:
    notes = sorted(DAILY.rglob("*.md"))
    if not notes:
        print("no daily notes found", file=sys.stderr)
        return 1

    errors = [error for note in notes for error in validate_note(note)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"validated {len(notes)} daily note(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

