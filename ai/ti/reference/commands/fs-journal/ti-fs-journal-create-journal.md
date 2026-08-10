---
title: ti fs-journal create-journal
summary: Create an append-only Filesystem journal.
---

# ti fs-journal create-journal

Creates a journal. If `--journal-id` is omitted, the service generates one.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-journal create-journal
  [--actor <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--journal-id <string>]
  [--journal-kind <string>]
  [--label <string>]
  [--title <string>]
  [--version]
```

## Options

- `--actor <string>`: Actor in the form `type:id`.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--journal-id <string>`: Journal ID; generated when omitted.
- `--journal-kind <string>`: Journal kind. \[default: agent]
- `--label <string>`: Journal label `key=value`; repeatable.
- `--title <string>`: Journal title.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create an agent journal:

    ```bash
    # Create an append-only journal for one agent task.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-id jrn-demo --journal-kind agent --title "demo task"
    ```

- Create a labeled deployment journal:

    ```bash
    # Attach actor and environment metadata for later searches.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-kind deployment --actor agent:ti --label env=dev
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
