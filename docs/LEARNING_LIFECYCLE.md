# Synthetic learning lifecycle

## Scenario

A fictional Helo lesson is applicable to one exact six-field key. The test generates synthetic operation receipts and an isolated database. These receipts are fixtures, not real authenticated execution evidence.

## Observed sequence in the shipped test

1. A write without explicit isolated database/root parameters is rejected.
2. A lesson with the test receipts is recorded and retrieved by its exact key.
3. Recording the same active applicability key is rejected as a duplicate.
4. A correction receipt labeled for another agent is rejected.
5. Two distinct failure-feedback operations are recorded.
6. The lesson is suspended and no longer returned by active exact lookup.
7. Replaying a feedback operation is rejected.
8. SQLite integrity and the untouched base test-store counts are checked.

Run [the example](../examples/learning-cycle/README.md) to reproduce the sequence. The test output groups several assertions; it is not a per-assertion machine-readable ledger.

## What the sequence means

The reference code can preserve and withdraw a procedural lesson under its declared test conditions. It does not prove that the original correction fixed a real task, that the caller was authenticated, or that a deployed agent used the lesson. The labels `verified_success` and `verified_failure` are inputs to this module, not independently computed verdicts.

## Proposed next evidence

Add negative fixtures for receipt tampering, ambiguous lookup and transaction rollback, then a separately authenticated integration with independently evaluated outcomes. Those are roadmap items, not claims about this demonstration.
