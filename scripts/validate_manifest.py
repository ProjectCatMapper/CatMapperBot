#!/usr/bin/env python3
"""Validate a manifest and, optionally, its recorded SHA-256 metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from catmapperbot.manifest import load_manifest, sha256, target_config  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--target", choices=["sociomap", "archamap"], default="sociomap")
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    rows = load_manifest(args.manifest, args.target)
    digest = sha256(args.manifest)
    if args.metadata:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        config = target_config(args.target)
        if metadata.get("target") != args.target:
            raise SystemExit("metadata target does not match --target")
        if metadata.get("wikidata_property") != config["property"]:
            raise SystemExit("metadata Wikidata property does not match target")
        if metadata.get("claim_datatype") != config["datatype"]:
            raise SystemExit("metadata claim datatype does not match target")
        if metadata.get("row_count") != len(rows):
            raise SystemExit("metadata row_count does not match manifest")
        if metadata.get("sha256") != digest:
            raise SystemExit("metadata sha256 does not match manifest")
        conflicts_path = args.metadata.parent / metadata.get("conflicts_file", "")
        if not conflicts_path.is_file():
            raise SystemExit("metadata conflict report is missing")
        if metadata.get("conflicts_sha256") != sha256(conflicts_path):
            raise SystemExit("metadata conflict report checksum does not match")
    print(f"valid {args.target}: {len(rows)} rows; sha256={digest}")


if __name__ == "__main__":
    main()
