---
title: tdc fs-journal append-journal-entries
summary: Append entries to a Filesystem journal.
---

# tdc fs-journal append-journal-entries

Appends one JSON event or a JSON array to a journal.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-journal append-journal-entries
  --journal-id <string>
  [--dry-run]
  [--entry-json <string>]
  [--entry-type <string>]
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--idempotency-key <string>]
  [--json-array]
  [--source <string>]
  [--subject <string>]
  [--version]
```

## Options

- `--journal-id <string>`: Journal ID. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--entry-json <string>`: One JSON journal entry object; repeatable.
- `--entry-type <string>`: Default entry type for entries missing type.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--idempotency-key <string>`: Append idempotency key; generated when omitted.
- `--json-array`: Read a JSON array from stdin instead of JSONL.
- `--source <string>`: Entry source.
- `--subject <string>`: Entry subject; repeatable.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Append a JSON journal entry

```bash
tdc fs-journal append-journal-entries --file-system-name workspace --journal-id jrn-demo --entry-json '{"type":"task.started"}'
```

### Append a typed idempotent entry

```bash
tdc fs-journal append-journal-entries --file-system-name workspace --journal-id jrn-demo --entry-type task.completed --subject issue-42 --idempotency-key issue-42-complete
```
