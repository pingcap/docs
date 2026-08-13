---
title: 配置 IP 访问列表
summary: 了解如何配置允许访问你的 TiDB Cloud Dedicated 集群的 IP 地址。
---

# 配置 IP 访问列表

对于 TiDB Cloud 中的每个 TiDB Cloud Dedicated 集群，你可以配置 IP 访问列表来过滤试图访问集群的互联网流量，其工作方式类似于防火墙访问控制列表。配置完成后，只有 IP 地址在 IP 访问列表中的客户端和应用程序才能连接到你的 TiDB Cloud Dedicated 集群。

> **注意：**
>
> 本文档适用于 [**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。如果你需要为 **TiDB Cloud Serverless** 配置 IP 访问列表，请参见 [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 添加 IP 地址 {#add-an-ip-address}

要将 IP 地址添加到 TiDB Cloud Dedicated 集群的 IP 访问列表中，请执行以下步骤：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Dedicated 集群的名称，进入其概览页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Settings** > **Networking**。
3. 在 **Networking** 页面上，点击 **Add IP Address**。
4. 在 **Add IP Address** 对话框中，添加 IP 地址，并可选择填写描述。对于每个 TiDB Cloud Dedicated 集群，最多可以添加 100 个 IP 地址。

    - 要添加自定义 IP 地址，点击 **+** 图标，以 CIDR 表示法输入 IP 地址（例如，`192.168.1.1/32`），并添加描述。
    - 要添加当前计算机的 IP 地址，点击 **Add Current IP**。
    - 要允许任何 IP 地址访问你的集群，点击 **Allow access from anywhere**。这会添加 `0.0.0.0/0` CIDR 条目。此操作风险极高，不建议在生产环境中使用。

5. 点击 **Save**。

## 修改 IP 地址 {#edit-an-ip-address}

如需修改 IP 访问列表中的现有 IP 地址，请执行以下步骤：

1. 在 **Networking** 页面中，在 **IP Access List** 里找到要修改的 IP 地址。
2. 在该 IP 地址所在行中点击 **...**，然后点击 **Edit**。
3. 在 **Edit IP Address** 对话框中，根据需要修改 IP 地址或描述。
4. 点击 **Submit**。

## 删除 IP 地址 {#delete-an-ip-address}

要从 IP 访问列表中删除现有的 IP 地址，请执行以下步骤：

1. 在 **Networking** 页面上的 **IP Access List** 中，找到要删除的 IP 地址。
2. 在该 IP 地址所在行中点击 **...**，然后点击 **Delete**。
3. 在确认对话框中，点击 **Delete**。
