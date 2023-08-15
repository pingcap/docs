---
title: TiFlash Performance Analysis and Optimization Methods
summary: Introduces the TiFlash section in the Performance Overview dashboard, helping you understand and monitor TiFlash workload.
---

# TiFlash Performance Analysis and Optimization Methods

This document introduces TiFlash resource utilization and key performance metrics. You can monitor and evaluate the performance of the TiFlash cluster using the [TiFlash panel](/grafana-performance-overview-dashboard.md#tiflash) in the Performance Overview dashboard.

## TiFlash cluster resource utilization

Using the following three metrics, you can quickly determine the resource utilization of the TiFlash cluster:

- CPU: CPU utilization of each TiFlash instance.
- Memory: Memory usage of each TiFlash instance.
- IO utilization: IO utilization of each TiFlash instance.

Example: Resource Utilization during [CH-benCHmark Load](/benchmark/benchmark-tidb-using-ch.md)

This TiFlash cluster consists of two nodes, each configured with 16 cores and 48GB of memory. During the CH-benCHmark load, CPU utilization can reach up to 1500%, memory usage can peak at 20GB, and IO utilization reaches 91%. This indicates that TiFlash node resources are approaching saturation.

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

## Key performance metrics for TiFlash

### Throughput metrics

Using the following metrics, you can understand the throughput of TiFlash:

- MPP Query count: Instant value of MPP query count for each TiFlash instance, representing the current number of MPP queries that need to be processed by the TiFlash instance (including those being processed and those not yet scheduled).
- Request QPS: The number of coprocessor requests received by all TiFlash instances.
    - `run_mpp_task`, `dispatch_mpp_task`, and `mpp_establish_conn` are MPP requests.
    - `batch`: Number of batch requests.
    - `cop`: Number of coprocessor requests directly sent through the coprocessor interface.
    - `cop_execution`: Number of coprocessor requests currently being executed.
    - `remote_read`, `remote_read_constructed`, and `remote_read_sent` are remote read-related metrics; an increase in remote reads generally indicates a problem in the system.
- Executor QPS: For all TiFlash instances, the count of each DAG operator in received requests, where `table_scan` is the table scan operator, `selection` is the filter operator, `aggregation` is the aggregation operator, `top_n` is the TopN operator, `limit` is the limit operator, and `join` represents join operators. `exchange_sender` and `exchange_receiver` are data sending and receiving operators.

### Latency metrics

Using the following metrics, you can understand the latency handling of TiFlash:

- Request Duration Overview: Stacked chart of the total duration of all request types processed by all TiFlash instances per second.

    - If the request type is `run_mpp_task`, `dispatch_mpp_task`, or `mpp_establish_conn`, it indicates that the execution of SQL statements has been partially or fully pushed down to TiFlash, typically involving join and data distribution operations. This is the most common service type in TiFlash.
    - If the request type is `cop`, it indicates that the entire statement has not been fully pushed down to TiFlash. Typically, TiDB will push down full table scan operators to TiFlash for data access and filtering. In the stacked chart, if `cop` dominates, careful consideration is needed.

        - If the amount of data accessed by the SQL query is large, the optimizer might estimate a lower cost for TiFlash full table scans based on the cost model.
        - If the table structure lacks appropriate indexes, even if the amount of data accessed is small, the optimizer can only push the query down to TiFlash for a full table scan. In such cases, creating suitable indexes makes accessing data through TiKV more efficient.

- Request Duration: Total processing time of each MPP and coprocessor request type for all TiFlash instances, including average and P99 processing latency.
- Request Handle Duration: Time from the start of execution to the end of execution for `cop` and `batch cop` requests, excluding waiting time. This includes only the `cop` and `batch cop` types, with average and P99 latency.

Example 1: Overview of TiFlash MPP Request Processing Time

As shown in the following chart, in this workload, the processing time of `run_mpp_task` and `mpp_establish_conn` requests is the highest, indicating that most requests are fully pushed down to TiFlash for MPP tasks.

The processing time of `cop` requests is relatively small, indicating that some requests are pushed down to TiFlash for data access and filtering through the coprocessor.

![CH-TiFlash-MPP](/media/performance/tiflash/ch-2tiflash-op.png)

Example 2: High Processing Time for TiFlash `cop` Requests

As shown in the following chart, in this workload, the processing time of `cop` requests is the highest. You can check the SQL execution plan to confirm the reasons for the generation of `cop` requests.

![Cop](/media/performance/tiflash/tiflash_request_duration_by_type.png)

### Raft-related metrics

Using the following metrics, you can understand the Raft synchronization status of TiFlash:

- Raft Wait Index Duration: Time spent by all TiFlash instances waiting for the local Region index >= read_index, which represents the delay of wait_index operation. If the Wait Index latency is too high, it indicates significant synchronization delay between TiKV and TiFlash. Possible reasons include:

    - TiKV resource overload
    - TiFlash resource overload, especially IO resources
    - Network bottleneck between TiKV and TiFlash

- Raft Batch Read Index Duration: Delay of Read Index for all TiFlash instances. If this metric is too high, it indicates slow interaction between TiFlash and TiKV. Possible reasons include:

    - TiFlash resource overload
    - TiKV resource overload
    - Network bottleneck between TiFlash and TiKV

### IO throughput metrics

Using the following metrics, you can understand the IO throughput situation of TiFlash:

- Write Throughput By Instance: Throughput of data written by each TiFlash instance, including the apply of Raft data logs and the throughput of Raft snapshots.
- Write flow: Traffic of disk write operations for all TiFlash instances.

    - File Descriptor: Stable layer of DeltaTree storage engine used by TiFlash.
    - Page: Refers to Pagestore, the Delta change layer of the DeltaTree storage engine used by TiFlash.

- Read flow: Traffic of disk read operations for all TiFlash instances.

    - File Descriptor: Stable layer of DeltaTree storage engine used by TiFlash.
    - Page: Refers to Pagestore, the Delta change layer of the DeltaTree storage engine used by TiFlash.

You can calculate the write amplification factor of the entire TiFlash cluster by `(Read flow + Write flow) ÷ Total Write Throughput By Instance`.

Example 1: Raft and IO Metrics for Local Deployment of [CH-benCHmark Load](/benchmark/benchmark-tidb-using-ch.md)

As shown in the figure below, the TiFlash cluster exhibits high Raft Wait Index and Raft Batch Read Index 99th percentile values, at 3.24 seconds and 753 milliseconds, respectively. This is due to the high load on the TiFlash cluster, resulting in data synchronization delays.

The cluster consists of two TiFlash nodes, and the incremental data synchronized from TiKV to TiFlash is approximately 28 MB per second. The maximum write throughput of the stable layer (File Descriptor) is 939 MB/s, and the maximum read throughput is 1.1 GiB/s. Meanwhile, the maximum write throughput of the Delta layer (Page) is 74 MB/s, and the maximum read throughput is 111 MB/s. In this environment, TiFlash employs dedicated NVME disks, resulting in strong IO throughput capabilities.

![CH-2TiFlash-OP](/media/performance/tiflash/ch-2tiflash-raft-io-flow.png)

Example 2: Raft and IO Metrics for Public Cloud Deployment of [CH-benCHmark Load](/benchmark/benchmark-tidb-using-ch.md)

As illustrated below, the 99th percentile of Raft Wait Index wait time is highest at 438 milliseconds, and the 99th percentile of Raft Batch Read Index wait time is highest at 125 milliseconds. The cluster only comprises a single TiFlash node, and the incremental data synchronized from TiKV to TiFlash is approximately 5 MB per second. The maximum write throughput of the stable layer (File Descriptor) is 78 MB/s, and the maximum read throughput is 221 MB/s. Additionally, the maximum write throughput of the Delta layer (Page) is 8 MB/s, and the maximum read throughput is 18 MB/s. In this environment, TiFlash utilizes AWS EBS cloud disks, which exhibit relatively weaker IO throughput capabilities.

![CH-TiFlash-MPP](/media/performance/tiflash/ch-1tiflash-raft-io-flow-cloud.png)