---
title: ti fs enable-file-system-token
summary: Enable a disabled TiDB Cloud Filesystem token.
---

# ti fs enable-file-system-token

Changes a disabled token to active by immutable token ID. Authentication caches can take approximately 10 seconds to converge. When `--fs-token` or `TI_FS_TOKEN` supplies owner Bearer authentication, the target must be an `fs_scoped` token. Configured TiDB Cloud API keys can enable either token kind.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs enable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem that owns the token. Required when using TiDB Cloud API credentials; optional when an owner token supplies the ID.
- `--token-id <string>`: Specify the immutable token ID returned by the list command. This option is required.
- `--fs-token <string>`: Authorize the request with an owner FS token. Defaults to `TI_FS_TOKEN`; when neither is present, the command uses configured TiDB Cloud API keys.
- `--dry-run`: Validate the request without changing remote token state.

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

- [`ti fs list-file-system-tokens`](/ai/ti/reference/commands/fs/ti-fs-list-file-system-tokens.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-disable-file-system-token.md)
