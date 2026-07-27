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
```

## Options

- `--append`: Append the contents of a local file to a file in the TiDB Cloud file system.
- `--create-parents`: Create missing local parent directories when copying from a TiDB Cloud file system.
- `--description <string>`: The file description for `--to-remote` operation.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--from-local <string>`: The local source path.
- `--from-remote <string>`: The source path in the TiDB Cloud file system.
- `--from-stdin`: Read from stdin and write to `--to-remote`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--layer-id <string>`: Write the copied file content into a file system layer instead of the base file system.
- `--overwrite`: Replace an existing destination file.
- `--recursive`: Copy directory structure recursively.
- `--resume`: Resume an active copy operation.
- `--tag <string>`: Create tags `key=value` for `--to-remote` operation; repeatable.
- `--to-local <string>`: The local destination path.
- `--to-remote <string>`: The destination path in the TiDB Cloud file system.
- `--to-stdout`: Write `--from-remote` to stdout.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Upload a local file

```bash
tdc fs copy-file --file-system-name workspace --from-local ./report.md --to-remote /reports/report.md
```

### Download a remote file

```bash
tdc fs copy-file --file-system-name workspace --from-remote /reports/report.md --to-local ./report.copy.md --create-parents
```
