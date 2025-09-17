---
title: TiDB 节点组概述
summary: 了解 TiDB 节点组功能的实现方式及使用场景。
---

# TiDB 节点组概述

你可以为 [TiDB Cloud Dedicated 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)创建 TiDB 节点组。TiDB 节点组会在物理层面将集群的计算节点（TiDB 层）进行分组，每个组包含特定数量的 TiDB 节点。该配置为各组之间的计算资源提供物理隔离，从而在多业务场景下实现高效的资源分配。

通过 TiDB 节点组，你可以根据业务需求将计算节点划分为多个 TiDB 节点组，并为每个 TiDB 节点组配置独立的连接端点。你的应用程序通过各自的端点连接到集群，请求会被路由到对应的节点组进行处理。这样可以确保某一组资源过度使用时不会影响其他组。

> **Note**:
>
> TiDB 节点组功能 **不** 支持 TiDB Cloud Serverless 集群。

## 实现方式

TiDB 节点组负责管理 TiDB 节点的分组，并维护端点与其对应 TiDB 节点之间的映射关系。

每个 TiDB 节点组都关联有一个专用的负载均衡器。当用户将 SQL 请求发送到某个 TiDB 节点组的端点时，请求会首先经过该组的负载均衡器，然后被专门路由到该组内的 TiDB 节点。

下图展示了 TiDB 节点组功能的实现方式。

![The implementation of the TiDB Node Group feature](/media/tidb-cloud/implementation-of-tidb-node-group.png)

TiDB 节点组中的所有节点都会响应来自对应端点的请求。你可以执行以下操作：

- 创建 TiDB 节点组并为其分配 TiDB 节点。
- 为每个组设置连接端点。支持的连接类型包括 [公网连接](/tidb-cloud/tidb-node-group-management.md#connect-via-public-connection)、[私有端点](/tidb-cloud/tidb-node-group-management.md#connect-via-private-endpoint) 和 [VPC Peering](/tidb-cloud/tidb-node-group-management.md#connect-via-vpc-peering)。
- 通过不同的端点将应用程序路由到指定的节点组，实现资源隔离。

## 使用场景

TiDB 节点组功能大幅提升了 TiDB Cloud Dedicated 集群的资源分配能力。TiDB 节点专注于计算，不存储数据。通过将节点划分为多个物理组，该功能确保某一组资源过度使用时不会影响其他组。

借助该功能，你可以：

- 将来自不同系统的多个应用整合到同一个 TiDB Cloud Dedicated 集群中。即使某个应用的负载增加，也不会影响其他应用的正常运行。TiDB 节点组功能确保事务型应用的响应时间不会受到数据分析或批量应用的影响。

- 在 TiDB Cloud Dedicated 集群上执行导入或 DDL 任务，而不会影响现有生产业务的性能。你可以为导入或 DDL 任务单独创建一个 TiDB 节点组。即使这些任务消耗大量 CPU 或内存资源，也只会占用其所属 TiDB 节点组的资源，确保其他 TiDB 节点组的业务不受影响。

- 将所有测试环境整合到一个 TiDB 集群中，或将资源消耗较大的批量任务分配到专用的 TiDB 节点组。这样可以提升硬件利用率，降低运维成本，并确保关键应用始终能够获得所需资源。

此外，TiDB 节点组易于扩缩容。对于高性能需求的关键应用，你可以按需为其分配 TiDB 节点。对于资源需求较低的应用，可以从较少的 TiDB 节点起步，按需扩容。高效利用 TiDB 节点组功能可以减少集群数量，简化运维，降低管理成本。

## 限制与配额

目前，TiDB 节点组功能免费。具体限制与配额如下：

- 你只能为部署在 AWS 或 Google Cloud 上的 TiDB Cloud Dedicated 集群创建 TiDB 节点组。对其他云服务商的支持将在近期推出。
- 配置为 4 vCPU 和 16 GiB 内存的 TiDB 集群不支持 TiDB 节点组功能。
- 默认情况下，你最多可以为一个 TiDB Cloud Dedicated 集群创建 5 个 TiDB 节点组。如需更多节点组，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
- 每个 TiDB 节点组至少包含 1 个 TiDB 节点。虽然单个组内的节点数量没有限制，但整个 TiDB Cloud Dedicated 集群中的 TiDB 节点总数不得超过 150。
- TiDB Cloud 会在 TiDB owner 节点上自动运行统计信息收集任务，该任务不受节点组边界影响，无法在单独的 TiDB 节点组内隔离。
- 对于 v8.1.2 之前版本的 TiDB 集群，`ADD INDEX` 任务无法在单独的 TiDB 节点组内隔离。

## SLA 影响

根据 TiDB Cloud [服务等级协议 (SLA)](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/)，多 TiDB 节点部署的 TiDB Cloud Dedicated 集群的月度可用性最高可达 99.99%。但在引入 TiDB 节点组后，如果你为每个 TiDB 节点组仅分配 1 个 TiDB 节点，则会失去各组的高可用性，集群的月度可用性将降级为单 TiDB 节点部署模式（即最高 99.9%）。

为保证高可用性，建议你为每个 TiDB 节点组至少配置 2 个 TiDB 节点。