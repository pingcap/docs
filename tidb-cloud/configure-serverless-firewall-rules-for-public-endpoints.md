---
title: 配置 TiDB Cloud Starter 或 Essential 公共端点的防火墙规则 
summary: 了解如何安全地为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群配置和管理具有公共访问权限的防火墙规则。
---

# 配置 TiDB Cloud Starter 或 Essential 公共端点的防火墙规则

本文档介绍了 TiDB Cloud Starter 和 TiDB Cloud Essential 集群的公共连接选项。你将学习如何安全地管理可通过互联网访问的集群的关键概念。

> **注意：**
>
> 本文档适用于 **TiDB Cloud Starter** 和 **TiDB Cloud Essential**。关于为 **TiDB Cloud Dedicated** 配置 IP 访问列表的说明，请参见 [Configure an IP Access List for TiDB Cloud Dedicated](/tidb-cloud/configure-ip-access-list.md)。

## 公共端点

在你的集群上配置公共访问后，可以通过公共端点访问该集群。也就是说，集群可以通过互联网访问。公共端点是一个可被公开解析的 DNS 地址。术语 “authorized network” 指的是你选择允许访问集群的一组 IP 地址范围。这些权限通过 **firewall rules** 强制执行。

### 公共访问的特性

- 只有指定的 IP 地址可以访问你的集群。  
    - 默认情况下，允许所有 IP 地址（`0.0.0.0 - 255.255.255.255`）访问。  
    - 你可以在集群创建后更新允许的 IP 地址。  
- 你的集群拥有一个可被公开解析的 DNS 名称。  
- 进出你集群的网络流量通过 **公有互联网** 路由，而不是私有网络。

### 防火墙规则

通过 **firewall rules** 授权 IP 地址访问。如果连接请求来自未被批准的 IP 地址，客户端将收到错误提示。

你最多可以创建 200 条 IP 防火墙规则。

### 允许 AWS 访问

如果你的 TiDB Cloud Starter 集群托管在 AWS 上，你可以参考官方 [AWS IP address list](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html) 启用来自 **所有 AWS IP 地址** 的访问。

TiDB Cloud 会定期更新该列表，并使用保留 IP 地址 **169.254.65.87** 代表所有 AWS IP 地址。

## 创建和管理防火墙规则

本节介绍如何为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群管理防火墙规则。启用公共端点后，只有在防火墙规则中指定的 IP 地址才能连接到你的集群。

要为 TiDB Cloud Starter 或 TiDB Cloud Essential 集群添加防火墙规则，请按照以下步骤操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，如果 **Public Endpoint** 处于禁用状态，请先启用。在 **Authorized Networks** 区域，点击 **+ Add Current IP**。这会自动使用 TiDB Cloud 识别到的你电脑的公网 IP 地址创建一条防火墙规则。

    > **注意：**
    >
    > 在某些情况下，TiDB Cloud 控制台检测到的 IP 地址与你实际访问互联网时使用的 IP 地址不同。因此，你可能需要更改起始和结束 IP 地址，以确保规则按预期生效。你可以使用搜索引擎或其他在线工具查询自己的 IP 地址。例如，搜索 “what is my IP”。

4. 点击 **Add rule** 以添加更多地址范围。在弹出的窗口中，你可以指定单个 IP 地址或一段 IP 地址范围。如果你只想允许单个 IP 地址访问，请在 **Start IP Address** 和 **End IP Address** 字段中输入相同的 IP 地址。开启防火墙后，管理员、用户和应用程序可以使用有效凭证访问集群上的任意数据库。点击 **Submit** 添加防火墙规则。

## 后续操作

- [通过公共端点连接 TiDB Cloud Starter 或 Essential](/tidb-cloud/connect-via-standard-connection-serverless.md)