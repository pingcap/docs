---
title: tdc fs create-hardlink
summary: Create a hard link in a TiDB Cloud Filesystem.
---

# tdc fs create-hardlink

Creates a hard link to an existing remote path. The command alias is `tdc fs hardlink`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs create-hardlink
  --link-path <string>
  --source-path <string>
  [--dry-run]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--link-path <string>`: The file path for the hard link being created in the TiDB Cloud file system. \[required]
- `--source-path <string>`: The existing file path in the TiDB Cloud file system. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create a hard link

```bash
tdc fs create-hardlink --file-system-name workspace --source-path /reports/final.md --link-path /reports/final-copy.md
```

### Preview hard-link creation with the alias

```bash
tdc fs hardlink --file-system-name workspace --source-path /reports/final.md --link-path /reports/backup.md --dry-run
```
