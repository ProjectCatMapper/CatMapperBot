# Provisional ArchaMap exact-match workflow

Wikidata currently has no approved ArchaMap-specific external-identifier property. Until one is approved, reviewed exact ArchaMap category mappings use [`P2888` (exact match)](https://www.wikidata.org/wiki/Property:P2888), whose datatype is URL.

For a validated ArchaMap category `AM123`, the only claim value produced by this repository is:

```text
https://catmapper.org/archamap/AM123
```

This is deliberately different from the SocioMap workflow:

| System | Property | Value |
| --- | --- | --- |
| SocioMap | `P14249` | `SM123` |
| ArchaMap, provisional | `P2888` | `https://catmapper.org/archamap/AM123` |

## Limits

- Only reviewed direct QID-to-`AM…` mappings are eligible; a shared label is never evidence of an exact match.
- The ArchaMap manifest is separate from the SocioMap manifest and is generated from source dataset `AD42544`.
- QIDs mapped to multiple `AM…` categories are placed in the generated conflict report and excluded from the write manifest pending human review.
- `P2888` claims express a high-confidence exact mapping only. They are not a substitute identifier property and do not authorize any `owl:sameAs` assertion.
- When Wikidata approves a dedicated ArchaMap property, stop adding new `P2888` claims under this policy. Audit existing claims and propose a reviewed migration; do not mass-remove or replace them automatically.
