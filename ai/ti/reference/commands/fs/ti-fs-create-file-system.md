---
title: ti fs create-file-system
summary: Create a TiDB Cloud Filesystem.
---

# ti fs create-file-system

Creates a Filesystem with a server-assigned ID and optional organization-visible display metadata. The response contains the owner `fs_token` once. `--wait` waits until data-plane access is ready.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

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

- `--display-name <string>`: Set a 4–64 character display name for the remote inventory. The value does not select the Filesystem in later commands.
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
