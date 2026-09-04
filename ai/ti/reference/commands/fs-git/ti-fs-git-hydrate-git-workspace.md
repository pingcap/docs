---
title: ti fs-git hydrate-git-workspace
summary: Hydrate clean Git objects in a Filesystem Git workspace.
---

# ti fs-git hydrate-git-workspace

Hydrates clean Git objects for an existing `ti` Git workspace.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-git hydrate-git-workspace
  --target-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--timeout <duration>]
  [--version]
```

## Options

- `--target-path <string>`: Mounted `ti fs` workspace path. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--timeout <duration>`: Maximum hydrate duration. \[default: `30m0s`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Finish hydrating a Git workspace:

    ```bash
    # Download missing clean Git objects for an existing blobless workspace.
    ti fs-git hydrate-git-workspace --file-system-id <file-system-id> --target-path /path/to/workspace/tidb --timeout 30m
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
