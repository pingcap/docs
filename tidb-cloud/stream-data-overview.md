---
title: Stream Data
summary: Learn about the options for streaming data changes from TiDB Cloud to downstream systems, including Changefeed and Data Pipeline.
---

# Stream Data

TiDB Cloud can continuously stream data changes from your TiDB Cloud instance to downstream systems, so that those systems stay up to date without a separate batch ETL process. This is useful for near-real-time analytics, data integration, and keeping copies of your data in sync.

TiDB Cloud provides the following options for streaming data:

- **Changefeed**: streams incremental row changes to downstream systems such as Apache Kafka, MySQL, TiDB Cloud, and cloud storage.
- **Data Pipeline**: exports a full snapshot of the selected data and then continuously replicates row changes to TiDB Cloud Lake.

## How it works

Both options capture changes from TiDB Cloud and write them to the target system, but they differ in how much data they move:

- A **Changefeed** replicates row changes (inserts, updates, and deletes) as they occur. You can narrow the replicated data with table filter rules and event filter rules.
- A **Data Pipeline** first exports a full snapshot of the selected source data, and then replicates subsequent row changes so that the target stays consistent with the source.

## Changefeed

A changefeed streams incremental data changes from TiDB Cloud to a downstream system. Use it when you only need ongoing changes and the downstream system can consume incremental events.

You can create and manage changefeeds on the **Changefeed** page in the TiDB Cloud console. For more information, see [Manage Changefeed](/tidb-cloud/changefeed-overview.md).

## Data Pipeline

A data pipeline replicates full data and incremental changes from your TiDB Cloud instance to TiDB Cloud Lake. It uses an external stage, such as Amazon S3 or Alibaba Cloud OSS, to buffer data between the source and the destination, which improves reliability and gives you control over cost and latency.

You can create and manage data pipelines on the **Data Pipeline** page in the TiDB Cloud console. For more information, see [Manage Data Pipeline](/tidb-cloud/data-pipeline-overview.md).

## See also

- [Manage Changefeed](/tidb-cloud/changefeed-overview.md)
- [Manage Data Pipeline](/tidb-cloud/data-pipeline-overview.md)
- [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md)
