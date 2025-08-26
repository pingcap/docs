---
title: 使用 MySQL Workbench 连接 TiDB
summary: 学习如何使用 MySQL Workbench 连接 TiDB。
---

# 使用 MySQL Workbench 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[MySQL Workbench](https://www.mysql.com/products/workbench/) 是为 MySQL 数据库用户提供的图形化工具集。

> **Warning:**
>
> - 虽然你可以因为 TiDB 的 MySQL 兼容性而使用 MySQL Workbench 连接 TiDB，但 MySQL Workbench 并不完全支持 TiDB。在使用过程中可能会遇到一些问题，因为它会将 TiDB 视为 MySQL。
> - 推荐使用官方支持 TiDB 的其他 GUI 工具，例如 [DataGrip](/develop/dev-guide-gui-datagrip.md)、[DBeaver](/develop/dev-guide-gui-dbeaver.md) 和 [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)。完整支持 TiDB 的 GUI 工具列表请参见 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md#gui)。

本教程将指导你如何使用 MySQL Workbench 连接到你的 TiDB 集群。

> **Note:**
>
> 本教程兼容 {{{ .starter }}}, {{{ .essential }}}, TiDB Cloud Dedicated 以及 TiDB 自建集群。

## 前提条件

完成本教程，你需要：

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** 或更高版本。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）按照 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 按照 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）按照 [创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 按照 [部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 连接 TiDB

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}} 或 Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `MySQL Workbench`。
    - **Operating System** 与你的环境一致。

4. 点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或者点击 **Reset Password** 生成新密码。

5. 启动 MySQL Workbench，点击 **MySQL Connections** 标题旁的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接起一个有意义的名称。
    - **Hostname**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...** 或 **Store in Vault**，输入 {{{ .starter }}} 集群的密码，然后点击 **OK** 存储密码。

        ![MySQL Workbench: store the password of {{{ .starter }}} in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    下图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for {{{ .starter }}}](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. 点击 **Test Connection** 验证与 {{{ .starter }}} 集群的连接。

8. 如果连接测试成功，你会看到 **Successfully made the MySQL connection** 消息。点击 **OK** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List** 或按照 [配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置后再首次连接。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 MySQL Workbench，点击 **MySQL Connections** 标题旁的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接起一个有意义的名称。
    - **Hostname**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...**，输入 TiDB Cloud Dedicated 集群的密码，然后点击 **OK** 存储密码。

        ![MySQL Workbench: store the password of TiDB Cloud Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    下图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Cloud Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. 点击 **Test Connection** 验证与 TiDB Cloud Dedicated 集群的连接。

7. 如果连接测试成功，你会看到 **Successfully made the MySQL connection** 消息。点击 **OK** 保存连接配置。

</div>
<div label="TiDB 自建集群">

1. 启动 MySQL Workbench，点击 **MySQL Connections** 标题旁的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接起一个有意义的名称。
    - **Hostname**：输入你的 TiDB 自建集群的 IP 地址或域名。
    - **Port**：输入你的 TiDB 自建集群的端口号。
    - **Username**：输入用于连接 TiDB 的用户名。
    - **Password**：点击 **Store in Keychain ...**，输入用于连接 TiDB 集群的密码，然后点击 **OK** 存储密码。

        ![MySQL Workbench: store the password of TiDB Self-Managed in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    下图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Self-Managed](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. 点击 **Test Connection** 验证与 TiDB 自建集群的连接。

4. 如果连接测试成功，你会看到 **Successfully made the MySQL connection** 消息。点击 **OK** 保存连接配置。

</div>
</SimpleTab>

## 常见问题

### 如何处理连接超时错误 "Error Code: 2013. Lost connection to MySQL server during query"？

该错误表示查询执行时间超过了超时时间限制。你可以通过以下步骤调整超时设置来解决此问题：

1. 启动 MySQL Workbench，进入 **Workbench Preferences** 页面。
2. 在 **SQL Editor** > **MySQL Session** 部分，配置 **DBMS connection read timeout interval (in seconds)** 选项。该选项设置了查询最大允许执行时间（秒），超时后 MySQL Workbench 会断开与服务器的连接。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

更多信息请参见 [MySQL Workbench 常见问题](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)。

## 后续步骤

- 通过 [MySQL Workbench 官方文档](https://dev.mysql.com/doc/workbench/en/) 了解更多 MySQL Workbench 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>