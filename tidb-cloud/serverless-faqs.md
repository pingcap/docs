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

### What are the limitations of a TiDB Serverless cluster?

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spend limit](/tidb-cloud/tidb-cloud-glossary.md#spend-limit) for the usage.

Some of TiDB Cloud features are partially supported or not supported on TiDB Serverless. See [TiDB Serverless Limitations and Quotas](/tidb-cloud/serverless-limitations.md) for details.

### When will TiDB serverless be available on cloud platforms other than AWS, such as GCP or Azure?

We are constantly working to bring TiDB serverless to other cloud platforms, including GCP and Azure. However, we can't give an exact timeline yet as we are still in the process of filling gaps and ensuring that the service works seamlessly in all environments. Rest assured that we are working hard to make TiDB serverless available on more cloud platforms, and we will keep our community updated once we have more information.

### I created a Developer Tier cluster before TiDB Serverless was available. Can I still use my cluster?

Yes, your Developer Tier cluster has been automatically migrated to the TiDB Serverless cluster, providing you with an improved user experience without any disruptions to your prior usage.

## Billing and Metering FAQs

### What are Request Units?

TiDB Serverless adopts a pay-as-you-go model, which entails that you only pay for the storage space and usage of your cluster. In this model, all cluster activities such as SQL queries, bulk operations, and background jobs are quantified in [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit). RUs offer an abstract measurement of the size and intricacy of requests initiated on your cluster. See [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/) for more information.

### Is there any free plan available for TiDB Serverless?

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:
- Row storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

Usage beyond the free quota will be charged. Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit) or the usage is reset upon the start of a new month.

For more information, see [TiDB Serverless usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### How can I estimate the number of RUs required by my workloads and plan for monthly budget?

To estimate the RU consumption of individual SQL statements, you can use the [EXPLAIN ANALYZE](/sql-statements/sql-statement-explain-analyze.md) SQL statement. You can see the RUs and storage your cluster has used in the Usage this month section of the Cluster Overview page. With past resource usage data and real-time resource usage graphs available on the Usage this month page, you can establish a reasonable spend limit for your cluster with the Edit Spend Limit feature. See [Manage Spend Limit for TiDB Serverless clusters](/tidb-cloud/manage-serverless-spend-limit.md) for more information.

### How the storage is being metered for TiDB Serverless

The storage is metered based on the amount of data stored in the TiDB cluster, measured in GB-months. This calculation is based on the sum of the size of all the tables and indexes in the cluster, without including data compression or replicas for high availability, and is multiplied by the number of hours the data is stored in the month.

### Why does the storage used size remain unchanged after dropping a table or database immediately?

TiDB retains dropped tables and databases for a period of time to ensure that transactions that depend on these tables can continue to run smoothly. Moreover, the extended retention time enables TiDB to provide the [FLASHBACK TABLE](/sql-statements/sql-statement-flashback-table.md)/[FLASHBACK DATABASE](/sql-statements/sql-statement-flashback-database.md) feature, which allows you to recover dropped tables and databases in the event that they were mistakenly deleted.

### Why are there RU consumptions when I'm not actively running any query?

RU consumptions can occur in various scenarios. One common scenario is during background queries, such as the synchronization of schema changes between TiDB instances. Another scenario is when certain web console features generate queries, like loading schemas. These processes utilize RUs even without explicit user triggers.

### Why there is spike in RU usage when my workload is steady?

A spike in RU usage can occur due to necessary background jobs in TiDB. These jobs, such as automatically analyzing tables and rebuilding statistic data, are required for generating optimized query plans.

## Security FAQs

### Is my TiDB Serverless shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared. To get managed TiDB service with isolated infrastructure and resources, you can upgrade it to [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated).

### How does TiDB Serverless ensure security?

- Your connections are encrypted by Transport Layer Security (TLS). For more information about using TLS to connect to TiDB Serverless, see [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).
- All persisted data on TiDB Serverless is encrypted-at-rest using the tool of the cloud provider that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB that my cluster is running on?

No. TiDB Serverless clusters are upgraded automatically as we roll out new TiDB versions on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud console](https://tidbcloud.com/console/clusters) or in the latest [release note](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to check the TiDB version.
