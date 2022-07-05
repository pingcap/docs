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

{{< copyable "sql" >}}

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

- To get the execution statistics of this query using TiFlash, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

> **Note:**
>
> Because the sample data is very small and the query in this document is very simple, if you have already forced the optimizer to choose TiKV for this query and run the same query again, TiKV will reuse its cache, so the query might be much faster. If the data is updated frequently, the cache will be missed.
