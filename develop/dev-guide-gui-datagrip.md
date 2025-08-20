---
title: 使用 JetBrains DataGrip 连接 TiDB
summary: 学习如何使用 JetBrains DataGrip 连接 TiDB。此教程同样适用于其他 JetBrains IDE（如 IntelliJ、PhpStorm 和 PyCharm）中的 Database Tools and SQL 插件。
---

# 使用 JetBrains DataGrip 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html) 是一款强大的数据库和 SQL 集成开发环境（IDE）。本教程将引导你使用 DataGrip 连接到你的 TiDB 集群。

> **注意：**
>
> 本教程适用于 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

你可以通过以下两种方式使用 DataGrip：

- 作为 [DataGrip IDE](https://www.jetbrains.com/datagrip/download) 独立工具。
- 作为 JetBrains IDE（如 IntelliJ、PhpStorm 和 PyCharm）中的 [Database Tools and SQL 插件](https://www.jetbrains.com/help/idea/relational-databases.html)。

本教程主要以独立 DataGrip IDE 为例。通过 JetBrains IDE 中的 Database Tools and SQL 插件连接 TiDB 的步骤类似。你也可以参考本文档中的步骤，在任何 JetBrains IDE 中连接 TiDB。

## 前置条件

完成本教程，你需要：

- [DataGrip **2023.2.1** 或更高版本](https://www.jetbrains.com/datagrip/download/) 或非社区版 [JetBrains](https://www.jetbrains.com/) IDE。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 连接 TiDB

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `DataGrip`
    - **Operating System** 与你的环境一致

4. 点击 **Generate Password** 生成随机密码。

    > **提示：**
    >
    > 如果你之前已创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 启动 DataGrip 并创建一个项目用于管理你的连接。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6. 在新建的项目中，点击 **Database Explorer** 面板左上角的 **+**，选择 **Data Source** > **Other** > **TiDB**。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7. 从 TiDB Cloud 连接对话框中复制连接字符串，粘贴到 **URL** 字段，其余参数会自动填充。示例如下：

    ![Configure the URL field for {{{ .starter }}}](/media/develop/datagrip-url-paste.jpg)

    如果出现 **Download missing driver files** 警告，点击 **Download** 下载驱动文件。

8. 点击 **Test Connection** 验证与 {{{ .starter }}} 集群的连接。

    ![Test the connection to a {{{ .starter }}} cluster](/media/develop/datagrip-test-connection.jpg)

9. 点击 **OK** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List** 或参考 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行配置后再首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 DataGrip 并创建一个项目用于管理你的连接。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

5. 在新建的项目中，点击 **Database Explorer** 面板左上角的 **+**，选择 **Data Source** > **Other** > **TiDB**。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

6. 将相应的连接字符串复制并粘贴到 DataGrip 的 **Data Source and Drivers** 窗口。DataGrip 字段与 TiDB Cloud Dedicated 连接字符串的对应关系如下：

    | DataGrip field | TiDB Cloud Dedicated connection string |
    | -------------- | ------------------------------- |
    | Host           | `{host}`                        |
    | Port           | `{port}`                        |
    | User           | `{user}`                        |
    | Password       | `{password}`                    |

    示例：

    ![Configure the connection parameters for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-connect.jpg)

7. 点击 **SSH/SSL** 标签页，勾选 **Use SSL**，并在 **CA file** 字段中填写 CA 证书路径。

    ![Configure the CA for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-ssl.jpg)

    如果出现 **Download missing driver files** 警告，点击 **Download** 下载驱动文件。

8. 点击 **Advanced** 标签页，向下滚动找到 **enabledTLSProtocols** 参数，并将其值设置为 `TLSv1.2,TLSv1.3`。

    ![Configure the TLS for TiDB Cloud Dedicated](/media/develop/datagrip-dedicated-advanced.jpg)

9. 点击 **Test Connection** 验证与 TiDB Cloud Dedicated 集群的连接。

    ![Test the connection to a TiDB Cloud Dedicated cluster](/media/develop/datagrip-dedicated-test-connection.jpg)

10. 点击 **OK** 保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 DataGrip 并创建一个项目用于管理你的连接。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

2. 在新建的项目中，点击 **Database Explorer** 面板左上角的 **+**，选择 **Data Source** > **Other** > **TiDB**。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

3. 配置以下连接参数：

    - **Host**：你的 TiDB 自建集群的 IP 地址或域名
    - **Port**：你的 TiDB 自建集群的端口号
    - **User**：用于连接 TiDB 自建集群的用户名
    - **Password**：该用户名的密码

    示例：

    ![Configure the connection parameters for TiDB Self-Managed](/media/develop/datagrip-self-hosted-connect.jpg)

    如果出现 **Download missing driver files** 警告，点击 **Download** 下载驱动文件。

4. 点击 **Test Connection** 验证与 TiDB 自建集群的连接。

    ![Test the connection to a TiDB Self-Managed cluster](/media/develop/datagrip-self-hosted-test-connection.jpg)

5. 点击 **OK** 保存连接配置。

</div>
</SimpleTab>

## 后续步骤

- 通过 [DataGrip 官方文档](https://www.jetbrains.com/help/datagrip/getting-started.html) 了解更多 DataGrip 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
