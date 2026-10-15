---
title: TiDB Cloud Filesystem Vault CLI Command Reference
summary: Reference every `ti fs-vault` command for secrets, delegated access, audit events, process injection, and mounts.
---

# TiDB Cloud Filesystem Vault CLI Command Reference

Use `ti fs-vault` to manage secrets and delegated access in TiDB Cloud Filesystem.

Most secret-management commands identify a secret by its name, such as `db-prod`. `replace-secret` and `run-with-secret` instead require its canonical Vault path, `/n/vault/<secret-name>`. `/n/vault/` is the root of the Vault namespace, so `/n/vault/db-prod` and the secret name `db-prod` identify the same secret.

## Commands

| Command | Description |
|---|---|
| [`create-secret`](/ai/ti/reference/ti-fs-vault-create-secret.md) | Creates a secret. |
| [`replace-secret`](/ai/ti/reference/ti-fs-vault-replace-secret.md) | Replaces a secret. |
| [`read-secret`](/ai/ti/reference/ti-fs-vault-read-secret.md) | Reads a secret. |
| [`list-secrets`](/ai/ti/reference/ti-fs-vault-list-secrets.md) | Lists secrets. |
| [`delete-secret`](/ai/ti/reference/ti-fs-vault-delete-secret.md) | Deletes a secret. |
| [`create-grant`](/ai/ti/reference/ti-fs-vault-create-grant.md) | Delegates limited access to a secret. |
| [`delete-grant`](/ai/ti/reference/ti-fs-vault-delete-grant.md) | Revokes delegated access. |
| [`list-audit-events`](/ai/ti/reference/ti-fs-vault-list-audit-events.md) | Lists Vault audit events. |
| [`run-with-secret`](/ai/ti/reference/ti-fs-vault-run-with-secret.md) | Injects a secret into a process. |
| [`mount-vault`](/ai/ti/reference/ti-fs-vault-mount-vault.md) | Mounts a read-only Vault view. |
| [`unmount-vault`](/ai/ti/reference/ti-fs-vault-unmount-vault.md) | Unmounts a Vault view. |

## See also

- [Manage TiDB Cloud Filesystem Vault Secrets](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)
- [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md)
