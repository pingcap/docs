---
title: 使用 DBeaver 连接 TiDB
summary: 学习如何使用 DBeaver Community 连接 TiDB。
---

# 使用 DBeaver 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[DBeaver Community](https://dbeaver.io/download/) 是一款免费且跨平台的数据库工具，适用于开发者、数据库管理员、分析师以及所有与数据打交道的人员。

在本教程中，你可以学习如何使用 DBeaver Community 连接你的 TiDB 集群。

> **Note:**
>
> 本教程兼容 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- [DBeaver Community **23.0.3** 或更高版本](https://dbeaver.io/download/)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 来创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 连接到 TiDB

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示连接对话框。

3. 确认连接对话框中的配置与您的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `DBeaver`
    - **Operating System** 与你的环境匹配。

4. 点击 **Generate Password** 以生成随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以使用原有密码，或者点击 **Reset Password** 生成新密码。

5. 启动 DBeaver，点击左上角的 **New Database Connection**。在 **Connect to a database** 对话框中，从列表中选择 **TiDB**，然后点击 **Next**。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

6. 从 TiDB Cloud 连接对话框中复制连接字符串。在 DBeaver 中，将 **Connect by** 设为 **URL**，并将连接字符串粘贴到 **URL** 字段中。

7. 在 **Authentication (Database Native)** 部分，输入你的 **Username** 和 **Password**。示例如下：

    ![Configure connection settings for {{{ .starter }}}](/media/develop/dbeaver-connection-settings-serverless.jpg)

8. 点击 **Test Connection**，验证是否成功连接到 {{{ .starter }}} 集群。

    如果显示 **Download driver files** 对话框，点击 **Download** 下载驱动文件。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，会显示如下 **Connection test** 对话框。点击 **OK** 关闭。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

9. 点击 **Finish** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，可以点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再进行首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 DBeaver，点击左上角的 **New Database Connection**。在 **Connect to a database** 对话框中，从列表中选择 **TiDB**，然后点击 **Next**。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

5. 将适用的连接字符串复制粘贴到 DBeaver 连接面板中。DBeaver 字段与 TiDB Cloud Dedicated 连接字符串的对应关系如下：

    | DBeaver 字段 | TiDB Cloud Dedicated 连接字符串 |
    |---------------|------------------------------|
    | Server Host   | `{host}`                     |
    | Port          | `{port}`                     |
    | Username      | `{user}`                     |
    | Password      | `{password}`                 |

    示例如下：

    ![Configure connection settings for TiDB Cloud Dedicated](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6. 点击 **Test Connection**，验证是否成功连接到 TiDB Cloud Dedicated 集群。

    如果显示 **Download driver files** 对话框，点击 **Download** 下载驱动文件。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，会显示如下 **Connection test** 对话框。点击 **OK** 关闭。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

7. 点击 **Finish** 保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 DBeaver，点击左上角的 **New Database Connection**。在 **Connect to a database** 对话框中，从列表中选择 **TiDB**，然后点击 **Next**。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

2. 配置以下连接参数：

    - **Server Host**：你的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **Port**：你的 TiDB Self-Managed 集群的端口号。
    - **Username**：用于连接你的 TiDB Self-Managed 集群的用户名。
    - **Password**：该用户名的密码。

    示例如下：

    ![Configure connection settings for TiDB Self-Managed](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3. 点击 **Test Connection**，验证是否成功连接到 TiDB Self-Managed 集群。

    如果显示 **Download driver files** 对话框，点击 **Download** 下载驱动文件。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，会显示如下 **Connection test** 对话框。点击 **OK** 关闭。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

4. 点击 **Finish** 保存连接配置。

</div>
</SimpleTab>

## 后续步骤

- 通过 [DBeaver 的文档](https://github.com/dbeaver/dbeaver/wiki) 了解更多 DBeaver 的用法。
- 参考 [开发者指南](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>