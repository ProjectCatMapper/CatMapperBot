#!/usr/bin/env python3
"""Create an unsubmitted, preflighted QuickStatements v1 pilot batch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://www.wikidata.org/w/api.php"
PROPERTY = "P14249"


def get_entities(qids: list[str]) -> dict[str, dict]:
    """Read current claims for no more than 50 Wikidata items at a time."""
    query = urlencode(
        {
            "action": "wbgetentities",
            "ids": "|".join(qids),
            "props": "claims|info",
            "format": "json",
        }
    )
    request = Request(
        f"{API_URL}?{query}",
        headers={"User-Agent": "CatMapperBot-pilot-manifest/1.0 (https://github.com/ProjectCatMapper/CatMapperBot)"},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)["entities"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be positive")

    with args.manifest.open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle))
    if not candidates or set(candidates[0]) != {"qid", "cmid"}:
        raise SystemExit("manifest must contain qid and cmid columns")

    selected: list[dict[str, str]] = []
    checked = 0
    skipped_existing = 0
    skipped_unreadable = 0
    for offset in range(0, len(candidates), 50):
        chunk = candidates[offset : offset + 50]
        entities = get_entities([row["qid"] for row in chunk])
        for row in chunk:
            checked += 1
            entity = entities.get(row["qid"], {})
            if entity.get("missing") or entity.get("redirect") or PROPERTY in entity.get("claims", {}):
                if PROPERTY in entity.get("claims", {}):
                    skipped_existing += 1
                else:
                    skipped_unreadable += 1
                continue
            selected.append(row)
            if len(selected) == args.limit:
                break
        if len(selected) == args.limit:
            break
    if len(selected) != args.limit:
        raise SystemExit(f"only found {len(selected)} eligible rows after checking {checked} candidates")

    manifest_sha256 = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    commands = "\n".join(f'{row["qid"]}\t{PROPERTY}\t"{row["cmid"]}"' for row in selected)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        f"""# SocioMap P14249 QuickStatements pilot ({args.limit} statements)

**Status:** Generated for review only. It has not been submitted to QuickStatements or Wikidata.

| Field | Value |
| --- | --- |
| Target property | `{PROPERTY}` (SocioMap ID) |
| Candidate manifest | `{args.manifest.as_posix()}` |
| Manifest SHA-256 | `{manifest_sha256}` |
| Generated UTC | `{generated_at}` |
| Preflighted candidate rows | {checked} |
| Skipped: existing `{PROPERTY}` | {skipped_existing} |
| Skipped: missing or redirected item | {skipped_unreadable} |
| Selected statements | {len(selected)} |

The selection is deterministic: the first {args.limit} manifest rows whose target items were readable and did not have a `{PROPERTY}` claim at preflight. Re-run this preflight immediately before any submission; an item can change after this file is generated. Do not submit if the pilot lacks explicit Wikidata reviewer approval.

## QuickStatements v1 commands

```text
{commands}
```

## Selected mappings

| Wikidata item | SocioMap ID |
| --- | --- |
"""
        + "".join(f"| {row['qid']} | {row['cmid']} |\n" for row in selected),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
