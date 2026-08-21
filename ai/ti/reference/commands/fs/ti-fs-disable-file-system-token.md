---
title: ti fs disable-file-system-token
summary: Temporarily disable a TiDB Cloud Filesystem token.
---

# ti fs disable-file-system-token

Disables an active token by immutable token ID without revoking it. A token used by a known local mount must be drained and unmounted first. When `--fs-token` or `TI_FS_TOKEN` supplies owner Bearer authentication, the target must be an `fs_scoped` token. Configured TiDB Cloud API keys can disable either token kind.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs disable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem that owns the token. Required when using TiDB Cloud API credentials; optional when an owner token supplies the ID.
- `--token-id <string>`: Specify the immutable token ID returned by the list command. This option is required.
- `--fs-token <string>`: Authorize the request with an owner FS token. Defaults to `TI_FS_TOKEN`; when neither is present, the command uses configured TiDB Cloud API keys.
- `--dry-run`: Validate credentials, identifiers, and known local mount conflicts without disabling the token.

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
    # The owner token identifies the Filesystem; drain any local mount that uses the target token first.
    TI_FS_TOKEN="<owner-fs-token>" ti fs disable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## Related documentation

- [`ti fs enable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-enable-file-system-token.md)
- [`ti fs delete-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-delete-file-system-token.md)
