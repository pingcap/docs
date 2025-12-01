---
title: Data Streaming
summary: Learn about data streaming concepts for TiDB Cloud.
---

# Data Streaming

TiDB Cloud lets you stream data changes from your TiDB Cluster to other systems such as Apache Kafka, MySQL, and object storage.

- For TiDB Cloud Dedicated, you can stream data to Apache Kafka, Apache Pulsar, MySQL, TiDB Cloud Serverless, and cloud storage.
- For TiDB Cloud Serverless, you can stream data to Apache Kafka.

## Changefeed

TiDB Cloud changefeed is a continuous data stream that helps you replicate data changes from TiDB Cloud to other data services.

- For TiDB Cloud Dedicated, you can access the changefeed feature on the **Changefeed** page in the [TiDB Cloud console](https://tidbcloud.com/).
- For TiDB Cloud Serverless, you can use the changefeed feature in [TiDB Cloud CLI](/tidb-cloud/get-started-with-cli).

You can create a changefeed, view a list of existing changefeeds, and operate the existing changefeeds (such as scaling, pausing, resuming, editing, and deleting a changefeed).

Replication includes only incremental data changes by default. If existing data must be replicated, it must be exported and loaded into the target system manually before starting the changefeed.

In TiDB Cloud, replication can be tailored by defining table filters (to specify which tables to replicate) and event filters (to include or exclude specific types of events such as `INSERT` or `DELETE`).

For more information, see [Changefeed for TiDB Cloud Dedicated](/tidb-cloud/changefeed-overview.md) and [Changefeed for TiDB Cloud Serverless](/tidb-cloud/serverless-changefeed-overview.md).