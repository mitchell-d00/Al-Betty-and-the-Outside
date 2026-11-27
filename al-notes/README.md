# Al Notes

Use this channel after participant submission or for ordinary development.
Test X Annas and sealed A/B participants follow only their assigned
pre-submission route. Public files remain discoverable through Git, search
and history. Keep keys, raw participant responses and restricted material in
their existing custody. Place public answers or scores in the appropriate
post-submission records and keep them off fresh entry routes.

## Read and relay

1. Start from the reviewed branch or exact PR head. Open the relevant
   numbered note. For a first version, copy [0000.v00.json](0000.v00.json)
   to `0001.v01.json`. Use `0001.v02.json` to supersede it. Keep earlier
   versions intact. Each version is a separate file. Betty can leave the
   first note for Al in a new repository.
2. Check the full `reviewed_commit` against the source being worked on.
   If it has moved, obtain a new note version for the new target before
   applying the advice. Evidence links identify specific revisions or
   receipts. The note records a proposal. It confers no permission and
   establishes no completion.
3. Mitchell gives direction via a trusted channel. Record it separately in
   `al-notes/authorizations/<id>.json`, cite the original direction in
   `source`, and link the record from `authorization_source`. Verify
   Mitchell's direction and its current scope before acting. To add or change
   approval on a published note, publish a new note version. Keep authorization
   and acknowledgment records append-only under new IDs. The mechanical
   checker validates references and scope. It cannot authenticate Mitchell,
   adjudicate evidence, or detect a revocation outside the record.
4. Betty records the full commit that last added or changed that version
   (`git log -1 --format=%H -- al-notes/0001.v01.json`) and files a separate
   `al-notes/acknowledgments/<id>.json`. Record each observed disposition
   as `applied`, `rejected`, `deferred`, or `tested`, with a reason.
   A tested item includes its test receipt. An applied item includes its
   work revision or other evidence. Only claim work or tests actually done.
   Reject or defer advice without treating it as authorization.
5. If Mitchell explicitly directs Al to implement, the note lists those advice
   IDs in `implementation_override`. The authorization grants the same IDs
   to Al. Al logs the action separately as Al work. It cannot count as an
   independent review. Betty acknowledges her own decisions separately.

Use the latest applicable note version for new action. Acknowledgments of an
older version remain readable as historical records. The relay can happen
through these files without copying advice between chats. Its effect on
accuracy, relay time and productivity remains unmeasured.

## Record examples

These are examples with placeholders. The checker scans registered records, not
the examples on this page.

Authorization in `al-notes/authorizations/example.json`:

```json
{
  "approved_by": "Mitchell",
  "source": "<trusted direction reference>",
  "note_path": "al-notes/0001.v01.json",
  "reviewed_commit": "<exact reviewed commit>",
  "grants": {"Betty": ["a1"], "Al": []}
}
```

Acknowledgment in `al-notes/acknowledgments/example.json`:

```json
{
  "author": "<named author>",
  "role": "Betty",
  "note_path": "al-notes/0001.v01.json",
  "note_commit": "<exact Git commit of this note version>",
  "work_base": "<same SHA as reviewed_commit>",
  "independent_review": false,
  "outcomes": [
    {"advice_id": "a1", "status": "applied", "detail": "<what changed>", "evidence": ["<commit or receipt>"]}
  ]
}
```

Run `python -B tools/check_al_notes.py` after committing the records locally.
Use a checkout with full Git history. Before acting, pass the actual current
source commit (for example, the reviewed PR head) with the exact note path:

```sh
python -B tools/check_al_notes.py --note al-notes/0001.v01.json --target "$reviewed_head"
```

This preflight checks the latest version for that note number and its target.
Historical acknowledgments remain valid as records of earlier work.
