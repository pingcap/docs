---
title: Overview of TiDB Node Group 
summary: Learn about the implementation and usage scenarios of the TiDB Node Group feature.
---

# Overview of TiDB Node Group

You can create TiDB node groups for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters. A TiDB node group physically groups the computing nodes (TiDB layer) of a cluster, with each group containing a specific number of TiDB nodes. This configuration provides physical isolation of computing resources between groups, enabling efficient resource allocation in multi-business scenarios.

With TiDB node groups, you can divide computing nodes into multiple TiDB node groups based on business requirements and configure unique connection endpoints for each TiDB node group. Your applications connect to the cluster through their respective endpoints, and requests route to the corresponding node group for processing. This ensures that resource overuse in one group does not affect other groups.

> **Note**:
>
> The TiDB Node Group feature is **NOT** available for {{{ .starter }}} and {{{ .essential }}} clusters.

## Implementation

TiDB node groups manage the grouping of TiDB nodes and maintain the mapping between endpoints and their corresponding TiDB nodes.

Each TiDB node group is associated with a dedicated load balancer. When a user sends a SQL request to the endpoint of a TiDB node group, the request first passes through that group's load balancer, which then routes it exclusively to TiDB nodes within the group.

The following diagram illustrates the implementation of the TiDB Node Group feature.

![The implementation of the TiDB Node Group feature](/media/tidb-cloud/implementation-of-tidb-node-group.png)

All nodes in a TiDB node group respond to requests from the corresponding endpoint. You can perform the following tasks:

- Create a TiDB node group and assign TiDB nodes to it.
- Set up connection endpoints for each group. Supported connection types include [public connection](/tidb-cloud/tidb-node-group-management.md#connect-via-public-connection), [private endpoint](/tidb-cloud/tidb-node-group-management.md#connect-via-private-endpoint), and [VPC peering](/tidb-cloud/tidb-node-group-management.md#connect-via-vpc-peering).
- Route applications to specific groups using distinct endpoints to achieve resource isolation.

## Scenarios

The TiDB Node Group feature significantly enhances resource allocation for TiDB Cloud Dedicated clusters. TiDB nodes are dedicated to computation and do not store data. By organizing nodes into multiple physical groups, the feature ensures that resource overuse in one group does not impact other groups.

With this feature, you can:

- Consolidate multiple applications from different systems into a single TiDB Cloud Dedicated cluster. As an application's workload grows, it will not affect the normal operation of other applications. The TiDB Node Group feature ensures that the response time of transactional applications is not impacted by data analysis or batch applications.

- Perform import or DDL tasks on the TiDB Cloud Dedicated cluster without affecting the performance of existing production workloads. You can create a separate TiDB node group for importing or DDL tasks. Even though these tasks consume significant CPU or memory resources, they only use the resources in their own TiDB node group, ensuring the workloads in other TiDB node groups are not impacted. 

- Combine all test environments into a single TiDB cluster or group resource-intensive batch tasks into a dedicated TiDB node group. This approach improves hardware utilization, reduces operating costs, and ensures that critical applications always have access to necessary resources.

In addition, TiDB node groups are easy to scale in or out. For key applications with high performance requirements, you can allocate TiDB nodes to the group as needed. For less demanding applications, you can start with a small number of TiDB nodes and scale out as needed. Efficient use of the TiDB Node Group feature reduces the number of clusters, simplifies operations and maintenance, and lowers management costs.

## Limitations and quotas

Currently, the TiDB Node Group feature is free of charge. The following are limitations and quotas:

- You can only create TiDB node groups for TiDB Cloud Dedicated clusters on AWS or Google Cloud. Support for other cloud providers is planned for the near future.
- TiDB clusters with 4 vCPUs and 16 GiB of memory do not support the TiDB Node Group feature.
- By default, you can create up to five TiDB node groups for a TiDB Cloud Dedicated cluster. If you need more groups, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). 
- Each TiDB node group must contain at least one TiDB node. While there is no limit to the number of nodes in a group, the total number of TiDB nodes in a TiDB Cloud Dedicated cluster must not exceed 150.
- TiDB Cloud runs automatic statistics collection tasks on the TiDB owner node, regardless of node group boundaries. These tasks cannot be isolated within individual TiDB node groups.
- For TiDB clusters of versions earlier than v8.1.2, `ADD INDEX` tasks cannot be isolated within individual TiDB node groups. 

## SLA impact

According to TiDB Cloud [Service Level Agreement (SLA)](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/), the Monthly Uptime Percentage of TiDB Cloud Dedicated clusters with multiple TiDB nodes deployment can reach up to 99.99%. However, after introducing TiDB Node Group, if you create multiple TiDB Node Groups with only 1 TiDB node in each group, you will lose the high availability for the groups and your cluster's monthly uptime percentage will downgrade to a single TiDB node deployment model (namely, up to 99.9%).  

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB node group.
