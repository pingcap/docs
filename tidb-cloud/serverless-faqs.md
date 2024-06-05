---
title: TiDB Serverless FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Serverless.
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB Serverless FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Serverless.

## General FAQs

### What is TiDB Serverless?

TiDB Serverless offers the TiDB database with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### How do I get started with TiDB Serverless?

Get started with the 5-minute [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md).

### How many TiDB Serverless clusters can I create in TiDB Cloud?

For each organization in TiDB Cloud, you can create a maximum of five [free clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan) by default. To create more TiDB Serverless clusters, you need to add a credit card and create [scalable clusters](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) for the usage.

### Are all TiDB Cloud features fully supported on TiDB Serverless?

Some of TiDB Cloud features are partially supported or not supported on TiDB Serverless. For more information, see [TiDB Serverless Limitations and Quotas](/tidb-cloud/serverless-limitations.md).

### When will TiDB serverless be available on cloud platforms other than AWS, such as Google Cloud or Azure?

We are actively working on expanding TiDB Serverless to other cloud platforms, including Google Cloud and Azure. However, we do not have an exact timeline for now as we currently focus on filling gaps and ensuring seamless functionality across all environments. Rest assured, we are working hard to make TiDB Serverless available on more cloud platforms, and we will keep our community updated as we progress.

### I created a Developer Tier cluster before TiDB Serverless was available. Can I still use my cluster?

Yes, your Developer Tier cluster has been automatically migrated to the TiDB Serverless cluster, providing you with an improved user experience without any disruptions to your prior usage.

### What is columnar storage in TiDB Serverless?

Columnar storage in TiDB Serverless acts as an additional replica of row-based storage, ensuring strong consistency. Unlike the traditional row-based storage that stores data in rows, this is structured in columns, which is particularly optimized for data analytics tasks. 

The columnar storage is a hallmark feature enabling the HTAP (Hybrid Transactional and Analytical Processing) capabilities of TiDB, providing a seamless blend of transactional and analytical capabilities.

To enhance this, TiDB Serverless employs a separate elastic TiFlash engine to effectively handle columnar storage data. During query execution, the cluster, guided by the optimizer, automatically determines whether to source data from the row-based or columnar storage.

### When do I need columnar storage in TiDB Serverless?

You should consider using columnar storage in TiDB Serverless when:

- You are engaging in analytics tasks that require efficient data scanning and aggregation.
- You prioritize improved performance, especially for analytics workloads.
- You want to ensure that analytical operations do not affect the performance of your transactional processing (TP) workload. The separation of columnar storage helps in isolating and optimizing these different types of tasks.

Using columnar storage under these circumstances can enhance query performance and ensure smooth and uninterrupted operations for diverse workloads in your system.

### How to use columnar storage in TiDB Serverless?

Using columnar storage in TiDB Serverless aligns closely with the procedures in TiFlash. You can apply columnar storage at both the table and database levels:

1. By Table: Designate a table's TiFlash replica to utilize columnar storage for that specific table.
2. By Database: Similarly, for the entire database, you can assign TiFlash replicas for all the tables within that database.

After you've set a table's TiFlash replica, the columnar storage for that table will automatically stay in sync with its row-based storage, ensuring data consistency and optimized analytics processing.

For a detailed guide on how to set up TiFlash replicas, you can refer to the [documentation](/tiflash/create-tiflash-replicas.md)

## Billing and metering FAQs

### What are Request Units?

TiDB Serverless adopts a pay-as-you-go model, meaning that you only pay for the storage space and cluster usage. In this model, all cluster activities such as SQL queries, bulk operations, and background jobs are quantified in [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit). RU is an abstract measurement for the size and intricacy of requests initiated on your cluster. For more information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/).

### Is there any free plan available for TiDB Serverless?

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

If you are using a scalable cluster, usage beyond the free quota will be charged. For a free cluster, once the free quota is reached, the read and write operations on this cluster will be throttled until you upgrade to a scalable cluster or the usage is reset upon the start of a new month.

