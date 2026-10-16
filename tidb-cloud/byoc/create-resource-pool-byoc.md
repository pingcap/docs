---
title: 创建资源池
summary: 了解如何为 TiDB Cloud BYOC 创建资源池。
---

# 创建资源池

资源池是 TiDB Cloud BYOC 部署中用于管理底层物理资源、网络和容量的管理单元。一个资源池可以承载一个或多个 BYOC 实例，并且每个 BYOC 实例只属于一个资源池。

本文档介绍如何在 TiDB Cloud 控制台中创建资源池。

## 开始之前 {#before-you-begin}

在创建资源池之前，请确保满足以下要求：

- 已为你的组织启用 BYOC。
- 已在目标云服务商和 Region 完成 BYOC 部署。
- 你拥有 `Organization Owner` 角色。只有 Organization Owners 才能创建和管理资源池。
- 你已为资源池规划专用的 CIDR 范围。
- 你的云账户具有足够的服务配额来预配所需的资源池容量。

## 创建资源池 {#create-a-resource-pool}

要创建资源池，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左侧导航栏中的 **BYOC Management** > **Resource Pools**。

2. 在 **Resource Pools** 页面，点击 **Create Resource Pool**。

3. 在 **Basic Settings** 区域，配置以下字段：

    - **Resource Pool Name**：输入资源池名称。该名称必须有效且唯一。
    - **Cloud Provider**：选择创建资源池的云服务商。
    - **Region**：选择创建资源池的 Region。

    你只能在已完成 BYOC 部署的云服务商和 Region 中创建资源池。如果目标 Region 不可用，请先完成该 Region 的 BYOC 部署，然后再创建资源池。资源池创建后，无法更改云服务商或 Region。

4. （可选）在 **Pool vCPU Limit** 区域，启用并设置 Pool vCPU Limit。

    Pool vCPU Limit 是资源池中所有与数据库相关资源允许预配的 TiDB vCPU 总容量上限，包括但不限于 TiDB、TiKV、TiFlash 和 PD。不包括 Observability (O11Y) Nodes 或 Admin Nodes 使用的 vCPU。如果不设置限制，资源使用将不受限制，并按实际消耗计费。

5. 在 **Pool Capacity** 区域，配置初始 TiKV 资源，并可选择配置 TiFlash 资源：

    - **TiKV**：TiKV 为必选项。选择初始的 vCPU 和 RAM 配置、存储大小以及节点数。节点数必须满足高可用要求，并且必须是 3 的倍数。资源池创建后，TiKV 可以根据工作负载需求自动扩容。你也可以提前手动扩容 TiKV。目前，TiDB Cloud 不支持在控制台中手动或自动对 TiKV 进行缩容，因为缩容可能存在风险。如需缩容 TiKV，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
    - **TiFlash**：TiFlash 为可选项。如果在创建资源池时未启用 TiFlash，TiDB Cloud 不会部署 TiFlash 节点。你可以稍后根据工作负载需求启用 TiFlash。如果启用 TiFlash，请选择 vCPU 和 RAM 配置、存储大小以及节点数。

    资源池创建后，你无法在控制台中手动更改 TiKV 机型。在自动扩容期间，TiDB Cloud 可能会根据工作负载需求更改 TiKV 机型。你可以在 TiDB Cloud 控制台中禁用 TiFlash。禁用 TiFlash 会影响资源池中的所有 BYOC 实例。TiFlash 资源将被移除，依赖 TiFlash 的分析型工作负载可能会不可用或出现性能下降。

    如果你设置了 Pool vCPU Limit，请确保初始 TiKV 和 TiFlash 资源的 vCPU 总数不超过 Pool vCPU Limit 的 50%。这有助于为后续实例创建和自动扩容预留容量。

6. 在 **High Availability** 区域，为资源池选择一种高可用模式。

    - **Zonal**：将资源池部署在单个可用区中，以获得更低的网络延时。
    - **Regional**：将资源池部署在多个可用区中，以获得更高的可用性以及更强的可用区级故障恢复能力。

    >**Note:**
    >
    > - 在创建资源池之前，必须先选择高可用模式。
    > - 如果你选择 **Regional** 模式，请确保该资源池所在的 Region 至少包含三个符合条件的可用区。如果不满足此要求，创建区域级资源池的过程可能无法完成。
    > - TiDB Cloud 会根据 [BYOC Region 配置](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#step-3-select-region-and-availability-zones-azs) 和可用的云资源来确定可用区。

    资源池创建后，无法更改其高可用模式或可用区部署位置。

7. 在 **Pool CIDR** 区域，查看或输入资源池的 CIDR 范围。

    资源池 CIDR 用作资源池内资源的网络地址范围，资源池创建后无法修改。

    资源池 CIDR 必须满足以下要求：

    - 必须位于以下受支持的私有网络地址范围之一：`10.0.0.0/8`、`172.16.0.0/12` 或 `192.168.0.0/16`。
    - 前缀长度必须在 `/16` 到 `/22` 之间。
    - 不得与同一 Region 中的 O11Y CIDR 或任何现有资源池 CIDR 重叠。
    - 不得与你的应用 VPC CIDR 或任何其他需要连接到此资源池的客户自主管理网络重叠。

    TiDB Cloud 会验证目标 Region 中已知的 TiDB Cloud 托管网络范围是否存在 CIDR 重叠。TiDB Cloud 无法检测与你的应用 VPC、本地网络或 VPN 网络的重叠情况。你必须在创建资源池之前自行验证这些客户自主管理的网络范围。

8. （可选）在 **AWS Resource Tags** 区域，添加标签。

    标签会应用于资源池内所有支持打标签的 AWS 资源。

    适用以下规则：

    - Tag key 为必填项。
    - Tag value 为可选项。
    - Tag key 和 Tag value 都是大小写敏感的。
    - Tag key 必须唯一，并按大小写敏感方式进行检查。
    - Tag key 长度必须为 1 到 128 个 UTF-8 字符。
    - Tag value 长度不得超过 256 个 UTF-8 字符。
    - 用户定义的 Tag key 不能以 `aws:` 开头。
    - 系统保留的 AWS 标签不能被覆盖或编辑。
    - 空行会被忽略且不会提交。
    - 标签必须符合 AWS 的标签限制。

9. 查看右侧的摘要信息，然后点击 **Create**。

提交请求后，TiDB Cloud 会验证配置并启动异步预配操作。新的资源池会显示在 **Resource Pools** 页面中，状态为 **Creating**。预配成功后，状态会变为 **Active**。

## 接下来做什么 {#what-s-next}

资源池变为 **Active** 后，你可以执行以下操作：

- 在资源池中[创建 BYOC 实例](/tidb-cloud/byoc/create-tidb-instance-byoc.md)。
- [管理资源池](/tidb-cloud/byoc/manage-resource-pools-byoc.md)，包括更新容量、更新 Pool vCPU Limit，以及管理 AWS 资源标签。