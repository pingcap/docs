---
title: tdc fs search-file-content
summary: Search file content in a TiDB Cloud Filesystem.
---

# tdc fs search-file-content

Searches remote file content, optionally in a layer. The command alias is `tdc fs grep`.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs search-file-content
  --pattern <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--path <string>]
  [--version]
```

## Options

- `--pattern <string>`: Content search matching pattern. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--layer-id <string>`: Search within a file system layer.
- `--limit <int32>`: Maximum number of search results; 0 uses the service default.
- `--path <string>`: File path prefix to be searched. \[default: /]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Search file content

```bash
tdc fs search-file-content --file-system-name workspace --path /workspace --pattern "TODO" --limit 50
```

### Search a layer with the grep alias

```bash
tdc fs grep --file-system-name workspace --path /workspace --pattern "deprecated" --layer-id "<layer-id>"
```
