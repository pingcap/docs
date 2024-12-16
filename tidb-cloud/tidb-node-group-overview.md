---
title: TiDB Node Group overview
summary: Learn about the overview of the TiDB Node Group feature.
---

# TiDB Node Group overview

TiDB Cloud lets you create TiDB node groups for TiDB Cloud Dedicated clusters. A TiDB node group physically groups the computing nodes (TiDB layer) of the cluster, each group is configured with a number of TiDB nodes. It provides a physical isolation of computing resources between different groups, allowing you to allocate reasonable resources to different businesses in multi-business situations.

With TiDB node groups, you can divide computing nodes into multiple TiDB node groups according to different business needs, and configure unique connection endpoints for each TiDB node group. Upper-layer businesses access the cluster through their respective endpoints, and requests are assigned to the corresponding TiDB node group for execution. Even if resources in one TiDB node group are overused, businesses in other TiDB node groups will not be affected.

## Implementations

TiDB node group can manage the grouping of TiDB nodes and maintain the mapping between endpoints and TiDB nodes. 

For each TiDB node group, there is a dedicated load balancer created. When a user executes a SQL request to the endpoint of a TiDB node group, the request first passes through the load balancer deployed the group, and then the load balancer distributes the request only to the TiDB nodes in this group. 

The following diagram shows the implementations of the TiDB Node Group feature

![The implementations of the TiDB Node Group feature](/media/tidb-cloud/implementation-of-tidb-node-group.png)

All nodes in a TiDB node group respond to requests coming from the cooresponding endpoint. You can do the following:

- Create a TiDB node group and assign TiDB nodes to the group.
- Set up connection endpoints for each group. The following three connection types are supported by TiDB node group's endpoints: public connection, private endpoint and VPC peering. 
- Let the applications send requests to different groups through different endpoints to achieve resource isolation.

## Scenarios 

The introduction of the TiDB Node Group feature is a big improvement for resource allocation of TiDB Cloud Dedicate clusters. TiDB nodes are for computing only and do not store data. TiDB node groups can divide TiDB nodes into multiple physical groups. Even if resources in one TiDB node group are overused, businesses in other TiDB node groups will not be affected.

With this feature, you can:

- Combine multiple applications from different systems into a single TiDB Cloud Dedicated cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. By using the TiDB node group feature , you can ensure that the response time of transactional applications is not affected by data analysis or batch applications.
- Do import or DDL tasks anytime for TiDB Cloud Dedicated cluster without concern about the performance impact for existing production workload. You can create separate TiDB node group for importing or DDL tasks. Even though importing or DDL tasks take a lot of CPU or memory resource, they only use the resource in their own TiDB node group, and the workload in other TiDB node group will not be impacted. 
- Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a TiDB node group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.

In addition, TiDB node groups are easily scaled in or out. For key applications with high performance requirments, you can plan enough TiDB nodes in the group. For applications that do not have high performance requirements, you can start with a small number of TiDB nodes and scale out when necessary.  The rational use of the TiDB Node Group feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## Limitations and quotas

Currently, the TiDB Node Group feature is in beta and free of charge.

- You can only create TiDB node groups for TiDB Cloud Dedicated clusters on AWS. It is planned to support this feature for other cloud providers in near future. 
- Clusters with TiDB 4 vCPU 16 Mem do not support the TiDB Node Group feature.
- For a TiDB Cloud Dedicated cluster, you can create a maximum of five TiDB node groups by default. If you need more groups, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). 
- Each TiDB node group must have at least one TiDB node. The maximum node count of a group is not limited. However, the total TiDB nodes in a TiDB Cloud Dedicated cluster must be fewer than 150. 

## SLA impact

According to TiDB Cloud [Service Level Agreement (SLA)](https://www.pingcap.com/legal/service-level-agreement-for-tidb-cloud-services/), the Monthly Uptime Percentage of TiDB Cloud Dedicated clusters with multiple TiDB nodes deployment can be up to 99.99%. However, after introducing the TiDB Node Group feature, TiDB Cloud can not provide high availability across TiDB node groups. If you create multiple TiDB node groups with only one TiDB node in each group, you will lose the high availability for the groups and your cluster's monthly uptime percentage will downgrade to a single TiDB node deployment model.   

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB node group.
