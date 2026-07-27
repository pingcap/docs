---
title: tdc fs-journal read-journal-entries
summary: Read entries from a Filesystem journal.
---

# tdc fs-journal read-journal-entries

Reads entries from one journal in sequence order.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-journal read-journal-entries
  --journal-id <string>
  [--after-seq <int64>]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--version]
```

## Options

- `--journal-id <string>`: Journal ID. \[required]
- `--after-seq <int64>`: Read entries after this sequence.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--limit <int32>`: Maximum entries to read. \[default: 100]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Read journal entries

```bash
tdc fs-journal read-journal-entries --file-system-name workspace --journal-id jrn-demo
```

### Read a page after a sequence number

```bash
tdc fs-journal read-journal-entries --file-system-name workspace --journal-id jrn-demo --after-seq 100 --limit 50
```
