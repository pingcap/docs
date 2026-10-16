---
title: 开始使用兼容 PostgreSQL 的 TiDB Cloud Starter
summary: 了解如何创建并连接到兼容 PostgreSQL 的 TiDB Cloud Starter 实例。
category: quick start
---

# 开始使用兼容 PostgreSQL 的 TiDB Cloud Starter

本教程将指导你创建并连接到一个兼容 PostgreSQL 的 TiDB Cloud Starter 实例。

> **Note:**
>
> 兼容 PostgreSQL 的 TiDB Cloud Starter 当前处于公测阶段。

此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上体验 TiDB 功能。

## 第 1 步：创建 {{{ .starter }}} 实例 {#step-1-create-a-starter-instance}

按照以下步骤创建 {{{ .starter }}} 实例：

1. 如果你还没有 TiDB Cloud 账户，请点击[这里](https://tidbcloud.com/free-trial)进行注册。

    你可以使用邮箱和密码注册，并通过 TiDB Cloud 管理密码；也可以选择使用 Google、GitHub 或 Microsoft 账户登录，通过单点登录（SSO）访问 TiDB Cloud。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账户。

    默认会显示 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

3. 按照以下步骤创建一个新的兼容 PostgreSQL 的 {{{ .starter }}} 实例：

    1. 点击 **Create Resource**。
    2. 在 **Create Resource** 页面中，选择 **Starter**。
    3. 在 **Compatibility Mode** 部分，选择 **PostgreSQL Compatible**。
    4. 输入 {{{ .starter }}} 实例名称，选择云服务提供商和目标区域，然后点击 **Create**。

    > **Note:**
    >
    > 在公测期间，兼容 PostgreSQL 的 {{{ .starter }}} 实例当前免费提供。
    >
    > 你的组织中的前 10 个兼容 PostgreSQL 的 {{{ .starter }}} 实例可享受免费配额。每个符合条件的实例每月包含以下免费配额：
    >
    > + 50 GiB 行存储
    > + 5 亿 Request Units (RUs)
    >
    > 当兼容 PostgreSQL 的 {{{ .starter }}} 实例达到其免费配额后，超出的资源消耗可能会受到使用限制或导致服务暂停。如果你预计会超出这些额度，请联系 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 讨论你的需求。

## 第 2 步：连接到你的 {{{ .starter }}} 实例 {#step-2-connect-to-your-starter-instance}

兼容 PostgreSQL 的 {{{ .starter }}} 实例支持 PostgreSQL wire 协议，因此你可以使用大多数 PostgreSQL 工具、驱动和 ORM 连接到它们。以下步骤以 PostgreSQL CLI 客户端 `psql` 为例。

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
2. 点击右上角的 **Connect**。系统会显示一个包含连接参数的连接对话框。
3. 确保连接对话框中的设置与你的运行环境匹配。
4. 点击 **Generate Password** 以创建一个随机密码。
5. 在 **Connect With** 下拉列表中，选择 **PostgreSQL CLI**。
6. 复制连接命令，将其粘贴到终端中，然后按 **Enter** 执行。

PostgreSQL CLI 客户端 `psql` 将打开并连接到你的 {{{ .starter }}} 实例。

## 接下来做什么 {#what-s-next}

- 如需了解 PostgreSQL 兼容性，请参见[PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。
- 如需了解 TiDB Cloud 当前支持的 PostgreSQL 扩展，请参见[PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)。