#!/usr/bin/env python3
"""Generate the read-only SocioMap ethnicity P14249 input manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from catmapperbot.manifest import TARGETS, validate_rows

SOURCES = {
    "sociomap": {
        "database": "SocioMap",
        "dataset_cmid": "SD2196",
        "category_scope": "ETHNICITY",
        "query": """
MATCH (:DATASET {CMID: $dataset_cmid})-[r:USES]->(c:CATEGORY:ETHNICITY)
WITH c.CMID AS cmid, r.Key AS source_key
WHERE source_key =~ '^ID == Q[0-9]+$'
RETURN DISTINCT cmid, source_key
ORDER BY cmid, source_key
""".strip(),
    },
    "archamap": {
        "database": "ArchaMap",
        "dataset_cmid": "AD42544",
        "category_scope": "CATEGORY with AM CMIDs",
        "query": """
MATCH (:DATASET {CMID: $dataset_cmid})-[r:USES]->(c:CATEGORY)
WITH c.CMID AS cmid, r.Key AS source_key
WHERE cmid =~ '^AM[0-9]+$' AND source_key =~ '^ID == Q[0-9]+$'
RETURN DISTINCT cmid, source_key
ORDER BY cmid, source_key
""".strip(),
    },
}
SOURCE_KEY_PATTERN = re.compile(r"^ID == (Q[1-9][0-9]*)$")


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"{name} must be set")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=sorted(SOURCES), default="sociomap")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--conflicts", type=Path)
    args = parser.parse_args()
    source = SOURCES[args.target]
    target = TARGETS[args.target]

    uri = required_env("CATMAPPER_NEO4J_URI")
    user = required_env("CATMAPPER_NEO4J_USER")
    password = required_env("CATMAPPER_NEO4J_PASSWORD")
    qid_to_cmids: dict[str, set[str]] = {}
    with GraphDatabase.driver(uri, auth=(user, password), encrypted=False) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            records = session.run(source["query"], dataset_cmid=source["dataset_cmid"])
            for record in records:
                match = SOURCE_KEY_PATTERN.fullmatch(record["source_key"] or "")
                if not match:
                    raise ValueError(f"unexpected source key: {record['source_key']!r}")
                qid_to_cmids.setdefault(match.group(1), set()).add(record["cmid"])

    rows = [
        {"qid": qid, "cmid": next(iter(cmids))}
        for qid, cmids in qid_to_cmids.items()
        if len(cmids) == 1
    ]
    conflicts = [
        {"qid": qid, "category_count": str(len(cmids)), "cmids": ";".join(sorted(cmids))}
        for qid, cmids in qid_to_cmids.items()
        if len(cmids) > 1
    ]
    rows.sort(key=lambda row: int(row["qid"][1:]))
    conflicts.sort(key=lambda row: int(row["qid"][1:]))
    validate_rows(rows, args.target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["qid", "cmid"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    conflicts_path = args.conflicts or args.output.with_name(f"{args.output.stem}-conflicts.csv")
    with conflicts_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["qid", "category_count", "cmids"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(conflicts)

    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    metadata = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "target": args.target,
        "database": source["database"],
        "dataset_cmid": source["dataset_cmid"],
        "category_scope": source["category_scope"],
        "wikidata_property": target["property"],
        "claim_datatype": target["datatype"],
        "query": source["query"],
        "source_qid_count": len(qid_to_cmids),
        "row_count": len(rows),
        "conflict_count": len(conflicts),
        "conflicts_file": conflicts_path.name,
        "conflicts_sha256": hashlib.sha256(conflicts_path.read_bytes()).hexdigest(),
        "sha256": digest,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
