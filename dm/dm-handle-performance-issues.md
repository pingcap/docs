---
title: Handle Performance Issues of TiDB Data Migration
summary: Learn about common performance issues that might exist in DM and how to deal with them.
---

# Handle Performance Issues of TiDB Data Migration

This document introduces common performance issues that might exist in DM and how to deal with them.

Before diagnosing an issue, you can refer to the [DM Benchmark Report](https://github.com/pingcap/docs-dm/blob/release-5.3/en/dm-benchmark-v5.3.0.md).

When diagnosing and handling performance issues, make sure that:

- The DM monitoring component is correctly configured and installed.
- You can view [monitoring metrics](/dm/monitor-a-dm-cluster.md#task) on the Grafana monitoring dashboard.
- The component you diagnose works well; otherwise, possible monitoring metrics exceptions might interfere with the diagnosis of performance issues.

In the case of a large latency in the data migration, to quickly figure out whether the bottleneck is inside the DM component or in the TiDB cluster, you can first check `DML queue remain length` in [Write SQL Statements to Downstream](#write-sql-statements-to-downstream).

## relay log unit

To diagnose performance issues in the relay log unit, you can check the `binlog file gap between master and relay` monitoring metric. For more information about this metric, refer to [monitoring metrics of the relay log](/dm/monitor-a-dm-cluster.md#relay-log). If this metric is greater than 1 for a long time, it usually indicates that there is a performance issue; if this metric is 0, it usually indicates that there is no performance issue.

If the value of `binlog file gap between master and relay` is 0, but you suspect that there is a performance issue, you can check `binlog pos`. If `master` in this metric is much larger than `relay`, a performance issue might exist. In this case, diagnose and handle this issue accordingly.

### Read binlog data

`read binlog event duration` refers to the duration that the relay log reads binlog from the upstream database (MySQL/MariaDB). Ideally, this metric is close to the network latency between DM-worker and MySQL/MariaDB instances.

- For data migration in one data center, reading binlog data is not a performance bottleneck. If the value of `read binlog event duration` is too large, check the network connection between DM-worker and MySQL/MariaDB.

- For data migration in the geo-distributed environment, try to deploy DM-worker and MySQL/MariaDB in one data center, while deploying the TiDB cluster in the target data center.

The process of reading binlog data from the upstream database includes the following sub-processes:

- The upstream MySQL/MariaDB reads the binlog data locally and sends it through the network. When no exception occurs in the MySQL/MariaDB load, this sub-process usually does not become a bottleneck.
- The binlog data is transferred from the machine where MySQL/MariaDB is located to the machine where DM-worker is located via the network. Whether this sub-process becomes a bottleneck mainly depends on the network connection between DM-worker and the upstream MySQL/MariaDB.
- DM-worker reads binlog data from the network data stream and constructs it as a binlog event. When no exception occurs in the DM-worker load, this sub-process usually does not become a bottleneck.

> **Note:**
>
> If the value of `read binlog event duration` is large, another possible reason is that the upstream MySQL/MariaDB has a low load. This means that no binlog event needs to be sent to DM for a period of time, and the relay log unit stays in a wait state, thus this value includes additional waiting time.

### binlog data decoding and verification

After reading the binlog event into the DM memory, DM's relay processing unit decodes and verifies data. This usually does not lead to performance bottleneck; therefore, there is no related performance metric on the monitoring dashboard by default. If you need to view this metric, you can manually add a monitoring item in Grafana. This monitoring item corresponds to `dm_relay_read_transform_duration`, a metric from Prometheus.

### Write relay log files

When writing a binlog event to a relay log file, the relevant performance metric is `write relay log duration`. This value should be microseconds when `binlog event size` is not too large. If `write relay log duration` is too large, check the write performance of the disk. To avoid low write performance, use local SSDs for DM-worker.

## Load unit

The main operations of the Load unit are to read the SQL file data from the local and write it to the downstream. The related performance metric is `transaction execution latency`. If this value is too large, check the downstream performance by checking the monitoring of the downstream database. You can also check whether there is a large network latency between DM and the downstream database.

## Binlog replication unit

To diagnose performance issues in the Binlog replication unit, first check `binlog file gap between master and syncer`. For more information about this metric, refer to [monitoring metrics of the Binlog replication](/dm/monitor-a-dm-cluster.md#binlog-replication).

- If this metric is greater than 1 for a period of time, continue locating the bottleneck.
- If this metric remains 0, the Binlog replication unit does not show file-level lag accumulation.

When `binlog file gap between master and syncer` is greater than 1 for a period of time, check `binlog file gap between relay and syncer`:

- If `binlog file gap between relay and syncer` remains low, the latency is more likely to exist in the relay log unit. In this case, refer to [relay log unit](#relay-log-unit).
- If `binlog file gap between relay and syncer` also keeps increasing, continue checking the Binlog replication unit.

### Locate the bottleneck by combining metrics

Besides `binlog file gap between master and syncer`, you can also check `replicate lag gauge`, `remaining time to sync`, `DML queue remain length`, `transaction execution latency`, and `ideal QPS`.

- If `replicate lag gauge` or `remaining time to sync` keeps increasing while `DML queue remain length` stays low, combine `read binlog event duration`, `transform binlog event duration`, and `transaction execution latency` to continue locating the bottleneck. A low DML queue length only means that DML jobs are not accumulating in the queue.
- If `DML queue remain length` keeps increasing and `transaction execution latency` is also increasing, check the path that writes SQL statements to the downstream first.
- If `binlog event QPS` drops to 0 and `replicate lag gauge` keeps increasing, check the task state, `shard lock resolving`, and DM logs to see whether the task is blocked by a downstream DDL, a shard DDL lock, or a long-running transaction.
- If `ideal QPS` decreases and `transaction execution latency` increases, the downstream execution capacity seen by DM is decreasing. In this case, check the downstream execution path first.

### Read binlog data

The Binlog replication unit reads binlog events either from the upstream MySQL/MariaDB or from the relay log file, depending on the configuration. The related performance metric is `read binlog event duration`.

- If the Binlog replication unit reads binlog events from upstream MySQL/MariaDB, to locate and resolve the issue, refer to [read binlog data](#read-binlog-data) in the "relay log unit" section.

- If the Binlog replication unit reads binlog events from the relay log file and `read binlog event duration` stays high, check the read performance of the disk. To avoid low disk I/O performance, use local SSDs for DM-worker.

### binlog event conversion

The Binlog replication unit constructs DML, parses DDL, and performs [table router](/dm/dm-table-routing.md) conversion from binlog event data. The related metric is `transform binlog event duration`.

This metric is mainly affected by the number of rows and the complexity of the upstream write operations. Take the `INSERT INTO` statement as an example. Converting a single `VALUES` clause and converting many `VALUES` clauses consume different amounts of time. If `transform binlog event duration` is high for a period of time while `read binlog event duration` and `transaction execution latency` stay low, check the conversion path first.

### Write SQL statements to downstream

When the Binlog replication unit writes the converted SQL statements to the downstream, the related performance metrics are `DML queue remain length` and `transaction execution latency`.

After constructing SQL statements from binlog event, DM uses `worker-count` queues to concurrently write these statements to the downstream. However, to avoid too many monitoring entries, DM performs the modulo `8` operation on the IDs of concurrent queues. This means that all concurrent queues correspond to one item from `q_0` to `q_7`.

`DML queue remain length` indicates, in each concurrent processing queue, the number of DML statements that have not been consumed and have not started to be written downstream. Ideally, the curves corresponding to each `q_*` are close to each other. If not, the concurrent load is unbalanced.

If the load is not balanced, confirm whether tables need to be migrated have primary keys or unique keys. If these keys do not exist, add the primary keys or the unique keys; if these keys do exist while the load is not balanced, upgrade DM to v1.0.5 or later versions.

- When there is no noticeable latency in the entire data migration link, the corresponding curve of `DML queue remain length` is close to 0.

- If you find a noticeable latency in the data migration link, and the curve of `DML queue remain length` corresponding to each `q_*` is close to 0, it indicates that DML jobs are not accumulating in the queue. In this case, combine `read binlog event duration`, `transform binlog event duration`, and `transaction execution latency` to continue locating the bottleneck. For troubleshooting, refer to the previous sections of this document.

If the corresponding curve of `DML queue remain length` stays above 0 for a period of time, it indicates that DML jobs are accumulating before execution. In this case, use `transaction execution latency` to view the time consumed to execute a single transaction to the downstream.

If `transaction execution latency` is high for a period of time, check the downstream performance based on the monitoring of the downstream database. You can also check whether there is a large network latency between DM and the downstream database.

To view the time consumed to write a single statement such as `BEGIN`, `INSERT`, `UPDATE`, `DELETE`, or `COMMIT` to the downstream, you can also check `statement execution latency`.

If the bottleneck exists in downstream execution, check the TiDB or TiKV cluster before changing DM configurations:

- If TiDB CPU usage is already high, scale out TiDB first.
- If TiDB query latency or TiDB KV-client backoff is high, the bottleneck might exist in the TiDB SQL layer or in the TiDB-to-TiKV path.
- If TiKV write path metrics such as write RPC latency, scheduler CPU usage, apply CPU usage, write stall, or PD TSO latency are high, check TiKV or PD before tuning DM.
- If the network latency between DM and the downstream database is large, resolve the network issue first.

After confirming that the downstream TiDB or TiKV cluster is not saturated, adjust the task configuration according to the actual scenario:

- If the DM-worker still has enough CPU resources, increase `worker-count` appropriately.
- If the upstream workload contains many bulk `INSERT`, `UPDATE`, or `DELETE` statements, consider enabling `multiple-rows` in the task configuration.
- If `multiple-rows` is already enabled but `transaction execution latency` is still high, check `replication transaction batch` and reduce `batch` appropriately.

For more information about configuration optimization, refer to [Optimize Configuration of DM](/dm/dm-tune-configuration.md).
