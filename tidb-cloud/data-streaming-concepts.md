---
title: Data Streaming
summary: Learn about data streaming concepts for TiDB Cloud.
---

# Data Streaming

TiDB Cloud lets you stream data changes from your TiDB Cluster to other systems like Kafka, MySQL, and object storage.

Currently, TiDB Cloud supports streaming data to Apache Kafka, MySQL, TiDB Cloud and cloud storage.

## Changefeed

TiDB Cloud changefeed is a continuous data stream that helps you replicate data changes from TiDB Cloud to other data services.

On the changefeed page in the TiDB Cloud console, you can create a changefeed, view a list of existing changefeeds, and operate the existing changefeeds (such as scaling, pausing, resuming, editing, and deleting a changefeed).

Replication includes only incremental data changes by default. If existing data must be replicated, it must be exported and loaded into the target system manually before starting the changefeed.

In TiDB Cloud, replication can be tailored by defining table filters (to specify which tables to replicate) and event filters (to include or exclude specific types of events like INSERT or DELETE).

For more information, see [Changefeed](/tidb-cloud/changefeed-overview.md).