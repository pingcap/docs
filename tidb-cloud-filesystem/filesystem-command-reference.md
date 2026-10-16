---
title: TiDB Cloud Filesystem 命令参考
summary: 查找用于配置 `ti` 以及管理 TiDB Cloud Filesystem 资源、数据、Git 工作区、日志（Journal）和 Vault Secret 的 TiDB Cloud CLI 命令参考。
---

# TiDB Cloud Filesystem 命令参考

TiDB Cloud CLI (`ti`) 提供了用于操作 TiDB Cloud Filesystem 的命令行接口。你可以使用它创建和管理文件系统，处理文件和目录，并使用文件系统功能，例如 Git 工作区、日志（Journal）和 Vault Secret。

将此页面用作与 TiDB Cloud Filesystem 相关的 TiDB Cloud CLI 参考索引。它还包含你在配置或更新 CLI 时可能需要的通用 `ti` 命令和行为参考。

> **Note:**
>
> 本页仅涵盖与文件系统相关的命令参考。TiDB Cloud Starter 数据库命令（例如 `ti db`）在[TiDB Cloud CLI 文档](/ai/ti/ti-overview.md)中单独说明。

## 通用 TiDB Cloud CLI 参考 {#general-tidb-cloud-cli-references}

使用以下参考来配置或更新 `ti`，并了解其通用行为。

- [TiDB Cloud CLI 参考](/ai/ti/reference/ti-cli-reference.md)
- [`ti configure`](/ai/ti/reference/ti-configure.md)
- [`ti update`](/ai/ti/reference/ti-update.md)

## TiDB Cloud Filesystem 命令组 {#tidb-cloud-filesystem-command-groups}

根据你想要执行的操作选择相应的命令组。

- [`ti fs` 命令](/ai/ti/reference/ti-filesystem.md) 用于创建和管理文件系统，以及处理文件系统数据。
- [`ti fs-git` 命令](/ai/ti/reference/ti-filesystem-git.md) 用于在文件系统上处理 Git 仓库和工作树。
- [`ti fs-journal` 命令](/ai/ti/reference/ti-filesystem-journal.md) 用于管理文件系统日志（Journal）。
- [`ti fs-vault` 命令](/ai/ti/reference/ti-filesystem-vault.md) 用于管理文件系统 Vault Secret。