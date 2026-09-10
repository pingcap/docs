---
title: ti fs-vault unmount-vault
summary: Unmount a Filesystem Vault view.
---

# ti fs-vault unmount-vault

Unmounts a local Filesystem Vault filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault unmount-vault
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--timeout <duration>]
  [--version]
```

## Options

- `--mount-path <string>`: Local mount path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--force`: Force-kill the mount process if graceful unmount times out.
- `--help`: Display help information.
- `--ignore-absent`: Return success when no `ti fs-vault` mount state exists for the path.
- `--timeout <duration>`: Time to wait for the mount process to exit. \[default: `30s`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Unmount a Vault view:

    ```bash
    # Detach the local read-only Vault mount.
    ti fs-vault unmount-vault --mount-path ./vault
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
