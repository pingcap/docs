---
title: tdc fs-git hydrate-git-workspace
summary: Hydrate clean Git objects in a Filesystem Git workspace.
---

# tdc fs-git hydrate-git-workspace

Hydrates clean Git objects for an existing `tdc` Git workspace.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-git hydrate-git-workspace
  --target-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--timeout <duration>]
  [--version]
```

## Options

- `--target-path <string>`: Mounted `tdc fs` workspace path. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--timeout <duration>`: Maximum hydrate duration. \[default: `30m0s`]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Finish hydrating a Git workspace:

    ```bash
    # Download missing clean Git objects for an existing blobless workspace.
    tdc fs-git hydrate-git-workspace --file-system-id <file-system-id> --target-path /path/to/workspace/tidb --timeout 30m
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/tdc/reference/tdc-filesystem-git.md)
