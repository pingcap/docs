---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with TiDB Cloud HTAP.
---

# TiDB Cloud HTAP Quick Start

This tutorial guides you through an easy way to experience Hybrid Transactional and Analytical Processing (HTAP) once you have already started your TiDB cluster on the TiDB Cloud and have TiFlash node in your cluster.

The content includes how to replicate tables to TiFlash, run queries with TiFlash and experience the performance boost.

## Before you begin

Before experiencing the benefit brought by HTAP, take the steps in [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a cluster with TiFlash nodes and import sample data to the cluster.

## Steps

### Step 1. Replicate the sample data to the columnar storage engine

After a cluster with TiFlash nodes is created, TiKV does not replicate data to TiFlash by default. You need to execute the following DDL statements in a MySQL client of TiDB to specify the tables to be replicated. After that, TiDB will create the specified replicas in TiFlash accordingly.

```sql
USE bikeshare;
ALTER TABLE trips SET TIFLASH REPLICA 1;
```

To check the replication progress, use the following command:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

### Step 2. Query data using HTAP

When the process of replication table is completed, you can start to run some queries in your Terminal.

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

    For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. In the preceding statement, `HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */` is used to force the optimizer to choose TiKV so you can check its execution statistics.

- To get the execution statistics of this query using TiFlash, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

> **Note:**
>
> Because the sample data is very small and the query in this document is very simple, if you have already forced the optimizer to choose TiKV for this query and run the same query again, TiKV will reuse its cache, and the query might be much faster. If the data is updated frequently, the cache will be missed.
