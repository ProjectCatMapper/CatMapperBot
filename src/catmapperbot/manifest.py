"""Validate deterministic QID-to-SocioMap-ID manifest rows."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

QID_PATTERN = re.compile(r"^Q[1-9][0-9]*$")
CMID_PATTERN = re.compile(r"^SM[1-9][0-9]*$")


def validate_rows(rows: list[dict[str, str]]) -> None:
    """Raise ValueError when rows cannot safely produce P14249 additions."""
    seen_qids: set[str] = set()
    if not rows:
        raise ValueError("manifest must contain at least one row")
    for index, row in enumerate(rows, start=2):
        if set(row) != {"qid", "cmid"}:
            raise ValueError(f"row {index}: expected exactly qid and cmid columns")
        qid = row["qid"].strip()
        cmid = row["cmid"].strip()
        if not QID_PATTERN.fullmatch(qid):
            raise ValueError(f"row {index}: invalid QID {qid!r}")
        if not CMID_PATTERN.fullmatch(cmid):
            raise ValueError(f"row {index}: invalid SocioMap category ID {cmid!r}")
        if qid in seen_qids:
            raise ValueError(f"row {index}: duplicate QID {qid}")
        seen_qids.add(qid)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    validate_rows(rows)
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

