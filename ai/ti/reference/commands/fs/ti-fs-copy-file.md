---
title: ti fs copy-file
summary: Copy files to, from, or within a TiDB Cloud Filesystem.
---

# ti fs copy-file

Copies files between local paths, remote paths, stdin, and stdout. The command alias is `ti fs cp`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs copy-file
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
- `--file-system-name <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_NAME`.
- `--from-local <string>`: The local source path.
- `--from-remote <string>`: The source path in the TiDB Cloud file system.
- `--from-stdin`: Read from stdin and write to `--to-remote`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--layer-id <string>`: Write the copied file content into a file system layer instead of the base file system.
- `--overwrite`: Replace an existing destination file.
- `--recursive`: Copy directory structure recursively.
- `--resume`: Resume an active copy operation.
- `--tag <string>`: Create tags `key=value` for `--to-remote` operation; repeatable.
- `--to-local <string>`: The local destination path.
- `--to-remote <string>`: The destination path in the TiDB Cloud file system.
- `--to-stdout`: Write `--from-remote` to stdout.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Upload a local file:

    ```bash
    # Copy a local report into the selected remote Filesystem.
    ti fs copy-file --file-system-name workspace --from-local ./report.md --to-remote /reports/report.md
    ```

- Download a remote file:

    ```bash
    # Create missing local parent directories while downloading the file.
    ti fs copy-file --file-system-name workspace --from-remote /reports/report.md --to-local ./downloads/report.md --create-parents
    ```

- Copy a remote directory:

    ```bash
    # Duplicate a complete directory tree without downloading it locally.
    ti fs copy-file --file-system-name workspace --from-remote /reports --to-remote /archive/reports --recursive
    ```

- Resume a large upload:

    ```bash
    # Continue an interrupted local-to-remote transfer instead of restarting it.
    ti fs copy-file --file-system-name workspace --from-local ./large.bin --to-remote /artifacts/large.bin --resume
    ```

- Append to a remote log:

    ```bash
    # Add local log data to the existing remote object efficiently.
    ti fs copy-file --file-system-name workspace --from-local ./tail.log --to-remote /logs/app.log --append
    ```

- Stream standard input to the Filesystem:

    ```bash
    # Upload generated content without creating an intermediate local file.
    printf 'ready\n' | ti fs copy-file --file-system-name workspace --from-stdin --to-remote /status.txt --tag source=stdin --description "generated status"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
