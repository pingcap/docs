---
title: ti fs delete-file-system-token
summary: Permanently revoke a TiDB Cloud Filesystem token.
---

# ti fs delete-file-system-token

Permanently revokes a Filesystem token. The token stops authenticating after the change propagates and no longer appears in list results. An owner token can revoke either token kind in the same Filesystem; a scoped token cannot use this command.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs delete-file-system-token
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
- `--dry-run`: Validate credentials, identifiers, and known local mount conflicts without revoking the token.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Revoke an old token after validating its replacement:

    ```bash
    # Revocation is permanent; use disable first when you need a reversible rollout.
    ti fs delete-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<old-token-id>"
    ```

- Revoke a token by using an owner token:

    ```bash
    # The owner token identifies the Filesystem; use the immutable ID of the token being revoked.
    TI_FS_TOKEN="<owner-fs-token>" ti fs delete-file-system-token \
      --token-id "<old-token-id>"
    ```

## Related documentation

- [Token-management authorization](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)
