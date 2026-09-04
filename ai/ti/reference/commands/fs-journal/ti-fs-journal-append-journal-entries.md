---
title: ti fs-journal append-journal-entries
summary: Append entries to a Filesystem journal.
---

# ti fs-journal append-journal-entries

Appends one JSON event or a JSON array to a journal.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-journal append-journal-entries
  --journal-id <string>
  [--dry-run]
  [--entry-json <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
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
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--idempotency-key <string>`: Append idempotency key; generated when omitted.
- `--json-array`: Read a JSON array from stdin instead of JSONL.
- `--source <string>`: Entry source.
- `--subject <string>`: Entry subject; repeatable.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Append one JSON entry:

    ```bash
    # Record an event object exactly as supplied on the command line.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-json '{"type":"task.started"}'
    ```

- Append an idempotent typed entry:

    ```bash
    # Prevent retries from recording the same completion event twice.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-type task.completed --subject issue-42 --idempotency-key issue-42-complete
    ```

- Append a JSON array from standard input:

    ```bash
    # Batch multiple ordered events in a single append operation.
    printf '[{"type":"step.started"},{"type":"step.completed"}]' | ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --json-array
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
