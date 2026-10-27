> Source snapshot: public PR #1 at `875323865625413d839cc771bf6641320b56b0a3`. PR status at preparation: OPEN. Commands for PR-added files require that revision; these pages do not imply that the additions are merged into main.

# API and data contract reference

## Base store: helo_memory.py

`initialize()` creates a new base database and refuses an existing database. `status()` returns agent, memory count, lesson count and SQLite integrity result. The module-level `DB` path defaults beside the module. The synthetic test redirects it before calling the initializer.

The base initializer creates identity, memories and lessons. It does not create the complete evidence and exact-index schema used by the lean workflow. The test adds those tables; this is not a production migration system.

## Retrieval: exact_retrieval.lookup(criteria, db=None)

The criteria dictionary must contain exactly `agent_id`, `scope`, `problem_signature`, `compatibility_contract`, `applicability` and `exceptions`. Each value must be a nonempty string of at most 256 characters; `agent_id` must be `Helo`.

Lookup returns a dictionary with `lesson_id`, `content` and `evidence_ref`, or `None` for no unique valid match. Invalid query shape raises ValueError. SQLite errors can propagate. The connection is read-only. Active lesson status, evidence labels and payload-hash consistency are required. `schema_sql()` returns the exact-index table and index definitions.

## Recording: lean_workflow.record_lesson(d, db=None, record_root=None)

The request contains the six retrieval fields plus `lesson_text`, `failure_record` and `correction_record`, with the same string bounds. An explicit non-default database and record root are required. The receipt paths must resolve under the root and use JSON. Failure and correction operation identifiers must differ.

The result is a status dictionary. Successful recording includes `lesson_id` and `readback_verified`. Rejections include an error string, such as invalid input, disabled default-database writes, duplicate active lesson, foreign database or unverified identity fields. SQLite and file errors are converted to rejection results by the reference workflow.

## Feedback: lean_workflow.record_application(d, db=None, record_root=None)

Required fields are `agent_id`, `lesson_id`, `operation_id`, `outcome` and `evidence_ref`. Values are bounded strings. Outcome must be `verified_success` or `verified_failure`. The receipt operation identifier must match the request. Successful output includes lesson status and failure count. Repeated operation identifiers are rejected; two failure labels suspend the lesson.

## Receipt validation is not authentication

`validate_8938()` checks tool/status/exit/timeout fields, required operation metadata, and identity labels. It returns operation identifier and receipt hash. It does not verify a digital signature, trusted transport, script bytes against the claimed script hash, or the business outcome. Those limitations are material and remain unresolved.


---
[Source document](https://github.com/jordanmrash/helo/blob/875323865625413d839cc771bf6641320b56b0a3/docs/API_REFERENCE.md) | [Wiki home](Home)
