---
title: TiDB Serverless Limitations and Quotas
summary: Learn about the limitations of TiDB Serverless.
---

# TiDB Serverless Limitations and Quotas

<!-- markdownlint-disable MD026 -->

This document describes the limitations of TiDB Serverless.

We are constantly filling in the feature gaps between TiDB Serverless and TiDB Dedicated. If you require these features or capabilities in the gap, use [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## Limitations

### SQL

- [Time to live (TTL)](/time-to-live.md) is not available for TiDB Serverless clusters currently.
- The [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) syntax is not applicable to [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) clusters.
- The [`SLEEP()` function](/functions-and-operators/miscellaneous-functions.md) only supports a maximum sleep time of 300 seconds.

### System tables

- Tables `CLUSTER_SLOW_QUERY`, `SLOW_QUERY`, `CLUSTER_STATEMENTS_SUMMARY`, `CLUSTER_STATEMENTS_SUMMARY_HISTORY`, `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY` are not available for TiDB Serverless clusters.

### Transaction

- The total size of a single transaction is set to no more than 10 MB on TiDB Serverless during the beta phase.

### Connection

- Only [Standard Connection](/tidb-cloud/connect-via-standard-connection.md) and [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) can be used. You cannot use [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to TiDB Serverless clusters. 
- No "IP Access List" support.

### Monitoring

- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently not available for TiDB Serverless.
- [Cluster Events](/tidb-cloud/tidb-cloud-events.md) are currently not available for TiDB Serverless.
- [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md) is currently not available for TiDB Serverless.

### Diagnosis

- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) is unavailable for TiDB Serverless.

### Stream data

* [Changefeed](/tidb-cloud/changefeed-overview.md) is not supported for TiDB Serverless currently.
* [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) is not supported for TiDB Serverless currently.

### Maintenance window

- [Maintenance window](/tidb-cloud/configure-maintenance-window.md) is unavailable for TiDB Serverless.

## Usage quota

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spend limit](/tidb-cloud/tidb-cloud-glossary.md#spend-limit) for the usage.

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. It is a metric that allows you to estimate the computational resources required to process a specific request in the database. The request unit is also the billing unit for TiDB Cloud Serverless service.

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit) or the usage is reset upon the start of a new month. For example, when the storage of a cluster exceeds 5 GiB, the maximum size limit of a single transaction is reduced from 10 MiB to 1 MiB.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a TiDB Serverless cluster with an additional quota, you can edit the spend limit on the cluster creation page. For more information, see [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster).

After creating a TiDB Serverless, you can still check and edit the spend limit on your cluster overview page. For more information, see [Manage Spend Limit for TiDB Serverless Clusters](/tidb-cloud/manage-serverless-spend-limit.md).