For more information, see [TiDB Serverless usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### What are the limitations of the free plan?

Under the free plan, cluster performance is limited due to non-scalable resources. This results in a restriction on memory allocation per query to 256 MiB and might cause observable bottlenecks in request units (RUs) per second. To maximize cluster performance and avoid these limitations, you can upgrade to a [scalable cluster](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan).

### How can I estimate the number of RUs required by my workloads and plan my monthly budget?

To get the RU consumption of individual SQL statements, you can use the [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL statement. However, it is important to note that the RUs usage returned in `EXPLAIN ANALYZE` does not incorporate egress RUs, as egress usage is measured separately in the gateway, which is unknown to the TiDB server.

To get the RUs and storage used by your cluster, view the **Usage this month** pane on your cluster overview page. With your past resource usage data and real-time resource usage in this pane, you can track your cluster's resource consumption and estimate a reasonable spending limit. If the free quota cannot meet your requirement, you can upgrade to a [scalable cluster](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) and edit the spending limit. For more information, see [TiDB Serverless usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### How can I optimize my workload to minimize the number of RUs consumed?

Ensure that your queries have been carefully optimized for optimal performance by following the guidelines in [Optimizing SQL Performance](/develop/dev-guide-optimize-sql-overview.md). In addition, minimizing the amount of egress traffic is also crucial for reducing RUs consumption. To achieve this, it is recommended to return only the necessary columns and rows in your query, which in turn helps reduce network egress traffic. This can be achieved by carefully selecting and filtering the columns and rows to be returned, thereby optimizing network utilization.

### How storage is metered for TiDB Serverless？

The storage is metered based on the amount of data stored in a TiDB Serverless cluster, measured in GiB per month. It is calculated by multiplying the total size of all the tables and indexes (excluding data compression or replicas) with the number of hours the data is stored in that month.

### Why does the storage usage size remain unchanged after dropping a table or database immediately?

This is because TiDB retains dropped tables and databases for a certain period of time. This retention period ensures that transactions dependent on these tables can continue execution without disruption. Additionally, the retention period makes the [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)/[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) feature feasible, which allows you to recover dropped tables and databases if they were mistakenly deleted.

### Why are there RU consumptions when I'm not actively running any queries?

RU consumptions can occur in various scenarios. One common scenario is during background queries, such as synchronizing schema changes between TiDB instances. Another scenario is when certain web console features generate queries, like loading schemas. These processes use RUs even without explicit user triggers.

### Why is there a spike in RU usage when my workload is steady?

A spike in RU usage can occur due to necessary background jobs in TiDB. These jobs, such as automatically analyzing tables and rebuilding statistics, are required for generating optimized query plans.

### What happens when my cluster exhausts its free quota or exceeds its spending limit?

Once a cluster reaches its free quota or spending limit, the cluster immediately denies any new connection attempts until the quota is increased or the usage is reset at the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling. For more information, see [TiDB Serverless Limitations and Quotas](/tidb-cloud/serverless-limitations.md#usage-quota).

### Why do I observe spikes in RU usage while importing data?

During the data import process of a TiDB Serverless cluster, RU consumption occurs only when the data is successfully imported, which leads to spikes in RU usage.

### What will I pay for when using columnar storage in TiDB Serverless?

The pricing for using columnar storage in TiDB Serverless is generally consistent with the pricing for row-based storage. When opting for columnar storage, you will have an additional replica that contains only the data, without any associated indexes. You do not need to pay for data synchronization from row-base storage to columnar storage.

For detailed pricing specifics and breakdowns related to TiDB Serverless (both row-based and columnar storage), please refer to [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-serverless-pricing-details/).

### Is using columnar storage more expensive?

When using columnar storage in TiDB Serverless, there is an added cost due to the additional replica, which requires more storage and incurs data synchronization overhead. However, it's crucial to note that the cost efficiency comes into play when executing analytical queries.

According to the TPC-H benchmark test, the cost of running analytic queries on columnar storage is about 1/3 of the cost when using row-based storage.

Therefore, while there might be an initial overhead due to the extra replica, the reduced computational costs during analytics can make it more cost-effective for specific use cases. Especially for users with analytical demands, columnar storage can notably reduce costs, offering considerable opportunities for cost savings.

## Security FAQs

### Is my TiDB Serverless shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared. To get managed TiDB service with isolated infrastructure and resources, you can upgrade it to [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated).

### How does TiDB Serverless ensure security?

- Your connections are encrypted by Transport Layer Security (TLS). For more information about using TLS to connect to TiDB Serverless, see [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).
- All persisted data on TiDB Serverless is encrypted-at-rest using the tool of the cloud provider that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB that my cluster is running on?

No. TiDB Serverless clusters are upgraded automatically as we roll out new TiDB versions on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud console](https://tidbcloud.com/console/clusters) or in the latest [release note](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to check the TiDB version.
