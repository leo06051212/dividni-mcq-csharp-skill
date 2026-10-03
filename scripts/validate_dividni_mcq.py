#!/usr/bin/env python3
"""Conservative static checks for a Dividni MCQ C# source file.

This does not compile C#, render images, or determine whether answers are correct.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


QUESTION_RE = re.compile(r"\bnew\s+(?:TruthQuestion|XyzQuestion)\s*\(")
ID_RE = re.compile(r'\bq\.Id\s*=\s*"([^"\r\n]+)"\s*;')
MARKS_RE = re.compile(r"\bq\.Marks\s*=\s*(\d+)\s*;")
IMAGE_RE = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*['\"]([^'\"]+)['\"]", re.I)


def check_source(path: Path, mode: str) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    observations: list[str] = []

    if path.suffix.lower() != ".cs":
        return ["Expected a .cs file."], warnings, observations
    try:
        source = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return [f"Cannot read source: {exc}"], warnings, observations

    question_count = len(QUESTION_RE.findall(source))
    prologue_count = len(re.findall(r"\bnew\s+InstructionalItem\s*\(", source))
    observations.append(f"Question factories: {question_count}; shared instructions: {prologue_count}")

    if question_count == 0:
        errors.append("No TruthQuestion or XyzQuestion constructor found.")
    if mode == "standalone" and question_count != 1:
        errors.append("Standalone mode expects exactly one MCQ; use --mode existing for a shared group or combined file.")

    ids = ID_RE.findall(source)
    if len(ids) != question_count:
        warnings.append(
            f"Found {len(ids)} literal q.Id assignments for {question_count} MCQ constructors; inspect dynamic IDs or missing assignments."
        )
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        errors.append("Duplicate literal q.Id values in file: " + ", ".join(duplicates))

    marks = [int(value) for value in MARKS_RE.findall(source)]
    if len(marks) != question_count:
        warnings.append(
            f"Found {len(marks)} literal q.Marks assignments for {question_count} MCQ constructors; inspect dynamic or missing marks."
        )
    if any(value <= 0 for value in marks):
        errors.append("Literal q.Marks values must be positive whole numbers.")

    images = IMAGE_RE.findall(source)
    observations.append(f"HTML image references: {len(images)}")
    for raw in images:
        src = html.unescape(raw).replace("\\\\", "\\")
        if "{" in src or "}" in src:
            warnings.append(f"Dynamic image source requires manual checking: {raw}")
            continue
        if src.lower().startswith("data:"):
            header, separator, payload = src.partition(",")
            if not separator or ";base64" not in header.lower():
                warnings.append("Non-base64 data URI requires rendered preview.")
                continue
            try:
                decoded = base64.b64decode(payload, validate=True)
            except binascii.Error:
                errors.append("Invalid base64 image data URI.")
                continue
            observations.append(f"Embedded {header[5:].split(';', 1)[0]} image: {len(decoded)} bytes")
            continue
        scheme = urlparse(src).scheme.lower()
        if scheme in {"http", "https"}:
            warnings.append(f"Remote image requires rendered preview: {raw}")
            continue
        image_path = Path(src)
        if not image_path.is_absolute():
            image_path = path.parent / image_path
        if not image_path.is_file():
            errors.append(f"Image file not found beside source or at stated path: {raw}")

    return errors, warnings, observations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Dividni C# source file")
    parser.add_argument(
        "--mode", choices=("standalone", "existing"), default="standalone",
        help="Use existing for a shared-stem group or combined exam file",
    )
    args = parser.parse_args()
    errors, warnings, observations = check_source(args.source, args.mode)
    for item in observations:
        print(f"INFO: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    print("Static check only: compilation, answer semantics, numbering, and rendering require separate verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
