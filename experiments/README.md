# Synthetic development experiments

Both comparisons use [27 frozen cases](fixtures.json) and one [input seal](fixtures.sha256). Betty wrote and sealed the public fixtures, recorded the A-arm replay, then implemented B and scored the same inputs. The same Betty session prepared and scored the cases. These are synthetic development results about specified rules. Fresh-session workflow evaluation is [NOT_RUN](../docs/AB-PILOT.md).

Run with Python 3.10 or newer from the repository root:

```sh
python -B experiments/run.py --output /tmp/teambuilding-results.json
```

Add `--arm A` or `--arm B` to reproduce either stored run. The runner exits with status 2 if the fixture bytes differ from the seal. A mismatch in B makes it exit with status 1 and still produces the per-case receipt.

| Measure | A, simple control | B, checked rules |
| --- | ---: | ---: |
| Report pin decisions correct | 6/13 | 13/13 |
| False-current decisions | 6 | 0 |
| Working-state decisions fully correct | 4/14 | 14/14 |
| False authorizations | 5 | 0 |
| False releases | 3 | 0 |

[Baseline per-case receipt](baseline-results.json) · [Checked per-case receipt](checked-results.json)

## E01 · Which report pin applies?

A reads the first matching label. B considers labels outside fenced examples and flags different live pins as ambiguous. The stable cases cover current, legacy, stale, missing, and conflicting pins, as well as fences with mismatched delimiters, CRLF, and a missing adjacent value. Non-current cases expose false acceptance. Current and repeated-consistent pins guard against rejecting valid reports. B must match every expected classification with zero false-current results. The checker models the report syntax used here and a bounded set of Markdown fences. It works on supplied candidate text and a supplied head.

The comparison adapts the failure reported by [MPLPB PR #101](https://github.com/mitchell-d00/Combined-MPLPB-A-closed-local-ledger-of-pages-that-answers-only-from-those-pages/pull/101). The 13 cases and their outputs belong to this repository.

## E02 · Can the next session recover the decision?

A takes the first available record and treats any direction as permission. B uses the exact-head report first, then the exact-head handoff if needed. A release requires a deployment receipt at the modeled revision. Authority requires the maintainer’s direction for the requested action and revision, with a recoverable current record. Authorization to replay or inspect can coexist with an open release gate. The scorer compares the record selected, gate, evidence ID, blockers, and authority. B must recover all five fields on every case with zero false authorizations and zero false releases.

The named release, hold, failure, and unexecuted states are modeled. Receipt IDs, role labels, and revisions are synthetic fixture fields. The replay performs no repository changes or verification of live identities, permissions, receipts, deployment, or the timing of decisions.
