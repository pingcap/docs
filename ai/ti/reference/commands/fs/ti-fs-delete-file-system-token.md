---
title: ti fs delete-file-system-token
summary: Permanently revoke a TiDB Cloud Filesystem token.
---

# ti fs delete-file-system-token

Permanently revokes a token by immutable token ID. Revocation is terminal and the service does not return revoked tokens in later list results. An owner token can revoke either token kind in the same Filesystem; a scoped token cannot use this command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs delete-file-system-token
  --file-system-id <string>
  --token-id <string>
  [--fs-token <string>]
  [--dry-run]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem that owns the token. This option is required.
- `--token-id <string>`: Specify the immutable token ID returned by the list command. This option is required.
- `--fs-token <string>`: Authorize the request with an owner FS token. Defaults to `TI_FS_TOKEN`; when neither is present, the command uses configured TiDB Cloud API keys.
- `--dry-run`: Validate credentials, identifiers, and known local mount conflicts without revoking the token.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Revoke an old token after validating its replacement:

    ```bash
    # Revocation is permanent; use disable first when you need a reversible rollout.
    ti fs delete-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<old-token-id>"
    ```

## Related documentation

- [`ti fs generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-disable-file-system-token.md)
