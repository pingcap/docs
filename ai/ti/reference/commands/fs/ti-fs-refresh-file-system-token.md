---
title: ti fs refresh-file-system-token
summary: Rotate one TiDB Cloud Filesystem token and return its replacement plaintext once.
---

# ti fs refresh-file-system-token

Rotates the supplied bearer token in place.

> **Warning:**
>
> Refresh is not idempotent. If the request succeeds but you do not receive the response, do not retry with the old token. Generate and distribute a replacement token instead.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs refresh-file-system-token
  [--file-system-id <string>]
  [--fs-token <string>]
  [--ttl <duration>]
  [--dry-run]
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Assert the Filesystem ID decoded from a supplied token. This option is required when loading a locally selected token.
- `--fs-token <string>`: Supply the current token. Prefer `TI_FS_TOKEN` to avoid shell history and process-list exposure. Defaults to `TI_FS_TOKEN`, then the selected local credential.
- `--ttl <duration>`: Set a new positive lifetime in whole seconds, up to 365 days. Omit it to preserve the previous lifetime period.
- `--dry-run`: Validate token selection, region, TTL, and known local mount conflicts without rotating the token.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Refresh the selected local credential:

    ```bash
    # ti atomically replaces the local credential after receiving the new token.
    ti fs refresh-file-system-token --file-system-id "<file-system-id>"
    ```

- Refresh a token supplied by a secret manager:

    ```bash
    # Capture the one-time replacement and update the external secret manager yourself.
    TI_FS_TOKEN="<current-token>" \
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token > ./refreshed-token.json
    ```

- Change the token lifetime during refresh:

    ```bash
    # Rotate the token and set its new lifetime to 30 days.
    TI_FS_TOKEN="<current-token>" \
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token --ttl 720h
    ```

## Related documentation

- [`ti fs generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
