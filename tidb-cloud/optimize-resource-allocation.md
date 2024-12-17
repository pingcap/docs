---
title: Optimize Your Resource Allocation
summary: Learn about how to optimize your resource allocation in TiDB Cloud.
---

# Optimize Your Resource Allocation

As a Hybrid Transactional and Analytical Processing (HTAP) database, [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters clusters often support multiple upper-level businesses, each with different quality of service (QoS) requirements. In some cases, you might need to allocate maximum resources to high-priority businesses to ensure their latency remains within an acceptable range.

TiDB Cloud Dedicated clusters offer resource optimization features, including [Resource Control](/tidb-resource-control.md) and the [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature (Private Beta). These capabilities enable you to allocate resources efficiently in multi-business situations.

## Resource Control

[Resource Control](/tidb-resource-control.md) allows you to divide the storage nodes (TiKV or TiFlash) of a TiDB Cloud Dedicated cluster into multiple logical groups. In systems with mixed workloads, you can assign different workloads to separate resource groups, ensuring resource isolation and meeting QoS requirements.

If the cluster encounters unexpected SQL performance issues, you can use [SQL bindings](/sql-statements/sql-statement-create-binding.md) or [manage runaway queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries) alongside resource groups to temporarily limit the resource consumption of a SQL statement.

Effectively using resource control can reduce the number of clusters, simplify operations and maintenance, and lower management costs.

## The TiDB Node Group feature

The [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature (Private Beta) physically groups the computing nodes (TiDB layer) of a TiDB Cloud Dedicated cluster. Each group is configured with a specific number of TiDB nodes, ensuring physical separation of computing resources between groups.

You can divide computing nodes into multiple TiDB node groups based on business requirements and assign unique connection endpoints to each TiDB node group. Upper-layer businesses access the cluster through their respective endpoints, and requests are directed to the corresponding TiDB node group. This setup ensures that resource overuse in one TiDB node group does not impact businesses in other TiDB node groups.

## Comparison between Resource Control and the TiDB Node Group feature

Depending on your application needs and budget, you can choose to use either Resource Control, the TiDB Node Group feature, or a combination of both, to achieve your desired resource isolation.

The following table compares the pros and cons of Resource Control and the TiDB Node Group feature:

| Comparison Item           | Resource Control         | TiDB Node Group         |
|--------------------------|---------------------------|------------------------|
| Level of isolation  | TiKV or TiFlash logical layer    | TiDB node physical layer   |
| Flow control        | Controls the flow of user read and write requests based on the quotas set for the resource groups. | Not supported. |
| Configuration experience  | Configured using SQL statements  | Configured via the TiDB Cloud console    |
| Distinguishing workloads | Supports binding resources at the following levels: </b>- User level. </b>- Session level (set the resource group per session). </b>- Statement level (set the resource group per statement). | Provide different connection endpoints for different workloads.   |
| Cost       | No extra cost     | Cost associated with adding TiDB nodes, but no extra cost for creating TiDB node groups.       |
