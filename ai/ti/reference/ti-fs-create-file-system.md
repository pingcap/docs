---
title: ti fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# ti fs create-file-system

Creates a Filesystem and returns its ID and owner token. The CLI stores and selects the token in the current profile. Use `--wait` to wait until the Filesystem is ready for use.

You can optionally set a display name and labels. These values appear in `list-file-systems` and `describe-file-system` output but do not select the Filesystem in later commands.

> **Important:**
>
> The service does not reveal the initial owner token again. If the CLI warns that it could not store the token, save the returned value before closing the terminal. If the local credential is later lost, use TiDB Cloud API credentials with [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) to create a replacement owner token.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs create-file-system
  [--display-name <string>]
  [--dry-run]
  [--help]
  [--label <string>]
  [--version]
  [--wait]
```

## Options

- `--display-name <string>`: Set a display name between 4 and 64 characters shown by Filesystem inventory commands. The value does not select the Filesystem in later commands.
- `--dry-run`: Validate the request without applying changes.
- `--help`: Display help information.
- `--label <string>`: Add an organization-visible `key=value` label. Repeat this option to add up to 30 labels. Do not put secrets or personal data in labels.
- `--version`: Display version information.
- `--wait`: Wait until the created file system is active.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a Filesystem and wait until it is ready:

    ```bash
    # Wait until the new Filesystem root is readable before returning.
    ti fs create-file-system \
      --display-name agent-workspace \
      --label environment=development \
      --label team=ai \
      --wait
    ```

- Create a Filesystem asynchronously:

    ```bash
    # Return after provisioning is accepted so work can continue in parallel.
    ti fs create-file-system
    ```

- Preview Filesystem creation:

    ```bash
    # Validate credentials, placement, and the request without provisioning storage.
    ti fs create-file-system --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
