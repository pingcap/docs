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
```

## Options

- `--from-remote <string>`: Source file path. \[required]
- `--to-remote <string>`: Destination file path. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--overwrite`: Replace an existing destination file.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Move a remote file

```bash
tdc fs move-file --file-system-name workspace --from-remote /draft.md --to-remote /reports/final.md
```

### Preview a move with the alias

```bash
tdc fs mv --file-system-name workspace --from-remote /draft.md --to-remote /reports/final.md --dry-run
```
