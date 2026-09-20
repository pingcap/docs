---
title: ti fs list-file-systems
summary: List remote TiDB Cloud Filesystems in a region.
---

# ti fs list-file-systems

Lists all Filesystems accessible with the selected TiDB Cloud credentials in the selected region. Results include display names, labels, status, quota and usage, and `has_local_token`, which indicates whether this machine has a matching local token. Token values are never included.

When available, quota data includes media and video extraction limits and usage.

The CLI retrieves every service page automatically and returns one complete, sorted result, so this command has no pagination options.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs list-file-systems
  [--display-name <string>]
  [--help]
  [--label <string>]
  [--version]
```

## Options

- `--display-name <string>`: Filter by a case-sensitive display-name substring. This is not an exact resource lookup.
- `--help`: Display help information.
- `--label <string>`: Filter by one exact `key=value` label.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List remotely managed Filesystems:

    ```bash
    # Return the remote inventory for the profile's region without exposing tokens.
    ti fs list-file-systems
    ```

- Filter Filesystems by display metadata:

    ```bash
    # Match a display-name substring and one exact organization-visible label.
    ti fs list-file-systems \
      --display-name workspace \
      --label environment=production
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
