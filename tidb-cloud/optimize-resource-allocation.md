---
title: Optimize Your Resource Allocation
summary: Learn about how to optimize your resource allocation in TiDB Cloud.
---

# Optimize Your Resource Allocation

As a Hybrid Transactional and Analytical Processing (HTAP) database, [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters need to support multiple upper-level businesses in most scenarios. Different upper-level businesses have different requirements for database quality of service (QoS). In some scenarios, you might need to allocate as many resources as possible to high-priority businesses to ensure that the latency of these businesses is within an acceptable range. 

TiDB Cloud Dedicated clusters provide resource optimization allocation capabilities including [Resource Control](/tidb-resource-control.md) and the [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature (Private Beta), allowing you to allocate reasonable resources to different businesses in multi-business situations.

## Resource Control

[Resource Control](/tidb-resource-control.md) can divide the storage nodes (TiKV or TiFlash layer) of a TiDB Cloud Dedicated cluster into multiple logical groups. When there are mixed workloads in a system, you can put different workloads into separate resource groups. By doing this, you can ensure resource isolation for your applications and meet QoS requirements. 

When the cluster encounters an unexpected SQL performance issue, you can use [SQL bindings](/sql-statements/sql-statement-create-binding.md) or [runaway queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries) along with resource groups to temporarily limit the resource consumption of a SQL statement. 

The rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## The TiDB Node Group feature

The [TiDB Node Group](/tidb-cloud/tidb-node-group-overview.md) feature (Private Beta) physically groups the computing nodes (TiDB layer) of a TiDB Cloud Dedicated cluster. Each group is configured with a number of TiDB nodes, achieving physical separation of computing resources between different groups. 

You can divide computing nodes into multiple TiDB node groups according to different business needs, and configure unique connection endpoints for each TiDB node group. Upper-layer businesses access the cluster through their respective endpoints, and requests are assigned to the corresponding TiDB Node Group for execution. Even if resources in one TiDB node group are overused, businesses in other TiDB node groups will not be affected.

## Comparison between Resource Control and the TiDB Node Group feature

Depending on your application needs and budget constraints, you can use either resource control or the TiDB Node Group feature, or a combination of them, to achieve the desired resource isolation goals. 

The following table lists the pros and cons of Resource Control and the TiDB Node Group feature. 

| Comparison Item           | Resource Control         | TiDB Node Group         |
|--------------------------|---------------------------|------------------------|
| Level of isolation  | TiKV or TiFlash logical layer    | TiDB node physical layer   |
| Flow control        | Control the flow of user read and write requests based on the quotas set for the resource groups. | Not supported. |
| Configuration experience  | Use SQL statements to configure  | Use the TiDB Cloud console to configure    |
| How to distinguish different workloads | Resource Control supports binding the following level of resource to different resource groups to distinguish different workload: <br>- User level. <br>- Session level. Set the resource group for the current session. <br>- Statement level. Set the resource group for the current statement. | Provide different connection endpoints for different workloads.   |
| Cost       | No extra cost     | Need cost for adding TiDB nodes. No extra cost for creating TiDB node groups.       |
