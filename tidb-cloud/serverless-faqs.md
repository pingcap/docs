---
title: TiDB Cloud Starter FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Starter.
---

# TiDB Cloud Starter FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud Starter.

## General FAQs

### What is TiDB Cloud Starter?

TiDB Cloud Starter offers the TiDB database with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### How do I get started with TiDB Cloud Starter?

Get started with the 5-minute [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md).

### How many TiDB Cloud Starter clusters can I create in TiDB Cloud?

For each organization in TiDB Cloud, you can create a maximum of five [free clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan) by default.

### Are all TiDB Cloud features fully supported on TiDB Cloud Starter?

Some of TiDB Cloud features are partially supported or not supported on TiDB Cloud Starter. For more information, see [TiDB Cloud Starter Limitations and Quotas](/tidb-cloud/serverless-limitations.md).

### When will TiDB Cloud Starter be available on cloud platforms other than Alibaba Cloud, such as Google Cloud or AWS?

We are actively working on expanding TiDB Cloud Starter to other cloud platforms, including Google Cloud and AWS. However, we do not have an exact timeline for now as we currently focus on filling gaps and ensuring seamless functionality across all environments. Rest assured, we are working hard to make TiDB Cloud Starter available on more cloud platforms, and we will keep our community updated as we progress.

### What is columnar storage in TiDB Cloud Starter?

Columnar storage in TiDB Cloud Starter acts as an additional replica of row-based storage, ensuring strong consistency. Unlike traditional row-based storage, which stores data in rows, columnar storage organizes data in columns, optimizing it for data analytics tasks.

Columnar storage is a key feature that enables the Hybrid Transactional and Analytical Processing (HTAP) capabilities of TiDB by seamlessly blending transactional and analytical workloads.

To efficiently manage columnar storage data, TiDB Cloud Starter uses a separate elastic TiFlash engine. During query execution, the optimizer guides the cluster to automatically decide whether to retrieve data from row-based or columnar storage.

### When should I use columnar storage in TiDB Cloud Starter?

Consider using columnar storage in TiDB Cloud Starter in the following scenarios:

- Your workload involves analytical tasks that require efficient data scanning and aggregation.
- You prioritize improved performance, especially for analytics workloads.
- You want to isolate analytical processing from transactional processing to prevent performance impact on your transactional processing (TP) workload. The separate columnar storage helps optimize these distinct workload patterns.

In these scenarios, columnar storage can significantly improve query performance and provide a seamless experience for mixed workloads in your system.

### How to use columnar storage in TiDB Cloud Starter?

Using columnar storage in TiDB Cloud Starter is similar to using it in TiFlash. You can enable columnar storage at both the table and database levels:

- Table level: Assign a TiFlash replica to a table to enable columnar storage for that specific table.
- Database level: Configure TiFlash replicas for all tables in a database to use columnar storage across the entire database.

Once a TiFlash replica is set up for a table, TiDB automatically replicates data from the row-based storage to the columnar storage for that table. This ensures data consistency and optimizes performance for analytical queries.

For more information about how to set up TiFlash replicas, see [Create TiFlash replicas](/tiflash/create-tiflash-replicas.md).

## Billing and metering FAQs

### What are Request Units?

TiDB Cloud Starter adopts a pay-as-you-go model, meaning that you only pay for the storage space and cluster usage. In this model, all cluster activities such as SQL queries, bulk operations, and background jobs are quantified in [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit). RU is an abstract measurement for the size and intricacy of requests initiated on your cluster. For more information, see [TiDB Cloud Starter Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/).

### Is there any free plan available for TiDB Cloud Starter?

For the first five TiDB Cloud Starter clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

For a free cluster, once the free quota is reached, the read and write operations on this cluster will be throttled until you add a spending limit or the usage is reset upon the start of a new month.

