# Security

Never commit real tenant configuration, identities, credentials, tokens, user conversations, execution records, or persistent memory databases.

The example code is for synthetic testing. A caller-provided agent name or operation status does not establish authenticated provenance.

Report security concerns privately to the repository owner. Do not post credentials in issues.

## Receipt authentication

Evidence receipts must include `receipt_hmac_sha256`, computed over canonical JSON with that field omitted, UTF-8 encoding, sorted keys, and compact separators. The verifier reads a minimum 256-bit key from `HELO_RECEIPT_HMAC_KEY_HEX`. Keep this key outside the evidence directory and repository, protect it with the runtime identity's operating-system secret store or a managed service such as Azure Key Vault, and rotate it through a controlled deployment. Missing, invalid, or mismatched authentication fails closed.

HMAC proves possession of the shared key, not independent non-repudiation. Deployments requiring separation between signer and verifier should replace HMAC with an Ed25519 signature verified against a pinned public key and retain receipt hashes in append-only audit storage.

## SQLite storage protection

The database opener rejects symbolic links and Windows reparse points for both the database and its parent directory. Read-only consumers use SQLite URI mode=ro plus PRAGMA query_only=ON. On POSIX, new databases are restricted to mode 0600 and existing databases with group or other permissions fail closed.

Windows deployments must additionally restrict the database directory and file to the dedicated Helo service identity and administrators with NTFS ACLs, verify the effective ACL during provisioning, and use BitLocker for volume encryption. Python chmod is not a complete Windows authorization boundary. Use SQLCipher or a managed encrypted database when application-layer encryption is required.
