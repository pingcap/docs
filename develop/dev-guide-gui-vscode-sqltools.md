---
title: 使用 Visual Studio Code 连接 TiDB
summary: 学习如何使用 Visual Studio Code 或 GitHub Codespaces 连接到 TiDB。
---

# 使用 Visual Studio Code 连接 TiDB

TiDB 是一个与 MySQL 兼容的数据库，[Visual Studio Code (VS Code)](https://code.visualstudio.com/) 是一个轻量但功能强大的源代码编辑器。本教程使用支持 TiDB 的 [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) 扩展，该扩展作为 [官方驱动](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 支持 TiDB。

在本教程中，你可以学习如何使用 Visual Studio Code 连接到你的 TiDB 集群。

> **注意：**
>
> - 本教程兼容 {{{ .starter }}}、TiDB Cloud Dedicated 和 TiDB Self-Managed。
> - 本教程也适用于 Visual Studio Code Remote Development 环境，例如 [GitHub Codespaces](https://github.com/features/codespaces)、[Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) 和 [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl)。

## 前提条件

完成本教程，你需要：

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0** 或更高版本。
- 为 Visual Studio Code 安装 [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 扩展。你可以通过以下任一方法安装：
    - 点击 <a href="vscode:extension/mtxr.sqltools-driver-mysql">此链接</a> 直接在 VS Code 中启动并安装扩展。
    - 访问 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 并点击 **Install**。
    - 在 VS Code 的 **Extensions** 选项卡中搜索 `mtxr.sqltools-driver-mysql`，找到 **SQLTools MySQL/MariaDB/TiDB** 扩展并点击 **Install**。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) 来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）参考 [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) 创建你自己的 TiDB Cloud 集群。
- 参考 [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) 或 [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) 来创建本地集群。

</CustomContent>

## 连接到 TiDB

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示连接对话框。

3. 确认连接对话框中的配置与操作环境匹配。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `VS Code`。
    - **Operating System** 与你的环境一致。

    > **Tip:**
    >
    > 如果你的 VS Code 在远程开发环境中运行，从列表中选择远程操作系统。例如，如果你使用 Windows Subsystem for Linux (WSL)，切换到对应的 Linux 发行版。如果你使用 GitHub Codespaces，则不需要此操作。

4. 点击 **Generate Password** 生成随机密码。

    > **Tip:**
    >
    > 如果之前创建过密码，可以使用原有密码，也可以点击 **Reset Password** 生成新密码。

5. 启动 VS Code，在导航栏中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分，点击 **Add New Connection**，选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. 在设置面板中，配置以下连接参数：

    - **Connection name**：为此连接命名。
    - **Connection group**：（可选）为此连接组命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Database**：输入你要连接的数据库。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Enabled**。 {{{ .starter }}} 需要安全连接。在 **SSL Options (node.TLSSocket)** 区域，配置 **Certificate Authority (CA) Certificate File** 字段为 TiDB Cloud 连接对话框中的 `CA` 参数。

            > **Note:**
            >
            > 如果你在 Windows 或 GitHub Codespaces 上运行，可以留空 **SSL**。默认情况下，SQLTools 信任由 Let's Encrypt 认证的知名 CA。更多信息请参见 [{{{ .starter }}} root certificate management](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)。

    ![VS Code SQLTools: configure connection settings for {{{ .starter }}}](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. 点击 **TEST CONNECTION** 以验证是否成功连接到 {{{ .starter }}} 集群。

    1. 在弹出窗口中，点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入你在步骤 4 中创建的密码。

        ![VS Code SQLTools: enter password to connect to {{{ .starter }}}](/media/develop/vsc-sqltools-password.jpg)

8. 如果连接测试成功，你会看到 **Successfully connected!** 提示。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击 **Configure IP Access List** 或按照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 的步骤进行配置，然后再进行首次连接。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息请参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 VS Code，在导航栏中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分，点击 **Add New Connection**，选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. 在设置面板中，配置以下连接参数：

    - **Connection name**：为此连接命名。
    - **Connection group**：（可选）为此连接组命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入 TiDB Cloud 连接对话框中的 `host` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `port` 参数。
    - **Database**：输入你要连接的数据库。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `user` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools: configure connection settings for TiDB Cloud Dedicated](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. 点击 **TEST CONNECTION** 以验证是否成功连接到 TiDB Cloud Dedicated 集群。

    1. 在弹出窗口中，点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入 TiDB Cloud Dedicated 集群的密码。

    ![VS Code SQLTools: enter password to connect to TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7. 如果连接测试成功，你会看到 **Successfully connected!** 提示。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 VS Code，在导航栏中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分，点击 **Add New Connection**，选择 **TiDB** 作为数据库驱动。

    ![VS Code SQLTools: add new connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. 在设置面板中，配置以下连接参数：

    - **Connection name**：为此连接命名。
    - **Connection group**：（可选）为此连接组命名。相同组名的连接会被归为一组。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入你的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **Port**：输入你的 TiDB Self-Managed 集群的端口号。
    - **Database**：输入你要连接的数据库。
    - **Username**：输入用于连接你的 TiDB Self-Managed 集群的用户名。
    - **Password mode**：

        - 如果密码为空，选择 **Use empty password**。
        - 否则，选择 **SQLTools Driver Credentials**。

    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools: configure connection settings for TiDB Self-Managed](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. 点击 **TEST CONNECTION** 以验证是否成功连接到 TiDB Self-Managed 集群。

    如果密码不为空，点击弹出窗口中的 **Allow**，然后输入 TiDB Self-Managed 集群的密码。

    ![VS Code SQLTools: enter password to connect to TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4. 如果连接测试成功，你会看到 **Successfully connected!** 提示。点击 **SAVE CONNECTION** 保存连接配置。

</div>
</SimpleTab>

## 后续步骤

- 通过 [Visual Studio Code 的文档](https://code.visualstudio.com/docs) 了解更多使用方法。
- 通过 [SQLTools 的文档](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) 和 [GitHub 仓库](https://github.com/mtxr/vscode-sqltools) 了解更多关于 VS Code SQLTools 扩展的使用。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 中的章节学习 TiDB 应用开发的最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/) 学习，并在考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>