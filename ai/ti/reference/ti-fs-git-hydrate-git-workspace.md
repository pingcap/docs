---
title: ti fs-git hydrate-git-workspace
summary: Hydrate clean Git objects in a Filesystem Git workspace.
---

# ti fs-git hydrate-git-workspace

Hydrates clean Git objects for an existing `ti` Git workspace.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
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
