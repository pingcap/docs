---
title: ti fs delete-file-system
summary: Delete a file system.
---

# ti fs delete-file-system

Starts deleting a file system. Deletion runs asynchronously after the command returns. You must specify `--file-system-id`; display names, labels, and file system tokens cannot identify a file system for deletion. This command requires TiDB Cloud API credentials.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs delete-file-system
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable file system ID. File system tokens cannot replace this option or authorize file system deletion. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Delete a file system:

    ```bash
    # Request asynchronous deletion and remove only the matching local credential after acceptance.
    ti fs delete-file-system --file-system-id <file-system-id>
    ```

- Preview file system deletion:

    ```bash
    # Validate the selected file system without sending the deletion request.
    ti fs delete-file-system --file-system-id <file-system-id> --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
