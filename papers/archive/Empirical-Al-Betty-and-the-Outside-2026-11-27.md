# Empirical Al, Betty and the Outside

**Mitchell D. McPhetridge** · **27 November 2026**\
*Preliminary empirical report and reproducible workflow specification*

## Abstract

Al, Betty and the Outside is a human-directed workflow for carrying software development and review across separate AI conversations. Betty implements and tests. Al reviews evidence and proposes the next test. Outside develops objections and alternatives. The human maintainer relays information and decides what work to authorize. Repository records preserve the tested revision, evidence, decisions, failures, and pending actions.

Two deterministic comparisons on 27 synthetic cases measured report-pin selection and working-state recovery. A simple baseline scored 6/13 and 4/14. The checked procedures scored 13/13 and 14/14. A later tester session reproduced the published receipts. A separate 24-slot fresh-session A/B pilot was prepared, but a launcher initialization failure left every participant slot `NOT_RUN`. In the public Test X exercise, two tool-assisted runs completed the Anna-to-Test-Betty sequence. Willow scored 15/16 under v1. Orchid scored 16/16 under the separately sealed v1.1. The runs illustrate how first attempts, scoring disagreements, and protocol changes can be preserved. Comparative accuracy, productivity, and timing remain unmeasured.

**Keywords** — Human–AI collaboration, software review, reproducibility, handoffs, provenance, role separation

## 1. Purpose and governance

The practical question is whether a maintainer can recover what happened and what may proceed after a conversation ends. Code can survive while the reason for accepting it disappears. A passing test can lose its connection to the tested revision, an older deployment can be mistaken for the current release, and a reviewer’s suggestion can be relayed as permission. The workflow records the artifact and the working state together. [1, 2]

| Role | Responsibility | Record or decision |
|---|---|---|
| Mitchell | Relays evidence and authorizes work | Scope and acceptance decisions |
| Betty | Implements, tests, and preserves attempts | Revision-pinned report and evidence |
| Al | Reviews public evidence in read-only mode | Evidence judgment and proposed test |
| Outside | Explores objections and alternatives | Advice the maintainer may relay |

The role names designate tasks. The conversations may use different models or settings. Independence of judgment or evidence requires separate controls.

On an existing repository, Al can inspect the artifact and propose a bounded assignment before Betty changes it. On a new project, Betty can build the initial artifact under direction and leave an Al note for review. The 25 November methods paper used a Betty-first starting procedure. The current companion governance prompt makes both entry paths explicit; it does not retroactively change that original paper. Both paths converge on one cycle. Betty tests and records, Mitchell relays the evidence, Al reviews, and Mitchell decides what to authorize next. Outside can contribute at any time through the maintainer. [1, 2]

### Recovering the working state

The commands `Run Betty`, `Run Al`, and `Run Outside` take a repository URL and an optional pull-request URL. An explicit PR selects the review target. Otherwise the procedure uses the newest PR by creation time, or the default-branch handoff if there is no PR. Compare the report pin with the actual PR head. When the report is inapplicable, look for a handoff at that revision. If neither record applies, the disputed state remains unverified. [1, 2]

A Betty report names the exact head, baseline, change, measured results and denominators, evidence, acceptance rule, failures, and one question for Al. When an archive is the test artifact, record its source commit and ZIP SHA-256. The tested candidate, merge, and deployed artifact need their own evidence. In the relay, the maintainer puts Al’s response and their own direction in distinct sections. The latter supplies the scope of authorized work. [1, 2]

## 2. Worked example from Combined MPLPB

Combined MPLPB illustrates the method on an existing document-reading project. Its FRUS evaluations measured discovery of passages, admission of supported propositions, and completion of the answer separately. In the presentation replay, discovery stayed at 4/4 while complete answers moved from 0/4 to 1/4. Removing the evidence needed for the new completion preserved a supported partial answer. In the later attribution replay, the relevant text was found, but it failed the attribution rule. The complete-answer count stayed at 1/4. The two results show how a handoff can record both a bounded improvement and a case where the procedure correctly withheld a claim. [3]

A separate MPLPB replay examined report pins printed inside fenced Markdown examples. Six synthetic PR bodies were run through both role commands against mocked HTTP. The repair moved expected decisions from 8/12 to 12/12 and reduced false-current decisions from four to zero. Those executions belong to the MPLPB case study. The dedicated repository’s 27 development cases are a separate experiment. [3]

## 3. Deterministic development experiments

The dedicated repository froze 13 report-pin cases and 14 working-state cases. The developer sealed the inputs, recorded baseline results, and scored the checked procedures on the same inputs. The replays require Python and run without a model endpoint. [4]

E01 tested which report applied. The baseline read the first matching pin label. The checked procedure ignored fenced examples, handled absent and stale pins, and treated conflicting live pins as ambiguous. E02 tested whether a subsequent session could recover the working-state decision. The baseline selected the first record and treated a direction as permission. The checked procedure selected evidence tied to the target revision, evaluated the modeled release receipt, and required maintainer direction matching the requested action and revision. E02 scored record selection, gate, evidence identifier, blockers, and authorization. [4]

