---
title: ti fs-journal verify-journal
summary: Verify a Filesystem journal hash chain.
---

# ti fs-journal verify-journal

Verifies the integrity of one journal hash chain.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-journal verify-journal
  --journal-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--journal-id <string>`: Journal ID. \[required]
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Verify a journal:

    ```bash
    # Validate the journal's ordered hash chain and integrity metadata.
    ti fs-journal verify-journal --file-system-id <file-system-id> --journal-id jrn-demo
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
