---
title: TiDB Cloud 快速入门
summary: 快速注册体验 TiDB Cloud 并创建你的 TiDB 集群。
category: quick start
---

# TiDB Cloud 快速入门

*预计完成时间：20 分钟*

本教程将引导你以简单的方式快速上手 TiDB Cloud。

此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上体验 TiDB 的功能。

## 第 1 步：创建 TiDB 集群

[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)（现称为 Starter）是体验 TiDB Cloud 的最佳方式。要创建 TiDB Cloud Starter 集群，请按照以下步骤操作：

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册。

    你可以使用邮箱和密码注册并由 TiDB Cloud 管理密码，或者选择使用 Google、GitHub 或 Microsoft 账号进行单点登录（SSO）到 TiDB Cloud。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

    默认会显示 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

3. 对于新注册用户，TiDB Cloud 会自动为你创建一个名为 `Cluster0` 的默认 TiDB Cloud Starter 集群。

    - 如果你想立即使用该默认集群体验 TiDB Cloud 的功能，请继续查看 [第 2 步：体验 AI 辅助 SQL 编辑器](#step-2-try-ai-assisted-sql-editor)。
    - 如果你想自行创建新的 TiDB Cloud Starter 集群，请按照以下步骤操作：

        1. 点击 **Create Cluster**。
        2. 在 **Create Cluster** 页面，**Starter** 会被默认选中。选择你的集群的云服务商和目标区域，如有需要可修改默认集群名称，然后点击 **Create**。你的 TiDB Cloud Starter 集群将在大约 30 秒内创建完成。

        <CustomContent language="en,zh">

        > **注意**
        >
        > 目前，TiDB Cloud Starter 已在 AWS 上正式开放，在阿里云上为公测版。本文档后续步骤以 AWS 为例。

        </CustomContent>

        <CustomContent language="ja">

        > **注意**
        >
        > 目前，TiDB Cloud Starter 已在 AWS 上正式开放。本文档后续步骤以 AWS 为例。

        </CustomContent>

## 第 2 步：体验 AI 辅助 SQL 编辑器

对于托管在 AWS 上的 TiDB Cloud Starter 集群，你可以在 TiDB Cloud 控制台中使用内置的 AI 辅助 SQL 编辑器，最大化数据价值。你无需本地 SQL 客户端即可对数据库运行 SQL 查询，并可直观地在表格或图表中查看查询结果，轻松查看查询日志。

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击某个集群名称进入其概览页面，然后在左侧导航栏点击 **SQL Editor**。

2. 若要体验 TiDB Cloud 的 AI 能力，请按照屏幕提示允许 PingCAP 和 AWS Bedrock 使用你的代码片段进行研究和服务改进，然后点击 **Save and Get Started**。

3. 在 SQL Editor 中，按下 <kbd>⌘</kbd> + <kbd>I</kbd>（macOS）或 <kbd>Control</kbd> + <kbd>I</kbd>（Windows 或 Linux），即可指示 [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询。

    例如，若要创建一个包含两列（`id` 和 `name`）的新表 `test.t`，你可以输入 `use test;` 指定数据库，按下 <kbd>⌘</kbd> + <kbd>I</kbd>，输入 `create a new table t with id and name` 作为指令，然后按 **Enter**，让 AI 自动生成相应的 SQL 语句。

    对于生成的语句，你可以点击 **Accept** 接受并根据需要进一步编辑，或点击 **Discard** 拒绝。

    > **注意：**
    >
    > AI 生成的 SQL 查询并非 100% 准确，可能仍需进一步调整。

4. 运行 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一个查询，按下 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 执行。

    - 如果编辑器中有多个查询，使用光标选中目标查询的行，然后按 **⌘ + Enter** 或点击 **Run** 顺序执行它们。

    - 若要顺序执行编辑器中的所有查询，按 **⇧ + ⌘ + Enter**，或用光标选中所有查询的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一个查询，按下 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 执行。

    - 如果编辑器中有多个查询，使用光标选中目标查询的行，然后按 **Ctrl + Enter** 或点击 **Run** 顺序执行它们。

    - 若要顺序执行编辑器中的所有查询，按 **Shift + Ctrl + Enter**，或用光标选中所有查询的行后点击 **Run**。

    </div>
    </SimpleTab>

运行查询后，你可以在页面底部立即看到查询日志和结果。

如需让 AI 生成更多 SQL 语句，你可以输入更多指令，如下例所示：

```sql
use test;

-- create a new table t with id and name 
CREATE TABLE
  `t` (`id` INT, `name` VARCHAR(255));

-- add 3 rows 
INSERT INTO
  `t` (`id`, `name`)
VALUES
  (1, 'row1'),
  (2, 'row2'),
  (3, 'row3');

-- query all
SELECT
  `id`,
  `name`
FROM
  `t`;
```

## 第 3 步：体验控制台引导式教程

TiDB Cloud 提供了交互式教程和精心设计的示例数据集，帮助你快速上手 TiDB Cloud。对于托管在 AWS 上的 TiDB Cloud Starter 集群，你可以通过该教程学习如何使用 TiDB Cloud 进行高性能数据分析。

1. 点击控制台右下角的 **?** 图标，选择 **Guided tour of SQL Editor**。
2. 选择你想用于体验的 TiDB Cloud Starter 集群，点击 **Import Dataset**。导入过程大约需要 1 分钟。
3. 示例数据导入完成后，按照屏幕提示完成教程。

## 后续操作

- 了解如何通过不同方式连接到你的集群，请参见 [连接到 TiDB Cloud Starter 或 Essential 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。
- 获取更多关于如何使用 SQL Editor 和 Chat2Query 探索数据的信息，请参见 [使用 AI 辅助 SQL 编辑器探索数据](/tidb-cloud/explore-data-with-chat2query.md)。
- 了解 TiDB SQL 的用法，请参见 [使用 TiDB 探索 SQL](/basic-sql-operations.md)。
- 若需生产环境使用，享受跨可用区高可用、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 等优势，请参见 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。