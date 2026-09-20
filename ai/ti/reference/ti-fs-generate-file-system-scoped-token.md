---
title: ti fs generate-file-system-scoped-token
summary: Generate a path-and-operation-limited token for one TiDB Cloud Filesystem.
---

# ti fs generate-file-system-scoped-token

Generates a scoped token with limited path and operation access from an owner token. The token value appears only in the command output and cannot be retrieved later. A scoped token can access only its allowed path prefixes and operations.

Scoped tokens support ordinary file, upload, Layer, and mount operations only when the requested paths and operations are covered. `chmod`, Git workspace APIs, Journal, Vault, SQL, fork, event, and token-management operations are not available to scoped tokens. Scoped tokens can refresh themselves without changing their scopes.

The operations have the following meanings. A command can require more than one operation, such as `read` on a copy source and `write` on its destination.

| Operation | Allows |
| --- | --- |
| `read` | Reading file content and metadata. |
| `list` | Listing entries under a directory. |
| `search` | Searching or finding files under the prefix. Requires `read`. |
| `write` | Creating or changing files, directories, links, and copy destinations. |
| `delete` | Deleting a path or removing a source path during a move. |

> **Important:**
>
> Include both `search` and `read` in the same `--allow` value when permitting searches. The CLI rejects a scope that includes `search` without `read`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
  [--help]
  [--version]
```

## Options

- `--ttl <duration>`: Set a finite positive token lifetime that resolves to whole seconds. This option is required.
- `--allow <prefix:ops>`: Allow operations under one remote path prefix. Repeat this option for multiple prefixes. Operations are `read`, `list`, `search`, `write`, and `delete`; `search` requires `read`. This option is required.
- `--file-system-id <string>`: Assert the Filesystem ID embedded in the owner token. This option is required only when loading a locally stored owner token.
- `--fs-token <string>`: Supply the Filesystem owner token. If omitted, the command uses the `TI_FS_TOKEN` environment variable. If neither is provided, the command uses the local token stored for the selected Filesystem.
- `--subject <string>`: Set an optional server-side audit label of at most 64 bytes. It is not a unique selector.
- `--store-locally`: Store and select the generated scoped token for this profile and Filesystem.
- `--replace`: Replace an existing selected local token. Requires `--store-locally` and does not revoke the previous remote token.
- `--dry-run`: Validate the owner credential, region, lifetime, scopes, and local storage preconditions without generating a token.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Give a sandbox read and write access to one workspace:

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager, then create a token limited to /workspace.
    ti fs generate-file-system-scoped-token \
      --subject sandbox-agent \
      --ttl 24h \
      --allow /workspace:read,list,write
    ```

- Separate writable workspace data from read-only artifacts:

    ```bash
    # Inject the owner TI_FS_TOKEN from a secret manager. Repeat --allow to assign different operations to independent prefixes.
    ti fs generate-file-system-scoped-token \
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
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md)
