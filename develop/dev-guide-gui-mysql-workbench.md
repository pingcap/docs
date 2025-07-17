---
title: 使用 MySQL Workbench 连接 TiDB
summary: 学习如何使用 MySQL Workbench 连接 TiDB。
---

# 使用 MySQL Workbench 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[MySQL Workbench](https://www.mysql.com/products/workbench/) 是一款面向 MySQL 数据库用户的图形界面工具集。

> **Warning:**
>
> - 虽然你可以利用 MySQL Workbench 连接到 TiDB，因为其与 MySQL 的兼容性，但 MySQL Workbench 并不完全支持 TiDB。在使用过程中可能会遇到一些问题，因为它将 TiDB 视为 MySQL。
> - 建议使用其他官方支持 TiDB 的图形界面工具，例如 [DataGrip](/develop/dev-guide-gui-datagrip.md)、[DBeaver](/develop/dev-guide-gui-dbeaver.md) 和 [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)。关于完全支持 TiDB 的图形界面工具的完整列表，请参见 [Third-party tools supported by TiDB](/develop/dev-guide-third-party-support.md#gui)。

在本教程中，你可以学习如何使用 MySQL Workbench 连接到你的 TiDB 集群。

> **Note:**
>
> 本教程兼容 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

完成本教程，你需要：

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** 或更高版本。
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

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示一个连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `MySQL Workbench`。
    - **Operating System** 与你的环境匹配。

4. 点击 **Generate Password** 以生成随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以使用原有密码，也可以点击 **Reset Password** 生成新密码。

5. 启动 MySQL Workbench，点击 **+**，在 **MySQL Connections** 标题旁。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为此连接命名，便于识别。
    - **Hostname**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...** 或 **Store in Vault**，输入 {{{ .starter }}} 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of {{{ .starter }}} in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    下面的示意图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for {{{ .starter }}}](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. 点击 **Test Connection**，验证是否能成功连接到 {{{ .starter }}} 集群。

8. 如果连接测试成功，会显示 **Successfully made the MySQL connection** 提示。点击 **OK** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示一个连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问白名单，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再进行首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 MySQL Workbench，点击 **+**，在 **MySQL Connections** 标题旁。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为此连接命名，便于识别。
    - **Hostname**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...**，输入 TiDB Cloud Dedicated 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of TiDB Cloud Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    下面的示意图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Cloud Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. 点击 **Test Connection**，验证是否能成功连接到 TiDB Cloud Dedicated 集群。

7. 如果连接测试成功，会显示 **Successfully made the MySQL connection** 提示。点击 **OK** 保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 MySQL Workbench，点击 **+**，在 **MySQL Connections** 标题旁。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为此连接命名，便于识别。
    - **Hostname**：输入你的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **Port**：输入你的 TiDB Self-Managed 集群的端口号。
    - **Username**：输入用于连接 TiDB 的用户名。
    - **Password**：点击 **Store in Keychain ...**，输入连接 TiDB 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of TiDB Self-Managed in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    下面的示意图展示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Self-Managed](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. 点击 **Test Connection**，验证是否能成功连接到 TiDB Self-Managed 集群。

4. 如果连接测试成功，会显示 **Successfully made the MySQL connection** 提示。点击 **OK** 保存连接配置。

</div>
</SimpleTab>

## 常见问题解答

### 如何处理连接超时错误 "Error Code: 2013. Lost connection to MySQL server during query"？

此错误表示查询执行时间超过了超时限制。你可以通过以下步骤调整超时设置以解决此问题：

1. 启动 MySQL Workbench，进入 **Workbench Preferences** 页面。
2. 在 **SQL Editor** > **MySQL Session** 部分，配置 **DBMS connection read timeout interval (in seconds)** 选项。此设置定义了查询最多可以耗时（以秒为单位），超过此时间后 MySQL Workbench 会断开连接。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

更多信息请参见 [MySQL Workbench frequently asked questions](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)。

## 后续步骤

- 通过 [MySQL Workbench 的文档](https://dev.mysql.com/doc/workbench/en/) 了解更多使用方法。
- 参考 [Developer guide](/develop/dev-guide-overview.md) 中的章节，学习 TiDB 应用开发的最佳实践，例如 [Insert data](/develop/dev-guide-insert-data.md)、[Update data](/develop/dev-guide-update-data.md)、[Delete data](/develop/dev-guide-delete-data.md)、[Single table reading](/develop/dev-guide-get-data-from-single-table.md)、[Transactions](/develop/dev-guide-transaction-overview.md) 和 [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB developer courses](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB certifications](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>