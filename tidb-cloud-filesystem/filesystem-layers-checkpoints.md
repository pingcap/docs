---
title: TiDB Cloud Filesystem Layers and Checkpoints
summary: TiDB Cloud Filesystem layer 用于将更改与基础文件系统隔离，而派生和 checkpoint 则可在更改提交前保留 layer 历史。
---

# TiDB Cloud Filesystem Layers and Checkpoints

文件系统 layer 会在基础文件系统中的某一路径上记录更改，同时将这些更改与共享的基础数据分离。只有在 layer 被提交后，layer 中的更改才会成为基础文件系统的一部分。

layer 还可以创建 checkpoint 或进行派生，这使你能够保留 layer 历史中的某个时间点，或在独立的子 layer 中继续工作。

文件系统 layer 独立于 Git branch，也不需要 Git 仓库。

有关创建、检查、派生、创建 checkpoint、提交或回滚 layer 的命令，请参见[管理文件系统 Layers 和 Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)。

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口可能会在不另行通知的情况下发生变化。

## 核心概念 {#core-concepts}

- **基础文件系统：** layer 之外的共享文件系统状态。layer 会在某个基础路径上记录更改，而不会立即修改该状态。
- **Layer：** 基础路径上的一组可写更改。在 layer 提交之前，其更改始终与基础文件系统分离。
- **Checkpoint：** layer 持久历史中的一个命名时间点。创建 checkpoint 会保留该时间点在 layer 历史中的状态，但不会将 layer 的更改应用到基础文件系统。
- **Fork：** 从另一个 layer 的当前状态或其某个 checkpoint 创建的新可写子 layer。派生之后，父子 layer 中后续产生的更改彼此独立。
- **Commit：** 将 layer 中生效的更改应用到基础文件系统。
- **Rollback：** 丢弃 layer 中尚未提交的更改，而不将其应用到基础文件系统。回滚不会将 layer 重置到更早的 checkpoint。

## layer 与基础文件系统 {#layers-and-the-base-file-system}

在 layer 中进行的更改可通过该 layer 看到，但在 layer 提交之前，这些更改在基础文件系统中不可见。

未指定 layer 的操作会访问基础文件系统。这意味着，未提交的 layer 不会改变其他用户或应用程序直接访问基础文件系统时所看到的内容。

layer 是覆盖在基础路径上的一层叠加，而不是整个文件系统的完整快照。派生或 checkpoint 会保留相关的 layer 历史，但不会冻结整个基础文件系统。因此，仍然从基础文件系统解析的数据可能会反映基础文件系统后续发生的更改。

## 派生和 checkpoint {#forks-and-checkpoints}

checkpoint 会保留某个 layer 持久历史中的一个时间点。它不会创建另一个可写 layer，也不会将更改发布到基础文件系统。

checkpoint 可以作为只读视图进行访问。若要从 checkpoint 继续进行更改，请从该 checkpoint 派生一个新的可写 layer。

派生会保留父 layer 在创建派生时的历史状态。此后，父 layer 和子 layer 中的新更改彼此独立。

有关创建 checkpoint 或使用已挂载 layer 时的操作要求，请参见[管理文件系统 Layers 和 Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)。

## 提交和回滚 {#commit-and-rollback}

提交 layer 会将其中所有生效的更改应用到基础文件系统。commit 不是 Git commit，也不会选择性地发布单个文件。

commit 会将更改应用到基础文件系统，而不是该 layer 的父 layer。如果基础文件系统中存在冲突的更改，则 commit 可能会失败，而不是自动合并这些更改。

回滚 layer 会丢弃其未提交的更改，而不是发布这些更改。它不会将 layer 重置到更早的 checkpoint。

## 边界和限制 {#boundaries-and-limitations}

layer 提供更改隔离能力，但它们并不是完整的文件系统快照、备份或授权边界。若要限制对文件系统路径或操作的访问，请使用[范围受限 Token](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens)。

当前的 layer 模型有以下限制：

- 不支持 Git 风格的 merge 和 rebase 操作。
- layer 不能原地重置到某个 checkpoint。若要从 checkpoint 继续，请派生一个新的 layer。
- 提交子 layer 不会将其更改合并到父 layer 中。
- 删除 layer 在逻辑上表示将其废弃，但如果后代 layer 仍依赖它，则这些后代 layer 引用的历史可能仍然可用。
- 在公测期间，涉及对 layer 创建的文件或继承元信息进行重复更改的复杂历史，可能存在一些限制。

有关命令语法、（命令行）标记/参数和输出字段，请参见 [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md)。