---
title: Serverless Tier FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Serverless Tier.
---

# Serverless Tier FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud Serverless Tier.

## General FAQs

### What is Serverless Tier?

TiDB Cloud Serverless Tier delivers the free starter TiDB clusters with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### How do I get started with Serverless Tier?

Get started with the 5-minute [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md).

### What are the limitations of a Serverless Tier cluster?

- For each TiDB Cloud account, you can create one complimentary Serverless Tier cluster to use during the beta phase. You need to delete the existing Serverless Tier cluster then create a new one.
- Each Serverless Tier cluster has the following limitations:
    - The storage size is limited to 5 GiB (logical size) of OLTP storage and 5 GiB of OLAP storage.
    - The compute resource is limited to 1 vCPU and 1 GiB RAM.
- There are some features that Serverless Tier does not support or partially supports. See [Serverless Tier Limitations](/tidb-cloud/serverless-tier-limitations.md) for details.

### Is Serverless Tier free during beta?

Yes. Serverless Tier cluster is free to use during beta phase. When Serverless Tier goes GA, we will still offer a free starter plan and have a usage-based billing plan for additional resources and maintain higher performance.

### What does it mean for beta release?

Serverless Tier is in beta while we continue to add new features and improve existing features before it becomes generally available. We do not provide SLA for beta products, therefore it should **not** be used in production.

### What Serverless Tier can be used for?

You can use your Serverless Tier cluster for non-production workloads such as prototype applications, development environments, hackathons, and academic courses, or to provide temporary data service for your datasets.

### I created a Developer Tier cluster before Serverless Tier was available. Can I still use my cluster?

  Yes, your free cluster will be automatically migrated to the Serverless Tier soon. Your ability to use your cluster should not be affected and will have the same improved Serverless Tier user experiences.

## Security FAQs

### Is my Serverless Tier shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared. Upgrade to Dedicated Tier for managed TiDB service with isolated infrastructure and resources.

### How does TiDB Serverless Tier ensure security?

- All traffic data(both internal and external) is encrypted by Transport Layer Security (TLS). For using TLS to connect to Serverless Tier, see [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).
- All persisted data on Serverless Tier is encrypted-at-rest using the cloud provider's tool that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB my cluster is running on?

No, Serverless Tier clusters are upgraded automatically as we release the new TiDB version on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud Console](https://tidbcloud.com/console/clusters) or in the latest [release note](https://docs.pingcap.com/tidbcloud/release-notes). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to find the TiDB version.