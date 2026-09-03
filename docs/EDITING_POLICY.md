# Editing policy

CatMapperBot is proposed to add configured missing claims to existing Wikidata items from reviewed manifests: `P14249` (SocioMap ID) for SocioMap and, provisionally, URL-valued `P2888` (exact match) claims for ArchaMap.

## Permitted action

Add one missing configured claim after confirming the Wikidata item is current and has no different value for that property:

- SocioMap: `P14249 = SM…`
- ArchaMap, until a dedicated identifier property exists: `P2888 = https://catmapper.org/archamap/AM…`

## Mandatory skips

- the same value already exists;
- a different value of the configured property exists;
- the item cannot be read or its revision changes during processing;
- the manifest row is malformed or fails validation;
- the QID-to-CMID mapping is ambiguous;
- the run lacks explicit approval, valid authentication, or bot permission for bulk edits.

## Prohibited actions

No item creation, merging, deletion, statement deletion, rank changes, reference changes, label/description/alias changes, or changes to any property other than adding the one configured missing claim. `P14249` must never receive ArchaMap `AM…` or `AD…` identifiers.

## Audit trail

Record the manifest SHA-256, source snapshot timestamp, QID, CMID, prior revision ID, action, edit summary, response, and post-edit revision. Read back every changed item. A rollback candidate list may be generated, but removal is always a human-reviewed operation.
