---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with TiDB Cloud HTAP.
---

# TiDB Cloud HTAP Quick Start

This tutorial guides you through an easy way to experience Hybrid Transactional and Analytical Processing (HTAP) once you have already started your TiDB cluster on the TiDB Cloud and have TiFlash node in your cluster.

The content includes how to replicate tables to TiFlash , run queries with TiFlash and experience the performance boost.

## Before you begin

Before experiencing the benefit brought by HTAP, take the steps in [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a cluster with TiFlash nodes and import sample data to the cluster.

## Steps

### Step 1. Replicate the sample data to the columnar storage engine

After a cluster with TiFlash nodes is created, TiKV does not replicate data to TiFlash by default. You need to execute the following DDL statements in a MySQL client of TiDB to specify the tables to be replicated. After that, TiDB will create the specified replicas in TiFlash accordingly.

```sql
USE bikeshare;
ALTER TABLE trips SET TIFLASH REPLICA 1;
```

2. When the process of replication table is completed, you can start to run some queries in your Terminal.
Check the number of trips by different start and end stations.

    ```sql
    SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

3. Now we can compare the execution statistics between TiKV storage and TiFlash Storage.

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[trips]) */ start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

4. TiDB Optimizer will automatically choose TiKV storage or TiFlash Storage. The  HINT /*+ READ_FROM_STORAGE(TIKV[trips]) */ will force the optimizer to choose TiKV storage.

    ```sql
    EXPLAIN ANALYZE SELECT start_station_name, end_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name, end_station_name
    ORDER BY count ASC;
    ```

Because of cache, the query with TiKV storage may be faster after the first time, since the sample data is very small and the query is very simple. Once the data is updated frequently, the cache will be missed.