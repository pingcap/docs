---
title: TiDB Cloud Releases
summary: Learn about TiDB Cloud release notes and maintenance notifications.
---

# TiDB Cloud Releases

[TiDB Cloud](https://www.pingcap.com/tidb/cloud/) is a fully managed Database-as-a-Service (DBaaS) that brings [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source Hybrid Transactional and Analytical Processing (HTAP) database, to your cloud. TiDB Cloud offers an easy way to deploy and manage databases to let you focus on your applications, not the complexities of databases. This document provides an overview of TiDB Cloud release notes and maintenance notifications.

## Release notes

<<<<<<< HEAD
TiDB Cloud release notes provide information about new features and improvements in each release. For detailed release notes, see [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md).
=======
## Cloud platform release notes

Cloud platform releases cover the TiDB Cloud console, APIs, and control plane, including new plan features, UI changes, integrations, and operational improvements across all TiDB Cloud plans.

- [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md)

## Database kernel release notes

The database kernel is the core engine that processes your SQL queries and manages your data. Depending on your TiDB Cloud plan, your resources run on different kernels, each with its own release cadence.

| Plan | Kernel | Default kernel version for newly created instances or clusters |
| --- | --- | --- |
| TiDB Cloud **Starter** | Running on a customized [TiDB X](/tidb-cloud/tidb-x-architecture.md) engine based on the classic TiDB kernel. | [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) |
| TiDB Cloud **Essential** | TiDB Cloud Essential instances created on or after June 30, 2026, are running on the [TiDB X](/tidb-cloud/tidb-x-architecture.md) kernel. | [TiDB-X-CLOUD.202603.1](/tidb-cloud/releases/tidb-x-cloud.202603.1.md) |
| TiDB Cloud **Premium** | Running on the [TiDB X](/tidb-cloud/tidb-x-architecture.md) kernel. | [TiDB-X-CLOUD.202603.1](/tidb-cloud/releases/tidb-x-cloud.202603.1.md) |
| TiDB Cloud **Dedicated** | Running on the classic TiDB kernel. | [TiDB v8.5.8](https://docs.pingcap.com/tidb/stable/release-8.5.8/) |
>>>>>>> 6696674461 (cloud: add tidb-x-cloud.202603.1.md (#23458))

## Maintenance notifications

TiDB Cloud maintenance notifications provide information about scheduled maintenance activities that might affect your TiDB Cloud services.
