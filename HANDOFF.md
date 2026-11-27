# Repository handoff

## Current Test X implementation checkpoint

**Betty implementer, in the existing Al/Outside conversation.** Mitchell explicitly
asked this instance to edit the repository for a self-contained test path. This
is not a fresh participant session. Base: `e29ec06f96d6f59fd4941fb1c5f9a1e964c0ae2a`.
Use the new PR report for the exact checked head and publication status.

- **Implemented:** [Test X v1](test_x/START.md), a complete public packet and entry
  prompt for unassigned → Anna → first submission → random-word Test Betty →
  reviewer explanation. Python handles naming, material hashes, first-response
  closure, fixed-field scoring and local notes. Text-only AIs have a labelled
  transcript-only route. The TeamBuilding guide archives the repeat prompt in
  a collapsed Test X section. [Participant note index](test_x/NOTES.md)
- **Boundaries:** unassigned does not prove statelessness. Completion assigns the
  role regardless of correctness; errors/timeouts stay Anna. Public answer-key
  scoring is not independent, and staged access is not technical blinding.
  Existing keys, pilot prompts and all 24 NOT_RUN slots remain unchanged. No
  participant was run while implementing Test X. The helper does not publish
  files or grant repository authority itself.
- **Verification:** six lifecycle tests cover correct and incorrect completion,
  malformed/empty answers, timeout/error preservation, material tampering and
  duplicate-write refusal. The original deterministic receipts reproduce;
  pilot public seals and local documentation links pass. [Final software receipt](test_x/verification.json)
- **Retained initial verification error:** the first receipt comparison wrapped
  the stored single-arm arrays twice and reported a comparison mismatch. The
  comparison script was corrected to flatten those arrays; original replay and
  Test X code were unchanged by that correction. The [first check](test_x/verification-first-check.json)
  remains recorded separately from the successful comparison.
- **Next review:** can a new tool-capable or text-only instance follow the single
  entry and leave an accurately qualified reviewer note without treating its
  role name or public score as independent workflow validation? Test X participant
  outcomes remain unmeasured; this checkpoint supplies the runnable procedure.

## Al note

**Betty — tester, in a fresh session.** I joined after the initial Betty build. I inspected the repository instructions, README, workflow guide, previous handoff, A/B protocol, experiment records and PR discussion. PR #1 was the newest applicable PR, open and draft with no reviews or discussion. At recovery its actual head and Al note agreed at `9f9ee2a7bf8b04e303dd9228ec3e0f7f6bfa173c`, based on `4a340289299b0d179fd2f65dedbc91f32ce6572b`. The artifact was the initial guides, templates, sealed Python replays and pilot proposal. [PR report and exact checkpoint pin](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/pull/1)

Mitchell’s current direction authorized this bounded evaluation, pushing the checkpoint and merging it after required checks. Al reviews and Outside suggestions are advisory. The checkpoint scope covers the initial artifact at the recovered head plus this evaluation, and carries no authority to publish a release or conduct work beyond the checkpoint. The next relay action is for Mitchell to take custody of the held materials and apply the sealed launch protocol when the runtime and isolation can be verified.

- **Executed and scored** — Replayed both Python arms together and separately at the recovered revision. Each single-arm per-case receipt was byte-identical to its published receipt, and the combined run was structurally identical across both arms. A tampered fixture in a temporary copy exited 2 and produced no receipt. Python 3.12.14. [Raw attempts and receipts](pilot/replay/attempts.json)
- **Deterministic results** — A recovered 6/13 pins and 4/14 working states, with 6 false-current, 5 false-authorization and 3 false-release decisions. B recovered 13/13 and 14/14, with zero in all three false-acceptance measures. These scores apply to deterministic software replays on known public fixtures.
- **Changed** — Added 12 matched pairs, exact participant inputs, a preregistered runtime, scoring rubric, attempt ledger and digest commitments. The transition fixtures checked distinct candidate and merge commits with identical trees. They include current signed deployment evidence and a stale-deployment control, with authority scored separately. Frozen runner, rules, old fixtures and published receipts are preserved. [Pilot relay package](pilot/README.md) · [Anna-to-Betty post-trial prompt](docs/ANNA-TO-BETTY.md)
- **Failures and open results** — Shell clone failed at the proxy. GitHub provided the files at the exact PR head. A no-packet Codex launcher probe failed during initialization on a read-only filesystem. The sealed API runtime was unavailable here. All 24 fresh slots are `NOT_RUN`. Fresh correctness, false decisions, elapsed time and Mitchell relay effort are unmeasured. End-to-end effectiveness is unmeasured. [Launcher failure](pilot/replay/launcher-probe.log) · [Slot ledger](pilot/status.json)
- **Custody and exposure** — I saw the original public fixtures and expected answers, then prepared and saw all new scenario variants, keys and allocation. I checked the deterministic receipts and scored no fresh participant. The key and allocation remain off-repository in the preparation workspace, with no custody transfer acknowledged at freeze. Distinct sessions alone do not establish independent evaluation. [Seal](pilot/SHA256SUMS)

**Question for Al** — In the stale production pair, does the frozen rubric give enough information for a blinded scorer to distinguish a correct same-tree verification from a false production release claim while still granting credit for Mitchell’s scoped inspection authority?

## Initial build record

Mitchell selected the Betty-first entry path and chose Combined MPLPB as the worked example. The initial Betty supplied the workflow guide, templates, two synthetic replays and the initial A/B proposal. The public development fixtures were prepared and scored in that build session. The historical handoff remains at the recovered head. [Initial Betty handoff](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/9f9ee2a7bf8b04e303dd9228ec3e0f7f6bfa173c/HANDOFF.md)
