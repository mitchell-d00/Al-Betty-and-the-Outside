# Disposable Git canary

Run from a clean checkout with Python 3.10+ and Git:

```sh
(cd experiments/git-canary && sha256sum -c SHA256SUMS)
python -B experiments/git_canary.py > /tmp/boa-git-canary.json
```

The [sealed plan](cases.json) fixes the cases, expectations and event order.
Every case creates its own disposable repository. A simulated Mitchell supplies
the scoped grant and a held readiness receipt. A simulated Al recommendation
does not satisfy the grant. The host owns the repository path, ref, intended
commit and write operation. The request supplies only action and expected
revision. The host rechecks it before dispatch. The runner clears inherited
Git environment variables so they cannot redirect the fixture to another repo. In the competition cases a
fixture writer advances the ref after that recheck, before Betty's
`git update-ref` with its expected-old argument. A competition case requires the Git error to
name the actual competing and expected initial commits.

The runner reads the ref, markers, parent and diff separately from the writer.
It retains each writer's stdout, stderr and exit status. The case fails if the
event order, writer count, Git exit or independent readback differs from the
plan. An unavailable or incomplete Git readback is inconclusive and fails the
suite. The in-memory reservation survives either Git outcome until the case
ends. It makes no persistence or multi-process deduplication claim.

This tests a real local Git ref change with a scripted, in-process host. The
grant and receipt are fixture records. The test does not authenticate remote
identities or mediate alternate Git write routes.
