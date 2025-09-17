---
title: 使用 Visual Studio Code 连接 TiDB
summary: 学习如何使用 Visual Studio Code 或 GitHub Codespaces 连接 TiDB。
---

# 使用 Visual Studio Code 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[Visual Studio Code (VS Code)](https://code.visualstudio.com/) 是一款轻量级但功能强大的源代码编辑器。本教程使用了 [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) 扩展，该扩展将 TiDB 作为[官方驱动](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)支持。

在本教程中，你可以学习如何使用 Visual Studio Code 连接到你的 TiDB 集群。

> **注意：**
>
> - 本教程兼容 {}、{}、TiDB Cloud Dedicated 集群和自托管 TiDB。
> - 本教程同样适用于 Visual Studio Code 远程开发环境，如 [GitHub Codespaces](https://github.com/features/codespaces)、[Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) 和 [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl)。

## 前置条件

完成本教程，你需要：

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0** 或更高版本。
- Visual Studio Code 的 [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 扩展。你可以通过以下任一方式安装：
    - 点击 <a href="vscode:extension/mtxr.sqltools-driver-mysql">此链接</a> 启动 VS Code 并直接安装扩展。
    - 访问 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 并点击 **Install**。
    - 在 VS Code 的 **Extensions** 标签页中，搜索 `mtxr.sqltools-driver-mysql` 获取 **SQLTools MySQL/MariaDB/TiDB** 扩展，然后点击 **Install**。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或[部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参照[创建 {} 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或[部署生产环境 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 创建本地集群。

</CustomContent>

## 连接 TiDB

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{} 或 Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**。会弹出连接对话框。

3. 确保连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `VS Code`。
    - **Operating System** 与你的环境一致。

    > **提示：**
    >
    > 如果你的 VS Code 运行在远程开发环境中，请从列表中选择远程操作系统。例如，如果你使用 Windows Subsystem for Linux (WSL)，请切换到对应的 Linux 发行版。如果你使用 GitHub Codespaces，则无需此操作。

4. 点击 **Generate Password** 生成一个随机密码。

    > **提示：**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 启动 VS Code，在导航栏选择 **SQLTools** 扩展。在 **CONNECTIONS** 区域，点击 **Add New Connection**，并选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. 在设置面板中，配置以下连接参数：

    - **Connection name**：为该连接命名，便于识别。
    - **Connection group**：（可选）为该组连接命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：填写 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：填写 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Database**：填写你要连接的数据库名。
    - **Username**：填写 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Enabled**。{} 要求安全连接。在 **SSL Options (node.TLSSocket)** 区域，将 **Certificate Authority (CA) Certificate File** 字段配置为 TiDB Cloud 连接对话框中的 `CA` 参数。

            > **注意：**
            >
            > 如果你在 Windows 或 GitHub Codespaces 上运行，可以将 **SSL** 留空。SQLTools 默认信任 Let's Encrypt 提供的知名 CA。更多信息参见 [{} 根证书管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)。

    ![VS Code SQLTools: configure connection settings for {}](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. 点击 **TEST CONNECTION** 验证与 {} 集群的连接。

    1. 在弹窗中点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入你在第 4 步创建的密码。

        ![VS Code SQLTools: enter password to connect to {}](/media/develop/vsc-sqltools-password.jpg)

8. 如果连接测试成功，你会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**。会弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List** 或参照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行首次连接前的配置。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 VS Code，在导航栏选择 **SQLTools** 扩展。在 **CONNECTIONS** 区域，点击 **Add New Connection**，并选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. 在设置面板中，配置以下连接参数：

    - **Connection name**：为该连接命名，便于识别。
    - **Connection group**：（可选）为该组连接命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：填写 TiDB Cloud 连接对话框中的 `host` 参数。
    - **Port**：填写 TiDB Cloud 连接对话框中的 `port` 参数。
    - **Database**：填写你要连接的数据库名。
    - **Username**：填写 TiDB Cloud 连接对话框中的 `user` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. 点击 **TEST CONNECTION** 验证与 TiDB Cloud Dedicated 集群的连接。

    1. 在弹窗中点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入 TiDB Cloud Dedicated 集群的密码。

    ![VS Code SQLTools: enter password to connect to TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7. 如果连接测试成功，你会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB 自托管">

1. 启动 VS Code，在导航栏选择 **SQLTools** 扩展。在 **CONNECTIONS** 区域，点击 **Add New Connection**，并选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. 在设置面板中，配置以下连接参数：

    - **Connection name**：为该连接命名，便于识别。
    - **Connection group**：（可选）为该组连接命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：填写你的 TiDB 自托管集群的 IP 地址或域名。
    - **Port**：填写你的 TiDB 自托管集群的端口号。
    - **Database**：填写你要连接的数据库名。
    - **Username**：填写连接 TiDB 自托管集群所用的用户名。
    - **Password mode**：

        - 如果密码为空，选择 **Use empty password**。
        - 否则，选择 **SQLTools Driver Credentials**。

    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Managed](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. 点击 **TEST CONNECTION** 验证与 TiDB 自托管集群的连接。

    如果密码不为空，在弹窗中点击 **Allow**，然后输入 TiDB 自托管集群的密码。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4. 如果连接测试成功，你会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
</SimpleTab>

## 后续步骤

- 通过 [Visual Studio Code 官方文档](https://code.visualstudio.com/docs) 学习更多 VS Code 的用法。
- 通过 [SQLTools 扩展文档](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) 和 [GitHub 仓库](https://github.com/mtxr/vscode-sqltools) 学习更多 VS Code SQLTools 扩展的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>