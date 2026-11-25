---
title: ti fs copy-file
summary: Copy files to, from, or within a file system.
---

# ti fs copy-file

Copies files between local paths, remote paths, stdin, and stdout. The command alias is `ti fs cp`.

Specify exactly one of the following source and destination pairs:

| Source | Destination |
| --- | --- |
| `--from-local` | `--to-remote` |
| `--from-stdin` | `--to-remote` |
| `--from-remote` | `--to-local` |
| `--from-remote` | `--to-stdout` |
| `--from-remote` | `--to-remote` |

`--append` supports only `--from-local` with `--to-remote`. It does not support standard input or remote sources.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs copy-file
  [--append]
  [--create-parents]
  [--description <string>]
  [--dry-run]
  [--file-system-id <string>]
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

- `--append`: Append the contents of a local file to a file in the file system. The existing-destination check does not apply.
- `--create-parents`: Create missing local parent directories when copying from a file system.
- `--description <string>`: The file description for `--to-remote` operation.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--from-local <string>`: The local source path. A URL scheme such as `file:///path` is not accepted.
- `--from-remote <string>`: The source path in the file system.
- `--from-stdin`: Read from stdin and write to `--to-remote`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--layer-id <string>`: Write one copied file into a file system layer instead of the base file system. Cannot be combined with `--recursive`. The existing-destination check does not apply, and `--overwrite` has no effect.
- `--overwrite`: Replace an existing destination. An upload or a download overwrites the destination directly. A copy within the file system (`--from-remote` with `--to-remote`) stages the source at `<destination>.ti-tmp-<id>` and renames it onto the destination; this needs read access to the source and destination and write and delete access in the destination's directory. Delete a staging file left by a failed rename with `ti fs delete-file`.
- `--recursive`: Copy directory structure recursively. Cannot be combined with `--layer-id`; seed a layer directory through a writable FUSE mount instead. An existing destination root is reused, the copy stops if a path below it exists, and `--overwrite` has no effect.
- `--resume`: Resume an active copy operation. The existing-destination check does not apply; on a download, an existing local file is replaced.
- `--tag <string>`: Create tags `key=value` for `--to-remote` operation; repeatable.
- `--to-local <string>`: The local destination path. A URL scheme such as `file:///path` is not accepted.
- `--to-remote <string>`: The destination path in the file system.
- `--to-stdout`: Write `--from-remote` to stdout.
- `--version`: Display version information.

If the destination is an existing directory or ends with a separator, the file is copied to `<destination>/<source-file-name>`. Without `--overwrite`, the command stops when that path exists.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Upload a local file:

    ```bash
    # Copy a local report into the selected remote file system.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./report.md --to-remote /reports/report.md
    ```

- Download a remote file:

    ```bash
    # Create missing local parent directories while downloading the file.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports/report.md --to-local ./downloads/report.md --create-parents
    ```

- Copy a remote directory:

    ```bash
    # Duplicate a complete directory tree without downloading it locally.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports --to-remote /archive/reports --recursive
    ```

- Replace an existing remote file:

    ```bash
    # Replace the published report with the draft.
    ti fs copy-file --file-system-id <file-system-id> --from-remote /reports/draft.md --to-remote /reports/report.md --overwrite
    ```

- Resume a large upload:

    ```bash
    # Continue an interrupted local-to-remote transfer instead of restarting it.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./large.bin --to-remote /artifacts/large.bin --resume
    ```

- Append to a remote log:

    ```bash
    # Add local log data to the existing remote object efficiently.
    ti fs copy-file --file-system-id <file-system-id> --from-local ./tail.log --to-remote /logs/app.log --append
    ```

- Stream standard input to the file system:

    ```bash
    # Upload generated content without creating an intermediate local file.
    printf 'ready\n' | ti fs copy-file --file-system-id <file-system-id> --from-stdin --to-remote /status.txt --tag source=stdin --description "generated status"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
