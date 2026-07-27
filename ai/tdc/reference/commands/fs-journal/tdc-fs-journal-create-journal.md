---
title: tdc fs-journal create-journal
summary: Create an append-only Filesystem journal.
---

# tdc fs-journal create-journal

Creates a journal. If `--journal-id` is omitted, the service generates one.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-journal create-journal
  [--actor <string>]
  [--dry-run]
  [--file-system-name <string>]
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
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--journal-id <string>`: Journal ID; generated when omitted.
- `--journal-kind <string>`: Journal kind. \[default: agent]
- `--label <string>`: Journal label `key=value`; repeatable.
- `--title <string>`: Journal title.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Create an agent journal

```bash
tdc fs-journal create-journal --file-system-name workspace --journal-id jrn-demo --journal-kind agent --title "demo task"
```

### Preview creation of a labeled deployment journal

```bash
tdc fs-journal create-journal --file-system-name workspace --journal-kind deployment --actor agent:tdc --label env=dev --dry-run
```
