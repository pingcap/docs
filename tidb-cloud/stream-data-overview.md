---
title: Stream Data
summary: Learn about the options for streaming data changes from TiDB Cloud to downstream systems, including Changefeed and Data Pipeline.
---

# Stream Data

TiDB Cloud can continuously stream data changes from your TiDB Cloud instance to downstream systems. It provides the following options for streaming data:

- **Changefeed**: streams incremental row changes to downstream systems such as Apache Kafka, MySQL, TiDB Cloud, and cloud storage.
- **Data Pipeline**: exports a full snapshot of the selected data and then continuously replicates row changes to TiDB Cloud Lake.

## Changefeed

A changefeed streams incremental data changes from TiDB Cloud to a downstream system. Use it when you only need to continuously replicate incremental changes and the downstream system can consume incremental events.

You can create and manage changefeeds on the **Changefeed** page in the TiDB Cloud console. For more information, see [Changefeed](/tidb-cloud/changefeed-overview.md).

## Data Pipeline (PREVIEW)

A data pipeline replicates full data and incremental changes from your TiDB Cloud instance to TiDB Cloud Lake. It uses an external stage, such as Amazon S3 or Alibaba Cloud OSS, to buffer data between the source and the destination, which improves reliability and gives you control over cost and latency. For more information, see [Data Pipeline](/tidb-cloud/data-pipeline.md).

> **Note:**
>
> The Data Pipeline feature in the TiDB Cloud console is currently in private preview and is available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, enter "Apply for `Data Pipeline to TiDB Cloud Lake`" in the **Description** field, and then click **Submit**.
