---
title: TiDB Cloud Releases
summary: Learn about TiDB Cloud release notes, kernel versioning, and maintenance notifications.
---

# TiDB Cloud Releases

[TiDB Cloud](https://www.pingcap.com/tidb/cloud/) is a fully managed Database-as-a-Service (DBaaS) that brings [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source Hybrid Transactional and Analytical Processing (HTAP) database, to your cloud.

TiDB Cloud offers two types of releases: [cloud platform releases](#cloud-platform-release-notes) and [database kernel releases](#database-kernel-release-notes). They follow independent release cycles and are documented separately.

## Cloud platform release notes

Cloud platform releases cover the TiDB Cloud console, APIs, and control plane, including new plan features, UI changes, integrations, and operational improvements across all TiDB Cloud plans.

- [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md)

## Database kernel release notes

The database kernel is the core engine that processes your SQL queries and manages your data. Depending on your TiDB Cloud plan, your resources run on different kernels, each with its own release cadence.

| Plan | Kernel information and release notes |
| --- | --- |
| TiDB Cloud **Starter** and **Essential** | Running on a customized [TiDB X](/tidb-cloud/tidb-x-architecture.md) engine based on the classic [TiDB v8.5.3](/releases/release-8.5.3.md) kernel. |
| TiDB Cloud **Premium** | Running on the [`TiDB-X-CLOUD.202510.1`](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) version of the [TiDB X](/tidb-cloud/tidb-x-architecture.md) kernel. |
| TiDB Cloud **Dedicated** | Running on the classic TiDB kernel, and the kernel version corresponds directly to TiDB Self-Managed versions. Currently, the default TiDB version of newly created TiDB Cloud Dedicated clusters is [v8.5.7](/releases/release-8.5.7.md). |

> **Note:**
>
> By default, TiDB Cloud Essential instances run on a customized TiDB X engine based on the classic TiDB v8.5.3 kernel. If you want to run your TiDB Cloud Essential instances on [`TiDB-X-CLOUD.202510.1`](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) as TiDB Cloud Premium, contact [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support). 

## Maintenance notifications

TiDB Cloud maintenance notifications provide information about scheduled maintenance activities that might affect your TiDB Cloud services. For the list of notifications, see the navigation pane on the left.
