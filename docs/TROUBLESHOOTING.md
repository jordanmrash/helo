# Troubleshooting

## ModuleNotFoundError

Use `python examples/learning-cycle/run.py`. The runner supplies the memory module path without changing the shell environment. Direct test invocation requires the PYTHONPATH commands in [getting started](GETTING_STARTED.md).

## Missing evidence or lesson_index table

The base initializer alone is not the full lean-workflow schema. The shipped test creates additional tables explicitly. Use the synthetic runner to inspect reference behavior; do not run ad hoc migrations against a production store.

## Existing database initialization refused

The initializer deliberately refuses an existing database. Use a new temporary test location. Do not delete an operational database to force initialization.

## Lookup returns None

Check all six exact fields, active status, matching evidence labels and payload-hash consistency. No match, multiple matches or invalid hash consistency can yield None. Do not loosen exact matching merely to obtain a result.

## Lesson write rejected

Inspect the returned error. The default database is blocked for lean writes; receipt paths, request shape, database identity, duplicate keys and identity labels are also checked. A valid-looking label still does not establish real authentication.

## Lesson disappears after feedback

Two failure labels suspend it. Active retrieval excludes suspended lessons. This is the reference lifecycle, not automatic proof that the feedback was independently verified.

## Test says production remains blank

The assertion concerns a redirected temporary base test store. It does not query or certify an actual production database. See [limitations](EVIDENCE_AND_LIMITATIONS.md).
