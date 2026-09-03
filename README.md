# CatMapperBot

Public, reviewable tooling for two proposed CatMapperBot tasks on Wikidata:

1. add the [SocioMap ID (`P14249`)](https://www.wikidata.org/wiki/Property:P14249) to existing Wikidata ethnicity items where CatMapper has a curated direct mapping; and
2. provisionally add [exact match (`P2888`)](https://www.wikidata.org/wiki/Property:P2888) URLs for reviewed ArchaMap categories until Wikidata approves an ArchaMap-specific identifier property.

This repository is the publication location for the bot-request statement:

> Source code and a reproducible input manifest will be published at https://github.com/ProjectCatMapper/CatMapperBot

## Scope and safeguards

- SocioMap scope is `ETHNICITY` categories from the Wikidata source dataset `SD2196`; it uses the external-ID property `P14249` and only `SM…` category IDs.
- ArchaMap scope is reviewed `AM…` categories from the Wikidata source dataset `AD42544`; it uses the URL-valued `P2888` claim `https://catmapper.org/archamap/AM…` provisionally. `P2888` is never represented as an ArchaMap identifier property.
- A candidate is a direct relationship key of the form `ID == Q...`; names are never used to infer identity.
- `P14249` is never used for ArchaMap `AM…` or `AD…` IDs.
- The generator rejects a QID mapped to more than one CMID.
- The public manifest generator and validation tools perform no Wikidata writes.
- A future, separately reviewed writer may add only a missing configured claim after a fresh revision check. It must skip matching claims and stop for a different value of the configured property. It must never create, merge, delete, or overwrite items or claims.

See [docs/EDITING_POLICY.md](docs/EDITING_POLICY.md) and [docs/MANIFEST.md](docs/MANIFEST.md).

## Reproduce the manifest

The committed manifest is a public snapshot. Regenerate it only with authorized, read-only access to SocioMap:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

export CATMAPPER_NEO4J_URI='bolt://…'
export CATMAPPER_NEO4J_USER='…'
export CATMAPPER_NEO4J_PASSWORD='…'
python scripts/generate_manifest.py \
  --output data/sociomap-ethnicity-p14249-manifest.csv \
  --metadata data/sociomap-ethnicity-p14249-manifest.json
python scripts/validate_manifest.py data/sociomap-ethnicity-p14249-manifest.csv
```

To build the separate, provisional ArchaMap `P2888` manifest, use the same read-only environment with `--target archamap` and separate output paths:

```bash
python scripts/generate_manifest.py --target archamap \
  --output data/archamap-exact-match-p2888-manifest.csv \
  --metadata data/archamap-exact-match-p2888-manifest.json
python scripts/validate_manifest.py --target archamap \
  data/archamap-exact-match-p2888-manifest.csv
```

Credentials are deliberately not stored, logged, or accepted through command-line arguments. The source query is embedded in `scripts/generate_manifest.py` and documented in [docs/MANIFEST.md](docs/MANIFEST.md).

## Verify the committed snapshot

```bash
python scripts/validate_manifest.py data/sociomap-ethnicity-p14249-manifest.csv \
  --metadata data/sociomap-ethnicity-p14249-manifest.json
python -m unittest discover -s tests -v
```

## License

MIT. The manifests contain public QIDs and public CatMapper IDs only.
