---
title: tdc fs-journal verify-journal
summary: Verify a Filesystem journal hash chain.
---

# tdc fs-journal verify-journal

Verifies the integrity of one journal hash chain.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc fs-journal verify-journal
  --journal-id <string>
  [--file-system-name <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--journal-id <string>`: Journal ID. \[required]
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Verify a journal

```bash
tdc fs-journal verify-journal --file-system-name workspace --journal-id jrn-demo
```

### Render verification results as text

```bash
tdc fs-journal verify-journal --file-system-name workspace --journal-id jrn-demo --output text
```
