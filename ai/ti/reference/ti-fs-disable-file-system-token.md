---
title: ti fs disable-file-system-token
summary: Temporarily disable a TiDB Cloud Filesystem token.
---

# ti fs disable-file-system-token

Temporarily disables a Filesystem token without revoking it. You can re-enable the token later with [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md). A token used by a known local mount must be drained and unmounted first. With owner token authentication, only scoped tokens can be disabled; TiDB Cloud API keys can disable either token kind.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs disable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem that owns the token. Required when using TiDB Cloud API credentials; optional when an owner token supplies the ID.
- `--token-id <string>`: Specify the immutable token ID returned by the list command. This option is required.
- `--fs-token <string>`: Authorize the request with an owner Filesystem token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem. If no Filesystem token is available, the command uses the configured TiDB Cloud API keys.
- `--dry-run`: Validate credentials, identifiers, and known local mount conflicts without disabling the token.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Disable a token after stopping its local mount:

    ```bash
    # Drain and unmount first when this token backs a mount on the current machine.
    ti fs drain-file-system --mount-path /path/to/workspace
    ti fs unmount-file-system --mount-path /path/to/workspace
    ti fs disable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- Disable a scoped token by using an owner token:

    ```bash
    # Inject TI_FS_TOKEN from a secret manager. The owner token identifies the Filesystem.
    # Drain any local mount that uses the target token first.
    ti fs disable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## Related documentation

- [Token-management authorization](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md)
- [`ti fs delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md)
