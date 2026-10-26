# Architecture

Helo is designed to reuse Microsoft 365 native capabilities rather than duplicating them. Its memory component uses SQLite and three conceptual operations: find applicable lessons, record validated lessons, and record application feedback.

The public reference includes a synthetic learning cycle. It does not contain tenant authentication configuration or production operational data.

The design draws on general lessons from ACL and AoR about verification, bounded execution, and isolation, but contains no ACL/AoR historical memory or lesson records.

Live production learning must remain fail closed until trusted caller identity and independently verified task outcomes are available.
