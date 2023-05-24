---
title: TiDB Serverless FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Serverless.
---

# TiDB Serverless FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Serverless.

## General FAQs

### What is TiDB Serverless?

TiDB Serverless offers the TiDB database with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### How do I get started with TiDB Serverless?

Get started with the 5-minute [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md).

### Is TiDB Serverless free during beta?

Until May 31, 2023, TiDB Serverless clusters are still free, with a 100% discount off. After that, usage beyond the free quota will be charged. Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit) or the usage is reset upon the start of a new month.

For more information, see [TiDB Serverless usage quota](/tidb-cloud/select-cluster-tier.md#usage-quota).

### What does it mean for beta release?

TiDB Serverless is in beta while we continuously add new features and improve existing features before it becomes generally available. We do not provide SLA for beta products. Therefore, TiDB Serverless should **NOT** be used in production currently.

### What are the limitations of a TiDB Serverless cluster in beta?

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spend limit](/tidb-cloud/tidb-cloud-glossary.md#spend-limit) for the usage.

Some of TiDB Cloud features are partially supported or not supported on TiDB Serverless. See [TiDB Serverless Limitations and Quotas](/tidb-cloud/serverless-tier-limitations.md) for details.

### What can TiDB Serverless be used for?

You can use your TiDB Serverless cluster for non-production workloads such as prototype applications, development environments, hackathons, and academic courses, or to provide temporary data service for your datasets.

### I created a Developer Tier cluster before TiDB Serverless was available. Can I still use my cluster?

Yes, your Developer Tier cluster will be automatically migrated to the TiDB Serverless cluster soon. Your ability to use your cluster should not be affected, and you will have the same improved TiDB Serverless user experiences.

## Security FAQs

### Is my TiDB Serverless shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared. To get managed TiDB service with isolated infrastructure and resources, you can upgrade it to [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

### How does TiDB Serverless ensure security?

- Your connections are encrypted by Transport Layer Security (TLS). For more information about using TLS to connect to TiDB Serverless, see [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).
- All persisted data on TiDB Serverless is encrypted-at-rest using the tool of the cloud provider that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB that my cluster is running on?

No. TiDB Serverless clusters are upgraded automatically as we roll out new TiDB versions on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud console](https://tidbcloud.com/console/clusters) or in the latest [release note](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to check the TiDB version.
