---
title: ti fs-journal append-journal-entries
summary: Append entries to a Filesystem journal.
---

# ti fs-journal append-journal-entries

Appends one JSON event or a JSON array to a journal.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--entry-json <string>`: One JSON journal entry object; repeatable. For the supported fields, see [Entry JSON format](#entry-json-format).
- `--entry-type <string>`: Entry type to use when an input object omits `type`. An explicit `type` in an input object takes precedence.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--help`: Display help information.
- `--idempotency-key <string>`: Key used to deduplicate retries of the same append request. If omitted, each invocation receives a new key.
- `--json-array`: Read a JSON array from stdin instead of JSONL.
- `--source <string>`: Entry source.
- `--subject <string>`: Entry subject; repeatable.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Entry JSON format

Each input object supports the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Event type. Required unless `--entry-type` supplies a default. It must start with a lowercase letter and can contain lowercase letters, digits, underscores (`_`), periods (`.`), or hyphens (`-`). |
| `schema_version` | integer | Schema version for the event payload. Values less than `1` use `1`. |
| `status` | string | Optional user-defined status. The CLI converts it to lowercase. |
| `occurred_at` | RFC3339 timestamp | Time when the event occurred. If omitted, the service supplies the time. |
| `actor` | object | Optional actor with `type` and `id` string fields. |
| `source` | string | Event source. Supported values are `self_reported`, `gateway_observed`, `server_observed`, and `imported`. \[default: `self_reported`] |
| `parent_entry_id` | string | Optional parent event ID. |
| `correlation_id` | string | Optional ID that groups related events. |
| `subjects` | array of strings | Subjects in `type:id` form. Values supplied with `--subject` are added to this array. |
| `summary` | JSON value | Optional inline event payload. |

Artifact references are not currently supported. Do not include `artifacts` or `artifact_refs` in an entry.

If you specify `--source`, it replaces the `source` value in every input object. `--entry-type` applies only to objects that omit `type`.

> **Important:**
>
> To make an append safe to retry, choose an idempotency key for the logical request and reuse that key for every retry. If you omit `--idempotency-key`, a retry receives a new key and can append duplicate entries.

## Examples

- Append one JSON entry:

    ```bash
    # Record an event object and let the CLI or service apply default metadata.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-json '{"type":"task.started"}'
    ```

- Append an idempotent typed entry:

    ```bash
    # Prevent retries from recording the same completion event twice.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-type task.completed --subject issue:42 --idempotency-key issue-42-complete
    ```

- Append a JSON array from standard input:

    ```bash
    # Batch multiple ordered events in a single append operation.
    printf '[{"type":"step.started"},{"type":"step.completed"}]' | ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --json-array
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
