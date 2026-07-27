---
title: tdc fs delete-file
summary: Delete a file from a TiDB Cloud Filesystem.
---

# tdc fs delete-file

Deletes a remote file or directory. The command alias is `tdc fs rm`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs delete-file
  --path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--recursive]
  [--version]
```

## Options

- `--path <string>`: File or directory path in the TiDB Cloud file system. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--recursive`: Delete a directory recursively.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Delete a file

```bash
tdc fs delete-file --file-system-name workspace --path /reports/obsolete.md
```

### Preview recursive directory deletion

```bash
tdc fs delete-file --file-system-name workspace --path /scratch --recursive --dry-run
```
