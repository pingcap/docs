---
title: Configure TiDB Cloud Filesystem AI Providers
summary: Configure AI providers for media extraction and embeddings in a TiDB Cloud Filesystem.
aliases: ['/ai/configure-filesystem-ai-providers']
---

# Configure TiDB Cloud Filesystem AI Providers

Use this guide when you want TiDB Cloud Filesystem to extract searchable content from images, audio, or video, or when you want to configure a custom embedding provider for semantic search.

- **Media extraction** uses an AI provider to extract text or descriptions from images, audio, or video so that the content can be searched.
- **Embeddings** represent text and extracted descriptions as vectors for semantic search.

These capabilities are optional and can be configured separately. For example, you can configure media extraction without configuring a custom embedding provider.

This guide shows you how to check the current configuration, configure providers for media extraction and embeddings, and disable a custom configuration when it is no longer needed.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing TiDB Cloud Filesystem and obtain its Filesystem ID.
- Configure TiDB Cloud API credentials. The commands in this guide require TiDB Cloud API credentials and an explicit Filesystem ID; they do not use a Filesystem token.
- If you want to enable or replace a provider configuration, obtain the provider endpoint, model name, and API key.

> **Note:**
>
> When you configure a custom provider, TiDB Cloud Filesystem sends content to that provider for processing. Make sure that the provider account and its data retention and privacy policies are appropriate for your data.

## Provide the API key of your AI provider

When you enable or replace a provider configuration, provide the API key of your AI provider through `TI_FS_AI_PROVIDER_API_KEY`.

For an interactive shell, read and export the key without placing it in shell history:

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

The TiDB Cloud CLI does not store the key locally. The Filesystem service stores it encrypted and returns only a masked value when you inspect the configuration later.

In CI, provide `TI_FS_AI_PROVIDER_API_KEY` through your CI secret-management mechanism.

> **Note:**
>
> When you enable, re-enable, or replace a provider configuration, the Filesystem service sends a small request to the provider to validate the credentials, connectivity, and model response. The provider might charge for this validation request. Disabling a provider or updating only an extraction prompt does not send a validation request.

## Configure media extraction

Media extraction lets TiDB Cloud Filesystem process images, audio, or video and make the extracted text or descriptions available for content search.

### Check the current configuration

Before changing the configuration, check the current extraction configuration for the media type you want to process:

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

Replace `image` with `audio` or `video` to inspect another media type.

### Enable or update media extraction

For example, to enable image extraction with an OpenAI-compatible provider:

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

The `openai` protocol supports image, audio, and video extraction. For audio extraction, you can also use the `qwen-asr` protocol with Alibaba Cloud Model Studio.

Other provider endpoints can be used only if they implement the required OpenAI-compatible API contract. Native interfaces for Anthropic, Gemini, Vertex AI, Amazon Bedrock, and Azure OpenAI are not supported.

For all available options, see [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md).

### Disable media extraction

To disable extraction for a media type:

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## Configure embeddings

Embeddings represent text content and extracted media descriptions as vectors for semantic search.

### Check the current configuration

Before configuring a custom embedding provider, check the current embedding configuration:

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

Check the `source` field in the output. If it is `database_auto`, embeddings are managed by the service and you cannot replace the configuration with a custom provider.

### Enable or update a custom embedding provider

If the current configuration allows a custom provider, configure an OpenAI-compatible embedding endpoint:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<embedding-model>"
```

The provider must return exactly 1024-dimensional vectors through the OpenAI-compatible embeddings API. Other vector dimensions are not supported.

For all available options, see [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md).

### Disable the custom embedding configuration

To disable the custom embedding configuration:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## Finish configuring providers

After you finish configuring providers, remove the provider API key from the current shell:

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

When custom media extraction is enabled, TiDB Cloud Filesystem sends the relevant media content to the configured extraction provider. When a custom embedding provider is enabled, text content and extracted media descriptions are sent to the embedding provider.

If an update fails because of a timeout, lost response, or another error where you cannot tell whether the update succeeded, do not immediately retry the command. Run the corresponding `describe-file-system-*-configuration` command first.

The Filesystem service might already have saved the configuration and sent the provider validation request even if the CLI did not receive the response.

## What's next

- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) to search Filesystem content.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for complete command syntax and options.
