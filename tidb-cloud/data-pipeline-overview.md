---
title: Data Pipeline to TiDB Cloud Lake
summary: TiDB Cloud Data Pipeline replicates full data and incremental changes from your TiDB Cloud instance to TiDB Cloud Lake without a third-party ETL tool.
---

# Data Pipeline to TiDB Cloud Lake

TiDB Cloud Data Pipeline replicates full data and incremental changes from your TiDB Cloud instance to TiDB Cloud Lake, without requiring a third-party ETL tool. It first exports a full snapshot of the selected source data, and then continuously replicates row changes so that the data in TiDB Cloud Lake stays up to date.

You can use Data Pipeline for the following scenarios:

- **One-time data loading**: export a full snapshot to TiDB Cloud Lake for initial data loading or migration.
- **Continuous data synchronization**: keep TiDB Cloud Lake in sync with your TiDB Cloud instance for analytics and reporting workloads.

## How it works

A data pipeline with continuous replication operates in two phases:

1. **Full snapshot export**: a one-time export of the selected source tables to TiDB Cloud Lake.
2. **Incremental replication**: continuous capture and replication of row changes (inserts, updates, and deletes) so that TiDB Cloud Lake stays current with the source.

You can also configure a pipeline to export only a full snapshot without ongoing replication.

An **external stage** (Amazon S3 or Alibaba Cloud OSS) is used as the intermediate storage between your TiDB Cloud instance and TiDB Cloud Lake. TiDB Cloud writes exported snapshots and captured row changes to the stage, and TiDB Cloud Lake loads data from the stage into the target warehouse. This decouples the write rate from the consumption rate, improving reliability and giving you control over cost and latency.

For more information, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).

## Availability and setup guide

| Plan | Status | Setup Guide |
| ---- | ------ | ----- |
| {{{ .premium }}} | Data pipeline feature in the [TiDB Cloud console](https://tidbcloud.com) is in private preview, and it is available upon request. | [Set Up Data Pipeline to TiDB Cloud Lake ({{{ .premium }}})](/tidb-cloud/data-pipeline-lake-setup-for-premium.md) |
| {{{ .essential }}} | Data pipeline feature in the [TiDB Cloud console](https://tidbcloud.com) is not available yet. Manual setup is required. | [Set Up Data Pipeline to TiDB Cloud Lake ({{{ .essential }}})](/tidb-cloud/data-pipeline-lake-setup-for-essential.md) |

> **Note:**
>
> Data Pipeline currently supports TiDB Cloud Lake as the destination. More destinations will be supported in the future to enable a broader range of data movement and migration scenarios within TiDB Cloud.

## What's next

- [Create and manage a data pipeline from your {{{ .premium }}} instance to TiDB Cloud Lake](/tidb-cloud/data-pipeline-lake-setup-for-premium.md)
- [TiDB Cloud Data Pipeline DDL, DML, and type support reference](/tidb-cloud/data-pipeline-lake-support-matrix.md)
- [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md)
