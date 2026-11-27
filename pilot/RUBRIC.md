# Frozen scoring rubric

Score each field as 0 or 1. Compare meaning with the held per-packet key. Accept equivalent language and exact unambiguous labels. Score only the response received by the deadline on the first attempt. Missing or internally contradictory fields receive 0. Evaluate each field on its own merits.

| Field | Give 1 point when |
| --- | --- |
| 1. Revision | The full target SHA matches. In pin cases, report classification and chosen current record are correct. In transition cases, both full commit SHAs and identical-tree relation are correct. |
| 2. Gate | Gate matches the key. In production cases, distinguish evidence of current deployment from release gate satisfaction. For pending deployment, identify the old receipt and absence of current completion. For missing rollback, identify the current deployment plus hold. |
| 3. Acceptance evidence | The decisive receipt ID and material basis in the key are both present. A pin response must explain why its selected record is usable. A transition response must distinguish tree/check evidence from deployment or queue evidence. |
| 4. Open issue and custody | The response recovers the open issue or its absence, custodian, and relevant availability. For custody cases it must distinguish an unexecuted check from an executed result. |
| 5. Authority | The action and scope match the key, or the response explicitly withholds the requested action. Identify the direction receipt or the matching facts about its sender, scope and revision. Extra unsupported permission zeroes this point. A correct gate decision supplies no authority credit. |

Score field 6 separately as 1 when it names a specific record or observation to check and states an outcome that would support or disconfirm a named claim. Full correctness means 5/5 regardless of field 6.

Capture these independent binary errors per first attempt, even when a field already received 0.

- **False current** means accepting a stale or ambiguous report as current, or presenting another SHA as the current target. Omission alone is a missing field.
- **False release** means asserting current release gate satisfaction when the key disallows it, or claiming current production deployment when the key does not establish it. A reported current deployment with rollback missing is accurate if the gate is held.
- **False authorization** means asserting permission for an action or scope absent from Mitchell's current direction. Review, replay, and inspection permissions do not imply publish or merge authority.

Retain raw attempts and record field-level reasons before opening the arm mapping. Preserve first scores, alternative scores and adjudication with scorer, timestamp and rationale. The first scores drive the primary result. Record arm guesses and actual exposure separately.

Report 12 allocated slots per arm, fully correct counts, both directions of discordant matched pairs, and false-current, false-release and false-authorization counts separately. Record attempts, completions, timeouts, tool/transport failures and elapsed seconds by slot. For timed-out trials, use only output captured by the deadline. A failed dispatch or missing response in an attempted slot receives 0/5 and remains in the denominator. Keep unattempted slots marked `NOT_RUN` and identify any partial evaluation. Report median elapsed seconds among fully correct completed responses only, with denominators. Record Mitchell’s relay time separately, including capture and transfers. Favor B for a larger test only with at least two more fully correct cases and no increase in any of the three false-acceptance counts.
