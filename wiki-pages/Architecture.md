> Source snapshot: public PR #1 at `875323865625413d839cc771bf6641320b56b0a3`. PR status at preparation: OPEN. Commands for PR-added files require that revision; these pages do not imply that the additions are merged into main.

# Architecture and trust boundaries

## Storage

The base SQLite module creates identity, memories and lessons tables. Identity and row checks constrain the agent label to Helo; insert triggers require Helo-prefixed evidence references. These are storage constraints, not caller authentication. The default database path is beside the module; the synthetic test redirects it into a temporary directory before initialization.

## Exact retrieval

The retrieval module accepts six exact fields and opens SQLite in read-only mode with query-only enabled. It joins the lesson index, active lessons and evidence. It filters for Helo records and the expected source/outcome labels, verifies the evidence payload hash, and returns a lesson only when exactly one matching row is valid. No fuzzy or semantic fallback is supplied.

## Lesson recording

The lean workflow validates request shape and receipt fields, refuses its default database for writes, then uses a transaction to record evidence, lesson content and an exact applicability index. It checks the database identity and active duplicate key. Receipt hashes bind the stored payload to the supplied bytes; they do not authenticate the producer.

## Feedback

Application feedback checks operation correspondence and inserts a uniquely keyed operation log. Verified-failure labels increment the failure count. At two failures the lesson becomes suspended and exact retrieval excludes it. A replayed operation is rejected by the unique key. The supplied outcome label is not independently evaluated by this module.

## Host boundary

Microsoft 365 host tools, deployment manifests, authentication, live receipts and operational databases are not packaged here. A production integration needs an independently trusted identity and outcome boundary. The public tests exercise reference logic only.


---
[Source document](https://github.com/jordanmrash/helo/blob/875323865625413d839cc771bf6641320b56b0a3/docs/ARCHITECTURE.md) | [Wiki home](Home)
