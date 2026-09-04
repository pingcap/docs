---
title: ti fs import-file-system-token
summary: Import an existing TiDB Cloud Filesystem token.
---

# ti fs import-file-system-token

Validates an existing FS token against its regional endpoint and stores it in the selected local profile. The file system ID is derived from the token; `--file-system-id` is an optional consistency assertion.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs import-file-system-token
  [--dry-run]
  [--file-system-id <string>]
  [--from-file <string>]
  [--fs-token <string>]
  [--help]
  [--replace]
  [--version]
```

## Options

- `--dry-run`: Validate the token and destination without writing local credentials.
- `--file-system-id <string>`: Assert that the token belongs to this file system ID.
- `--from-file <string>`: Read the token from an owner-only file, or use `-` for standard input.
- `--fs-token <string>`: Supply the token directly. Prefer `TI_FS_TOKEN` or `--from-file` to avoid process argument exposure.
- `--help`: Display help information.
- `--replace`: Replace a different locally stored token for the same file system after validation.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Import a token from a protected file:

    ```bash
    # Validate the token remotely and store it under its embedded file system ID.
    chmod 600 ./fs-token
    ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
    ```

- Import a token from standard input:

    ```bash
    # Avoid placing the token in shell history or a process argument.
    cat ./fs-token | ti fs import-file-system-token --from-file - --region aws-us-east-1
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
