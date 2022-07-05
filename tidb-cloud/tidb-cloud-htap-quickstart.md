---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with HTAP in TiDB Cloud.
---

# TiDB Cloud HTAP Quick Start

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) means Hybrid Transactional and Analytical Processing. The HTAP cluster in TiDB Cloud is composed of [TiKV](https://tikv.org), a row-based storage engine designed for transactional processing, and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), a columnar storage designed for analytical processing. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is a real-time replication from the row storage to the columnar storage.

This tutorial guides you through an easy way to experience the Hybrid Transactional and Analytical Processing (HTAP) feature of TiDB Cloud. The content includes how to replicate tables to TiFlash, how to run queries with TiFlash, and how to experience the performance boost.

## Before you begin

Before experiencing the HTAP feature, follow [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a cluster with TiFlash nodes, connect to the TiDB cluster, and import the Capital Bikeshare sample data to the cluster.

## Steps

### Step 1. Replicate the sample data to the columnar storage engine

After a cluster with TiFlash nodes is created, TiKV does not replicate data to TiFlash by default. You need to execute DDL statements in a MySQL client of TiDB to specify the tables to be replicated. After that, TiDB will create the specified table replicas in TiFlash accordingly.

For example, to replicate the `trips` table (in the Capital Bikeshare sample data) to TiFlash, execute the following statements:

```sql
USE bikeshare;
ALTER TABLE trips SET TIFLASH REPLICA 1;
```

To check the replication progress, execute the following statement:

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bikeshare' and TABLE_NAME = 'trips';
```

In the result of the preceding statement:

- `AVAILABLE` indicates whether the TiFlash replica of a specific table is available or not. `1` means available and `0` means unavailable. Once a replica becomes available, this status does not change anymore.
- `PROGRESS` means the progress of the replication. The value is between `0.0` and `1.0`. `1` means at least one replica is replicated.

### Step 2. Query data using HTAP

When the process of replication is completed, you can start to run some queries.

For example, you can check the number of trips by different start and end stations:

```sql
SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
GROUP BY start_station_name, end_station_name
ORDER BY count ASC;
```

### Step 3. Compare the query performance between row-based storage and columnar storage

In this step, you can compare the execution statistics between TiKV (row-based storage) and TiFlash (columnar storage).

- To get the execution statistics of this query using TiKV, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[trips]) */ start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use either TiKV or TiFlash replicas based on the cost estimation. In the preceding `EXPLAIN ANALYZE` statement, `HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */` is used to force the optimizer to choose TiKV so you can check the execution statistics of TiKV.

    > **Note:**
    >
    > MySQL command-line clients earlier than 5.7.7 strip optimizer hints by default. If you are using the `Hint` syntax in these earlier versions, add the `--comments` option when starting the client. For example: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                         | estRows   | actRows | task      | access object | execution info                                                | operator info                                                                                                                                          | memory  | disk
    +----------------------------+-----------+---------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+---------
    Sort_5                     | 633.00    | 73633   | root      |               | time:1.62s, loops:73                                                | Column#15                                                                                                                                          | 6.88 MB | 0 Bytes
    └─Projection_7             | 633.00    | 73633   | root      |               | time:1.57s, loops:76, Concurrency:OFF                                                | bikeshare.trips.start_station_name, bikeshare.trips.end_station_name, Column#15                                                                                                                                          | 6.20 MB | N/A
    └─HashAgg_15             | 633.00    | 73633   | root      |               | time:1.57s, loops:76, partial_worker:{wall_time:1.47893859s, concurrency:5, task_num:2, tot_wait:6.634815646s, tot_exec:207.540472ms, tot_time:6.871165452s, max:1.478839153s, p95:1.478839153s}, final_worker:{wall_time:1.567581676s, concurrency:5, task_num:10, tot_wait:7.202583959s, tot_exec:578.41826ms, tot_time:7.781014597s, max:1.56610292s, p95:1.56610292s} | group by:bikeshare.trips.end_station_name, bikeshare.trips.start_station_name, funcs:count(Column#16)->Column#15, funcs:firstrow(bikeshare.trips.start_station_name)->bikeshare.trips.start_station_name, funcs:firstrow(bikeshare.trips.end_station_name)->bikeshare.trips.end_station_name | 58.0 MB | N/A
        └─TableReader_16       | 633.00    | 111679  | root      |               | time:1.34s, loops:3, cop_task: {num: 2, max: 1.34s, min: 940.1ms, avg: 1.14s, p95: 1.34s, max_proc_keys: 532575, p95_proc_keys: 532575, tot_proc: 2.24s, rpc_num: 2, rpc_time: 2.28s, copr_cache_hit_ratio: 0.00}                                                | data:HashAgg_8                                                                                                                                          | 7.55 MB | N/A
        └─HashAgg_8          | 633.00    | 111679  | cop[tikv] |               | tikv_task:{proc max:830ms, min:470ms, p80:830ms, p95:830ms, iters:798, tasks:2}, scan_detail: {total_process_keys: 816090, total_process_keys_size: 166701995, total_keys: 816092, rocksdb: {delete_skipped_count: 0, key_skipped_count: 816090, block: {cache_hit_count: 374, read_count: 2348, read_byte: 28.4 MB}}}                                                | group by:bikeshare.trips.end_station_name, bikeshare.trips.start_station_name, funcs:count(bikeshare.trips.ride_id)->Column#16                                                                                                                                          | N/A     | N/A
            └─TableFullScan_14 | 816090.00 | 816090  | cop[tikv] | table:trips   | tikv_task:{proc max:490ms, min:310ms, p80:490ms, p95:490ms, iters:798, tasks:2}                                                | keep order:false                                                                                                                                          | N/A     | N/A
    (6 rows)
    ```

- To get the execution statistics of this query using TiFlash, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                                | estRows   | actRows | task         | access object | execution info | operator info                                                                                         | memory  | disk
    +------------------------------------+-----------+---------+--------------+---------------+------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+---------
    Sort_5                             | 633.00    | 73633   | root         |               | time:420.2ms, loops:73 | Column#15                                                                                         | 5.61 MB | 0 Bytes
    └─Projection_7                     | 633.00    | 73633   | root         |               | time:368.7ms, loops:73, Concurrency:OFF | bikeshare.trips.start_station_name, bikeshare.trips.end_station_name, Column#15                                                                                         | 4.94 MB | N/A
    └─TableReader_34                 | 633.00    | 73633   | root         |               | time:368.6ms, loops:73, cop_task: {num: 2, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00} | data:ExchangeSender_33                                                                                         | N/A     | N/A
        └─ExchangeSender_33            | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:360.7ms, loops:1, threads:8} | ExchangeType: PassThrough                                                                                         | N/A     | N/A
        └─Projection_29              | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:330.7ms, loops:1, threads:8} | Column#15, bikeshare.trips.start_station_name, bikeshare.trips.end_station_name                                                                                         | N/A     | N/A
            └─HashAgg_30               | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:330.7ms, loops:1, threads:1} | group by:bikeshare.trips.end_station_name, bikeshare.trips.start_station_name, funcs:sum(Column#19)->Column#15, funcs:firstrow(bikeshare.trips.start_station_name)->bikeshare.trips.start_station_name, funcs:firstrow(bikeshare.trips.end_station_name)->bikeshare.trips.end_station_name | N/A     | N/A
            └─ExchangeReceiver_32    | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:280.7ms, loops:12, threads:8} |                                                                                         | N/A     | N/A
                └─ExchangeSender_31    | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:272.3ms, loops:256, threads:2} | ExchangeType: HashPartition, Hash Cols: [name: bikeshare.trips.start_station_name, collate: utf8mb4_bin], [name: bikeshare.trips.end_station_name, collate: utf8mb4_bin]                                                                                         | N/A     | N/A
                └─HashAgg_12         | 633.00    | 73633   | mpp[tiflash] |               | tiflash_task:{time:252.3ms, loops:256, threads:1} | group by:bikeshare.trips.end_station_name, bikeshare.trips.start_station_name, funcs:count(bikeshare.trips.ride_id)->Column#19                                                                                         | N/A     | N/A
                    └─TableFullScan_28 | 816090.00 | 816090  | mpp[tiflash] | table:trips   | tiflash_task:{time:92.3ms, loops:16, threads:2} | keep order:false                                                                                         | N/A     | N/A
    (10 rows)
    ```

> **Note:**
>
> Because the sample data is very small and the query in this document is very simple, if you have already forced the optimizer to choose TiKV for this query and run the same query again, TiKV will reuse its cache, so the query might be much faster. If the data is updated frequently, the cache will be missed.
