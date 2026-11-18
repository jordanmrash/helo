# Helo

A lean, evidence-gated memory and procedural-lessons reference implementation for a Microsoft 365 declarative agent. This repository publishes sanitized, reusable components and synthetic tests, not the internal runtime, tenant configuration, or operational data.

## What is included
- SQLite schema and Helo-only isolation checks.
- Exact structured lesson retrieval.
- Transactional learning and feedback reference logic.
- Synthetic isolated regression test.

## What is not included
- Live agent manifests, tenant endpoints, private connection settings, user data, operation logs, local paths, production databases, or ACL/AoR memory corpora.
- Production authentication: live autonomous lesson activation remains disabled until independently verified caller attribution and task outcomes exist.

## Local synthetic test
Run `python tests/test_lean_workflow.py` from a working environment where the `memory` folder is on PYTHONPATH. The test uses temporary files and must never import a production database.

## Design principles
One SQLite store, exact matching, evidence-first promotion, duplicate and replay rejection, bounded recall, feedback-based suspension, and no inherited ACL/AoR memories.

## Status
Reference source only. Published-agent tools and deployment are managed separately. This repository is not a production-ready authenticated MCP server.
