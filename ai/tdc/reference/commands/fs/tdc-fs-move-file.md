---
title: tdc fs move-file
summary: Move a file in a TiDB Cloud Filesystem.
---

# tdc fs move-file

Moves or renames a remote path. The command alias is `tdc fs mv`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs move-file
    --from-remote <string>
    --to-remote <string>
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--overwrite]
    [--version]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs move-file --from-remote /draft.md --to-remote /reports/final.md
tdc fs mv --from-remote /draft.md --to-remote /reports/final.md --dry-run
```
