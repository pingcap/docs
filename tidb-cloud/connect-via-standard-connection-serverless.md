---
title: 通过 Public Endpoint 连接 TiDB Cloud Serverless
summary: 了解如何通过 public endpoint 连接到你的 TiDB Cloud Serverless 集群。
---

# 通过 Public Endpoint 连接 TiDB Cloud Serverless

本文介绍如何通过 public endpoint，使用你电脑上的 SQL 客户端连接到 TiDB Cloud Serverless 集群，以及如何禁用 public endpoint。

## 通过 public endpoint 连接

> **Tip:**
>
> 如需了解如何通过 public endpoint 连接到 TiDB Cloud Dedicated 集群，请参见 [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md)。

要通过 public endpoint 连接到 TiDB Cloud Serverless 集群，请按照以下步骤操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 在对话框中，保持连接类型的默认设置为 `Public`，并选择你偏好的连接方式和操作系统，以获取对应的连接字符串。

    > **Note:**
    >
    > - 保持连接类型为 `Public`，表示通过标准 TLS 连接进行连接。更多信息，请参见 [TLS Connection to TiDB Cloud Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    > - 如果你在 **Connection Type** 下拉列表中选择 **Private Endpoint**，则表示通过私有 endpoint 进行连接。更多信息，请参见 [Connect to TiDB Cloud Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

4. TiDB Cloud Serverless 支持为你的集群创建 [branches](/tidb-cloud/branch-overview.md)。创建 branch 后，你可以通过 **Branch** 下拉列表选择连接到指定 branch。`main` 代表集群本身。

5. 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。生成的密码只会显示一次，请妥善保存。

6. 使用连接字符串连接到你的集群。

    > **Note:**
    >
    > 连接到 TiDB Cloud Serverless 集群时，必须在用户名中包含集群的前缀，并用引号包裹用户名。更多信息，请参见 [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。
    > 你的客户端 IP 必须在集群 public endpoint 的允许 IP 规则中。更多信息，请参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 禁用 public endpoint

如果你不需要使用 TiDB Cloud Serverless 集群的 public endpoint，可以将其禁用，以防止来自互联网的连接：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Disable**。此时会弹出确认对话框。

4. 在确认对话框中点击 **Disable**。

禁用 public endpoint 后，连接对话框的 **Connection Type** 下拉列表中的 `Public` 选项会被禁用。如果用户仍尝试通过 public endpoint 访问集群，将会收到错误提示。

> **Note:**
>
> 禁用 public endpoint 不会影响已有的连接，只会阻止新的互联网连接。

你可以在禁用后重新启用 public endpoint：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Enable**。

## 后续操作

成功连接到 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。