| Measure | Simple baseline | Checked procedures |
|---|---:|---:|
| Report-pin decisions correct | 6/13 | 13/13 |
| False-current decisions | 6 | 0 |
| Working-state cases fully correct | 4/14 | 14/14 |
| False authorizations | 5 | 0 |
| False releases | 3 | 0 |

The error categories can overlap. These outcomes measure the specified rules against a deliberately simple control on fixtures authored during development. The fixtures model records and authority, so the counts do not authenticate real people, deployments, or permissions. [4]

A later tester session reproduced both single-arm receipts byte for byte. A tampered fixture returned exit status 2 before it could produce a receipt. During Test X implementation, a comparison script initially double-wrapped the stored single-arm arrays. The first failure was retained and the corrected comparison reproduced the published results. Six lifecycle tests covered completion, malformed and empty responses, errors and timeouts, material modification, and refusal to replace an existing submission. Those tests used simulated responses. [5, 6]

## 4. Prepared fresh-session A/B pilot

The separate pilot pairs ordinary summaries with structured handoffs containing equivalent checkable facts. It allocates 12 matched pairs and 24 slots. The design covers revision disputes, preservation and release, evidence custody, and proposal versus authorization. It specifies matched runtime settings, fresh sessions, an eight-minute budget, retained first attempts, and separate measurement of human relay effort. [7]

The isolated launcher failed during initialization. **All 24 slots remain `NOT_RUN` at the evidence cutoff.** The protocol and materials establish the intended comparison. Accuracy, false-acceptance rates, effort, and elapsed time for the two arms remain unobserved. [7]

## 5. Public Test X method

Test X provides a one-request entry path with three fictional record-recovery tasks. The tasks cover a live report pin beside a fenced example, a held handoff with limited authority, and the relationship among tested source, merged source, and deployed artifacts. The participant records initial context and exposure, takes the Anna role, submits a first answer, and leaves a reviewer record. A nonempty completed submission earns a Test Betty identifier. Errors and timeouts retain Anna. The role measures completion. Correctness is a separate outcome. [8, 9]

The Python tool seals the materials, retains the first response before scoring, and records closure time and the response hash. The public scorer compares 16 fixed fields. Free-text explanations and proposed checks are available for review. A text-only path records a self-reported submission boundary. No deadline applies to Test X, and elapsed time describes only the recorded start-to-close interval. [8, 9]

After the first run, v1.1 specified that the scoped-action field must contain both the action and the target revision label. The revised entry and runner were sealed under a new manifest with the same expected values and exact comparison. It also tells the maintainer to use a separate conversation for each repeat and tells Anna to leave earlier runs and scoring materials unopened until closure and disclose any exposure. The public key and packet still rely on participant adherence to staged access. The encrypted run archive protects the retained records when its credential remains with the maintainer. [8, 9]

## 6. Participant observations

Both runs recorded the sequence **unassigned → Anna → first submission → Test Betty → reviewer record**. They are two observations across different packet versions. The scores count fields within a submission, so the 32 field results do not represent 32 participant trials.

| Run | Protocol | Tested revision | Exact matches | Local elapsed time |
|---|---|---|---:|---:|
| Willow | v1 | `3adc687fdf22` | 15/16 | 13.074 s |
| Orchid | v1.1 | `e2886fbadd1d` | 16/16 | 11.311 s |

**Willow.** The final audit received a separate maintainer-supplied copy of the original run and supplement. The first response, prompt and manifest matched their recorded hashes and the pinned v1 source. Reapplying that scorer reproduced **15/16**: the structured action omitted the target revision, while the preserved explanation explicitly limited inspection to M. That contextual interpretation is separate from the unchanged exact score. The local timestamps differ by 13.074382 seconds. The original encrypted record remains unchanged; the separately supplied ZIP is preserved as an additional encrypted audit copy. The audit did not receive the original archive's credential and does not newly attest that ciphertext's contents. [8, 9, 12]

**Orchid.** The maintainer supplied a ZIP containing the first answer, the frozen prompt, a closure record, the score, and the reviewer account. The final audit compared the duplicate answer files byte for byte, verified the response and prompt hashes, and matched the packet and manifest to the pinned v1.1 commit. Reapplying that commit's scorer to the preserved first response reproduced all 16 exact matches. The recorded timestamps differ by 11.310575 seconds, consistent with the elapsed field. This checks internal record consistency, not an external timing source. Orchid reported no known earlier exposure and no access to the key or earlier runs before closure. Exact model, reasoning, and memory settings were unknown; the structured prior-exposure field was also unknown. Exposure and isolation remain self-reported. The original ZIP is retained in encrypted custody for authorized review. [9, 10]

The second submission demonstrates that one participant completed the revised procedure and supplied an exact match in the clarified field. The outcomes cannot isolate the effect of the wording change because the participants, protocol versions, and runtime settings were uncontrolled. The two local intervals omit setup and relay effort and do not estimate productivity.

