# Test X v1 implementation and verification

This is a new public self-administered route, requested by Mitchell on
2026-11-27. It requires no access to off-repository pilot keys, allocation or API
launcher. The entry page is self-contained; a read-capable AI can use its inline
packet, while Python 3.10+ adds first-response artifacts and deterministic scoring.

## Reproduce software verification

```sh
python -B experiments/run.py --output /tmp/original-replay.json
python -B -m unittest discover -s test_x -p 'test_*.py' -v
git diff --check
```

Run `sha256sum -c SHA256SUMS --ignore-missing` inside `pilot/` to verify public
pilot materials; this skips held files and does not establish custody of them.
Compare the two original replay arms with `experiments/baseline-results.json`
and `experiments/checked-results.json`; each stored single-arm file is an array.
[Verification receipt](verification.json) records results and Python version.
[Initial comparison-script failure](verification-first-check.json) is retained.

The six Test X tests use explicitly simulated responses in temporary directories.
They establish lifecycle behavior and scoring mechanics, not fresh AI accuracy.
The standard CI runs the original replay and Test X lifecycle tests. No network,
model or external dependency is needed for those commands.

## Review scope

The 16 fixed expected fields cover a fenced stale pin, a current held handoff
with inspection authority and inaccessible key, and a same-tree merge whose
production receipt is stale. Free-text reasoning and proposed next checks are
retained for reviewer judgment. The packet and expected answers are public and
synthetic. Model configuration, prior context and truthfulness of participant
exposure are not attested by the helper. The local receipt is not a signed,
tamper-proof audit log: a writer could replace the entire directory and its
hashes. Submit/exclusive-create checks prevent ordinary accidental overwrites;
immutable Git commits and independent custody, when actually used, supply further
evidence. Hashes bind bytes, not identity, authority or truth.

To revise this protocol, preserve the old commit and manifest, create a new
version, and label future runs accordingly. Do not reclassify old Test X runs as
sealed A/B participant trials. No participant results are claimed at introduction.
