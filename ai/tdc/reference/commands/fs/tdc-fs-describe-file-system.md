---
title: tdc fs describe-file-system
summary: Describe a locally registered TiDB Cloud Filesystem.
---

# tdc fs describe-file-system

Describes one locally registered Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs describe-file-system
  --file-system-name <string>
  [--help]
  [--version]
```

## Options

- `--file-system-name <string>`: Set the file system name. \[required]
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Describe a file system

```bash
tdc fs describe-file-system --file-system-name workspace
```

### Render file system details as text

```bash
tdc fs describe-file-system --file-system-name workspace --output text
```
