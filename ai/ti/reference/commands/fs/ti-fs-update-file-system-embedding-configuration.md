---
title: ti fs update-file-system-embedding-configuration
summary: Replace embedding configuration for a TiDB Cloud Filesystem.
---

# ti fs update-file-system-embedding-configuration

Enables or disables optional app-managed embedding for one Filesystem. Enabling performs a real provider validation request that can incur a small provider charge. After enablement, text or extracted descriptions are sent to the selected embedding provider.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs update-file-system-embedding-configuration
  --enabled <boolean>
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--version]
```

## Options

- `--enabled <boolean>`: Enter `true` with a complete provider configuration, or `false` without provider options. \[required]
- `--file-system-id <string>`: Set the immutable Filesystem ID. \[required]
- `--dry-run`: Validate the request without contacting the Filesystem backend or embedding provider.
- `--provider-api-base <string>`: Set a valid HTTPS OpenAI-compatible provider base URL.
- `--provider-model <string>`: Set an embedding model that returns exactly 1024 dimensions.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

The provider API key is accepted only from `TI_FS_AI_PROVIDER_API_KEY`. It is sent to the Filesystem backend for validation and encrypted storage, is never stored locally by `ti`, and is returned only in masked form. Embedding requires an exact OpenAI-compatible `/v1/embeddings` contract. Native provider interfaces are not supported.

A Filesystem whose `source` is `database_auto` uses database-managed embedding and cannot be changed with this command. Do not retry an update blindly after a timeout or lost response. Run the describe command first to determine whether the update succeeded.

## Examples

- Enable app-managed embedding:

    ```bash
    # Configure a model that returns exactly 1024 dimensions.
    TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small
    ```

- Preview enablement without validating or saving the provider:

    ```bash
    # Validate local inputs and show a redacted request plan.
    TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small \
      --dry-run
    ```

- Disable app-managed embedding:

    ```bash
    # Remove custom embedding configuration without changing normal file access.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled false
    ```

## Related documentation

- [`ti fs describe-file-system-embedding-configuration`](/ai/ti/reference/commands/fs/ti-fs-describe-file-system-embedding-configuration.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
