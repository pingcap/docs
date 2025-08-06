---
title: 通过 SQL Shell 连接
summary: 了解如何通过 SQL Shell 连接到你的 TiDB 集群。
---

# 通过 SQL Shell 连接

在 TiDB Cloud SQL Shell 中，你可以尝试 TiDB SQL，快速测试 TiDB 对 MySQL 的兼容性，并管理数据库用户权限。

> **注意：**
>
> 你无法使用 SQL Shell 连接到 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。要连接到你的 TiDB Cloud Serverless 集群，请参阅 [连接到 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。

要使用 SQL shell 连接到你的 TiDB 集群，请按照以下步骤操作：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并导航到你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群的名称，进入该集群的概览页面，然后点击左侧导航栏中的 **Settings** > **Networking**。
3. 在 **Networking** 页面，点击右上角的 **Web SQL Shell**。
4. 在弹出的 **Enter password** 行中，输入当前集群的 root 密码。然后你的应用就会连接到 TiDB 集群。