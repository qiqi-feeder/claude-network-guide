# Security and privacy

[简体中文](../../SECURITY.md) | **English** · [Guide home](../../README.en.md)

Never submit passwords, real UUIDs, Reality private keys, subscription URLs, personal email addresses, or account tokens in issues, pull requests, screenshots, logs, or public files. Full client YAML files contain credentials and must stay private.

The `private`, `outputs`, `backups`, and `reports` directories are ignored by Git. Prefer storing secrets outside the repository. Check the working tree, staging area, and history before publishing; ignore patterns and simple scans cannot replace review.

If credentials were exposed, revoke or rotate them first, then repair repository history. Deleting a file or rewriting history alone does not invalidate a credential. Never repeat a secret in a public report.

Provide a redacted minimal reproduction for security reports. There is no dedicated reporting email. Use GitHub private vulnerability reporting if available, or contact the maintainer to arrange a private channel.
