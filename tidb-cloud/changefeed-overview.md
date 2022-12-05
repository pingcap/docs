---
title: Changefeed
---

# Changefeed

TiDB Cloud provides the following changefeeds to help you stream data from TiDB Cloud:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-tcu.md).

> **Note:**
>
> If you have want to use the Changefeed feature, make sure that your TiDB cluster version is at least v6.4.0 and the TiKV node size is at least 8 vCPU and 16 GiB.
>
> You cannot [pause your cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md) if it has any changefeeds. You need to delete the existing changefeeds ([Delete Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#manage-the-changefeed) and [Delete Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink)) before pausing the cluster.