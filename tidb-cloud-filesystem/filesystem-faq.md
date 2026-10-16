---
title: TiDB Cloud Filesystem 常见问题
summary: 查找有关 TiDB Cloud Filesystem 使用、共享写入、Region、挂载、SDK、搜索、checkpoint、公测策略和定价的答案。
---

# TiDB Cloud Filesystem 常见问题

TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口如有变更，恕不另行通知。

## 什么是 TiDB Cloud Filesystem？ {#what-is-tidb-cloud-filesystem}

TiDB Cloud Filesystem 为应用程序、自动化流程和 AI agent 提供持久化的共享文件存储。文件可独立于创建它们的机器或进程持续可用，因此其他会话、沙箱、agent 或审阅者都可以继续使用同一个工作区。

你可以通过 TiDB Cloud CLI (`ti`) 命令访问文件，也可以将文件系统挂载为本地目录。你无需预配或管理 TiDB 数据库。更多信息，请参见 [TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md)。

## 如果我的沙箱已经提供持久化能力，还需要 TiDB Cloud Filesystem 吗？ {#do-i-need-tidb-cloud-filesystem-if-my-sandbox-already-provides-persistence}

如果你的工作流始终在同一个沙箱平台内运行，那么该平台提供的快照、暂停与恢复功能或持久卷可能已经足够。当你需要从另一个平台、机器、agent、审阅者或 CI 作业访问同一个工作目录时，可以考虑使用 TiDB Cloud Filesystem。

示例请参见 [自动化与 AI Agent 工作流](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md)。

## 文件变更会立即对其他环境可见吗？ {#are-file-changes-immediately-available-to-other-environments}

不一定。挂载点可能会先在本地缓冲变更，然后再上传到远程文件系统。FUSE 挂载默认就是这样工作的，因此本地写入完成并不意味着其他环境已经可以读到更新后的文件。

对于 FUSE 挂载，请先停止应用程序写入、关闭已打开的文件，然后使用 [`ti fs drain-file-system --mount-path <local-mount-path>`](/ai/ti/reference/ti-fs-drain-file-system.md) 在保持挂载运行的同时上传待处理的写入。正常卸载 FUSE 也会上传待处理的写入。WebDAV 不支持此命令；请先停止应用程序写入、关闭已打开的文件，然后执行卸载。

