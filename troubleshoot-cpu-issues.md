---
title: Troubleshoot Increased Read and Write Latency
summary: Learn how to troubleshoot the issue of increased read and write latency.
---

# Troubleshoot Increased Read and Write Latency

This document introduces the possible causes of read and write latency and jitters, and how to troubleshoot these issues.

## Common causes

### Incorrect TiDB execution plan

The execution plan of queries is unstable and might select the incorrect index, which causes higher latency.

#### Phenomenon

* If the query execution plan is output in the slow log, you can directly view the plan. Execute the `select tidb_decode_plan('xxx...')` statement to parse the detailed execution plan.
* The number of scanned keys in the monitor abnormally increases; in the slow log, the number of `Scan Keys` are large.
* The SQL execution duration in TiDB is greatly different than that of other databases such as MySQL. You can compare the execution plan of other databases (for example, whether `Join Order` is different).

#### Possible reason

The statistical information is inaccurate.

#### Handling methods

* Update the statistical information
    * Execute `analyze table` manually and execute `analyze` periodically with the `crontab` command to keep the accuracy of the statistical information
    * Execute `auto analyze` automatically. Lower the threshold value of `analyze ratio`, increase the frequency of information collection, and set the runtime threshold. See the following examples:
        * `set global tidb_auto_analyze_ratio=0.2;`
        * `set global tidb_auto_analyze_start_time='00:00 +0800';`
        * `set global tidb_auto_analyze_end_time='06:00 +0800';`
* Bind the execution plan
    * Modify the application SQL statements and execute `use index` to consistently use the index of the column.
    * In 3.0 versions, you do not need to modify the application SQL statements. Use `create global binding` to create the binding SQL statement of `force index`.
    * In 4.0 versions, [SQL Plan Management](/sql-plan-management.md) is supported, which avoids the performance decrease caused by unstable execution plans.

### PD anomalies

#### Phenomenon

There is an abnormal increase of the `wait duration` metric for the PD TSO. This metric represents the duration of waiting for PD to return.

#### Possible reasons

* Disk issue. The I/O usage of the node where PD is located is full. You can check the Grafana -> **disk performance** -> `latency` and `load` metrics to see whether there is any other component with high I/O usage and the health status of the disk. You can also check with the fio tool.

* Network issues between PD peers. The `"lost the TCP streaming connection"` error is output in the PD log. You can check the Grafana -> **PD** -> **etcd** -> `round trip` metric to see whether the network issue exists.

* High server load. You can see `"server is likely overloaded"` in the log.

* The leader cannot be elected. The `"lease is not expired"` error is output in the PD log. This issue was fixed in v3.0.x and v2.1.19.

* The leader election is slow. It takes a long time to load Regions. Execute `grep "regions cost"` to search the PD log (for example, `load 460927 regions cost 11.77099s` might be in the log). If the loading time is at the second-level, the election is slow. In v3.0, you can enable the Region Storage feature by setting `use-region-storage` to `true`. This feature can greatly shorten the loading time of Region.

* The network issue between TiDB and PD. You can check the Grafana -> **blackbox_exporter** -> `ping latency` metric to see whether the network between TiDB and the PD leader is fine.