## 7. What the evidence supports

The deterministic results show that revision selection and working-state checks can be made explicit and replayed on frozen inputs. The MPLPB example shows how a PR can retain a success, a partial result, a withheld decision, and the next question. The two Test X runs show that the public entry can produce a first-attempt record, a score, and a reviewer account across successive runs.

The public answer key, developer-authored fixtures, simple controls, same-session scoring, and two uncontrolled runs limit the conclusions. A hash verifies correspondence between bytes and a digest. It cannot establish the event’s truth, the participant’s identity, or the timing of access to other material. An unassigned role describes the workflow state. Claims about model memory, independence, reasoning settings, general reliability, and comparative effectiveness require further evidence.

The prepared A/B pilot targets recovery from handoffs. A separate end-to-end study would be needed to estimate effects on accepted functionality, defects, rework, human intervention, elapsed time, and resource use. A test of reasoning settings would require holding the other study conditions fixed. Failed launches, incomplete responses, and scoring disagreements are observations to retain in either design.

## 8. Reproducibility and sources

The deterministic replays and lifecycle tests can be run from the repository root at the cited revision.

```sh
python -B experiments/run.py --output /tmp/teambuilding-results.json
python -B -m unittest discover -s test_x -p 'test_*.py' -v
```

To repeat the public participant exercise, open a separate conversation with only the entry request and the pinned v1.1 revision. Record actual exposure and preserve the first attempt. The public source enables rerunning the procedure. Review of original participant material goes through the maintainer’s archive custody process. These papers and participant archives are post-submission research material and should remain unopened during an Anna submission. Their public availability does not establish blinding. [9]

The archive also retains the supplied full-repository ZIP byte for byte. Its SHA-256 is `9ad74f6bc63c8a553e3e87c99371f397f2d2f7c25ac2dd9040764808957348f6`. It is a content-pinned composite of the original PR #4 protocol tree and PR #5 paper additions, not a source export from a single Git commit or the final merged tree. Its snapshot manifest identifies the two source pins and member hashes. [11]

1. McPhetridge, M. D. *Al, Betty, and the Outside: A human-directed review and implementation pipeline* (25 November 2026). [Original seven-page methods paper](Al-Betty-and-the-Outside-2026-11-25.pdf), preserved byte for byte; SHA-256 `f0a5b771351d60a0cf207b68fdc341f58c4b1a14f1faeb6626b9de3cb7489525`. See also the dedicated repository’s [workflow specification](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/docs/WORKFLOW.md).
2. McPhetridge, M. D. [*TeamBuilding Governance Prompt*](../TeamBuilding-Governance-Prompt.md), current companion document revised 27 November 2026. The original appendix remains in reference 1.
3. Combined MPLPB worked example, including the linked presentation, attribution, and report-pin replays. [Case records](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/docs/MPLPB-EXAMPLE.md).
4. Synthetic development fixtures, procedures, and published per-case receipts. [Experiment record](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/experiments/README.md).
5. Subsequent tester’s deterministic reproduction and tamper check. [Replay attempts](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/pilot/replay/attempts.json).
6. Test X implementation and lifecycle verification. [Implementation record and retained checks](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/test_x/IMPLEMENTATION.md).
7. Fresh-session recovery A/B pilot. [Protocol](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/docs/AB-PILOT.md) · [Public slot ledger](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/pilot/status.json).
8. Test X v1, tested at `3adc687fdf2269749bbc0787dac96b34fb1499ca`. [Entry and packet](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/3adc687fdf2269749bbc0787dac96b34fb1499ca/test_x/START.md).
9. Test X v1.1, tested at `e2886fbadd1def33900408404910f81c97018a32`. [Entry and packet](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/e2886fbadd1def33900408404910f81c97018a32/test_x/START.md) · [Material seal](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/e2886fbadd1def33900408404910f81c97018a32/test_x/MANIFEST.json) · [Encrypted archive index](https://github.com/mitchell-d00/Al-Betty-and-the-Outside/blob/e2886fbadd1def33900408404910f81c97018a32/test_x/NOTES.md).
10. Test-Orchid-80b6b8c0c370. Participant ZIP supplied by the maintainer, 27 November 2026. Exact original ZIP SHA-256 `9e49db57e668deecb3a9629d49921eeea6a7d7ce8a9f00fe636319b29c535a3a`. [Audit and custody record](AUDIT-2026-11-27.md). Archive inspected and scorer replayed for this revision; identity and access order not independently established.
11. [Supplied repository snapshot and manifest](snapshots/README.md), 27 November 2026. A pinned content artifact, distinct from subsequent Git merges.
12. Test-Willow-27e9a4197734. Participant ZIP supplied by the maintainer for final audit, 27 November 2026. SHA-256 `f5c5acbcb81f5b98606ad56db80c16b19c7e98249e5c5391ed221fcc1c1e6db9`. First response and original exact score checked against v1; contextual interpretation recorded separately.
