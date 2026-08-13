---
title: ti fs list-file-system-tokens
summary: List token metadata for one TiDB Cloud Filesystem.
---

# ti fs list-file-system-tokens

Lists non-secret token metadata for one Filesystem. The response never contains token plaintext.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs list-file-system-tokens
  --file-system-id <string>
  [--include-expired]
  [--limit <int32>]
  [--offset <int32>]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem whose tokens are listed. This option is required.
- `--include-expired`: Include expired token metadata. Revoked tokens are not returned by the service.
- `--offset <int32>`: Set the zero-based token offset [default: 0].
- `--limit <int32>`: Set the maximum number of tokens to return, from 1 through 200 [default: 50].

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- List current token metadata as text:

    ```bash
    # Use token_id, not the non-unique token name, for later mutations.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --output text
    ```

- Inspect expired token metadata with pagination:

    ```bash
    # Request up to 100 rows starting at offset 0.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --include-expired \
      --offset 0 \
      --limit 100
    ```

## Related documentation

- [`ti fs generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
