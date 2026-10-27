# Release checks and evidence

Run `python scripts/release_check.py` from the repository root. Add `--json results.json` to retain a machine-readable report. Python 3.11 is the baseline; ACL also requires Node.js for JavaScript checks. The gate uses the standard library and performs no network requests.

## What the gate observes

- Tracked and non-ignored files: forbidden database, key, log and secret artifact names, plus selected user-path, tunnel and credential patterns.
- Markdown: existence of relative link targets, excluding fragment anchors and external URLs.
- Source: Python AST parsing, JSON parsing and JavaScript syntax where present.
- Runtime: the repository-specific synthetic example and regression checks.

A green result is a statement about those checks, not proof that every disclosure pattern is absent. The scanner is deliberately narrow; it does not replace manual review. JSON parsing is not full JSON Schema validation. Link checks do not validate anchors or external websites. Syntax checks do not establish runtime correctness.

## Reproducing and reviewing a change

Use a fresh checkout, run the gate, inspect the diff, and retain the result alongside the commit identifier. Generated results are local evidence, not inputs to the application. A reviewer should inspect both accepted and rejected synthetic cases and verify that documentation does not convert a local test into a live-deployment claim.

## CI

The public-depth workflow runs the same gate on Windows and Ubuntu with Python 3.11 and Node.js 20. Workflow presence is not evidence of a successful CI run. Inspect the pull request checks for the actual result. Live platform tests, identity verification and production activation are outside this workflow.
