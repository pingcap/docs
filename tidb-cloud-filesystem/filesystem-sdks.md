---
title: TiDB Cloud Filesystem SDK
summary: 了解 TiDB Cloud Filesystem 与 Drive9 workspace engine 的关系，并查找六种编程语言的客户端 SDK 文档。
---

# TiDB Cloud Filesystem SDK

TiDB Cloud Filesystem 使用 Drive9 workspace engine 来执行文件系统操作。TiDB Cloud Filesystem 是 PingCAP 在 TiDB Cloud 上提供的官方托管 Drive9 服务。Drive9 是由 PingCAP 拥有的开源社区项目，而 TiDB Cloud Filesystem 是其托管云服务。在 API 和 SDK layer，你将直接调用由 TiDB Cloud Filesystem 服务暴露的 drive9 endpoint。

Drive9 是一个开源项目（Apache 2.0），维护在 [mem9-ai/drive9 仓库](https://github.com/mem9-ai/drive9) 中。除了 workspace engine 之外，该仓库还发布了多种编程语言的客户端 SDK。这些 SDK 及其文档都在该仓库中维护，因此本页列出的指南是 SDK 安装、配置和 API 细节的权威来源。

SDK 指南说明了客户端如何连接到 Drive9 server，包括如何提供 server URL 和 API key。

下表显示了应使用哪种 TiDB Cloud Filesystem 凭证。当 SDK 指南要求提供 API key 时，请使用 file system token。

|TiDB Cloud Filesystem 对象|Drive9 SDK/API 用法|
|:--|:--|
|TiDB Cloud API Key|文件系统控制面操作|
|File System Token|文件系统数据面操作|

请为每个 TiDB Cloud Filesystem Region 使用以下 server URL。

| TiDB Cloud Filesystem Region| Drive9 SDK/API 的 Server URL | API Key|
|:--|:--|:--|
|`aws-us-east-1`|`https://aws-us-east-1.drive9.ai`| FS token|
|`aws-us-west-2`|`https://aws-us-west-2.drive9.ai`| FS token|
|`aws-ap-southeast-1`|`https://aws-ap-southeast-1.drive9.ai`| FS token|
|`gcp-us-east1`|`https://gcp-us-east1.drive9.ai`| FS token|
|`azure-centralus`|`https://azure-centralus.drive9.ai`|FS token|
|`alicloud-ap-southeast-1`|`https://alicloud-ap-southeast-1.drive9.ai`|FS token|

始终将 SDK server URL 设置为你的文件系统所在 Region 的 endpoint。如果你未设置 server URL，大多数 SDK 会回退到 `https://api.drive9.ai`，但这不是 TiDB Cloud Filesystem 的 endpoint，并且会拒绝 TiDB Cloud Filesystem token。file system token 只能与其所属 Region 的 endpoint 一起使用。

## 可用的 SDK {#available-sdks}

| 语言 | 仓库位置 | 文档 |
| --- | --- | --- |
| TypeScript | `clients/drive9-js` | [TypeScript SDK 集成指南](https://github.com/mem9-ai/drive9/blob/main/docs/guides/typescript-sdk-integration.md) |
| Go | `pkg/client` | [Go SDK 集成指南](https://github.com/mem9-ai/drive9/blob/main/docs/guides/go-sdk-integration.md) |
| Python | `clients/drive9-py` | [drive9-py README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-py/README.md) |
| Rust | `clients/drive9-rs` | [drive9-rs README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-rs/README.md) |
| Kotlin | `clients/drive9-kotlin` | [drive9-kotlin README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-kotlin/README.md) |
| Swift | `clients/drive9-swift` | [drive9-swift README](https://github.com/mem9-ai/drive9/blob/main/clients/drive9-swift/README.md) |

这些 SDK 随 Drive9 项目一起开发和发布，因此其进度可能会领先于 TiDB Cloud Filesystem 服务。在你为 TiDB Cloud Filesystem 工作负载采用某个 SDK 之前，请先查看其文档，确认当前的 server endpoint、凭证以及支持的操作。

## 后续步骤 {#what-s-next}

- [TiDB Cloud CLI (`ti`)](/ai/ti/ti-quick-start.md)：安装、配置和更新 CLI。
- [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md)：从命令行管理文件系统数据。
- [自动化和 AI Agent 工作流](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)：在自动化工作流中使用文件系统。