---
title: ti fs update-file-system-extract-configuration
summary: Update media extraction configuration for a TiDB Cloud Filesystem.
---

# ti fs update-file-system-extract-configuration

Updates optional image, audio, or video extraction configuration for one Filesystem. Enabling or replacing a provider performs a real provider validation request that can incur a small provider charge. After enablement, Filesystem media is sent to the selected provider for extraction.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs update-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--dry-run]
  [--enabled <boolean>]
  [--help]
  [--prompt <string>]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--provider-protocol <string>]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable Filesystem ID. \[required]
- `--media-type <string>`: Select `image`, `audio`, or `video`. \[required]
- `--dry-run`: Validate the request without contacting the Filesystem backend or AI provider.
- `--enabled <boolean>`: Explicitly enable or disable extraction. Enter `true` or `false`.
- `--prompt <string>`: Set a prompt of at most 8 KiB. Pass an empty string to restore backend default prompt behavior.
- `--provider-api-base <string>`: Set a valid HTTPS provider base URL.
- `--provider-model <string>`: Set the provider model name.
- `--provider-protocol <string>`: Set `openai`, or `qwen-asr` for audio only. The default is `openai`.
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

The provider API key is accepted only from `TI_FS_AI_PROVIDER_API_KEY`. It is sent to the Filesystem backend for validation and encrypted storage, is never stored locally by `ti`, and is returned only in masked form. `openai` supports image, audio, and video. Alibaba Cloud Model Studio Qwen ASR is supported for audio through `qwen-asr`. Other services work only when they implement the exact required OpenAI-compatible contract. Native Anthropic, Gemini, Vertex AI, Bedrock, and Azure OpenAI interfaces are not supported.

Do not retry an update blindly after a timeout or lost response. The provider might already have charged for validation and the backend might have saved the configuration. Run the matching describe command first.

## Examples

- Enable image extraction with an OpenAI-compatible provider:

    ```bash
    # Supply the secret through the environment so it is not written to shell arguments.
    TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model <vision-model>
    ```

- Enable Alibaba Cloud Model Studio Qwen ASR for audio:

    ```bash
    # Use the DashScope OpenAI-compatible endpoint with the qwen-asr protocol.
    TI_FS_AI_PROVIDER_API_KEY="<dashscope-api-key>" \
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --enabled true \
      --provider-api-base https://dashscope.aliyuncs.com/compatible-mode/v1 \
      --provider-model qwen3-asr-flash \
      --provider-protocol qwen-asr
    ```

- Change only the prompt of an enabled image configuration:

    ```bash
    # Keep the existing provider credentials and update only extraction instructions.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --prompt "Describe the image and return searchable attributes."
    ```

- Disable image extraction:

    ```bash
    # Remove the custom image provider configuration without changing normal file access.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled false
    ```

## Related documentation

- [`ti fs describe-file-system-extract-configuration`](/ai/ti/reference/commands/fs/ti-fs-describe-file-system-extract-configuration.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
