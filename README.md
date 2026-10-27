# Helo

**An isolated memory and procedural-lessons reference implementation that makes learning inspectable, bounded and reversible.** This public repository contains reusable Python/SQLite components and synthetic regression tests. It is not a complete installable Microsoft 365 agent or an authenticated production memory service.

## See the learning boundary first

Python 3.11 and the standard library are sufficient:

```sh
python examples/learning-cycle/run.py
```

The runner executes the shipped regression test with the correct module path. It uses temporary synthetic databases and receipts, checks lesson recording and exact retrieval, rejects duplicate and foreign-identity cases, applies feedback, suspends a lesson after repeated failures, and rejects replay. It does not read a production database or authenticate a live caller.

## Why this exists

A lesson that is easy to remember but impossible to verify can make an agent less reliable. Helo separates an exact applicability key, evidence references, a stored lesson and application feedback. It also keeps its own records separate from ACL and AoR histories.

## Start here

- [Getting started](docs/GETTING_STARTED.md): clean-checkout commands and prerequisites.
- [Architecture](docs/ARCHITECTURE.md): storage, retrieval, recording and feedback boundaries.
- [API and data contracts](docs/API_REFERENCE.md): functions, fields and rejection behavior.
- [Learning lifecycle](docs/LEARNING_LIFECYCLE.md): the synthetic scenario and state changes.
- [Capability map](docs/CAPABILITIES.md): public components versus separately operated tools.
- [Evidence and limitations](docs/EVIDENCE_AND_LIMITATIONS.md): reproducible tests and production blockers.
- [Troubleshooting](docs/TROUBLESHOOTING.md), [roadmap](docs/ROADMAP.md) and [release checks](docs/RELEASE_CHECKS.md).

## Repository map

`memory/helo_memory.py` defines the base store and isolation checks. `memory/exact_retrieval.py` performs structured read-only lookup. `memory/lean_workflow.py` contains lesson and feedback transactions. `tests/test_lean_workflow.py` exercises the synthetic cycle. `examples/learning-cycle/` supplies a one-command runner; `scripts/` supplies the offline gate.

## Validation

```sh
python scripts/release_check.py
```

The gate parses Python, checks local documentation links and selected disclosure patterns, and runs the synthetic cycle. The public-depth CI workflow runs the same gate on Windows and Ubuntu. A workflow file is not a claim that its checks have already passed.

## Important boundary

Receipt fields claiming an authenticated identity are data, not cryptographic authentication. The reference validator checks those fields; it does not establish a trusted caller or independently verify the business outcome. Production lesson activation remains outside this public implementation. See [limitations](docs/EVIDENCE_AND_LIMITATIONS.md).

## Relationship to ACL and AoR

Helo focuses on isolated exact memory and procedural lessons. ACL focuses on construct and adapter evidence. AoR is the broader operating-foundation reference. Helo does not ship their private memory corpora or acquire their operational status by association.

## Contributing

Use synthetic data and preserve unresolved limitations. See [contribution guidance](CONTRIBUTING.md), [security](SECURITY.md) and [change history](CHANGELOG.md).
