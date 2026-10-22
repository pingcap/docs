---
title: 通过公共连接接入 TiDB Cloud Dedicated
summary: 了解如何通过公共连接接入你的 TiDB Cloud 集群。
---

# 通过公共连接接入 TiDB Cloud Dedicated

本文档介绍如何通过公共连接接入你的 TiDB Cloud Dedicated 集群。公共连接会暴露一个带有流量过滤器的公共端点，因此你可以通过 SQL 客户端从你的笔记本电脑连接到 TiDB Cloud Dedicated 集群。

> **Tip:**
>
> 如果你想了解如何通过公共连接接入 {{{ .starter }}} 或 {{{ .essential }}} 实例，请参见 [Connect to {{{ .starter }}} or Essential via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)。

## 前置条件 {#prerequisites}

在通过公共连接连接到 TiDB Cloud Dedicated 集群之前，请确保满足以下要求：

- 已为你的集群启用公共端点。对于新创建的 TiDB Cloud Dedicated 集群，公共端点默认处于禁用状态。要启用它，请打开集群的概览页面，点击 **Settings** > **Networking**，如果你的集群有多个节点组，则选择目标 TiDB 节点组，然后在 **Public Endpoint** 部分点击 **Enable**。如果你的集群已启用公共端点，则无需执行任何操作。
- 你的客户端 IP 地址已在 IP 访问列表中。对于公共连接，TiDB Cloud Dedicated 只允许来自 IP 访问列表中的地址的客户端连接。如果你还没有配置 IP 访问列表，或者你的客户端 IP 地址不在列表中，请按照 [配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md) 中的步骤，在首次连接前将其添加到列表中。

## 连接到集群

要通过公共连接接入 TiDB Cloud Dedicated 集群，请按照以下步骤操作：

1. 打开目标 TiDB Cloud Dedicated 集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请使用左上角的下拉框先切换到目标组织。

    2. 点击目标 TiDB Cloud Dedicated 集群的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    如果你还没有配置 IP 访问列表，请点击 **Configure IP Access List**，或按照 [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md) 中的步骤，在首次连接前进行配置。

4. 点击 **CA cert** 下载用于 TLS 连接 TiDB 集群的 CA 证书。该 CA 证书默认支持 TLS 1.2 版本。

5. 选择你偏好的连接方式，然后参考该标签页上的连接字符串和示例代码，连接到你的 TiDB Cloud Dedicated 集群。

## 后续操作

成功连接到 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
