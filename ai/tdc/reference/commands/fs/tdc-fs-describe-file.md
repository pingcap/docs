---
title: tdc fs describe-file
summary: Describe a file in a TiDB Cloud Filesystem.
---

# tdc fs describe-file

Describes metadata for one remote path. The command alias is `tdc fs stat`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-file
  --path <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--path <string>`: File or directory path in the TiDB Cloud file system. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Describe a file

```bash
tdc fs describe-file --file-system-name workspace --path /reports/report.md
```

### Use the stat alias with text output

```bash
tdc fs stat --file-system-name workspace --path /reports/report.md --output text
```
