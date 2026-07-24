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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-journal append-journal-entries --journal-id jrn-demo --entry-json '{"type":"task.started"}'
tdc fs-journal append-journal-entries --journal-id jrn-demo --entry-type task.completed --subject issue-42 --idempotency-key issue-42-complete
```
