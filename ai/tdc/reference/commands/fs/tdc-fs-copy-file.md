---
title: tdc fs copy-file
summary: Copy files to, from, or within a TiDB Cloud Filesystem.
---

# tdc fs copy-file

Copies files between local paths, remote paths, stdin, and stdout. The command alias is `tdc fs cp`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs copy-file
    [--append]
    [--create-parents]
    [--description <string>]
    [--dry-run]
    [--file-system-name <string>]
    [--from-local <string>]
    [--from-remote <string>]
    [--from-stdin]
    [--fs-token <string>]
    [--help]
    [--layer-id <string>]
    [--overwrite]
    [--recursive]
    [--resume]
    [--tag <string>]
    [--to-local <string>]
    [--to-remote <string>]
    [--to-stdout]
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
tdc fs copy-file --from-local ./report.md --to-remote /reports/report.md
tdc fs copy-file --from-remote /reports/report.md --to-local ./report.copy.md --create-parents
```
