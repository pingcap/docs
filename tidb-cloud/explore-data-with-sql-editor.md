---
title: 使用 SQL Editor (PREVIEW) 探索你的数据
summary: 了解如何在 TiDB Cloud 控制台中使用 SQL Editor 编写和运行 SQL 查询、管理 SQL 文件以及查看查询结果。
aliases: ['/zh/tidbcloud/explore-data-with-chat2query','/zh/tidbcloud/use-chat2query-api','/zh/tidbcloud/use-chat2query-knowledge','/zh/tidbcloud/use-chat2query-sessions']
---

# 使用 SQL Editor (PREVIEW) 探索你的数据

你可以使用 [TiDB Cloud 控制台](https://tidbcloud.com/)内置的 SQL Editor，最大化挖掘数据价值。

在 SQL Editor 中，你无需本地 SQL 客户端即可针对数据库编写和运行 SQL 查询。你可以直观地以表格或图表形式查看查询结果，并轻松检查查询日志。

## 使用场景 {#use-cases}

SQL Editor 的推荐使用场景如下：

- 快速测试 TiDB 的 MySQL 兼容性。
- 使用你自己的数据集轻松探索 TiDB 中的 SQL 功能。

## 限制 {#limitations}

- SQL Editor 目前处于公测阶段，可以在 AWS 上的 [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) 实例上使用。如需在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 SQL Editor，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 访问 SQL Editor {#access-sql-editor}

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 点击你的 {{{ .starter }}} 实例或 TiDB Cloud Dedicated 集群名称，然后在左侧导航栏中点击 **SQL Editor**。

    > **Note:**
    >
    > 在以下情况下，**SQL Editor** 入口会显示为灰色且不可点击。
    >
    > - 你的 TiDB Cloud Dedicated 集群版本早于 v6.5.0。要使用 SQL Editor，你需要联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 升级集群。
    > - 你的 TiDB Cloud Dedicated 集群刚刚创建，SQL Editor 的运行环境仍在准备中。在这种情况下，请等待几分钟，SQL Editor 即可使用。
    > - 你的 TiDB Cloud Dedicated 集群已[暂停](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 编写并运行 SQL 查询 {#write-and-run-sql-queries}

在 SQL Editor 中，你可以使用自己的数据集编写并运行 SQL 查询。

1. 编写 SQL 查询。

2. 运行 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一条查询，要运行它，请按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run**。

    - 如果编辑器中有多条查询，要按顺序运行其中一条或多条，请用光标选中目标查询所在的行，然后按 **⌘ + Enter** 或点击 **Run**。

    - 要按顺序运行编辑器中的所有查询，请按 **⇧ + ⌘ + Enter**，或用光标选中所有查询所在的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一条查询，要运行它，请按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run**。

    - 如果编辑器中有多条查询，要按顺序运行其中一条或多条，请用光标选中目标查询所在的行，然后按 **Ctrl + Enter** 或点击 **Run**。

    - 要按顺序运行编辑器中的所有查询，请按 **Shift + Ctrl + Enter**，或用光标选中所有查询所在的行后点击 **Run**。

    </div>
    </SimpleTab>

运行查询后，你可以立即在页面底部看到查询日志和结果。

> **Note:**
>
> 返回结果的大小限制为 8 MiB。

## 管理 SQL 文件 {#manage-sql-files}

在 SQL Editor 中，你可以将 SQL 查询保存到不同的 SQL 文件中，并按如下方式管理 SQL 文件：

- 要添加 SQL 文件，请在 **SQL Files** 选项卡上点击 **+**。
- 要重命名 SQL 文件，请将光标移动到文件名上，点击文件名旁边的 **...**，然后选择 **Rename**。
- 要删除 SQL 文件，请将光标移动到文件名上，点击文件名旁边的 **...**，然后选择 **Delete**。请注意，当 **SQL Files** 选项卡上只有一个 SQL 文件时，你无法将其删除。

## 管理 SQL Editor 设置 {#manage-sql-editor-settings}

在 SQL Editor 中，你可以更改以下设置：

- 查询结果中的最大行数
- 是否在 **Schemas** 选项卡上显示系统数据库模式

要更改设置，请执行以下步骤：

1. 在 **SQL Editor** 右上角，点击 **...** 并选择 **Settings**。
2. 根据需要更改设置。
3. 点击 **Save**。