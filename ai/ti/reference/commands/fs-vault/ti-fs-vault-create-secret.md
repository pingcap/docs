---
title: ti fs-vault create-secret
summary: Create a secret in Filesystem Vault.
---

# ti fs-vault create-secret

Creates a secret from one or more `NAME=value` or `NAME=@file` fields.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-vault create-secret
  --field <string>
  --secret-name <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## Options

- `--field <string>`: Secret field assignment `key=value`, `key=@file`, or `key=-`; repeatable. \[required]
- `--secret-name <string>`: Vault secret name. \[required]
- `--dry-run`: Validate the request without applying changes.
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Create a secret from values and a file:

    ```bash
    # Keep the password out of the command line by reading it from a local file.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL=mysql://example --field PASSWORD=@./password.txt
    ```

- Read a secret field from standard input:

    ```bash
    # Supply a sensitive token through a pipe instead of a process argument.
    printf '%s' "$API_TOKEN" | ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=-
    ```

- Preview secret creation:

    ```bash
    # Validate field assignments without storing secret material.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=@./token.txt --dry-run
    ```

## Related documentation

- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
