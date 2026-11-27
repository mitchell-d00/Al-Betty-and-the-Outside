# Test X participant archive

Anna leaves this archive unopened until the first submission is closed.
Mitchell holds the decryption credentials outside Git and shares them privately
with designated reviewers after their own submissions close.

| Run identifier | Protocol | Tested revision | Encrypted record |
| --- | --- | --- | --- |
| Test-Willow-27e9a4197734 | `test-x-v1` | `3adc687fdf2269749bbc0787dac96b34fb1499ca` | [Original encrypted archive](runs/Test-Willow-27e9a4197734/record.zip.asc) · [Separately supplied audit copy](runs/Test-Willow-27e9a4197734/audited-supplied-record.zip.asc) |
| Test-Orchid-80b6b8c0c370 | `test-x-v1.1` | `e2886fbadd1def33900408404910f81c97018a32` | [Encrypted archive](runs/Test-Orchid-80b6b8c0c370/record.zip.asc) |

## After closure

With explicit permission to publish, package the original run directory,
including any failure or partial submission, and encrypt it before staging
anything in Git. Store the ciphertext under `runs/<identifier>/`. Append one
row with the identifier, protocol, tested revision and ciphertext link. Put
only the ciphertext and index metadata in the public branch and PR. Keep the
response, its digest, score, notes, receipts and credentials off the public
repository, including in PR comments. Preserve earlier entries and first
attempts. If encryption or private custody is unavailable, keep the artifacts
local and report publication as pending.

The archives use GnuPG symmetric encryption. Use a fresh, randomly generated
passphrase per archive. Send the passphrase privately to Mitchell, separately
from the repository. A reviewer who has received the passphrase can decrypt
locally with GnuPG and unpack the resulting ZIP outside the checkout:

```sh
gpg --output /tmp/test-x-review.zip --decrypt /path/to/record.zip.asc
```

Each public entry attests only to the presence of an encrypted record; the
contents require a credential and reviewer inspection. The public exercise
packet and scoring materials still rely on staged access.
