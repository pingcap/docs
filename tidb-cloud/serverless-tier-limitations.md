---
title: Serverless Tier Limitations and Quotas
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tier Limitations and Quotas

<!-- markdownlint-disable MD026 -->

This document describes the limitations of Serverless Tier.

We are constantly filling in the feature gaps between Serverless Tier and Dedicated Tier. If you require these features or capabilities in the gap, use [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## Limitations

### SQL

- [Time to live (TTL)](/time-to-live.md) is not available for Serverless Tier clusters currently.
- The [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) syntax is not applicable to TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.
- The [`SLEEP()` function](/functions-and-operators/miscellaneous-functions.md) only supports a maximum sleep time of 300 seconds.

### System tables

- Tables `CLUSTER_SLOW_QUERY`, `SLOW_QUERY`, `CLUSTER_STATEMENTS_SUMMARY`, `CLUSTER_STATEMENTS_SUMMARY_HISTORY`, `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY` are not available for Serverless Tier clusters.

### Transaction

- The total size of a single transaction is set to no more than 10 MB on Serverless Tier during the beta phase.

### Connection

- Only [Standard Connection](/tidb-cloud/connect-via-standard-connection.md) can be used. You cannot use [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) or [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to Serverless Tier clusters. 
- No "IP Access List" support.

### Monitoring

- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently not available for Serverless Tier.
- [Cluster Events](/tidb-cloud/tidb-cloud-events.md) are currently not available for Serverless Tier.
- [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md) is currently not available for Serverless Tier.

### Diagnosis

- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) is unavailable for Serverless Tier.

### Stream data

* [Changefeed](/tidb-cloud/changefeed-overview.md) is not supported for Serverless Tier currently.
* [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) is not supported for Serverless Tier currently.

### Maintenance window

- [Maintenance window](/tidb-cloud/configure-maintenance-window.md) is unavailable for Serverless Tier.

## Usage quota

For each organization in TiDB Cloud, you can create a maximum of five Serverless Tier clusters by default. To create more Serverless Tier clusters, you need to add a credit card and set a [spend limit](/tidb-cloud/tidb-cloud-glossary.md#spend-limit) for the usage.

For the first five Serverless Tier clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. It is a metric that allows you to estimate the computational resources required to process a specific request in the database. The request unit is also the billing unit for TiDB Cloud Serverless service.

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit) or the usage is reset upon the start of a new month. For example, when the storage of a cluster exceeds 5 GiB, the maximum size limit of a single transaction is reduced from 10 MiB to 1 MiB.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Cloud Serverless Tier Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a Serverless Tier cluster with an additional quota, you can edit the spend limit on the cluster creation page. For more information, see [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster).

After creating a Serverless Tier, you can still check and edit the spend limit on your cluster overview page. For more information, see [Manage Spend Limit for Serverless Tier Clusters](/tidb-cloud/manage-serverless-spend-limit.md).
