---
title: 使用 Navicat 连接 TiDB
summary: 学习如何使用 Navicat 连接 TiDB。
---

# 使用 Navicat 连接 TiDB

TiDB 是兼容 MySQL 的数据库，[Navicat](https://www.navicat.com) 是一套为数据库用户设计的 GUI 工具。本教程将使用 [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) 工具连接 TiDB。

在本教程中，你可以学习如何使用 Navicat 连接到你的 TiDB 集群。

> **注意：**
>
> 本教程兼容 {}、{}、TiDB Cloud Dedicated 集群和自托管 TiDB。

## 前提条件

完成本教程，你需要：

- [Navicat Premium](https://www.navicat.com) **17.1.6** 或更高版本。
- 一个 Navicat Premium 付费账号。
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

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确认连接对话框中的配置与你的操作环境一致。

    - **Connection Type** 设置为 `Public`。
    - **Branch** 设置为 `main`。
    - **Connect With** 设置为 `Navicat`。
    - **Operating System** 与你的环境一致。

4. 点击 **Generate Password** 生成一个随机密码。

    > **提示：**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或点击 **Reset Password** 生成新密码。

5. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 列表中选择 **PingCAP**，在右侧面板双击 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接命名，便于识别。
    - **Host**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **User Name**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：输入 {} 集群的密码。

    ![Navicat: configure connection general panel for {}](/media/develop/navicat-premium-connection-config-serverless-general.png)

7. 点击 **SSL** 标签页，勾选 **Use SSL**、**Use authentication** 和 **Verify server certificate against CA** 复选框。然后，将 TiDB Cloud 连接对话框中的 `CA` 文件选择到 **CA Certificate** 字段。

    ![Navicat: configure connection SSL panel for {}](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8. 点击 **Test Connection** 测试与 {} 集群的连接。

9. 如果连接测试成功，你会看到 **Connection Successful** 消息。点击 **OK** 完成连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称，进入集群概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表选择 **Public**。

    如果你还未配置 IP 访问列表，点击 **Configure IP Access List**，或参照 [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) 进行首次连接前的配置。

    除了 **Public** 连接类型，TiDB Cloud Dedicated 集群还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息参见 [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 点击 **CA cert** 下载 CA 证书。

5. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 列表中选择 **PingCAP**，在右侧面板双击 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接命名，便于识别。
    - **Host**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **User Name**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password**：输入 TiDB Cloud Dedicated 集群的密码。

    ![Navicat: configure connection general panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7. 点击 **SSL** 标签页，勾选 **Use SSL**、**Use authentication** 和 **Verify server certificate against CA** 复选框。然后，将第 4 步下载的 CA 文件选择到 **CA Certificate** 字段。

    ![Navicat: configure connection SSL panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8. **Test Connection** 测试与 TiDB Cloud Dedicated 集群的连接。

9. 如果连接测试成功，你会看到 **Connection Successful** 消息。点击 **OK** 完成连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 列表中选择 **PingCAP**，在右侧面板双击 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

2. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接命名，便于识别。
    - **Host**：输入你的自托管 TiDB 集群的 IP 地址或域名。
    - **Port**：输入你的自托管 TiDB 集群的端口号。
    - **User Name**：输入连接 TiDB 所用的用户名。
    - **Password**：输入连接 TiDB 所用的密码。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3. 点击 **Test Connection** 测试与自托管 TiDB 集群的连接。

4. 如果连接测试成功，你会看到 **Connection Successful** 消息。点击 **OK** 完成连接配置。

</div>
</SimpleTab>

## 后续步骤

- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 以及 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
