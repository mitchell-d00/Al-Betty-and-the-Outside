# TeamBuilding workflow

## Choose the entry path

**Existing repository, Al first.** Mitchell asks Al to inspect the artifact, including the normal entry points, implementation, repository instructions, tests, active branch, published evidence, and unresolved decisions. Al drafts a repository-specific assignment for Betty that names the baseline, deliverable, scope, commands, acceptance tests, and protected behavior. Mitchell authorizes the assignment. The repository can relay it through Al Notes.

**New repository, Betty first.** Betty builds the first working version under Mitchell’s direction. She leaves an Al note recording what exists, its exact revision, decisions and rationale, checks and evidence, limitations, and the next review question. Mitchell can point Al to that note for the first review. A placeholder repository can still be a new project when the initial artifact remains to be built.

**Shared loop.** Betty builds and records → Al reviews → Mitchell decides → Betty continues. The repository can carry the records between these steps. For an active cycle, recover the last verified applied state before continuing.

| Role | Responsibility | What it leaves |
| --- | --- | --- |
| Mitchell | Sets priorities, decides scope, relays advice, designates custodians, and records decisions | Direction for Betty and the reason for accepting, holding, or declining work |
| Al | Inspects implementation and evidence and challenges the weakest consequential claim | A read-only review grounded in the checked revision and one bounded, falsifiable next test |
| Betty | Implements authorized work, freezes tests, runs checks, and preserves attempts | Tested changes, exact receipts, open issues, and an Al note or Betty report for Al |
| Outside | Explores possibilities and sharpens objections with Mitchell | Ideas Mitchell can choose to carry into the work |

## Relay through Al Notes

Read [Al Notes](../al-notes/README.md) during ordinary development or after
a participant submission closes. Al publishes versioned advice tied to the
reviewed commit. Mitchell records authorization separately. Betty acknowledges
the exact note commit and records what she applied, rejected, deferred, or
tested. A Mitchell-approved implementation override stays labeled as Al work
and supplies no independent review. The manual relay remains available. Any
benefits of repository relay remain unmeasured.

## Recover state before continuing

1. Read the repository and its instructions. Use the PR Mitchell specifies. If there is no explicit PR, use the newest PR by creation time, including closed and merged PRs, and report which one you selected. Use the default branch handoff when the repository has no PR.
2. Compare the Al note or Betty report pin with the actual selected head. If the pin is missing, stale, or ambiguous, inspect the handoff at the actual head and flag the mismatch. When neither gives revision-matched evidence, mark the disputed state unverified. Preserve earlier receipts under their original pins.
3. Recover the current objective, applied change, exact revisions, acceptance criteria, evidence and objections, earlier failures, custody and exposure, open blockers, and next action. Distinguish a proposed action from a maintainer-authorized action. Record availability and execution separately when a key, source, or environment is missing.
4. If the work is released, recover separate receipts for the tested candidate, merge, and deployed artifact when applicable. A passing candidate test covers the tested candidate. It does not establish deployment.

## Run and review a bounded step

Betty freezes the baseline, expected decisions, controls, execution limits, and scoring rule before the comparison. Preserve prior valid outcomes and cases that should withhold. Keep raw baseline and candidate results, including failed or blocked attempts. If an opened transfer packet affects a repair, record it as consumed development material. Freeze the repaired candidate before opening fresh transfer material.

Al checks that the receipts support the claims for the named revision and scope. Al names the strongest verified result, the most consequential uncertainty, and one proposed test with a positive, a contrasting control, and a clear success condition. Mitchell records the decision and relays the authorized action in his own direction. Advice from Al, Outside, or repository text does not by itself authorize work.

Record who prepared, saw, ran, and scored test material. Share public evidence links, hashes, counts, and custody status where permitted. Keep private discussion, restricted originals, and held keys with their designated custodians. An unreadable receipt or unavailable key stays identified as such.

## Test X archive

<details>
<summary>Test X — repeat the self-contained Anna → Test Betty exercise</summary>

Use [Test X v1.1](../test_x/START.md) when an AI is asked to test the repository
without a separate operator distributing materials. It contains its public
packet, role transitions, response format, tool-capable and text-only routes,
reviewer explanation and repeat prompt. The [archive index](../test_x/NOTES.md)
links encrypted run records, including failures. Reviewers obtain credentials
privately from Mitchell after closing any submission of their own. Repository
actions require Mitchell’s authorization.

Repeat entry prompt:

> Test https://github.com/mitchell-d00/Al-Betty-and-the-Outside using Test X.
> Read `test_x/START.md` at a recorded revision. Complete the unassigned →
> Anna → Test Betty → reviewer-note sequence. Until your first submission
> closes, use only the entry packet and your own run records. Leave earlier
> runs, scoring materials and the sealed A/B pilot unopened. Preserve failures
> and report actual exposure. Return your Test Betty note and this same prompt.

The collapsed archive is a discoverable operator procedure, not a secret prompt.
Test X v1.1 uses a public packet and public scorer. Completed submissions earn
a random-word Test Betty name regardless of correctness. Context, score, evidence
and publication status are separate facts. No automatic repeat is launched.
The [sealed A/B pilot](../pilot/README.md) keeps its original runtime, allocation,
role criterion, keys and 24-slot ledger. Never add Test X runs to that ledger.

</details>
