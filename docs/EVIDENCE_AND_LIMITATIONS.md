# Evidence and limitations

## Reproducible public evidence
Run the synthetic test in `tests/test_lean_workflow.py`. It exercises the reference logic using isolated data; it is not a test of a live Microsoft 365 agent.

## Previously observed outside this repository
- A published Helodev conversation retrieved active memory observations.
- A separate session wrote candidate memories to an inbox and an independent SQLite readback confirmed four pending records.
- Local regression suites tested duplicate rejection, retrieval, feedback and suspension.

These observations are not independently reproducible from this repository alone. Operational logs and real data are intentionally excluded.

## Production boundary
The available unauthenticated execution bridge did not establish verifiable Helo-specific caller attribution or independently verified correction outcomes. Therefore autonomous production lesson activation remains disabled. Process exit code zero does not prove task success.

## Disclosure policy
Only synthetic test inputs and sanitized code are publishable. Never commit production databases, conversations, operation records, tokens, tunnel endpoints or organization-specific settings.


## Source-review caveats for this public upgrade

The receipt validator checks identity labels but does not cryptographically authenticate them. It accepts operation-completion fields without independently establishing a task outcome. Hashing receipt bytes establishes consistency, not producer trust. The test creates synthetic receipts and redirects the base database into a temporary directory; its production wording is not a live production inspection.

The base initializer does not create every evidence/index table required by the lean workflow. The test adds those tables explicitly. Complete initialization, authenticated integration and independent outcome verification remain unresolved. The new example and release gate preserve these limitations rather than treating a green test as production readiness.
