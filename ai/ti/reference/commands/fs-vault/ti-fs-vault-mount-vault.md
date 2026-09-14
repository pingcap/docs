---
title: ti fs-vault mount-vault
summary: Mount a read-only Filesystem Vault view.
---

# ti fs-vault mount-vault

Mounts readable vault fields as a local read-only FUSE filesystem.

On Linux, install FUSE3 and make `/dev/fuse` available. On macOS, install macFUSE and approve its system extension. Vault mounts are not supported on Windows; use `read-secret`, `list-secrets`, or `run-with-secret` instead.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs-vault mount-vault
  --mount-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--ready-timeout <duration>]
  [--vault-token <string>]
  [--version]
```

## Options

- `--mount-path <string>`: Local mount path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--ready-timeout <duration>`: Time to wait for a background mount to become ready. \[default: `30s`]
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Mount a delegated Vault view:

    ```bash
    # Expose only the paths allowed by the delegated Vault token.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault --vault-token "$TI_VAULT_TOKEN"
    ```

- Allow more time for the Vault mount to become ready:

    ```bash
    # Increase the readiness timeout on a slower host or network.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault --ready-timeout 60s
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