* PD returns the `FATAL` error. The `"range failed to find revision pair"` error is output in the log, which was fixed in v3.0.8. See [#2040](https://github.com/pingcap/pd/pull/2040) for details.

* When you use the `/api/v1/regions` interface, too many Regions cause PD to run out of memory (OOM). This issue was fixed in v3.0.8. See [#1986](https://github.com/pingcap/pd/pull/1986) for details.

* PD OOM occurs during the rolling upgrade and the size of a gRPC message is not limited. From the monitoring panel, you can see that `TCP InSegs` is large. This issue was fixed in v3.0.6. See [#1952](https://github.com/pingcap/pd/pull/1952) for details.

* PD panics and you can report the bug.

* Report a bug when you use `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2` to get the gorountine.

### TiKV anomalies

#### Phenomenon

The `KV Cmd Duration` metric in the monitor increases abnormally. This metric represents the duration between the time that TiDB sends a request to TiKV and the time that TiDB receives the response.

#### Possible reasons

* Check the `gRPC duration` metric. This metric represents the total duration of a gRPC request in TiKV. You can find out the potential network issue by comparing `gRPC duration` of TiKV and `KV duration` of TiDB. For example, the gRPC duration is short but the KV duration of TiDB is long, which indicates that the network latency between TiDB and TiKV might be high, or that the NIC bandwidth between TiDB and TiKV is fully occupied.

* The TiKV restart causes the re-election.
    * TiKV panics and is then restarted by `systemd` to run normally. You can check the TiKV log to confirm whether `panic` exists. This situation is unexpected and you need to report a bug.
    * TiKV is stopped by `stop`/`kill` by a third party. Then TiKV is restarted by `systemd`. You can view `dmesg` and `TiKV log` to confirm the cause.
    * OOM occurs in TiKV and TiKV is restarted.
    * The dynamical adjustment of `THP` is hung.

* Check monitor: Check Grafana -> **TiKV-details** -> **errors** -> `server is busy`, and you can see that the write stall occurs in TiKV RocksDB that causes the re-election.

* Network isolation occurs in TiKV that causes the re-election.

* `block-cache` is configured too large a value that causes OOM. You can confirm this cause by selecting the corresponding instances in the Grafana -> **TiKV-details** panel and viewing the `block cache size` metric of RocksDB. At the same time, check whether the `[storage.block-cache] capacity = # "1GB"` parameter value is properly configured. By default, the `block-cache` value of TiKV is set to 45% of the total machine memory. For the containerized deployment, you need to explicitly specify this parameter, because the memory of the physical machine obtained by TiKV might exceed the memory limit of a single container.

* Coprocessor receives many large queries and the amount of data to return is large. The speed at which gRPC messages are sent falls behind the speed at which Coprocessor exports data to the client, which causes the OOM. You can confirm this cause by checking whether the `response size` metric in the Grafana -> **TiKV-details** -> **coprocessor overview** panel exceeds `network outbound`.

### Bottleneck of a single TiKV thread

There are some single threads in TiKV that might become the bottleneck.

* Too many Regions on a single TiKV node cause the single gRPC threads to become the bottleneck (see Grafana -> **TiKV-details** -> `Thread CPU/gRPC CPU Per Thread`). In v3.x and later versions, you can resolve this issue by enabling the Hibernate Region feature.
* In versions earlier than v3.0, when the single `raftstore` thread or the single `apply` thread becomes the bottleneck (Grafana -> **TiKV-details** -> `Thread CPU/raft store CPU` and `Async apply CPU` exceed `80%`), you can scale out the TiKV instance (for v2.x) or upgrade to v3.x for the multi-threaded mode.

### CPU load increases

#### Phenomenon

The usage of CPU resources becomes the bottleneck.

#### Possible reasons

* Hotspot issue
* High overall load. Check the slow queries and expensive queries of TiDB. Optimize the executing queries by adding indexes or executing queries in batches. Another option to handle the issue of high load is to scale out the cluster.

## Other causes

### Cluster maintenance

Most of each online cluster has three or five nodes. If the machine to be maintained has the PD component, you need to determine whether the node is the leader or the follower. Disabling a follower has no impact on the cluster operation. Before disabling a leader, you need to switch the leadership. During the leadership change, performance jitter of about 3 seconds will occur.

### Minority of replicas are offline

By default, each TiDB cluster has three replicas, so each Region has three replicas in the cluster. These Regions elect the leader and replicate data through the Raft protocol. The Raft protocol ensures that TiDB can still provide services even when the nodes (that are fewer than half of replicas) fail or are isolated without data loss. For the cluster with three replicas, the failure of one node might cause performance jitter but the usability and correctness in theory are not affected.

### New indexes

Creating indexes consumes a huge amount of resources when TiDB scans tables and backfills indexes. Index creation might even conflict with the frequently updated fields, which affects the application. Creating indexes on a large table often takes a long time, so you must try to balance the index creation time and the cluster performance (for example, creating indexes at the off-peak time).

**Parameter adjustment:**

Currently, you can use `tidb_ddl_reorg_worker_cnt` and `tidb_ddl_reorg_batch_size` to dynamically adjust the speed of index creation. Usually, the smaller the values, the smaller the impact on the system, with longer execution time though.

In general cases, you can first keep their default values (`4` and `256`), observe the resource usage and response speed of the cluster, and then increase the value of `tidb_ddl_reorg_worker_cnt` to increase the concurrency. If no obvious jitter is observed in the monitor, increase the value of `tidb_ddl_reorg_batch_size`. If the columns involved in the index creation are frequently updated, the many resulting conflicts will cause the index creation to fail and be retried.

In addition, you can also set the value of `tidb_ddl_reorg_priority` to `PRIORITY_HIGH` to prioritize the index creation and speed up the process. But in the general OLTP system, it is recommended to keep its default value.

### High GC pressure

The transaction of TiDB adopts the Multi-Version Concurrency Control (MVCC) mechanism. When the newly written data overwrites the old data, the old data is not replaced but stored with the newly written data. Timestamps are used to mark different versions. The task of GC is to clear the obsolete data.

* In the phase of Resolve Locks, a large amount of `scan_lock` requests are created in TiKV, which can be observed in the gRPC-related metrics. These `scan_lock` requests call all Regions.
* In the phase of Delete Ranges, a few (or no) `unsafe_destroy_range` requests are sent to TiKV, which can be observed in the gRPC-related metrics and the **GC tasks** panel.
* In the phase of Do GC, each TiKV by default scans the leader Regions on the machine and performs GC to each leader, which be observed in the **GC tasks** panel.
