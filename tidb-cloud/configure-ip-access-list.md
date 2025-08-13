---
title: 配置 IP 访问列表
summary: 了解如何配置允许访问你的 TiDB Cloud Dedicated 集群的 IP 地址。
---

# 配置 IP 访问列表

对于 TiDB Cloud 中的每个 TiDB Cloud Dedicated 集群，你可以配置 IP 访问列表来过滤试图访问集群的互联网流量，其工作方式类似于防火墙访问控制列表。配置完成后，只有 IP 地址在 IP 访问列表中的客户端和应用程序才能连接到你的 TiDB Cloud Dedicated 集群。

> **注意：**
>
> 本文档适用于 [**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。如果你需要为 **TiDB Cloud Serverless** 配置 IP 访问列表，请参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

要为你的 TiDB Cloud Dedicated 集群配置 IP 访问列表，请按照以下步骤操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏，点击 **Settings** > **Networking**。
3. 在 **Networking** 页面，点击 **Add IP Address**。
4. 在弹出的对话框中，选择以下选项之一：

    - **Allow access from anywhere**：允许所有 IP 地址访问 TiDB Cloud。此选项会将你的集群完全暴露在互联网中，风险极高。
    - **Use IP addresses**（推荐）：你可以添加允许通过 SQL 客户端访问 TiDB Cloud 的 IP 列表和 CIDR 地址。

5. 如果你选择 **Use IP addresses**，请添加 IP 地址或 CIDR 范围，并可选填写描述。每个 TiDB Cloud Dedicated 集群最多可添加 100 个 IP 地址。
6. 点击 **Confirm** 保存更改。