# Synthetic learning-cycle example

Run `python examples/learning-cycle/run.py` from the repository root. Python 3.11 and the standard library are sufficient. The runner sets the memory module path and executes the existing regression test, preserving its assertions and exit behavior.

The test creates temporary synthetic stores and receipt files. It exercises recording, exact retrieval, duplicate and foreign-identity rejection, feedback, suspension and replay rejection. No live agent or production store is contacted.

The receipt identity and outcome labels are fictional. Their acceptance demonstrates reference validation logic, not authenticated caller attribution or independently verified task success. The final base-store assertion refers to a temporary redirected test database. See [learning lifecycle](../../docs/LEARNING_LIFECYCLE.md) and [limitations](../../docs/EVIDENCE_AND_LIMITATIONS.md).