在删除机器或其本地缓存之前，请使用 `ti fs read-file` 验证所需变更是否已到达远程文件系统。如果刷写或卸载失败，请保留机器及其本地数据，以便后续恢复。详情请参见 [安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。

## 哪些 Region 支持 TiDB Cloud Filesystem？ {#which-regions-support-tidb-cloud-filesystem}

当前列表请参见 [支持的区域](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions)。文件系统的可用性与 TiDB Cloud Starter 的可用性不同。

通过 CLI 创建文件系统时，可使用 `ti configure` 选择受支持的 Region，或通过 `--region` 覆盖该命令的默认配置。创建流程请参见 [TiDB Cloud Filesystem 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)。

## 我可以在自己的笔记本电脑上挂载文件系统吗？ {#can-i-mount-a-file-system-on-my-laptop}

可以，在 macOS 或 Linux 上均可。对于评估场景，建议使用与文件系统位于同一 Region 的云虚拟机（VM）。如果你只需要读取远程文件，可以不挂载，直接使用 `ti fs read-file`。

Windows 不支持原生挂载。有关平台要求和替代方案，请参见 [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)。

## TiDB Cloud Filesystem 支持 POSIX 吗？ {#does-tidb-cloud-filesystem-support-posix}

支持。挂载后，TiDB Cloud Filesystem 提供兼容 POSIX 的访问方式：应用程序和 agent 可以通过普通本地路径、shell 命令和文件系统 API 读写文件。

不同平台和驱动的挂载能力有所不同。例如，layer 和 checkpoint 挂载需要 FUSE。请参见 [挂载平台支持](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#mount-platform-support)。

## TiDB Cloud Filesystem 是否提供 SDK？ {#are-sdks-available-for-tidb-cloud-filesystem}

提供。你可以使用适用于 TypeScript、Go、Python、Rust、Kotlin 和 Swift 的 Drive9 客户端 SDK。Drive9 是 TiDB Cloud Filesystem 使用的工作区引擎。

请使用文件系统 token 作为 SDK 的 API key，并将服务器 URL 设置为你的文件系统所在 Region 对应的 TiDB Cloud Filesystem endpoint。默认的 `https://api.drive9.ai` endpoint 不接受 TiDB Cloud Filesystem token。某些 SDK 版本可能包含托管服务尚未支持的操作，因此在使用前请先查阅 SDK 文档。

有关 endpoint 映射和集成指南，请参见 [TiDB Cloud Filesystem SDK](/tidb-cloud-filesystem/filesystem-sdks.md)。

## 我可以对文件使用语义搜索或向量搜索吗？ {#can-i-use-semantic-or-vector-search-over-my-files}

可以。语义搜索通过向量嵌入按语义查找内容，向量嵌入会将文本表示为数值向量。若要搜索图片、音频或视频，请配置媒体内容提取，以生成可搜索的文本或描述。

语义搜索需要向量嵌入。在设置 provider 之前，请先检查文件系统的向量嵌入配置：某些文件系统使用服务托管的向量嵌入，不允许自定义 provider。媒体内容提取和自定义嵌入 provider 都是可选项，并且可以分别配置。

`ti fs search-file-content` 命令接受文本查询，用于全文搜索；当向量嵌入可用时，也可用于语义搜索。其 `--pattern` 值不是正则表达式，也不是 glob。若要按名称、类型、标签、大小或修改时间查找路径，请使用 `ti fs find-files`。

有关设置，请参见 [为文件系统配置 AI 提供方](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)。有关搜索示例，请参见 [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md)。

## 公测是否支持 checkpoint 和回滚？ {#does-the-public-preview-support-checkpoints-and-rollback}

支持。layer 允许你在不修改共享基础文件系统的情况下更改文件，直到你提交该 layer。使用 `ti fs create-layer-checkpoint` 可以保存 layer 历史中的某个时间点。使用 `ti fs rollback-layer` 可以丢弃其未提交的更改。

回滚不会恢复到更早的 checkpoint。若要从某个 checkpoint 继续工作，请将其派生为一个新的可写 layer。checkpoint 会保留 layer 历史，但不会冻结整个基础文件系统，也不能替代备份。在公测期间，复杂的 layer 历史还存在额外限制；请参见 [边界和限制](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md#boundaries-and-limitations)。

有关概念和限制，请参见 [Layers 和 Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md)。有关命令，请参见 [管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md)。

## 公测期间是否提供服务级别协议（SLA）？ {#is-a-service-level-agreement-sla-available-during-public-preview}

不提供。请在 TiDB Cloud Filesystem 之外保留评估数据的备份，并报告任何异常行为。

## 公测结束后，我的工作区会怎样？ {#what-happens-to-my-workspace-after-public-preview-ends}

公测结束后，工作区是保留还是删除，相关策略尚未最终确定。请在 TiDB Cloud Filesystem 之外保留重要数据的备份。

## TiDB Cloud Filesystem 的费用是多少？ {#how-much-does-tidb-cloud-filesystem-cost}

TiDB Cloud Filesystem 对读、写、存储和互联网出口流量采用按量计费。每个组织每月可获得 $5.00 的免费额度，该额度在所有文件系统、计费项和 Region 之间共享。此额度用于抵扣使用费用，并不是每月账单上限。

公测价格在正式发布时可能会发生变化。有关当前各 Region 的费率、免费额度详情以及无需信用卡时的限制，请参见 [TiDB Cloud Filesystem Pricing Details](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/)。