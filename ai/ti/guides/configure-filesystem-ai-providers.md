---
title: Configure TiDB Cloud Filesystem AI Providers
summary: Learn how to inspect and configure media extraction and embedding providers for a TiDB Cloud Filesystem by using the CLI.
---

# Configure TiDB Cloud Filesystem AI Providers

A TiDB Cloud Filesystem can optionally extract text from media files and generate embeddings for stored content. To enable these capabilities, you can configure one or more AI providers through the CLI.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Obtain the target Filesystem ID.
- Obtain the API key required by your selected AI provider.

The configuration commands require TiDB Cloud API credentials and an explicit Filesystem ID. Set the provider key through `TI_FS_AI_PROVIDER_API_KEY`. The CLI does not persist the key locally. The Filesystem service stores it encrypted and returns only a masked value in subsequent configuration output.

For an interactive shell, read and export the provider key without placing it in shell history:

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

In CI, inject `TI_FS_AI_PROVIDER_API_KEY` from a masked secret. Unset the variable after you finish configuring providers.

> **Note:**
>
> When you enable, re-enable, or replace a provider configuration, the Filesystem service sends a small built-in request to the provider endpoint to validate the credentials, connectivity, and model response. This validation request might incur a provider charge. A disable-only or prompt-only update does not make a validation request.

## Inspect media extraction configuration

Read the effective extraction configuration for a media type:

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

## Update media extraction configuration

Use [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) to enable, update, or disable image, audio, or video extraction. For example, configure image extraction through an OpenAI-compatible provider:

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

The `openai` protocol supports image, audio, and video extraction. The `qwen-asr` protocol is supported only for audio extraction through Alibaba Cloud Model Studio. An endpoint from another provider might work if it implements the required OpenAI-compatible API contract. Native interfaces for Anthropic, Gemini, Vertex AI, Amazon Bedrock, and Azure OpenAI are not supported.

To disable extraction for a media type:

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## Inspect embedding configuration

Read whether embeddings are managed by the application or database:

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

## Update embedding configuration

Use [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) to update the optional application-managed embedding configuration. For example:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model text-embedding-3-small
```

Application-managed embeddings require an OpenAI-compatible endpoint that returns 1024-dimensional vectors. They are available for Shared Filesystems and Native Filesystems whose effective embedding mode is `fts_only`. If a Native Filesystem uses database-managed automatic embeddings, the service rejects this update and reports `source=database_auto`.

After you finish configuring providers, remove the key from the current shell:

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

To disable that configuration:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## Data flow after configuration

After you enable extraction, the Filesystem service sends media content to the configured extraction provider. It sends the extracted text or descriptions to the configured embedding provider. Choose provider accounts and retention policies appropriate for your data.

If an update fails because of a timeout, lost response, or another ambiguous network error, run the matching `describe-file-system-*-configuration` command before retrying. The provider validation request might have succeeded and incurred a charge even if the CLI did not receive the response.

## What's next

- [Work with TiDB Cloud Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
