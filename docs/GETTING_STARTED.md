# Getting started

This repository is a sanitized memory reference implementation, not a complete installable Microsoft 365 agent. Python 3.11 and the standard library are sufficient for the included test.

## Test the reference implementation
From the repository root, run:

```powershell
$env:PYTHONPATH="memory"
python tests/test_lean_workflow.py
```

On macOS/Linux:

```sh
PYTHONPATH=memory python3 tests/test_lean_workflow.py
```

The test uses temporary synthetic evidence. It must not connect to or copy a production SQLite database.

## Integrating with an agent
Provide a separately authorized tool boundary for read-only retrieval, evidence-gated lesson recording, and application feedback. Keep credentials, private manifests, tenant identifiers, local paths, and production memory outside this repository. Do not assume that a declarative agent identity is authenticated merely because it is included in a request.

## What is not supplied
No deployable MCP gateway, Microsoft 365 plugin manifest, cloud authentication configuration, live agent instructions, or real session records are shipped. A Microsoft 365 host can provide native capabilities separately.
