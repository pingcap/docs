---
title: TiDB Cloud Filesystem
summary: 了解什么是 TiDB Cloud Filesystem、何时使用它，以及如何在应用程序、自动化流程和 AI 代理之间访问和共享持久化文件。
---

# TiDB Cloud Filesystem

TiDB Cloud Filesystem 是一个面向应用程序、自动化流程和 AI 代理的持久化共享云文件系统。文件可独立于创建它们的机器或进程持续可用，因此你可以在不同会话和环境之间复用同一个工作区。

当文件需要在某个进程或沙箱结束后仍然可用、工作流跨越多台机器或临时环境，或者多个用户或工作负载需要以受控方式访问同一批文件时，可以使用 TiDB Cloud Filesystem。

例如，你可以将文件系统用于以下任务：

- 从不同的机器或环境访问并修改同一批文件。
- 与用户、应用程序、CI 作业或 AI 代理共享文件和结果。
- 将文件系统挂载为本地目录，以便需要本地文件路径的工具使用。
- 在将文件变更应用到共享文件之前，先在 layer 中隔离这些变更。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## TiDB Cloud Filesystem 的工作原理 {#how-tidb-cloud-filesystem-works}

TiDB Cloud Filesystem 独立于访问它的机器和进程，持久化存储在 TiDB Cloud 中。因此，不同的已授予权限环境可以访问同一批文件，而无需在机器之间复制这些文件。

要创建和管理文件系统，你可以使用 [TiDB Cloud console](https://tidbcloud.com/) 或 [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md)。使用 TiDB Cloud Filesystem 无需预配或管理 TiDB 数据库。

控制台还支持浏览文件和目录，并查看其元信息，例如文件大小和修改时间。

要读取文件内容或修改文件和目录，请使用以下方法之一：

- **使用 `ti fs` 命令**：无需挂载文件系统，即可直接通过命令行上传、下载、读取、整理和搜索文件。
- **将文件系统挂载为本地目录**：让应用程序和工具通过常规本地文件路径访问文件系统数据。

更多信息，请参见[使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md)和[挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)。

## 跨环境共享文件 {#share-files-across-environments}

多台机器或多个环境可以同时访问同一个文件系统。每个环境都可以使用自己的文件系统 Token，因此无需在不同环境之间共享凭据。

例如：

- CI 作业可以将构建输出写入文件系统，另一个环境稍后可以读取这些内容。
- AI 代理可以继续处理在先前会话中创建的文件。
- 审阅者可以获得对特定目录的只读访问权限。

TiDB Cloud Filesystem 提供所有者 Token 和范围受限 Token，因此你可以控制每个用户或工作负载能够访问哪些文件以及可执行哪些操作。

更多信息，请参见 [TiDB Cloud Filesystem 授权](/tidb-cloud-filesystem/filesystem-authorization.md) 和 [共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)。

## 隔离并管理变更 {#isolate-and-manage-changes}

为了让多个任务基于同一批文件工作而不修改共享基础内容，你可以创建文件系统 layer。

每个 layer 都提供一个隔离视图，你可以在其中独立进行变更。你可以为某个 layer 创建 checkpoint，之后再将选定的变更提交到基础文件系统。

更多信息，请参见 [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md)。

## 开始使用 {#get-started}

请选择与你的目标相匹配的路径：

- **创建新的文件系统：**参见 [通过控制台快速开始](/tidb-cloud-filesystem/filesystem-quick-start-console.md) 或 [通过 CLI 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)。
- **使用他人共享给你的文件系统：**参见 [访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md)。
- **查看支持的 Region、平台和当前限制：**参见 [Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md)。
- **将客户端 SDK 集成到你的应用程序中：**参见 [TiDB Cloud Filesystem SDK](/tidb-cloud-filesystem/filesystem-sdks.md)。