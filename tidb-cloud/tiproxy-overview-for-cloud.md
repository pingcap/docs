---
title: Overview of TiProxy for TiDB Cloud
summary: Learn about the usage scenarios of TiProxy for TiDB Cloud.
---

# Overview of TiProxy for TiDB Cloud

TiProxy is the official proxy component of PingCAP. It is placed between the client and the TiDB server to provide load balancing, connection persistence, and other features for TiDB.

For more information, see [TiProxy Overview](https://docs.pingcap.com/tidb/stable/tiproxy-overview).

> **Note:**
>
> TiProxy is in beta and is currently available only for TiDB Cloud Dedicated clusters deployed on AWS. 

## Scenarios

TiProxy is suitable for the following scenarios:

- Connection persistence: When a TiDB server performs scaling in, rolling upgrade, or rolling restart, the client connection breaks, resulting in an error. If the client does not have an idempotent error retry mechanism, you need to manually check and fix the error, which greatly increases the operational overhead. TiProxy can keep the client connection, so that the client does not report an error.
- Frequent scaling in and scaling out: The workload of an application might change periodically. To save costs, you can deploy TiDB on the cloud and automatically scale in and scale out TiDB servers according to the workload. However, scaling in might cause the client to disconnect, and scaling out might result in an unbalanced load. TiProxy can keep the client connection and achieve load balancing.
- CPU load imbalance: When background tasks consume a significant amount of CPU resources, or workloads across connections vary significantly, leading to an imbalanced CPU load, TiProxy can migrate connections based on CPU usage to achieve load balancing. For more details, see [CPU-based load balancing](https://docs.pingcap.com/tidb/stable/tiproxy-load-balance#cpu-based-load-balancing).

For more scenarios, see [TiProxy User Scenarios](https://docs.pingcap.com/tidb/stable/tiproxy-overview#user-scenarios).

## Limitations

TiProxy cannot preserve client connections in the following scenarios:

- Upgrading AWS EKS, Azure AKS, Google Cloud GKE, or Alibaba Cloud ACK.
- Disabling, scaling in, upgrading, or restarting TiProxy.
- A single statement or transaction that runs for more than 20 seconds. If your application needs a longer timeout, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

For more scenarios, see [TiProxy Limitations](https://docs.pingcap.com/tidb/stable/tiproxy-overview#limitations).

## Billing

TiProxy introduces two types of costs:

- Node costs. For more information, see [Node Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)
- Data transfer costs. For more information, see [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost). TiProxy prioritizes routing traffic to the TiDB nodes in the same availability zone (AZ). However, if the TiDB workloads are uneven, it also routes traffic to other AZs, which can incur additional data transfer costs.

You can view the TiProxy bill on the **Billing** page. For more information, see [View TiProxy bills](/tidb-cloud/tiproxy-management.md#view-tiproxy-bills).

## SLA impact

TiProxy has no impact on SLA.
