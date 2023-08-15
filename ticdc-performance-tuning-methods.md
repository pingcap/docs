---
title: TiCDC Performance Analysis and Optimization Methods
summary: Introduces the TiCDC metrics on the Performance Overview dashboard, helping you understand and monitor the workload of TiCDC.
---

# TiCDC Performance Analysis and Optimization Methods

This document introduces resource utilization and key performance metrics of TiCDC. You can monitor and evaluate TiCDC performance on data replication through the [CDC panel](/grafana-performance-overview-dashboard.md#cdc) on the Performance Overview dashboard.

## Resource utilization of a TiCDC cluster

With the following three metrics, you can quickly get the resource utilization of a TiCDC cluster:

- CPU usage: the CPU usage per TiCDC node.
- Memory usage: the memory usage per TiCDC node.
- Goroutine count: the number of goroutines per TiCDC node.

## Key metrics for TiCDC data replication

### TiCDC overall metrics

With the following metrics, you can get an overview of TiCDC data replication:

- Changefeed checkpoint lag: the progress lag of data replication between the upstream and the downstream, measured in seconds.

    If the speed at which TiCDC consumes data and writes downstream can keep up with upstream data changes, this metric remains within a small latency range, typically within 10 seconds. Otherwise, this metric will continue to increase.

    When this metric (that is, TiCDC checkpoint lag) increases, common reasons are as follows:

    - Insufficient system resources: if the CPU, memory, or disk space of TiCDC is insufficient, it might cause data processing to be too slow, which results in a long checkpoint of the TiCDC changefeed.
    - Network issues: if network interruptions, lags, or insufficient bandwidth occur in TiCDC, it might affect data transfer speed, which results in a long checkpoint of the TiCDC changefeed.
    - High QPS in the upstream: if the data to be processed by TiCDC is excessively large, it might cause data processing timeouts, which results in an increased checkpoint of the TiCDC changefeed. Typically, a single TiCDC node can handle a maximum QPS of around 60K.
    - Database issues:
        - The gap between the `min resolved ts` of the upstream TiKV cluster and the latest PD TSO is significant. This is usually due to that TiKV fails to advance the resolved ts in time when the write load of the upstream is excessively heavy.
        - The write latency in downstream databases is high, blocking TiCDC from replicating data to the downstream in a timely manner.

- Changefeed resolved ts lag: the progress difference between the internal replication status of a TiCDC node and the upstream, measured in seconds. If this metric is high, it indicates that the data processing capability of the TiCDC Puller or Sorter module might be insufficient, or there might be network latency or slow disk read/write speed issues. In such cases, to ensure the efficient and stable operation of TiCDC, you need to take appropriate measures, such as increasing the number of TiCDC instances or optimizing the network configuration.
- The status of changefeeds: for status explanations of changefeeds, see [Changefeed state transfer](/ticdc/ticdc-changefeed-overview.md).

Example 1: high upstream QPS causes high checkpoint lag when a single TiCDC node is used

As shown in the following diagram, because the upstream QPS is excessively high and there is only one TiCDC node in the cluster, the TiCDC node is overloaded. The CPU usage is high, and both Changefeed checkpoint lag and Changefeed resolved ts lag keep increasing. The status of changefeeds intermittently transitions from 0 to 1, indicating ongoing changefeed errors. You can attempt to resolve this issue by:

- Adding TiCDC nodes: Expand the TiCDC cluster to multiple nodes to increase processing capacity.
- Optimizing resources for TiCDC nodes: Enhance CPU and memory configurations of TiCDC nodes to improve performance.

![TiCDC overview](/media/performance/cdc/cdc-slow.png)

### Data Flow Throughput Metrics and Downstream Latency Information

Using the following metrics, you can understand data flow throughput and downstream latency information:

- Puller output events/s: The rate at which the Puller module in TiCDC nodes outputs data change rows to the Sorter module per second.
- Sorter output events/s: The rate at which the Sorter module in TiCDC nodes outputs rows to the Mounter module per second.
- Mounter output events/s: The rate at which the Mounter module in TiCDC nodes outputs rows to the Sink module per second.
- Table sink output events/s: The rate at which the Table Sorter module in TiCDC nodes outputs rows to the Sink module per second.
- SinkV2 - Sink flush rows/s: The rate at which the Sink module in TiCDC nodes outputs rows to the downstream per second.
- Transaction Sink Full Flush Duration: The average and p999 latency of writing downstream transactions in the MySQL Sink module of TiCDC nodes.
- MQ Worker Send Message Duration Percentile: The latency of MQ worker sending messages to Kafka downstream.
- Kafka Outgoing Bytes: The workload of MQ writing downstream transactions.

Example 2: Impact of Downstream Database Write Speed on TiCDC Data Replication Performance

As shown in the figure below, both upstream and downstream in this environment are TiDB clusters. The value of `TiCDC Puller output events/s` confirms the QPS value of the upstream database. The `Transaction Sink Full Flush Duration` indicates that the average write latency of the downstream database is high during the first load period, whereas it is low during the second load period.

- During the first load period, slow data writing in the downstream TiDB cluster causes TiCDC's data consumption rate to fall behind the upstream QPS, leading to a continuous increase in Changefeed checkpoint lag. However, Changefeed resolved ts lag remains within 300 milliseconds, indicating that replication latency and throughput bottlenecks are not in the puller and sorter modules, but in the downstream sink module.
- During the second load period, due to the fast data writing speed in the downstream TiDB cluster, TiCDC's data replication rate fully catches up with the upstream speed, resulting in Changefeed checkpoint lag and Changefeed resolved ts lag staying within 500 milliseconds. At this point, TiCDC's replication speed is relatively ideal.

![TiCDC overview](/media/performance/cdc/cdc-fast-1.png)

![data flow and txn latency](/media/performance/cdc/cdc-fast-2.png)
