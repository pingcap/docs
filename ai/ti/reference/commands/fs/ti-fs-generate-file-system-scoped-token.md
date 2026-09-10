---
title: ti fs generate-file-system-scoped-token
summary: Generate a path-and-operation-limited token for one TiDB Cloud Filesystem.
---

# ti fs generate-file-system-scoped-token

Uses an owner Filesystem token to generate a finite `fs_scoped` token. The plaintext `fs_token` appears only in the successful response. A scoped token can access only its allowed path prefixes and operations.

Scoped tokens support ordinary file, upload, Layer, and mount operations only when the requested paths and operations are covered. `chmod`, Git workspace APIs, Journal, Vault, SQL, fork, event, and token-management operations are not available to scoped tokens. Scoped tokens can refresh themselves without changing their scopes.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs generate-file-system-scoped-token
  --ttl <duration>
  --allow <prefix:ops>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--subject <string>]
  [--store-locally]
  [--replace]
  [--dry-run]
```

## Options

- `--ttl <duration>`: Set a finite positive token lifetime that resolves to whole seconds. This option is required.
- `--allow <prefix:ops>`: Allow operations under one remote path prefix. Repeat this option for multiple prefixes. Operations are `read`, `list`, `search`, `write`, and `delete`; `search` requires `read`. This option is required.
- `--file-system-id <string>`: Assert the Filesystem ID embedded in the owner token. This option is required only when loading a locally stored owner token.
- `--fs-token <string>`: Supply the owner token. Defaults to `TI_FS_TOKEN`, then the selected local credential.
- `--subject <string>`: Set an optional server-side audit label of at most 64 bytes. It is not a unique selector.
- `--store-locally`: Store and select the generated scoped token for this profile and Filesystem.
- `--replace`: Replace an existing selected local token. Requires `--store-locally` and does not revoke the previous remote token.
- `--dry-run`: Validate the owner credential, region, lifetime, scopes, and local storage preconditions without generating a token.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Give a sandbox read and write access to one workspace:

    ```bash
    # Use an owner token to create a 24-hour token limited to /workspace.
    export TI_FS_TOKEN="<owner-fs-token>"
    ti fs generate-file-system-scoped-token \
      --subject sandbox-agent \
      --ttl 24h \
      --allow /workspace:read,list,write
    ```

- Separate writable workspace data from read-only artifacts:

    ```bash
    # Repeat --allow to assign different operations to independent prefixes.
    ti fs generate-file-system-scoped-token \
      --fs-token "<owner-fs-token>" \
      --ttl 8h \
      --allow /workspace:read,list,write,delete \
      --allow /artifacts:read,list
    ```

- Select the generated scoped token for later local commands:

    ```bash
    # Replacing the local selection does not revoke the previous remote owner token.
    ti fs generate-file-system-scoped-token \
      --file-system-id "<file-system-id>" \
      --ttl 1h \
      --allow /task:read,list,write \
      --store-locally \
      --replace
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [`ti fs generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [`ti fs refresh-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-refresh-file-system-token.md)
