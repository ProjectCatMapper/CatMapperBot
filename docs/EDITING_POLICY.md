# Editing policy

CatMapperBot is proposed to add missing `P14249` (SocioMap ID) claims to existing Wikidata items from the reviewed manifest.

## Permitted action

Add one missing `P14249` claim using the manifest's `cmid`, after confirming the Wikidata item is current and has no different `P14249` value.

## Mandatory skips

- the same value already exists;
- a different `P14249` value exists;
- the item cannot be read or its revision changes during processing;
- the manifest row is malformed or fails validation;
- the QID-to-CMID mapping is ambiguous;
- the run lacks explicit approval, valid authentication, or bot permission for bulk edits.

## Prohibited actions

No item creation, merging, deletion, statement deletion, rank changes, reference changes, label/description/alias changes, or changes to any property other than adding a missing `P14249` claim.

## Audit trail

Record the manifest SHA-256, source snapshot timestamp, QID, CMID, prior revision ID, action, edit summary, response, and post-edit revision. Read back every changed item. A rollback candidate list may be generated, but removal is always a human-reviewed operation.

