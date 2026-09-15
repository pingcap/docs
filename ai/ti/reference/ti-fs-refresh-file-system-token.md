---
title: ti fs refresh-file-system-token
summary: Rotate one TiDB Cloud Filesystem token and return its replacement plaintext once.
---

# ti fs refresh-file-system-token

Rotates the supplied Filesystem token and returns its replacement value once. The previous value stops working after authentication changes propagate, which can take approximately 10 seconds.

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
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Capture the one-time replacement and update the external secret manager yourself.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token > ./refreshed-token.json
    unset TI_FS_TOKEN
    ```

- Change the token lifetime during refresh:

    ```bash
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Rotate the token and set its new lifetime to 30 days.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token --ttl 720h
    unset TI_FS_TOKEN
    ```

## Related documentation

- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
