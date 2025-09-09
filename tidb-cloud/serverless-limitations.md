---
title: Limitations and Quotas of {{{ .starter }}} and Essential
summary: Learn about the limitations of {{{ .starter }}}.
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# Limitations and Quotas of {{{ .starter }}} and Essential

<!-- markdownlint-disable MD026 -->

{{{ .starter }}} and Essential work with almost all workloads that TiDB supports, but there are some feature differences compared with TiDB Self-Managed or TiDB Cloud Dedicated clusters. This document describes the limitations of {{{ .starter }}} and {{{ .essential }}}.

We are constantly filling in the feature gaps between {{{ .starter }}}/Essential and TiDB Cloud Dedicated. If you require these features or capabilities in the gap, use [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) or [contact us](https://www.pingcap.com/contact-us/?from=en) for a feature request.

## Limitations

### Audit logs

- [Database audit logging](/tidb-cloud/tidb-cloud-auditing.md) is currently unavailable.

### Connection

- Only [Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) and [Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) can be used. You cannot use [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to connect to {{{ .starter }}} or {{{ .essential }}} clusters. 
- No [Firewall Rules](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md) support for Private Endpoint.

> **Note:**
> Due to the [limitations of AWS Global Accelerator](https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html#about-idle-timeout), the idle timeout for a Public Endpoint network connection on AWS is 340 seconds. Additionally, you cannot use TCP keep-alive packets to maintain an open connection to the public endpoint on AWS because of the same limitation.
>

### Encryption

- Data persisted in your {{{ .starter }}} or {{{ .essential }}} cluster is encrypted using the encryption tool provided by the cloud provider that manages your cluster. For {{{ .starter }}} (with spending limit > 0) and {{{ .essential }}} clusters, an optional second layer of encryption is available during the cluster creation process, providing an additional level of security beyond the default encryption at rest.
- Using [customer-managed encryption keys (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek.md) is currently unavailable.

### Maintenance window

- [Maintenance window](/tidb-cloud/configure-maintenance-window.md) is currently unavailable.

### Monitoring and diagnosis

- [Third-party Monitoring integrations](/tidb-cloud/third-party-monitoring-integrations.md) are currently unavailable.
- [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md) is currently unavailable.
- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) is currently unavailable.

### Self-service upgrades

- {{{ .starter }}} and {{{ .essential }}} are fully managed deployments of TiDB. Major and minor version upgrades of {{{ .starter }}} and {{{ .essential }}} are handled by TiDB Cloud and therefore cannot be initiated by users.

### Stream data

- [Changefeed](/tidb-cloud/changefeed-overview.md) is not supported for {{{ .starter }}} and {{{ .essential }}} currently.
- [Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) is not supported for {{{ .starter }}} and {{{ .essential }}} currently.

### Time to live (TTL)

- In {{{ .starter }}} and {{{ .essential }}}, the [`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) attribute for a table is fixed at `15m` and cannot be modified. This means that {{{ .starter }}} and {{{ .essential }}} schedule a background job every 15 minutes to clean up expired data.

### Others

- Transaction can not last longer than 30 minutes.
- For more details about SQL limitations, refer to [Limited SQL Features](/tidb-cloud/limited-sql-features.md).

## Usage quota

For each organization in TiDB Cloud, you can create a maximum of five [free {{{ .starter }}} clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) by default. To create more {{{ .starter }}} clusters, you need to add a credit card and [set a monthly spending limit](/tidb-cloud/manage-serverless-spend-limit.md) for the usage.

For the first five {{{ .starter }}} clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. It is a metric that allows you to estimate the computational resources required to process a specific request in the database. The request unit is also the billing unit for {{{ .starter }}} service.

Once a cluster reaches its usage quota, it immediately denies any new connection attempts until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/).

If you want to create a {{{ .starter }}} cluster with an additional quota, you can set the monthly spending limit on the cluster creation page. For more information, see [Create a {{{ .starter }}} cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

After creating a {{{ .starter }}} cluster, you can still check and edit the spending limit on your cluster overview page. For more information, see [Manage Spending Limit for {{{ .starter }}} Clusters](/tidb-cloud/manage-serverless-spend-limit.md).
