---
title: Overview of TiProxy
summary: Learn about the usage scenarios of TiProxy.
---

# Overview of TiProxy

TiProxy is the official proxy component of PingCAP. It is placed between the client and the TiDB server to provide load balancing, connection persistence, and other features for TiDB.

For more details, see [TiProxy Overview](/tiproxy/tiproxy-overview.md).

## Scenarios

TiProxy is suitable for the following scenarios:

- Connection persistence: When a TiDB server performs scaling in, rolling upgrade, or rolling restart, the client connection is broken, resulting in an error. If the client does not have an idempotent error retry mechanism, you need to manually check and fix the error, which greatly increases the labor cost. TiProxy can keep the client connection, so that the client does not report an error.
- Frequent scaling in and scaling out: The workload of an application might change periodically. To save costs, you can deploy TiDB on the cloud and automatically scale in and scale out TiDB servers according to the workload. However, scaling in might cause the client to disconnect, and scaling out might result in unbalanced load. TiProxy can keep the client connection and achieve load balancing.
- CPU load imbalance: When background tasks consume a significant amount of CPU resources or workloads across connections vary significantly, leading to an imbalanced CPU load, TiProxy can migrate connections based on CPU usage to achieve load balancing. For more details, see [CPU-based load balancing](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing).

For more senarios, see [TiProxy User Senarios](/tiproxy/tiproxy-overview.md#user-scenarios).

## Limitations

TiProxy cannot preserve client connections in the following senarios:

- Upgrading Google Cloud GKE, AWS EKS, or Alibaba Cloud ACK.
- Disable, scale in, upgrade, or restart TiProxy.
- A single statement or single transaction that runs exceeds 20 seconds.

For more senarios, see [TiProxy Limitations](/tiproxy/tiproxy-overview.md#limitations).

## Billing

TiProxy introduces 2 parts of cost:

- Node cost, see [Node Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)
- Data transfer cost, see [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost). TiProxy will prioritize routing to the TiDB instances in the same AZ. However, if the TiDB loads are uneven, it will also route to other AZs, resulting in additional data transfer costs.

You can view the TiProxy bill in the billing page. For the detailed steps, see [View Tiproxy billing](/tidb-cloud/tiproxy-management.md#view-tiproxy-billing).

## SLA impact

TiProxy has no impact on SLA.
