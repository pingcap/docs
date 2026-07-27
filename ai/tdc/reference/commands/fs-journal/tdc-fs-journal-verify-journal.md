---
title: tdc fs-journal verify-journal
summary: Verify a Filesystem journal hash chain.
---

# tdc fs-journal verify-journal

Verifies the integrity of one journal hash chain.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Verify a journal:

    ```bash
    # Validate the journal's ordered hash chain and integrity metadata.
    tdc fs-journal verify-journal --file-system-name workspace --journal-id jrn-demo
    ```

## Related documentation

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/tdc/reference/tdc-filesystem-journal.md)
