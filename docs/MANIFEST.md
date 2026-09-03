# Reproducible input manifest

Each target has its own immutable, reviewable manifest. `data/sociomap-ethnicity-p14249-manifest.csv` supports the SocioMap `P14249` task. `data/archamap-exact-match-p2888-manifest.csv` supports the provisional ArchaMap `P2888` task when it is generated and reviewed separately. Each row is one proposed relationship between an existing Wikidata item and a public CatMapper category.

| Column | Meaning |
| --- | --- |
| `qid` | Existing Wikidata item identifier. |
| `cmid` | Public CatMapper category identifier used to render the target property value. |

The accompanying JSON file records the generator version, database/dataset scope, query, eligible row count, conflict count, SHA-256 checksums, and UTC snapshot time. The generator also writes a CSV conflict report for source QIDs linked to more than one CatMapper category; conflicted QIDs are excluded from the eligible manifest.

## Source query

The generator executes this read-only Cypher query against the SocioMap database:

```cypher
MATCH (:DATASET {CMID: $dataset_cmid})-[r:USES]->(c:CATEGORY:ETHNICITY)
WITH c.CMID AS cmid, coalesce(r.Key, r.key) AS source_key
WHERE source_key =~ '^ID == Q[0-9]+$'
RETURN DISTINCT cmid, source_key
ORDER BY cmid, source_key
```

`dataset_cmid` is fixed to `SD2196` (Wikidata) for SocioMap. The separate ArchaMap target uses `AD42544` and accepts only `AM…` category IDs. The script parses each `source_key` into its QID. A QID that maps to exactly one CMID is eligible; a QID mapped to more than one CMID is written to the conflict report and excluded. Reproducibility means rerunning this exact version of the source query and generator against the specified CatMapper snapshot; counts may legitimately differ as the live database changes.

## Target claim values

| Target | Property | Datatype | Stored claim value |
| --- | --- | --- | --- |
| SocioMap | `P14249` | external ID | `SM…` |
| ArchaMap (provisional) | `P2888` | URL | `https://catmapper.org/archamap/AM…` |

The ArchaMap target does not write `AM…` or `AD…` as a `P14249` value. When a dedicated ArchaMap identifier property is approved, the `P2888` policy and target configuration require a separate review and migration plan.

## Review before any write

The CSV alone does not authorize edits. Before a pilot or batch, an operator must regenerate the manifest, validate the checksum, inspect changes from the previous snapshot, and obtain explicit approval. Each target item must then be read immediately before a write; an existing different value for the configured property is a conflict, not a replacement opportunity.
