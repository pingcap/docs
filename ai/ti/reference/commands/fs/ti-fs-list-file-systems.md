---
title: ti fs list-file-systems
summary: List remote TiDB Cloud Filesystems in a region.
---

# ti fs list-file-systems

Lists every Filesystem that the selected TiDB Cloud credentials can access in the effective region. Results include authoritative display metadata, quota and usage, and `has_local_token`, which indicates whether this machine has a matching data-plane token. Quota data includes media and video extraction limits and counters when returned by the service. Tokens are never returned.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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
