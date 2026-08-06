---
title: tdc fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# tdc fs create-file-system

Creates a Filesystem with a server-assigned ID. The response contains the owner `fs_token` once. `--wait` waits until data-plane access is ready.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs create-file-system
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## Options

- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.
- `--wait`: Wait until the created file system is active.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Create a Filesystem and wait until it is ready:

    ```bash
    # Wait until the new Filesystem root is readable before returning.
    tdc fs create-file-system --wait
    ```

- Create a Filesystem asynchronously:

    ```bash
    # Return after provisioning is accepted so work can continue in parallel.
    tdc fs create-file-system
    ```

- Preview Filesystem creation:

    ```bash
    # Validate credentials, placement, and the request without provisioning storage.
    tdc fs create-file-system --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/tdc/reference/tdc-filesystem.md)
