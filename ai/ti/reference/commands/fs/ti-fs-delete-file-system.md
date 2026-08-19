---
title: ti fs delete-file-system
summary: Delete a TiDB Cloud Filesystem.
---

# ti fs delete-file-system

Requests asynchronous Filesystem deletion by immutable ID. Display names, labels, and FS tokens cannot select or authorize a resource for deletion. This command requires TiDB Cloud API credentials and an explicit `--file-system-id`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs delete-file-system
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable Filesystem ID. FS tokens cannot replace this option or authorize Filesystem deletion. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a Filesystem:

    ```bash
    # Request asynchronous deletion and remove only the matching local credential after acceptance.
    ti fs delete-file-system --file-system-id <file-system-id>
    ```

- Preview Filesystem deletion:

    ```bash
    # Validate the selected Filesystem without sending the deletion request.
    ti fs delete-file-system --file-system-id <file-system-id> --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
