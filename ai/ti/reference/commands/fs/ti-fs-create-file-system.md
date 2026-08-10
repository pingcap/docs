---
title: ti fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# ti fs create-file-system

Creates a Filesystem. `--wait` waits until data-plane access is ready.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs create-file-system
  --file-system-name <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.
- `--wait`: Wait until the created file system is active.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a Filesystem and wait until it is ready:

    ```bash
    # Wait until the new Filesystem root is readable before returning.
    ti fs create-file-system --file-system-name workspace --wait
    ```

- Create a Filesystem asynchronously:

    ```bash
    # Return after provisioning is accepted so work can continue in parallel.
    ti fs create-file-system --file-system-name scratch
    ```

- Preview Filesystem creation:

    ```bash
    # Validate credentials, placement, and the request without provisioning storage.
    ti fs create-file-system --file-system-name workspace --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
