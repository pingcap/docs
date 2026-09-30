---
title: ti fs search-file-content
summary: Search file content in a file system.
---

# ti fs search-file-content

Searches remote file content, optionally in a layer. The command alias is `ti fs grep`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs search-file-content
  --pattern <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--path <string>]
  [--version]
```

## Options

- `--pattern <string>`: Text query used for full-text and, when configured, semantic search over extracted file content and descriptions. The value is not a regular expression or glob. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--layer-id <string>`: Search within a file system layer.
- `--limit <int32>`: Maximum number of search results; 0 uses the service default.
- `--path <string>`: File path prefix to be searched. \[default: /]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Search base file system content:

    ```bash
    # Find matching text under a remote directory and limit the result count.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "TODO" --limit 50
    ```

- Search content in a layer:

    ```bash
    # Inspect uncommitted layer content separately from the base file system.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "deprecated" --layer-id "<layer-id>"
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
