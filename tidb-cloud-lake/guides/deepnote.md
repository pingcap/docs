---
title: 使用 Deepnote 连接到 TiDB Cloud Lake
summary: Deepnote 让你能够与朋友和同事在同一平台上实时协作，轻松开展数据科学项目，帮助你更快地将想法和分析转化为产品。Deepnote 基于浏览器构建，因此你可以在任何平台（Windows、Mac、Linux 或 Chromebook）上使用它。无需下载，并且每天都会向你推送更新。所有更改都会被即时保存。
---

# 使用 Deepnote 连接到 TiDB Cloud Lake

[Deepnote](https://deepnote.com) 让你能够与朋友和同事在同一平台上实时协作，轻松开展数据科学项目，帮助你更快地将想法和分析转化为产品。Deepnote 基于浏览器构建，因此你可以在任何平台（Windows、Mac、Linux 或 Chromebook）上使用它。无需下载，并且每天都会向你推送更新。所有更改都会被即时保存。

你可以通过 Deepnote 与 ClickHouse 兼容的集成，并使用安全连接，将 Deepnote 连接到 {{{ .lake }}}。

## 教程：与 Deepnote 集成 {#tutorial-integrating-with-deepnote}

本教程将指导你完成将 {{{ .lake }}} 与 Deepnote 集成的过程。

### 步骤 1：设置环境 {#step-1-set-up-environment}

请确保你可以登录到你的 {{{ .lake }}} 账户，并获取某个计算集群 (Warehouse) 的连接信息。更多详情，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

### 步骤 2：连接到 {{{ .lake }}} {#step-2-connect-to-lake}

1. 登录 Deepnote；如果你还没有账户，请先创建一个。

2. 点击左侧边栏中 **INTEGRATIONS** 右侧的 **+**，然后选择 **ClickHouse**。

    ![与 ClickHouse 集成](/media/tidb-cloud-lake/integration-clickhouse.png)

3. 使用你的连接信息填写各个字段。

    | 参数 | 说明 |
    | ---------------- | ---------------------------------- |
    | Integration name | 例如，`TiDB Cloud Lake` |
    | Host name | 从连接信息中获取 |
    | Port | `443` |
    | Username | `cloudapp` |
    | Password | 从连接信息中获取 |

4. 创建一个 notebook。

5. 在 notebook 中，进入 **SQL** 部分，然后选择你之前创建的连接。

现在一切就绪！有关如何使用该工具，请参阅 Deepnote 文档。
