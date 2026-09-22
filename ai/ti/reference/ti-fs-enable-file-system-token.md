---
title: ti fs enable-file-system-token
summary: Enable a disabled TiDB Cloud Filesystem token.
---

# ti fs enable-file-system-token

Re-enables a disabled Filesystem token. The token can take approximately 10 seconds to become usable. With owner token authentication, only scoped tokens can be enabled; TiDB Cloud API keys can enable either token kind.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs enable-file-system-token
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
- `--fs-token <string>`: Authorize the request with a Filesystem owner token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem. If no Filesystem token is available, the command uses the configured TiDB Cloud API keys.
- `--dry-run`: Validate the request without changing remote token state.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Enable a known token:

    ```bash
    # Allow about 10 seconds for all authentication caches to observe the change.
    ti fs enable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- Enable a scoped token by using an owner token:

    ```bash
    # The owner token identifies and authorizes token management for its Filesystem.
    TI_FS_TOKEN="<owner-fs-token>" ti fs enable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## Related documentation

- [Token-management authorization](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)
