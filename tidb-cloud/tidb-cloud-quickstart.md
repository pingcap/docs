---
title: TiDB Cloud 快速入门
summary: 快速注册体验 TiDB Cloud 并创建一个 {{{ .starter }}} 实例。
category: quick start
---

# TiDB Cloud 快速入门

*预计完成时间：20 分钟*

本教程将指导你以简单的方式快速上手 TiDB Cloud。

此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上体验 TiDB 的功能。

## 第 1 步：创建一个 {{{ .starter }}} 实例 {#step-1-create-a-starter-instance}

[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 是开始使用 TiDB Cloud 的最佳方式。要创建一个 {{{ .starter }}} 实例，请按照以下步骤操作：

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册。

    你可以使用邮箱和密码注册，并通过 TiDB Cloud 管理密码；也可以选择使用 Google、GitHub 或 Microsoft 账号登录，通过单点登录（SSO）使用 TiDB Cloud。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

    默认会显示 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

3. 对于新注册用户，TiDB Cloud 会自动为你创建一个默认的 {{{ .starter }}} 实例，名称为 `Instance0`。

    - 若要立即使用这个默认的 {{{ .starter }}} 实例体验 TiDB Cloud 功能，请继续阅读[第 2 步：体验 AI 辅助 SQL 编辑器](#step-2-try-ai-assisted-sql-editor)。
    - 若要自行创建一个新的 {{{ .starter }}} 实例，请按照以下步骤操作：

        1. 点击 **Create Resource**。
        2. 在 **Create Resource** 页面，默认已选择 **Starter**。输入 {{{ .starter }}} 实例名称，选择云服务提供商和目标区域，然后点击 **Create**。大约 30 秒后即可创建完成。

        <CustomContent language="en,zh">

        > **注意**
        >
        > 当前，{{{ .starter }}} 在 AWS 上已正式发布，在阿里云上处于公测阶段。本文档后续步骤以 AWS 为例。

        </CustomContent>

        <CustomContent language="ja">

        > **注意**
        >
        > 当前，{{{ .starter }}} 在 AWS 上已正式发布。本文档后续步骤以 AWS 为例。

        </CustomContent>

## 第 1 步：创建 TiDB 集群

[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 是体验 TiDB Cloud 的最佳方式。要创建 TiDB Cloud Starter 集群，请按照以下步骤操作：

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册。

    你可以使用邮箱和密码注册并由 TiDB Cloud 管理密码，或者选择使用 Google、GitHub 或 Microsoft 账号进行单点登录（SSO）到 TiDB Cloud。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

    默认会显示 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

3. 对于新注册用户，TiDB Cloud 会自动为你创建一个名为 `Cluster0` 的默认 TiDB Cloud Starter 集群。

    - 如果你想立即使用该默认集群体验 TiDB Cloud 的功能，请继续阅读 [第 2 步：体验 AI 辅助 SQL 编辑器](#step-2-try-ai-assisted-sql-editor)。
    - 如果你想自行创建新的 TiDB Cloud Starter 集群，请按照以下步骤操作：

        1. 点击 **Create Cluster**。
        2. 在 **Create Cluster** 页面，**Starter** 会被默认选中。选择你的集群所需的云服务商和目标区域，如有需要可修改默认集群名称，然后点击 **Create**。你的 TiDB Cloud Starter 集群将在大约 30 秒内创建完成。

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

## 第 3 步：体验控制台引导式教程

TiDB Cloud 提供了交互式教程和精心设计的示例数据集，帮助你快速上手 TiDB Cloud。对于托管在 AWS 上的 TiDB Cloud Starter 实例，你可以通过该教程学习如何使用 TiDB Cloud 进行高性能数据分析。

1. 点击控制台右下角的 **?** 图标，选择 **Guided tour of SQL Editor**。
2. 选择你想用于教程的 TiDB Cloud Starter 实例，点击 **Import Dataset**。导入过程大约需要 1 分钟。
3. 示例数据导入完成后，按照页面提示完成教程。

## 后续操作

- 了解如何通过不同方式连接到你的 {{{ .starter }}} 实例，请参见 [Connect to a {{{ .starter }}} or Essential instance](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。
- 了解如何使用 SQL Editor 和 Chat2Query 探索你的数据，请参见 [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md)。
- 了解 TiDB SQL 的使用方法，请参见 [Explore SQL with TiDB](/basic-sql-operations.md)。
- 若需生产环境使用，享受跨可用区高可用、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 等优势，请参见 [Create a TiDB Cloud Dedicated cluster](/tidb-cloud/create-tidb-cluster.md)。