For more information, see [TiDB Cloud Starter usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### What are the limitations of the free plan?

Under the free plan, cluster performance is limited due to non-scalable compute resources. This results in a restriction on memory allocation per query to 256 MiB and might cause observable bottlenecks in request units (RUs) per second. To maximize cluster performance and avoid these limitations, you can add a spending limit.

### How can I estimate the number of RUs required by my workloads and plan my monthly budget?

To get the RU consumption of individual SQL statements, you can use the [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL statement. However, it is important to note that the RUs usage returned in `EXPLAIN ANALYZE` does not incorporate egress RUs, as egress usage is measured separately in the gateway, which is unknown to the TiDB server.

To get the RUs and storage used by your cluster, view the **Usage this month** pane on your cluster overview page. With your past resource usage data and real-time resource usage in this pane, you can track your cluster's resource consumption and estimate a reasonable spending limit. If the free quota cannot meet your requirements, you can edit the spending limit. For more information, see [TiDB Cloud Starter usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### How can I optimize my workload to minimize the number of RUs consumed?

Ensure that your queries have been carefully optimized for optimal performance by following the guidelines in [Optimizing SQL Performance](/develop/dev-guide-optimize-sql-overview.md). To identify the SQL statements that consume the most RUs, navigate to **Diagnosis > SQL Statements** on your cluster overview page, where you can observe SQL execution and view the top statements sorted by **Total RU** or **Mean RU**. For more information, see [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis). In addition, minimizing the amount of egress traffic is also crucial for reducing RUs consumption. To achieve this, it is recommended to return only the necessary columns and rows in your query, which in turn helps reduce network egress traffic. This can be achieved by carefully selecting and filtering the columns and rows to be returned, thereby optimizing network utilization.

### How storage is metered for TiDB Cloud Starter？

The storage is metered based on the amount of data stored in a TiDB Cloud Starter cluster, measured in GiB per month. It is calculated by multiplying the total size of all the tables and indexes (excluding data compression or replicas) with the number of hours the data is stored in that month.

### Why does the storage usage size remain unchanged after dropping a table or database immediately?

This is because TiDB retains dropped tables and databases for a certain period of time. This retention period ensures that transactions dependent on these tables can continue execution without disruption. Additionally, the retention period makes the [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)/[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) feature feasible, which allows you to recover dropped tables and databases if they were mistakenly deleted.

### Why are there RU consumptions when I'm not actively running any queries?

RU consumptions can occur in various scenarios. One common scenario is during background queries, such as synchronizing schema changes between TiDB instances. Another scenario is when certain web console features generate queries, like loading schemas. These processes use RUs even without explicit user triggers.

### Why is there a spike in RU usage when my workload is steady?

A spike in RU usage can occur due to necessary background jobs in TiDB. These jobs, such as automatically analyzing tables and rebuilding statistics, are required for generating optimized query plans.

### What happens when my cluster exhausts its free quota or exceeds its spending limit?

Once a cluster reaches its free quota or spending limit, the cluster immediately denies any new connection attempts until the quota is increased or the usage is reset at the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling. For more information, see [TiDB Cloud Starter Limitations and Quotas](/tidb-cloud/serverless-limitations.md#usage-quota).

### Why do I observe spikes in RU usage while importing data?

During the data import process of a TiDB Cloud Starter cluster, RU consumption occurs only when the data is successfully imported, which leads to spikes in RU usage.

### What costs are involved when using columnar storage in TiDB Cloud Starter?

The pricing for columnar storage in TiDB Cloud Starter is similar to that for row-based storage. When you use columnar storage, an additional replica is created to store your data (without indexes). The replication of data from row-based to columnar storage does not incur extra charges.

For detailed pricing information, see [TiDB Cloud Starter pricing details](https://www.pingcap.com/tidb-serverless-pricing-details/).

### Is using columnar storage more expensive?

Columnar storage in TiDB Cloud Starter incurs additional costs due to the extra replica, which requires more storage and resources for data replication. However, columnar storage becomes more cost-effective when running analytical queries.

According to the TPC-H benchmark test, the cost of running analytic queries on columnar storage is about one-third of the cost when using row-based storage.

Therefore, while there might be an initial cost due to the extra replica, the reduced computational costs during analytics can make it more cost-effective for specific use cases. Especially for users with analytical demands, columnar storage can significantly reduce costs, offering considerable cost savings opportunities.

## Security FAQs

### Is my TiDB Cloud Starter shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared.

### How does TiDB Cloud Starter ensure security?

- Your connections are encrypted by Transport Layer Security (TLS). For more information about using TLS to connect to TiDB Cloud Starter, see [TLS Connection to TiDB Cloud](/tidb-cloud/secure-connections-to-serverless-clusters.md).
- All persisted data on TiDB Cloud Starter is encrypted-at-rest using the tool of the cloud provider that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB that my cluster is running on?

No. TiDB Cloud Starter clusters are upgraded automatically as we roll out new TiDB versions on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud console](https://console.tidb.io/clusters). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to check the TiDB version.
