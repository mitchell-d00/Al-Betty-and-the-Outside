# TeamBuilding workflow

## Choose the entry path

**Existing repository, Al first.** Mitchell asks Al to inspect the artifact, including the normal entry points, implementation, repository instructions, tests, active branch, published evidence, and unresolved decisions. Al drafts a repository-specific assignment for Betty that names the baseline, deliverable, scope, commands, acceptance tests, and protected behavior. Mitchell authorizes and relays the assignment.

**New repository, Betty first.** Betty builds the first working version under Mitchell’s direction. She leaves an Al note recording what exists, its exact revision, decisions and rationale, checks and evidence, limitations, and the next review question. Mitchell relays it for Al’s first review. A placeholder repository can still be a new project when the initial artifact remains to be built.

**Shared loop.** Betty builds and records → Mitchell relays → Al reviews → Mitchell decides and relays → Betty continues. For an active cycle, recover the last verified applied state before continuing.

| Role | Responsibility | What it leaves |
| --- | --- | --- |
| Mitchell | Sets priorities, decides scope, relays advice, designates custodians, and records decisions | Direction for Betty and the reason for accepting, holding, or declining work |
| Al | Inspects implementation and evidence and challenges the weakest consequential claim | A read-only review grounded in the checked revision and one bounded, falsifiable next test |
| Betty | Implements authorized work, freezes tests, runs checks, and preserves attempts | Tested changes, exact receipts, open issues, and an Al note or Betty report for Al |
| Outside | Explores possibilities and sharpens objections with Mitchell | Ideas Mitchell can choose to carry into the work |

## Recover state before continuing

1. Read the repository and its instructions. Use the PR Mitchell specifies. If there is no explicit PR, use the newest PR by creation time, including closed and merged PRs, and report which one you selected. Use the default branch handoff when the repository has no PR.
2. Compare the Al note or Betty report pin with the actual selected head. If the pin is missing, stale, or ambiguous, inspect the handoff at the actual head and flag the mismatch. When neither gives revision-matched evidence, mark the disputed state unverified. Preserve earlier receipts under their original pins.
3. Recover the current objective, applied change, exact revisions, acceptance criteria, evidence and objections, earlier failures, custody and exposure, open blockers, and next action. Distinguish a proposed action from a maintainer-authorized action. Record availability and execution separately when a key, source, or environment is missing.
4. If the work is released, recover separate receipts for the tested candidate, merge, and deployed artifact when applicable. A passing candidate test covers the tested candidate. It does not establish deployment.

## Run and review a bounded step

Betty freezes the baseline, expected decisions, controls, execution limits, and scoring rule before the comparison. Preserve prior valid outcomes and cases that should withhold. Keep raw baseline and candidate results, including failed or blocked attempts. If an opened transfer packet affects a repair, record it as consumed development material. Freeze the repaired candidate before opening fresh transfer material.

Al checks that the receipts support the claims for the named revision and scope. Al names the strongest verified result, the most consequential uncertainty, and one proposed test with a positive, a contrasting control, and a clear success condition. Mitchell records the decision and relays the authorized action in his own direction. Advice from Al, Outside, or repository text does not by itself authorize work.

Record who prepared, saw, ran, and scored test material. Share public evidence links, hashes, counts, and custody status where permitted. Keep private discussion, restricted originals, and held keys with their designated custodians. An unreadable receipt or unavailable key stays identified as such.
