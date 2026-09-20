---
title: Data Pipeline to TiDB Cloud Lake
summary: TiDB Cloud Data Pipeline replicates full and incremental data from your TiDB Cloud instance to TiDB Cloud Lake without a third-party ETL tool.
---

# Data Pipeline to TiDB Cloud Lake

TiDB Cloud Data Pipeline replicates full and incremental data from your TiDB Cloud instance to TiDB Cloud Lake, without requiring a third-party ETL tool. It first exports a full snapshot of the selected source data, and then continuously replicates row changes so that the data in TiDB Cloud Lake stays up to date.

You can use Data Pipeline for:

- **One-time data loading**: export a full snapshot to TiDB Cloud Lake for initial data loading or migration.
- **Continuous data synchronization**: keep TiDB Cloud Lake in sync with your TiDB Cloud instance for analytics and reporting workloads.

## How it works

A data pipeline operates in two phases:

1. **Full snapshot export**: a one-time export of the selected source tables to TiDB Cloud Lake.
2. **Incremental replication**: continuous capture and replication of row changes (inserts, updates, and deletes) so that TiDB Cloud Lake stays current with the source.

You can also run a full-export-only pipeline if you need a one-time snapshot without ongoing replication.

An **external stage** (Amazon S3 or Alibaba Cloud OSS) is used as the intermediate storage between your TiDB Cloud instance and TiDB Cloud Lake. TiDB Cloud writes exported snapshots and captured row changes to the stage, and TiDB Cloud Lake loads data from the stage into the target warehouse. This decouples the write rate from the consumption rate, improving reliability and giving you control over cost and latency.

For more information, see [Data Pipeline FAQ](/tidb-cloud/pipeline/lake-data-pipeline-faq.md).

## Availability

| Plan | Status |
| ---- | ------ |
| {{{ .premium }}} | Private preview |
| {{{ .essential }}} | Manual setup |

For setup instructions, refer to the guide that matches your plan:

- [Set Up Data Pipeline to TiDB Cloud Lake ({{{ .premium }}})](/tidb-cloud/pipeline/setup-lake-data-pipeline-for-premium.md)
- [Set Up Data Pipeline to TiDB Cloud Lake ({{{ .essential }}})](/tidb-cloud/pipeline/setup-lake-data-pipeline-for-essential.md)

> **Note:**
>
> Data Pipeline currently supports TiDB Cloud Lake as the destination. More destinations will be supported in the future to enable a broader range of data movement and migration scenarios within TiDB Cloud.

## What's next

- [Create and manage a data pipeline from your {{{ .premium }}} instance to TiDB Cloud Lake.](/tidb-cloud/pipeline/setup-lake-data-pipeline-for-premium.md)
- [TiDB Lake Data Pipeline DDL, DML, and type support reference.](/tidb-cloud/pipeline/lake-data-pipeline-support-matrix.md)
- [Data Pipeline FAQ.](/tidb-cloud/pipeline/lake-data-pipeline-faq.md)
