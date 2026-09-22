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
- `--fs-token <string>`: Set the Filesystem owner token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem. For delegated authentication, use `--vault-token` or `TI_VAULT_TOKEN` instead.
- `--help`: Display help information.
- `--ready-timeout <duration>`: Time to wait for a background mount to become ready. \[default: `30s`]
- `--vault-token <string>`: Delegated `ti fs-vault` token; prefer `TI_VAULT_TOKEN`.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

Before running either example, inject a delegated Vault token. In an interactive shell, read and export it without placing it in shell history:

```bash
printf 'Delegated Vault token: ' >&2
read -r -s TI_VAULT_TOKEN
printf '\n' >&2
export TI_VAULT_TOKEN
```

When the mount is no longer needed, unmount it and run `unset TI_VAULT_TOKEN`.

- Mount a delegated Vault view:

    ```bash
    # Expose only the paths allowed by TI_VAULT_TOKEN.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault
    ```

- Allow more time for the Vault mount to become ready:

    ```bash
    # Increase the readiness timeout on a slower host or network.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault --ready-timeout 60s
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
