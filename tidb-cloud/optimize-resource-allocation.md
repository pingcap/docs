---
title: Optimize Resource Allocation for TiDB Cloud Dedicated
summary: Learn about how to optimize your resource allocation for TiDB Cloud Dedicated clusters.
---

# Optimize Resource Allocation for TiDB Cloud Dedicated

As a Hybrid Transactional and Analytical Processing (HTAP) database, [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters can support multiple business applications, each with different quality of service (QoS) requirements. In some cases, you might need to allocate more resources to high-priority applications to maintain acceptable latency levels.

TiDB Cloud Dedicated offers resource optimization features, including [Resource Control](/tidb-resource-control-ru-groups.md) and the [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature. These features help you allocate resources efficiently in multi-business scenarios.

## Use Resource Control

[Resource Control](/tidb-resource-control-ru-groups.md) lets you divide the storage nodes (TiKV or TiFlash) of a TiDB Cloud Dedicated cluster into multiple logical groups. In systems with mixed workloads, you can assign workloads to separate resource groups to ensure resource isolation and meet QoS requirements.

If the cluster experiences unexpected SQL performance issues, you can use [SQL bindings](/sql-statements/sql-statement-create-binding.md) or [manage runaway queries](/tidb-resource-control-runaway-queries.md) alongside resource groups to temporarily limit the resource consumption of specific SQL statements.

By using Resource Control effectively, you can reduce the number of clusters, simplify operations and maintenance, and lower management costs.

## Use TiDB Node Group

The [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature physically groups the computing nodes (TiDB layer) of a TiDB Cloud Dedicated cluster. Each group is configured with a specific number of TiDB nodes, ensuring the physical separation of computing resources between groups.

You can divide computing nodes into multiple TiDB node groups based on business requirements and assign unique connection endpoints to each group. Your applications connect to the cluster through their respective endpoints, and requests route to the corresponding node group for processing. This ensures that resource overuse in one group does not affect other groups.

## Choose between Resource Control and TiDB Node Group

You can use Resource Control, the TiDB Node Group feature, or a combination of both based on your application needs and budget to achieve resource isolation.

The following table compares the features of Resource Control and TiDB Node Group:

| Comparison item           | Resource Control         | TiDB Node Group         |
|--------------------------|---------------------------|------------------------|
| Isolation level   | TiKV or TiFlash logical layer    | TiDB node physical layer   |
| Flow control        | Controls the flow of user read and write requests based on quotas set for resource groups. | Not supported. |
| Configuration method  | Configured using SQL statements  | Configured through the TiDB Cloud console |
| Distinguishing workloads | Supports binding resources at the following levels: <ul><li>User level.</li><li>Session level (set the resource group per session). </li><li>Statement level (set the resource group per statement).</li></ul>| Provides different connection endpoints for different workloads.   |
| Cost       | No extra cost     | Cost associated with adding TiDB nodes, but no extra cost for creating TiDB node groups.       |
