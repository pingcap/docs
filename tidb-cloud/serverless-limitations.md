---
title: TiDB Cloud Starter Limitations and Quotas
summary: Learn about the limitations of TiDB Cloud Starter.
---

# TiDB Cloud Starter Limitations and Quotas

<!-- markdownlint-disable MD026 -->

TiDB Cloud Starter works with almost all workloads that TiDB supports, but there are some feature differences between TiDB Self-Managed and TiDB Cloud Starter clusters. This document describes the limitations of TiDB Cloud Starter.

If you require the features listed in this document, [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## Limitations

### Audit logs

- Database audit logging is currently unavailable.

### Connection

- Only [Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) and [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) can be used. You cannot use VPC Peering to connect to TiDB Cloud Starter clusters.

### Encryption

- Data persisted in your TiDB Cloud Starter cluster is encrypted using the encryption tool provided by the cloud provider that manages your cluster. <!--TBD, ToDo: For [scalable clusters](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan), the spending limit must be set to a minimum of $0.01. Also, the scalable cluster can have a free quota if it meets the qualifications. The scalable cluster with a free quota will consume the free quota first.-->

### Maintenance window

- Maintenance window is currently unavailable.

### Monitoring and diagnosis

- Third-party Monitoring integrations are currently unavailable.
- Built-in Alerting is currently unavailable.
- Key Visualizer is currently unavailable.
- Index Insight is currently unavailable.

### Self-service upgrades

- TiDB Cloud Starter is a fully managed deployment of TiDB. Major and minor version upgrades of TiDB Cloud Starter are handled by TiDB Cloud and therefore cannot be initiated by users.

### Stream data

- Changefeed is not supported for TiDB Cloud Starter currently.
- The Data Migration feaure that migrates data from MySQL-compatible databases to TiDB Cloud is not supported for TiDB Cloud Starter currently.

### Time to live (TTL)

- In TiDB Cloud Starter, the [`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) attribute for a table is fixed at `15m` and cannot be modified. This means that TiDB Cloud Starter schedules a background job every 15 minutes to clean up expired data.

### Others

- Transaction can not last longer than 30 minutes.
- For more details about SQL limitations, refer to [Limited SQL Features](/tidb-cloud/limited-sql-features.md).

## Usage quota

For each organization in TiDB Cloud, you can create a maximum of five [free clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan) by default. To create more TiDB Cloud Starter clusters, you need to add a credit card and specify a spending limit.

For the first five TiDB Cloud Starter clusters in your organization, whether they are free or scalable, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. It is a metric that allows you to estimate the computational resources required to process a specific request in the database. The request unit is also the billing unit for TiDB Cloud Starter service.

Once a cluster reaches its usage quota, it immediately denies any new connection attempts until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Cloud Starter Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details). <!--TBD, ToDo: Not sure the Pricing URL for TiDB Cloud Starter-->

If you want to create a TiDB Cloud Starter cluster with an additional quota, you can select the scalable cluster plan and edit the spending limit on the cluster creation page. For more information, see [Create a TiDB Cloud Starter cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

After creating a TiDB Cloud Starter cluster, you can still check and edit the spending limit on your cluster overview page. For more information, see [Manage Spending Limit for TiDB Cloud Starter Clusters](/tidb-cloud/manage-serverless-spend-limit.md).
