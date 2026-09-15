---
title: ti fs mount-file-system
summary: Mount a TiDB Cloud Filesystem.
---

# ti fs mount-file-system

Mounts a Filesystem through automatic, FUSE, or WebDAV mode. The command alias is `ti fs mount`.

The command starts the mount process in the background, waits for the mount to become ready, and then prints the result. If startup fails, the error includes a log path for diagnosis. Use `ti fs unmount-file-system` to end the mount.

> **Important:**
>
> Layer and checkpoint mounts require FUSE. On macOS, where automatic selection normally uses WebDAV, install macFUSE and specify `--driver fuse`. Checkpoint mounts are always read-only.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs mount-file-system
  --mount-path <string>
  [--cache-dir <string>]
  [--checkpoint-id <string>]
  [--driver <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-ref <string>]
  [--local-root <string>]
  [--mount-profile <string>]
  [--no-auto-unpack]
  [--pack-path <string>]
  [--read-cache-max-file-mb <int64>]
  [--read-cache-size-mb <int64>]
  [--read-cache-ttl <duration>]
  [--read-only]
  [--ready-timeout <duration>]
  [--remote-path <string>]
  [--unpack-archive-path <string>]
  [--version]
  [--write-back-cache]
```

## Options

- `--mount-path <string>`: Local mount path. \[required]
- `--cache-dir <string>`: Local FUSE cache directory. If omitted, uses `~/.ti/cache/mounts/<mount-hash>`.
- `--checkpoint-id <string>`: Mount this checkpoint of `--layer-ref` read-only. Requires FUSE.
- `--driver <string>`: Mount driver: `auto`, `fuse`, or `webdav`. \[default: auto]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--layer-ref <string>`: Mount through a writable layer ID, unique name, or [tag reference](/ai/ti/reference/ti-filesystem.md#layer-references). Requires FUSE.
- `--local-root <string>`: Local overlay root. If omitted, uses `~/.ti/local/fs/<mount-hash>`.
- `--mount-profile <string>`: Select a [mount profile](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays): `coding-agent`, `portable`, or `none`. If omitted, uses `none`.
- `--no-auto-unpack`: Skip default auto-unpack for portable mount profile before mounting.
- `--pack-path <string>`: Local overlay path included by automatic or manual pack. Repeatable.
- `--read-cache-max-file-mb <int64>`: Maximum file size admitted to the FUSE read cache in MiB. 0 uses the default. \[default: 4]
- `--read-cache-size-mb <int64>`: FUSE read cache size in MiB. 0 uses the default. \[default: 128]
- `--read-cache-ttl <duration>`: FUSE read cache time to live. \[default: `30s`]
- `--read-only`: Read-only mount mode.
- `--ready-timeout <duration>`: Time to wait for a background mount to become ready. \[default: `30s`]
- `--remote-path <string>`: The TiDB Cloud file system root path to mount. \[default: /]
- `--unpack-archive-path <string>`: Restore the pack archive before mounting.
- `--version`: Display version information.
- `--write-back-cache`: Persist FUSE writes locally before writing them to the file system on flush. This behavior is enabled by default; specify `--write-back-cache=false` to disable it. Unavailable for checkpoint mounts, which are always read-only. \[default: true]

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Mount a Filesystem with the default driver:

    ```bash
    # Let the CLI select the default driver for the current platform.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- Create a read-only FUSE mount:

    ```bash
    # Expose the remote namespace through FUSE without permitting writes.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-only
    ```

- Use WebDAV on macOS without macFUSE:

    ```bash
    # Select WebDAV explicitly when a FUSE runtime is unavailable.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver webdav
    ```

- Tune the FUSE read cache:

    ```bash
    # Increase cache capacity for repeated reads of medium-sized files.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --read-cache-size-mb 256 --read-cache-max-file-mb 16
    ```

- Mount a writable child layer:

    ```bash
    # Expose only the selected copy-on-write timeline at the local path.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/experiment --remote-path /workspace --driver fuse --layer-ref experiment
    ```

- Compare an immutable historical checkpoint:

    ```bash
    # A checkpoint mount is always read-only.
    ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/checkpoint --remote-path /workspace --driver fuse --layer-ref experiment --checkpoint-id v5
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
