# CatMapperBot

Public, reviewable tooling for the proposed CatMapperBot task on Wikidata: add the [SocioMap ID (`P14249`)](https://www.wikidata.org/wiki/Property:P14249) to existing Wikidata ethnicity items where CatMapper has a curated direct mapping.

This repository is the publication location for the bot-request statement:

> Source code and a reproducible input manifest will be published at https://github.com/ProjectCatMapper/CatMapperBot

## Scope and safeguards

- The initial scope is SocioMap `ETHNICITY` categories from the Wikidata source dataset `SD2196` only.
- A candidate is a direct relationship key of the form `ID == Q...`; names are never used to infer identity.
- Only `P14249` values matching `SM` or `SD` followed by digits are valid. This initial manifest contains only `SM` category IDs.
- The generator rejects a QID mapped to more than one CMID.
- The public manifest generator and validation tools perform no Wikidata writes.
- A future, separately reviewed writer may add a missing `P14249` claim only after a fresh revision check. It must skip matching claims and stop for a different existing `P14249` value. It must never create, merge, delete, or overwrite items or claims.

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

Credentials are deliberately not stored, logged, or accepted through command-line arguments. The source query is embedded in `scripts/generate_manifest.py` and documented in [docs/MANIFEST.md](docs/MANIFEST.md).

## Verify the committed snapshot

```bash
python scripts/validate_manifest.py data/sociomap-ethnicity-p14249-manifest.csv \
  --metadata data/sociomap-ethnicity-p14249-manifest.json
python -m unittest discover -s tests -v
```

## License

MIT. The manifest contains public QIDs and public CatMapper IDs only.

