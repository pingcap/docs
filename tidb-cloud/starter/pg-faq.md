---
title: PostgreSQL 兼容的 TiDB Cloud Starter 常见问题
summary: 查找关于 PostgreSQL 兼容的 TiDB Cloud Starter 在公测期间的常见问题解答。
---

# PostgreSQL 兼容的 TiDB Cloud Starter 常见问题

本文档解答了关于 PostgreSQL 兼容的 {{{ .starter }}} 在公测期间的常见问题。

PostgreSQL 兼容的 {{{ .starter }}} 使开发者能够直接在 TiDB Cloud 控制台中创建和管理 PostgreSQL 兼容的数据库实例。它支持实例生命周期中的核心能力，包括连接、监控、备份和恢复，以及 PostgreSQL 生态能力，例如兼容 pgvector 的向量搜索和部分 PostgreSQL 扩展。

在公测期间，PostgreSQL 兼容的 {{{ .starter }}} 可免费使用，但受使用配额限制。预览期间不启用计费。

## 常规常见问题 {#general-faqs}

### 如何创建 PostgreSQL 兼容的 Starter 实例？ {#how-can-i-create-a-postgresql-compatible-starter-instance}

PostgreSQL 兼容的 {{{ .starter }}} 现已进入公测。

要创建实例，请在 TiDB Cloud 控制台中选择 **Starter**，然后选择 **PostgreSQL Compatible** 选项，检查配置后创建实例。

在公测期间，PostgreSQL 兼容性仅适用于 {{{ .starter }}}。{{{ .essential }}} 和 {{{ .premium }}} 当前不支持此选项。

### 当前哪些 Region 支持 PostgreSQL 兼容的 Starter？ {#which-regions-currently-support-postgresql-compatible-starter}

在公测期间，PostgreSQL 兼容的 {{{ .starter }}} 可在以下 Region 使用：

- AWS US East (N. Virginia): `us-east-1`

随着公测范围扩大，后续可能会开放更多 Region。新 Region 的可用性将在准备就绪后公布。

### 我可以在同一个 TiDB Cloud 组织中同时使用 MySQL 兼容和 PostgreSQL 兼容的 Starter 实例吗？ {#can-i-use-both-mysql-compatible-and-postgresql-compatible-starter-instances-in-the-same-tidb-cloud-organization}

可以。你可以在同一个组织、项目和 Region 中同时使用 MySQL 兼容和 PostgreSQL 兼容的 {{{ .starter }}} 实例。

TiDB Cloud 会在资源列表和实例概览中显示数据库类型，以便你区分这两类实例。

### 我可以创建多少个 Starter 实例？ {#how-many-starter-instances-can-i-create}

默认情况下，付费组织总共最多可以创建 **100 个 {{{ .starter }}} 实例**，其中包括 MySQL 兼容和 PostgreSQL 兼容实例。对于 MySQL 兼容实例，每个 branch 也会计为一个实例。

免费实例额度包括：

- 前 **5 个 MySQL 兼容** {{{ .starter }}} 实例。
- 前 **10 个 PostgreSQL 兼容** {{{ .starter }}} 实例。

### 我可以在生产环境中使用 PostgreSQL 兼容的 Starter 吗？ {#can-i-use-postgresql-compatible-starter-in-production}

在公测期间，你可以使用 PostgreSQL 兼容的 {{{ .starter }}} 对开发、测试和类生产负载进行评估。**公测期间不提供服务级别协议（SLA）承诺。**

由于该服务仍处于预览阶段，且部分能力可能仍会持续演进，我们建议在正式发布（GA）之后再将 PostgreSQL 兼容的 {{{ .starter }}} 用于生产负载。

## 功能与操作常见问题 {#features-and-operations-faqs}

### PostgreSQL 兼容的 Starter 当前提供哪些功能？ {#what-features-are-currently-available-in-postgresql-compatible-starter}

PostgreSQL 兼容的 {{{ .starter }}} 包含以下能力：

- **实例管理：** 在 TiDB Cloud 控制台中创建、列出、监控和删除 PostgreSQL 兼容的 {{{ .starter }}} 实例。
- **连接能力：** 通过公共端点，使用 PostgreSQL 兼容的客户端和驱动进行连接。
- **数据导入：** 使用熟悉的 PostgreSQL 工作流导入数据，例如 `psql` 和 `COPY`。
- **备份与恢复：** 使用每日自动备份，并将快照恢复到新的 PostgreSQL 兼容 {{{ .starter }}} 实例。
- **可观测性：** 查看内置指标，包括存储使用量、每秒查询数（QPS）、连接数和查询时长。
- **AI 和向量搜索：** 使用兼容 pgvector 的向量搜索、全文搜索、服务端向量嵌入能力以及部分 PostgreSQL 扩展。

随着 PostgreSQL 兼容的 {{{ .starter }}} 在公测期间持续演进，后续还将推出更多能力。

### 如何连接到 PostgreSQL 兼容的 Starter 实例？ {#how-do-i-connect-to-a-postgresql-compatible-starter-instance}

在 TiDB Cloud 控制台中，打开 PostgreSQL 兼容 {{{ .starter }}} 实例的连接信息，即可查看其公共端点、端口、用户名以及连接示例。

PostgreSQL 兼容的 {{{ .starter }}} 当前不支持私有端点。

### PostgreSQL 兼容的备份可以恢复到 MySQL 兼容实例中吗？ {#can-a-postgresql-compatible-backup-be-restored-into-a-mysql-compatible-instance}

不可以。不支持跨协议恢复。PostgreSQL 兼容的备份只能恢复到 PostgreSQL 兼容的 {{{ .starter }}} 实例中。

### `tidbcloud_com_cell_*` 表是什么？ {#what-are-the-tidbcloud-com-cell-tables}

PostgreSQL 兼容的 {{{ .starter }}} 使用 `public` 数据库模式中的系统管理表来管理数据库用户并安全地处理变更。这些表存储的是服务元信息，而不是应用数据。

- **`tidbcloud_com_cell_principals`：** 跟踪由 TiDB Cloud 管理的数据库用户。
- **`tidbcloud_com_cell_sql_versions`：** 跟踪受管数据库资源的变更，并帮助防止冲突修改。
- **`tidbcloud_com_cell_sql_receipts`：** 记录操作结果，以便安全地处理重试。此表不存储密码。

TiDB Cloud 会自动维护这些表。**请勿修改或删除这些表，也不要使用它们存储应用数据。** 否则可能会干扰受管数据库用户操作。

## 计费与计量常见问题 {#billing-and-metering-faqs}

### 我的使用量是如何计量的？ {#how-is-my-usage-measured}

PostgreSQL 兼容的 {{{ .starter }}} 遵循 TiDB Cloud Starter 的使用模型，计量以下内容：

- **Request Units (RUs)**
- **基于行的存储**

在公测期间，RU 使用量暂不显示，也不会产生计费费用。

### PostgreSQL 兼容的 Starter 在公测期间是免费的吗？ {#is-postgresql-compatible-starter-free-during-public-preview}

是的。PostgreSQL 兼容的 {{{ .starter }}} 在公测期间免费提供，但受使用配额限制。在此期间不启用计费。

对于每个组织中的前 **10 个 PostgreSQL 兼容 {{{ .starter }}} 实例**，每个实例的免费额度为：

- **基于行的存储：** 50 GiB
- **Request Units (RUs)：** 每月 5 亿

如果资源使用量超出免费额度，TiDB Cloud 可能会限制进一步使用或暂停服务。

如果你预计会超出这些额度，或需要更多资源，请联系 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 讨论你的需求。