---
title: Configure TiDB Cloud Filesystem AI Providers
summary: Learn how to inspect and configure media extraction and embedding providers for a TiDB Cloud Filesystem by using the CLI.
---

# Configure TiDB Cloud Filesystem AI Providers

Configure optional media extraction and embedding providers when applications need a Filesystem to process or embed stored content.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Obtain the target Filesystem ID.
- Obtain the credentials required by your selected provider.

The configuration commands require TiDB Cloud API credentials and an explicit Filesystem ID. Set the provider key through `TI_FS_AI_PROVIDER_API_KEY`; the CLI does not persist it locally. Provider validation can send a small built-in request and incur a provider charge.

## Inspect media extraction configuration

Read the effective extraction configuration for a media type:

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

## Update media extraction configuration

Use [`update-file-system-extract-configuration`](/ai/ti/reference/commands/fs/ti-fs-update-file-system-extract-configuration.md) to enable, update, or disable image, audio, or video extraction. For example, configure image extraction through an OpenAI-compatible provider:

```shell
TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

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

Use [`update-file-system-embedding-configuration`](/ai/ti/reference/commands/fs/ti-fs-update-file-system-embedding-configuration.md) to update the optional application-managed embedding configuration. For example:

```shell
TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model text-embedding-3-small
```

To disable that configuration:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

After extraction is enabled, Filesystem media content is sent to the selected extraction provider. Text or extracted descriptions are sent to the embedding provider. Choose provider accounts and retention policies appropriate for your data.

## What's next

- [Work with TiDB Cloud Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
