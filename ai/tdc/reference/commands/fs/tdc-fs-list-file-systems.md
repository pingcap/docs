---
title: tdc fs list-file-systems
summary: List locally registered TiDB Cloud Filesystems.
---

# tdc fs list-file-systems

Lists Filesystems registered in the selected local profile.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs list-file-systems
  [--help]
  [--version]
```

## Options

- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### List registered file systems as text

```bash
tdc fs list-file-systems --output text
```

### Return registered file system names

```bash
tdc fs list-file-systems --query 'file_systems[].file_system_name'
```
