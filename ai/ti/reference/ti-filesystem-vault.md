---
title: TiDB Cloud Filesystem Vault CLI Command Reference
summary: Reference every `ti fs-vault` command for secrets, delegated access, audit events, process injection, and mounts.
---

# TiDB Cloud Filesystem Vault CLI Command Reference

Use `ti fs-vault` to manage secrets and delegated access in TiDB Cloud Filesystem.

## Commands

| Command | Description |
|---|---|
| [`create-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-create-secret.md) | Creates a secret. |
| [`replace-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-replace-secret.md) | Replaces a secret. |
| [`read-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-read-secret.md) | Reads a secret. |
| [`list-secrets`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-list-secrets.md) | Lists secrets. |
| [`delete-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-delete-secret.md) | Deletes a secret. |
| [`create-grant`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-create-grant.md) | Delegates limited access to a secret. |
| [`delete-grant`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-delete-grant.md) | Revokes delegated access. |
| [`list-audit-events`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-list-audit-events.md) | Lists Vault audit events. |
| [`run-with-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-run-with-secret.md) | Injects a secret into a process. |
| [`mount-vault`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-mount-vault.md) | Mounts a read-only Vault view. |
| [`unmount-vault`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-unmount-vault.md) | Unmounts a Vault view. |

## See also

- [Manage TiDB Cloud Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md)
- [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/reference/ti-vault-agent-secrets-example.md)
