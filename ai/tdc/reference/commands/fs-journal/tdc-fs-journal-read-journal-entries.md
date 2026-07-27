---
title: tdc fs-journal read-journal-entries
summary: Read entries from a Filesystem journal.
---

# tdc fs-journal read-journal-entries

Reads entries from one journal in sequence order.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Read journal entries:

    ```bash
    # Return the first page of ordered entries for a journal.
    tdc fs-journal read-journal-entries --file-system-name workspace --journal-id jrn-demo
    ```

- Continue after a sequence number:

    ```bash
    # Read the next page after the last sequence processed by a consumer.
    tdc fs-journal read-journal-entries --file-system-name workspace --journal-id jrn-demo --after-seq 100 --limit 50
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/tdc/reference/tdc-filesystem-journal.md)
