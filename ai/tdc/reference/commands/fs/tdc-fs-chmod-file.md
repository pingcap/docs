---
title: tdc fs chmod-file
summary: Change file permissions in a TiDB Cloud Filesystem.
---

# tdc fs chmod-file

Changes POSIX mode metadata for a remote path. The command alias is `tdc fs chmod`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs chmod-file
  --mode <string>
  --path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--mode <string>`: The permission mode as an octal value such as 0644. \[required]
- `--path <string>`: File or directory path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Change file permissions

```bash
tdc fs chmod-file --file-system-name workspace --path /reports/final.md --mode 0600
```

### Preview a permission change with the alias

```bash
tdc fs chmod --file-system-name workspace --path /reports/final.md --mode 0644 --dry-run
```
