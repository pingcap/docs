---
title: ti fs-journal create-journal
summary: Create an append-only file system journal.
---

# ti fs-journal create-journal

Creates a journal. If `--journal-id` is omitted, the service generates one.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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

- `--actor <string>`: Actor in the form `type:id`. Both parts are user-defined non-empty strings; the CLI converts `type` to lowercase.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected file system.
- `--help`: Display help information.
- `--journal-id <string>`: Journal ID; generated when omitted.
- `--journal-kind <string>`: User-defined journal category. It must contain 1 to 64 characters, start with a lowercase letter, and use only lowercase letters, digits, underscores (`_`), periods (`.`), or hyphens (`-`). \[default: agent]
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
