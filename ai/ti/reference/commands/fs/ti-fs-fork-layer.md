---
title: ti fs fork-layer
summary: Fork a copy-on-write child layer in a TiDB Cloud Filesystem.
---

# ti fs fork-layer

Forks a writable child timeline from a parent layer tip or one parent checkpoint. Forking pins the parent overlay without copying its file tree.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs fork-layer
  --parent-layer-ref <string>
  [--actor-id <string>]
  [--checkpoint-id <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--layer-name <string>]
  [--version]
```

## Options

- `--parent-layer-ref <string>`: Parent layer ID, unique name, or supported tag reference. \[required]
- `--actor-id <string>`: Actor ID identifying the child owner.
- `--checkpoint-id <string>`: Pin the child to this checkpoint of the parent. If omitted, pins the serialized parent tip.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--layer-id <string>`: Stable child layer ID. If omitted, the service generates one.
- `--layer-name <string>`: Human-readable child layer name.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Fork from the parent tip:

    ```bash
    # Start an independent writable timeline at the parent's current serialized tip.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --layer-name experiment-a --actor-id agent-a
    ```

- Fork from a stable checkpoint:

    ```bash
    # Continue from an earlier review boundary without changing the original timeline.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --checkpoint-id seed --layer-name experiment-b --actor-id agent-b
    ```

Layer names remain visible after logical deletion and can become ambiguous. Automation should capture and use the returned layer ID.

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [`ti fs mount-file-system`](/ai/ti/reference/commands/fs/ti-fs-mount-file-system.md)
