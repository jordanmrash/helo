> Source snapshot: public PR #1 at `875323865625413d839cc771bf6641320b56b0a3`. PR status at preparation: OPEN. Commands for PR-added files require that revision; these pages do not imply that the additions are merged into main.

# Getting started

## Public reference, not agent installation

Use Python 3.11 and a fresh checkout. The included code uses the standard library. No tenant, tunnel, connector or signed-in browser is required for the synthetic run. This checkout does not install a live declarative agent.

## One-command run

```sh
python examples/learning-cycle/run.py
python scripts/release_check.py
```

The runner sets the module search path locally, executes the existing regression script and preserves assertion failures. It uses temporary synthetic databases. No environment-wide PYTHONPATH change is needed.

## Direct regression run

On PowerShell:

```powershell
$env:PYTHONPATH="memory"
python tests/test_lean_workflow.py
```

On macOS/Linux:

```sh
PYTHONPATH=memory python3 tests/test_lean_workflow.py
```

The test prints named aggregate outcomes and exits nonzero if an assertion fails. Its wording about production refers to its isolated test guard, not inspection of an actual production database.

## Before integrating

Read [API contracts](https://github.com/jordanmrash/helo/blob/875323865625413d839cc771bf6641320b56b0a3/docs/API_REFERENCE.md) and [limitations](https://github.com/jordanmrash/helo/blob/875323865625413d839cc771bf6641320b56b0a3/docs/EVIDENCE_AND_LIMITATIONS.md). The base initializer does not create every table required by the lean workflow; the shipped test adds evidence and exact-index tables explicitly. There is no complete production migration or authenticated gateway here. Do not use a live database to fill that gap.


---
[Source document](https://github.com/jordanmrash/helo/blob/875323865625413d839cc771bf6641320b56b0a3/docs/GETTING_STARTED.md) | [Wiki home](Home)
