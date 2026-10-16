---
title: TiDB Cloud Filesystem 区域与限制
summary: 了解 TiDB Cloud Filesystem 支持的区域、挂载平台要求、持久性边界以及当前产品限制。
---

# TiDB Cloud Filesystem 区域与限制

TiDB Cloud Filesystem 仅在下列区域和环境中可用。在创建文件系统或选择如何访问其数据之前，请先确认这些边界条件。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 支持的区域 {#supported-regions}

| 提供商 | 位置 | 规范区域代码 |
| --- | --- | --- |
| AWS | 弗吉尼亚北部 | `aws-us-east-1` |
| AWS | 俄勒冈 | `aws-us-west-2` |
| AWS | 新加坡 | `aws-ap-southeast-1` |
| Alibaba Cloud | 新加坡 | `alicloud-ap-southeast-1` |
| Google Cloud | 南卡罗来纳 | `gcp-us-east1` |
| Microsoft Azure | 美国中部 | `azure-centralus` |

TiDB Cloud Starter 还支持一些 TiDB Cloud Filesystem 不可用的区域。在这些区域中执行文件系统命令会失败，并显示一条错误信息，指出该区域的服务不可用，同时列出受支持的区域。受支持的文件系统区域内置于每个 `ti` 发布版本中。如果某个区域的支持是在你已安装版本发布之后才新增的，请升级 `ti`；仅指定服务 URL 并不能启用该区域的支持。

`list` 和 `describe` 文件系统命令仅查询当前所选区域。它们不会聚合跨区域的资源。有关 CLI 范围内的区域选择和 Starter 可用性，请参见[TiDB Cloud CLI 区域、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions)。

## 挂载平台支持 {#mount-platform-support}

| 平台 | 文件系统挂载 | Vault 挂载 | 要求与替代方案 |
| --- | --- | --- | --- |
| macOS | 文件系统挂载默认使用 WebDAV，即使已安装 macFUSE 也是如此。要使用 FUSE，请指定 `--driver fuse`。layer 和 checkpoint 挂载需要 FUSE。 | FUSE | 内置的 WebDAV helper 支持文件系统挂载。对于 FUSE 或 Vault 挂载，请安装 macFUSE 并批准其系统扩展。 |
| Linux | FUSE | FUSE | 安装 `fuse3` 软件包，并提供对 `/dev/fuse` 的访问。WebDAV 挂载不受支持。 |
| Windows | 不支持 | 不支持 | 请改用 `ti fs` 数据平面命令以及非挂载类 Vault 命令。 |

FUSE 和 WebDAV 由随附的文件系统运行时组件实现。CLI 不会回退到单独的原生挂载实现。正在运行的挂载会继续使用其启动时加载的运行时版本；更新 `ti` 后，请先卸载再重新挂载。

Ubuntu 26.04 还会使用 AppArmor 限制 `fusermount3`。请使用位于 `$HOME` 或 `/mnt` 下的挂载路径；即使 `ti` 以 root 身份运行，`/workspace` 也需要显式的本地 AppArmor 规则。有关设置和变通方法，请参见[在 Linux 上挂载文件系统](/tidb-cloud-filesystem/filesystem-mount-linux.md#ubuntu-2604-mount-path-restrictions)。

## 持久性边界 {#durability-boundaries}

- 默认的 FUSE 行为会在配套组件允许的情况下使用本地缓冲和异步远程处理。若突然终止挂载进程或删除机器，可能会丢失尚未提交的内存状态或回写状态。
- 当你使用 `--mount-profile coding-agent` 选择 `coding-agent` 挂载预设时，依赖树、生成输出、缓存以及 Git 内部数据会存储在本地。仅保存在本地的数据会在其所在磁盘消失时一并消失，除非这些数据已被打包或通过其他方式保留。
- 已远程提交的文件系统数据在客户端或沙箱被删除后仍会保留；删除机器不会删除远程文件系统。

有关受支持的刷写和优雅的卸载工作流，请参见[安全结束使用](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)。`drain-file-system` 是仅适用于 FUSE 的在线持久性屏障；WebDAV 不支持它。

## 当前限制 {#current-limitations}

- 日志（Journal）为仅追加，且当前公开的命令接口没有删除日志（Journal）的命令。
- 本地凭证存储会为每个配置（Profile）和文件系统保留一个已选中的 Token。它不会镜像所有远程 Token。较早创建或导入、且没有已知 Token ID 的凭证仍可使用，但无法与远程 Token 元信息建立关联。
- 文件系统的媒体内容提取和向量嵌入 provider 配置是可选的。即使不进行配置，也不会阻止资源管理、文件访问、搜索、layer、Git、日志（Journal）、Vault 或挂载工作流。
- OpenAI provider 接口支持用于向量嵌入以及镜像、音频和视频的媒体内容提取。Alibaba Cloud Model Studio Qwen ASR 仅支持音频媒体内容提取。其他厂商仅能通过完全兼容 OpenAI 的契约实现有条件兼容；不支持原生 Anthropic、Gemini、Vertex AI、Bedrock 和 Azure OpenAI 接口。
- 应用管理的向量嵌入要求 provider 模型精确返回 1024 维。报告 `source=database_auto` 的文件系统使用数据库管理的向量嵌入，并会拒绝应用管理的配置。有关配置步骤，请参见[为文件系统配置 AI 提供方](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)。
- 文件系统运行时操作（包括直接文件访问、layer、挂载、Git 工作区、日志（Journal）和 Vault 操作）依赖于随 `ti` 一起安装的文件系统运行时组件。

如遇 Token 或挂载失败问题，请参见[排查 TiDB Cloud Filesystem 问题](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。有关命令语法和选项，请参见[TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)。