# Security

Never commit real tenant configuration, identities, credentials, tokens, user conversations, execution records, or persistent memory databases.

The example code is for synthetic testing. A caller-provided agent name or operation status does not establish authenticated provenance.

Report security concerns privately to the repository owner. Do not post credentials in issues.

## Receipt authentication

Evidence receipts must include `receipt_hmac_sha256`, computed over canonical JSON with that field omitted, UTF-8 encoding, sorted keys, and compact separators. The verifier reads a minimum 256-bit key from `HELO_RECEIPT_HMAC_KEY_HEX`. Keep this key outside the evidence directory and repository, protect it with the runtime identity's operating-system secret store or a managed service such as Azure Key Vault, and rotate it through a controlled deployment. Missing, invalid, or mismatched authentication fails closed.

HMAC proves possession of the shared key, not independent non-repudiation. Deployments requiring separation between signer and verifier should replace HMAC with an Ed25519 signature verified against a pinned public key and retain receipt hashes in append-only audit storage.