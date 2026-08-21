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
  [--file-system-id <string>]
  [--fs-token <string>]
  [--include-expired]
  [--limit <int32>]
  [--offset <int32>]
```

## Options

- `--file-system-id <string>`: Specify the Filesystem whose tokens are listed. Required when using TiDB Cloud API credentials; optional when `--fs-token` or `TI_FS_TOKEN` supplies an owner token, because `ti` derives the ID from that token.
- `--fs-token <string>`: Authorize the request with an owner FS token. Defaults to `TI_FS_TOKEN`; when neither is present, the command uses configured TiDB Cloud API keys. Scoped tokens cannot list token metadata.
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

- List token metadata with an owner token:

    ```bash
    # The owner token identifies the Filesystem, so --file-system-id is not needed.
    TI_FS_TOKEN="<owner-fs-token>" ti fs list-file-system-tokens --output text
    ```

## Related documentation

- [`ti fs generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [`ti fs generate-file-system-scoped-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-scoped-token.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
