# Al, Betty, and the Outside

A human-directed review and implementation pipeline by Mitchell D. McPhetridge.

[Papers, current governance prompt and pinned repository snapshot](papers/README.md)
are post-submission research material. An Anna should leave them unopened until
closing the first Test X response.

**Inspect → define responsibilities → implement → test → record → review → decide.**

## Ask an AI to test it

> Test https://github.com/mitchell-d00/Al-Betty-and-the-Outside using Test X.
> Read `test_x/START.md` at a recorded revision. Complete the unassigned →
> Anna → Test Betty → reviewer-note sequence. Until your first submission
> closes, use only the entry packet and your own run records. Leave earlier
> runs, scoring materials and the sealed A/B pilot unopened. Preserve failures
> and report actual exposure. Return your Test Betty note and this same prompt.

[Test X](test_x/START.md) contains the complete public exercise, automatic random
identifier/receipt helper, text-only fallback and repeat instructions. No held
packet, API key or second role prompt is needed. It records context rather than
assuming statelessness, and completion rather than correctness assigns Test Betty.
Its public self-administered results are separate from the sealed A/B study.

Choose the entry path based on what already exists:

- **Existing repository — Al first.** Al inspects the code, instructions, evidence, and working state, then drafts a repository-specific assignment for Betty. Mitchell decides what to authorize and relays the assignment.
- **New repository — Betty first.** Betty builds the initial project under Mitchell’s direction and leaves an **Al note** recording what exists, decisions, checks, limitations, and the next review question.

This repository is the new-project, Betty-first example. Its first build leaves an [Al note](HANDOFF.md). [Combined MPLPB](docs/MPLPB-EXAMPLE.md) is the existing-repository, Al-first example.

Both paths enter the same loop. **Betty builds and records → Mitchell relays → Al reviews → Mitchell decides and relays → Betty continues.** **Outside** is a separate sounding board for exploring ideas and sharpening objections. Mitchell decides what to carry back into the work.

The pull request and handoff preserve the exact revision, available evidence, acceptance criteria, decisions, objections, failures, custody, blockers, and next action. A fresh session should recover why a change was accepted and what it has scope to do next. Connections suggest what to investigate. Evidence and authority cross a boundary only under the rules for that project.

## Run a cycle

1. Read the [workflow guide](docs/WORKFLOW.md) and the target repository’s instructions. Use Al first when there is an artifact to inspect. Use Betty first when the initial artifact still needs to be built. Resume an active cycle from the newest applicable Betty report.
2. Give Betty an exact baseline, authorized scope, and acceptance criteria. Use the [experiment plan](templates/EXPERIMENT.md) to freeze the inputs, controls, and scoring.
3. Have Betty test and file an [Al note or Betty report for Al](templates/BETTY-REPORT.md). Check the pin against the current PR head. Use [HANDOFF.md](HANDOFF.md) for this repository’s starting state.
4. Give the report to Al in a separate chat. Relay Al’s review and your direction for Betty as two named sections. Open Outside separately whenever you want to challenge an assumption or compare proposals.

Use `Run Al <repository URL> [PR URL]`, `Run Betty <repository URL> [PR URL]`, or `Run Outside <repository URL>`. The command selects a role. Mitchell’s explicit direction supplies the scope for repository actions.

## Run the experiments

From the repository root, with Python 3.10 or newer:

```sh
python -B experiments/run.py --output /tmp/teambuilding-results.json
```

The runner checks the input digest, then compares both arms on the same 27 synthetic cases without network access. The checked rules passed all 27. The two experiments cover report-pin selection and recovery of evidence, release state, and authorization. [Cases, receipts, and results](experiments/README.md)

The [MPLPB worked example](docs/MPLPB-EXAMPLE.md) follows the existing-repository, Al-first path and shows how Mitchell used frozen comparisons, withhold controls, retained failures, and exact deployment receipts. The [workflow A/B protocol](docs/AB-PILOT.md) has a [frozen relay package](pilot/README.md). All fresh trials remain **NOT_RUN**. Separate role chats provide role separation. Independent evaluation requires its own controls and custody.
