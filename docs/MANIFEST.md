# Reproducible input manifest

`data/sociomap-ethnicity-p14249-manifest.csv` is the immutable, reviewable input to the proposed pilot. Each row is one proposed relationship between an existing Wikidata item and a public SocioMap category.

| Column | Meaning |
| --- | --- |
| `qid` | Existing Wikidata item identifier. |
| `cmid` | Public SocioMap category identifier to use as the `P14249` value. |

The accompanying JSON file records the generator version, database/dataset scope, query, row count, SHA-256 checksum, and UTC snapshot time.

## Source query

The generator executes this read-only Cypher query against the SocioMap database:

```cypher
MATCH (:DATASET {CMID: $dataset_cmid})-[r:USES]->(c:CATEGORY:ETHNICITY)
WITH c.CMID AS cmid, coalesce(r.Key, r.key) AS source_key
WHERE source_key =~ '^ID == Q[0-9]+$'
RETURN DISTINCT cmid, source_key
ORDER BY cmid, source_key
```

`dataset_cmid` is fixed to `SD2196` (Wikidata). The script parses each `source_key` into its QID and rejects malformed or duplicate QID-to-CMID mappings. Reproducibility means rerunning this exact version of the source query and generator against the specified CatMapper snapshot; counts may legitimately differ as the live database changes.

## Review before any write

The CSV alone does not authorize edits. Before a pilot or batch, an operator must regenerate the manifest, validate the checksum, inspect changes from the previous snapshot, and obtain explicit approval. Each target item must then be read immediately before a write; an existing different `P14249` claim is a conflict, not a replacement opportunity.

