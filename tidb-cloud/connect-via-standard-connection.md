---
title: 通过公共连接接入 TiDB Cloud Dedicated
summary: 了解如何通过公共连接接入你的 TiDB Cloud 集群。
---

# 通过公共连接接入 TiDB Cloud Dedicated

本文档介绍如何通过公共连接接入你的 TiDB Cloud Dedicated 集群。公共连接会暴露一个带有流量过滤器的公共端点，因此你可以通过 SQL 客户端从你的笔记本电脑连接到 TiDB Cloud Dedicated 集群。

> **Tip:**
>
> 如果你想了解如何通过公共连接接入 TiDB Cloud Serverless 集群，请参见 [Connect to TiDB Cloud Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 前置条件：配置 IP 访问列表

对于公共连接，TiDB Cloud Dedicated 只允许来自 IP 访问列表中的地址的客户端连接。如果你还没有配置 IP 访问列表，请按照 [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md) 中的步骤，在首次连接前进行配置。

## 连接到集群

要通过公共连接接入 TiDB Cloud Dedicated 集群，请按照以下步骤操作：

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    如果你还没有配置 IP 访问列表，请点击 **Configure IP Access List**，或按照 [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md) 中的步骤，在首次连接前进行配置。

4. 点击 **CA cert** 下载用于 TLS 连接 TiDB 集群的 CA 证书。该 CA 证书默认支持 TLS 1.2 版本。

5. 选择你偏好的连接方式，然后参考该标签页上的连接字符串和示例代码，连接到你的集群。

## 后续操作

成功连接到 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。