---
title: TiDB Node Group Overview
summary: Learn about the overview of the TiDB Node Group feature.
---

# TiDB Node Group Overview

TiDB Cloud allows you to create TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters. A TiDB node group physically groups the computing nodes (TiDB layer) of the cluster, with each group configured with a set number of TiDB nodes. This setup provides physical isolation of computing resources between groups, enabling efficient resource allocation in multi-business situations.

Using TiDB node groups, you can divide computing nodes into multiple TiDB node groups based on business needs, and configure unique connection endpoints for each TiDB node group. Upper-layer businesses access the cluster through their respective endpoints, and requests are routed to the corresponding TiDB node group for execution. This ensures that even if resources in one TiDB node group are overused, businesses in other TiDB node groups will not be affected.

> **Note**:
>
> The TiDB Node Group feature is **NOT** available for TiDB Cloud Serverless clusters.

## Implementations

TiDB node groups manage the grouping of TiDB nodes and maintain the mapping between endpoints and the corresponding TiDB nodes.

Each TiDB node group is associated with a dedicated load balancer. When a user sends a SQL request to the endpoint of a TiDB node group, the request first passes through the group's load balancer, and then the load balancer distributes the request exclusively to the TiDB nodes within that group.

The following diagram illustrates the implementation of the TiDB Node Group feature.

![The implementations of the TiDB Node Group feature](/media/tidb-cloud/implementation-of-tidb-node-group.png)

All nodes in a TiDB node group respond to requests from the corresponding endpoint. You can perform the following tasks:

- Create a TiDB node group and assign TiDB nodes to it.
- Set up connection endpoints for each group. Supported connection types include [public connection](/tidb-cloud/tidb-node-group-management.md#connect-via-public-connection), [private endpoint](/tidb-cloud/tidb-node-group-management.md#connect-via-private-endpoint), and [VPC peering](/tidb-cloud/tidb-node-group-management.md#connect-via-vpc-peering).
- Direct applications to send requests to different groups through distinct endpoints to achieve resource isolation.

## Scenarios 

The TiDB Node Group feature significantly enhances resource allocation for TiDB Cloud Dedicated clusters. TiDB nodes are dedicated to computation and do not store data, and TiDB node groups allow you to organize these nodes into multiple physical groups. This isolation ensures that resource overuse in one node group does not impact businesses in other groups.

With this feature, you can:

- Consolidate multiple applications from different systems into a single TiDB Cloud Dedicated cluster. As an application's workload grows, it will not affect the normal operation of other applications. The TiDB Node Group feature ensures that the response time of transactional applications is not impacted by data analysis or batch applications.

- Perform import or DDL tasks on the TiDB Cloud Dedicated cluster without affecting the performance of the existing production workloads. You can create separate TiDB node group for importing or DDL tasks. Even though importing or DDL tasks take a lot of CPU or memory resource, they only use the resource in their own TiDB node group, and the workload in other TiDB node group will not be impacted. 

- Combine all test environments into a single TiDB cluster or group resource-intensive batch tasks into a dedicated TiDB node group. This approach improves hardware utilization, reduces operating costs, and ensures that critical applications always have access to necessary resources.

In addition, TiDB node groups are easy to scale in or out. For key applications with high performance requirments, you can allocate sufficient TiDB nodes to the group. For less demanding applications, you can start with a small number of TiDB nodes and scale out as needed. Efficient use of the TiDB Node Group feature can reduce the number of clusters, simplify operations and maintenance, and lower management costs.

## Limitations and quotas

Currently, the TiDB Node Group feature is in private beta and free of charge. The following are limitations and quotas:

- You can only create TiDB node groups for TiDB Cloud Dedicated clusters on AWS. Support for other cloud providers is planned for the near future.
- TiDB clusters with 4 vCPU and 16 GiB memory do not support the TiDB Node Group feature.
- By default, you can create up to five TiDB node groups for a TiDB Cloud Dedicated cluster. If you need more groups, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). 
- Each TiDB node group must contain at least one TiDB node. While there is no limit to the number of nodes in a group, the total number of TiDB nodes in a TiDB Cloud Dedicated cluster must not exceed 150.

## SLA impact

According to TiDB Cloud [Service Level Agreement (SLA)](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/), the Monthly Uptime Percentage of TiDB Cloud Dedicated clusters with multiple TiDB nodes deployment can reach up to 99.99%. However, after introducing the TiDB Node Group feature, TiDB Cloud can not provide high availability across TiDB node groups. If you create multiple TiDB node groups with only one TiDB node in each group, you will lose the high availability for the groups and your cluster's monthly uptime percentage will downgrade to a single TiDB node deployment model.   

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB node group.
