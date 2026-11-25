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

- `--append`: Append the contents of a local file to a file in the file system.
- `--create-parents`: Create missing local parent directories when copying from a file system.
- `--description <string>`: The file description for `--to-remote` operation.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--from-local <string>`: The local source path. Pass a plain file system path. A URL scheme such as `file:///path` is rejected.
- `--from-remote <string>`: The source path in the file system.
- `--from-stdin`: Read from stdin and write to `--to-remote`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--layer-id <string>`: Write one copied file into a file system layer instead of the base file system. Cannot be combined with `--recursive`.
- `--overwrite`: Replace an existing destination. An upload or a download overwrites the destination directly. When you copy within the file system to a base file system destination (`--from-remote` with `--to-remote`, without `--layer-id`), the file system does not replace an existing path, so `ti` copies the source to a temporary sibling named `<destination>.ti-tmp-<id>` and then renames it onto the destination. The rename replaces the target in one step, so a reader sees either the previous file or the complete new file. This requires read access to the source and the destination, and read, write, and delete access in the destination's directory. If the rename fails and `ti` cannot remove the temporary file, the error names the path. Delete it with `ti fs delete-file --path <temporary-path>` using the same `--file-system-id` and a token that has delete access. With `--recursive`, `--overwrite` has no effect: the copy is not staged or renamed, an existing destination root is reused, and the command stops before copying any files if a path below that root already exists. With `--layer-id`, the copy is not staged or renamed either; it writes directly to the layer.
- `--recursive`: Copy directory structure recursively. Cannot be combined with `--layer-id`; seed a layer directory through a writable FUSE mount instead.
- `--resume`: Resume an active copy operation.
- `--tag <string>`: Create tags `key=value` for `--to-remote` operation; repeatable.
- `--to-local <string>`: The local destination path. Pass a plain file system path. A URL scheme such as `file:///path` is rejected.
- `--to-remote <string>`: The destination path in the file system.
- `--to-stdout`: Write `--from-remote` to stdout.
- `--version`: Display version information.

If the destination is an existing directory, or if its path ends with a separator, the file is copied to `<destination>/<source-file-name>`. Unless you pass `--overwrite`, the command stops when the resolved destination already exists. The check is skipped for `--append` (which extends an existing remote file), for `--resume` (which continues an existing transfer, and on a download ignores the flag and replaces the local file, so protect that file before you resume), for `--recursive` (which reuses an existing destination root and stops only if a path below it already exists), and for `--layer-id` (which writes to the layer and replaces any existing file at that path).

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
    # Replace the published report with the draft, without downloading either file.
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
