---
title: 为文件系统配置 AI 提供方
summary: 为文件系统配置用于媒体内容提取和向量嵌入的 AI 提供方。
aliases: ['/zh/ai/configure-filesystem-ai-providers']
---

# 为文件系统配置 AI 提供方

当你希望 TiDB Cloud Filesystem 从镜像、音频或视频中提取可搜索内容，或者希望为语义搜索配置自定义嵌入提供方时，请使用本指南。

- **媒体内容提取** 使用 AI 提供方从镜像、音频或视频中提取文本或描述，以便搜索这些内容。
- **向量嵌入** 将文本和提取出的描述表示为向量，用于语义搜索。

这些能力都是可选的，并且可以分别配置。例如，你可以只配置媒体内容提取，而不配置自定义嵌入提供方。

本指南介绍如何检查当前配置、为媒体内容提取和向量嵌入配置提供方，以及在不再需要时禁用自定义配置。

## 前提条件 {#prerequisites}

开始之前，请确保：

- [安装 TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 可以访问一个现有文件系统，并获取其文件系统 ID。
- 已配置 TiDB Cloud API 凭证。本指南中的命令需要 TiDB Cloud API 凭证和显式指定的文件系统 ID；它们不使用文件系统 Token。
- 如果你想启用或替换某个提供方配置，请准备好提供方 endpoint、模型名称和 API key。

> **Note:**
>
> 当你配置自定义提供方时，TiDB Cloud Filesystem 会将内容发送给该提供方进行处理。请确保该提供方账户及其数据保留和隐私策略适合你的数据。

## 提供 AI 提供方的 API key {#provide-the-api-key-of-your-ai-provider}

当你启用或替换某个提供方配置时，需要通过 `TI_FS_AI_PROVIDER_API_KEY` 提供 AI 提供方的 API key。

对于交互式 shell，可以按如下方式读取并导出该 key，以避免将其写入 shell 历史记录：

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

TiDB Cloud CLI 不会在本地存储该 key。文件系统服务会以加密方式存储它，并且当你稍后检查配置时，只会返回脱敏后的值。

在 CI 中，请通过 CI 的 Secret 管理机制提供 `TI_FS_AI_PROVIDER_API_KEY`。

> **Note:**
>
> 当你启用、重新启用或替换某个提供方配置时，文件系统服务会向该提供方发送一个小型请求，以验证凭证、连通性和模型响应。该提供方可能会对此验证请求收费。禁用提供方或仅修改提取提示词时，不会发送验证请求。

## 配置媒体内容提取 {#configure-media-extraction}

媒体内容提取使 TiDB Cloud Filesystem 能够处理镜像、音频或视频，并将提取出的文本或描述用于内容搜索。

### 检查当前配置 {#check-the-current-configuration}

在修改配置之前，请先检查你要处理的媒体类型的当前提取配置：

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

将 `image` 替换为 `audio` 或 `video`，即可查看其他媒体类型。

### 启用或修改媒体内容提取 {#enable-or-update-media-extraction}

例如，要使用兼容 OpenAI 的提供方启用镜像提取：

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

`openai` 协议支持镜像、音频和视频提取。对于音频提取，你还可以结合 Alibaba Cloud Model Studio 使用 `qwen-asr` 协议。

只有在其他提供方 endpoint 实现了所需的 OpenAI-compatible API contract 时，才能使用这些 endpoint。当前不支持 Anthropic、Gemini、Vertex AI、Amazon Bedrock 和 Azure OpenAI 的原生接口。

有关所有可用选项，请参见 [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md)。

### 禁用媒体内容提取 {#disable-media-extraction}

要禁用某种媒体类型的提取：

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## 配置向量嵌入 {#configure-embeddings}

向量嵌入将文本内容和提取出的媒体描述表示为向量，用于语义搜索。

### 检查当前配置 {#check-the-current-configuration}

在配置自定义嵌入提供方之前，请先检查当前嵌入配置：

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

检查输出中的 `source` 字段。如果其值为 `database_auto`，则表示向量嵌入由服务管理，你无法用自定义提供方替换该配置。

### 启用或修改自定义嵌入提供方 {#enable-or-update-a-custom-embedding-provider}

如果当前配置允许使用自定义提供方，请配置一个兼容 OpenAI 的嵌入 endpoint：

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<embedding-model>"
```

该提供方必须通过兼容 OpenAI 的 embeddings API 返回**恰好** 1024 维向量。不支持其他向量维度。

有关所有可用选项，请参见 [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md)。

### 禁用自定义嵌入配置 {#disable-the-custom-embedding-configuration}

要禁用自定义嵌入配置：

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## 完成提供方配置 {#finish-configuring-providers}

完成提供方配置后，请从当前 shell 中移除提供方 API key：

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

启用自定义媒体内容提取后，TiDB Cloud Filesystem 会将相关媒体内容发送到已配置的提取提供方。启用自定义嵌入提供方后，文本内容和提取出的媒体描述会被发送到嵌入提供方。

如果由于超时、响应丢失或其他错误导致修改失败，并且你无法判断修改是否成功，请不要立即重试该命令。请先运行对应的 `describe-file-system-*-configuration` 命令。

即使 CLI 没有收到响应，文件系统服务也可能已经保存了配置，并发送了提供方验证请求。

## 接下来做什么 {#what-s-next}

- [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md) 来搜索文件系统内容。
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md) 了解完整的命令语法和选项。