---
title: tdc fs-vault mount-vault
summary: Mount a read-only Filesystem Vault view.
---

# tdc fs-vault mount-vault

Mounts readable vault fields as a local read-only FUSE filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-vault mount-vault
  --mount-path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--foreground]
  [--fs-token <string>]
  [--help]
  [--ready-timeout <duration>]
  [--vault-token <string>]
  [--version]
```

## Options

- `--mount-path <string>`: Local mount path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--foreground`: Run mount runtime in the foreground until interrupted.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--ready-timeout <duration>`: Time to wait for a background mount to become ready. \[default: `30s`]
- `--vault-token <string>`: Delegated `tdc fs-vault` token; prefer `TDC_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Mount a delegated Vault view:

    ```bash
    # Expose only the paths allowed by the delegated Vault token.
    tdc fs-vault mount-vault --file-system-name workspace --mount-path ./vault --vault-token "$TDC_VAULT_TOKEN"
    ```

- Run the Vault mount in the foreground:

    ```bash
    # Keep the runtime attached for containers or process supervisors.
    tdc fs-vault mount-vault --file-system-name workspace --mount-path ./vault --foreground --ready-timeout 60s
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/tdc/reference/tdc-filesystem-vault.md)
