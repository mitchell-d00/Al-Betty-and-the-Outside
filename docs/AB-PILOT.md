# A/B pilot for fresh-session recovery

**Status: NOT_RUN.** This is a proposed protocol. Mitchell decides whether to run it and appoints a custodian.

## Question

Can a fresh session recover more complete and accurate working state from a structured TeamBuilding handoff than from an ordinary repository-and-PR summary, within the same time budget? This measures recovery from a handoff. End-to-end productivity requires a separate experiment.

| Arm | Starting material |
| --- | --- |
| A | Repository snapshot, selected PR, available receipts, and an ordinary chronological summary |
| B | Equivalent repository snapshot, selected PR, available receipts, and a structured Betty report using the same checkable facts |

Keep the evidence available and the information budget comparable. Give both arms the same task. Return the revision, decision, acceptance reason with receipt, unresolved issue and custody status, authorized next action or explicit withhold, and one proposed next check. Use a fixed eight-minute session budget and the same output form, model and version, tools, system instructions, and token limit. Capture actual settings before opening packets.

## Cases and scoring

- Ask the custodian to prepare 12 matched pairs of fresh scenario variants with equivalent required decisions. Use three pairs each for stale or ambiguous pins, preservation and release, restricted or unavailable evidence, and proposal versus authorization. Within each family include a valid, recoverable contrast. The public replay fixtures are development examples.
- Before running, seal the packets, key, rubric, allocation seed, stop time, and configuration. Use the seed to assign one variant in each pair to each arm and balance run order. Use a fresh session for every variant. Keep the answer key with the custodian and blind the scorer to arm where the records permit. Record any exposure or unblinding.
- Award one exactly specified point for each of five fields. Score the exact revision, release or gate decision, acceptance reason with a corroborating receipt, unresolved issue with custody status, and authorized next action or explicit withhold. A case is fully correct at 5/5. Score the proposed check separately for falsifiability. A timeout stays in the denominator and receives credit only for fields submitted before the limit. Record tool failures separately.
- Report full correctness per arm, both directions of discordant matched pairs, false-current/false-release/false-authorization counts, and elapsed time separately. Give the number of completed and timed-out runs. Report median completion time among fully correct runs only with its denominator. The pilot favors B for a larger follow-up if B has at least two more fully correct cases and no increase in any false acceptance count. General speed or reliability claims require evidence beyond this pilot.

## Follow-up Betty tests

| Test | Question and contrasting control | Decides |
| --- | --- | --- |
| B1 · Resume after a merge | Can a reviewer recover an exact tested candidate, merge, actual deployment, and distinct unresolved work? Include an older successful deployment beside the new pending candidate. | Whether the report makes release claims traceable across revisions. |
| B2 · Preserve custody | Can a reviewer distinguish a key that exists but is inaccessible from a check that executed and failed? Pair both with an accessible passing receipt. | Whether the record preserves execution status and custody as separate facts. |
| B3 · Resolve conflicting authority | Can a reviewer distinguish Mitchell’s scoped direction from an Al suggestion or an Outside objection? Include a valid current authorization and an old authorization for the same action. | Whether the human decision is recoverable without broadening scope. |
| B4 · Choose the entry path | Give a fresh session a mature implementation in one scenario and a placeholder README with a new-project assignment in the other. Require the proper first role and its first deliverable in each case. | Whether the instructions distinguish an inspectable artifact from a repository that still needs its first build. |
| B5 · Test the full cycle | Does reviewer separation change the rate of detected missed controls or acceptance errors? Compare single-session review with separate Al review after the same implementation, with the same human gate and independently scored outcomes. | Whether a larger trial of the full workflow is warranted. Track reviewer time and Mitchell’s relay time. |

B1–B3 can supply fresh recovery scenarios. B4 and B5 need their own frozen packets or designs and remain `NOT_RUN`. Keep raw attempts, scoring disagreements, and all reported limits with the final receipt.
