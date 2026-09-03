#!/usr/bin/env python3
"""Validate a manifest and, optionally, its recorded SHA-256 metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from catmapperbot.manifest import load_manifest, sha256  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    rows = load_manifest(args.manifest)
    digest = sha256(args.manifest)
    if args.metadata:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        if metadata.get("row_count") != len(rows):
            raise SystemExit("metadata row_count does not match manifest")
        if metadata.get("sha256") != digest:
            raise SystemExit("metadata sha256 does not match manifest")
    print(f"valid: {len(rows)} rows; sha256={digest}")


if __name__ == "__main__":
    main()

