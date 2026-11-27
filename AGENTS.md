# Working in this repository

When the user explicitly asks to **test using Test X**, follow
[the self-contained entry](test_x/START.md) first. Before closing the participant
submission, do not inspect the public expected answers or previous participant
notes. Record actual prior context and exposure. This public exercise is not a
slot in the sealed A/B pilot. Ordinary development follows the instructions below.

Read [README.md](README.md), [HANDOFF.md](HANDOFF.md), and the relevant evidence before continuing. [The workflow guide](docs/WORKFLOW.md) defines Al, Betty, and Outside. Start with Al for an existing project with an artifact to inspect. Start with Betty for an initial build and leave an Al note. Mitchell directs repository actions and relays between chats.

Before extending the experiments, read [the current experiment record](experiments/README.md). Preserve existing sealed inputs and raw results when a change motivates a new packet. Run `python -B experiments/run.py` before handing off a change to the checked rules or runner. Give the exact tested revision, checks, open state, and question for Al in the next report.
