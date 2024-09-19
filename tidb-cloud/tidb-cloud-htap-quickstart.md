---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with HTAP in TiDB Cloud.
aliases: ['/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP Quick Start

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) means Hybrid Transactional and Analytical Processing. The HTAP cluster in TiDB Cloud is composed of [TiKV](https://tikv.org), a row-based storage engine designed for transactional processing, and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), a columnar storage designed for analytical processing. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is a real-time replication from the row-based storage to the columnar storage.

This tutorial guides you through an easy way to experience the Hybrid Transactional and Analytical Processing (HTAP) feature of TiDB Cloud. The content includes how to replicate tables to TiFlash, how to run queries with TiFlash, and how to experience the performance boost.

## Before you begin

Before experiencing the HTAP feature, follow [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a TiDB Cloud Serverless cluster and import the **Steam Game Stats** sample dataset to the cluster.

## Steps

### Step 1. Replicate the sample data to the columnar storage engine

After a cluster with TiFlash nodes is created, TiKV does not replicate data to TiFlash by default. You need to execute DDL statements in a MySQL client of TiDB to specify the tables to be replicated. After that, TiDB will create the specified table replicas in TiFlash accordingly.

For example, to replicate the `games` table (in the **Steam Game Stats** sample dataset) to TiFlash, execute the following statements:

```sql
USE game;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

To check the replication progress, execute the following statement:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'game' and TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| game         | games      |       88 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.20 sec)
```

In the result of the preceding statement:

- `AVAILABLE` indicates whether the TiFlash replica of a specific table is available or not. `1` means available and `0` means unavailable. Once a replica becomes available, this status does not change anymore.
- `PROGRESS` means the progress of the replication. The value is between `0` and `1`. `1` means at least one replica is replicated.

### Step 2. Query data using HTAP

When the process of replication is completed, you can start to run some queries.

For example, you can check the number of games released every year, as well as the average price and average playtime:

```sql
SELECT
  YEAR(`release_date`) AS `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`average_playtime_forever`) AS `average_playtime`
FROM
  `games`
GROUP BY
  `release_year`
ORDER BY
  `release_year` DESC;
```

### Step 3. Compare the query performance between row-based storage and columnar storage

In this step, you can compare the execution statistics between TiKV (row-based storage) and TiFlash (columnar storage).

- To get the execution statistics of this query using TiKV, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT /*+ READ_FROM_STORAGE(TIKV[games]) */
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use either TiKV or TiFlash replicas based on the cost estimation. In the preceding `EXPLAIN ANALYZE` statement, the `/*+ READ_FROM_STORAGE(TIKV[games]) */` hint is used to force the optimizer to choose TiKV so you can check the execution statistics of TiKV.

    > **Note:**
    >
    > MySQL command-line clients earlier than 5.7.7 strip optimizer hints by default. If you are using the `Hint` syntax in these earlier versions, add the `--comments` option when starting the client. For example: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                         | estRows  | actRows | task      | access object | execution info                             | operator info                                 | memory  | disk    
    ---------------------------+----------+---------+-----------+---------------+--------------------------------------------+-----------------------------------------------+---------+---------
    Sort_5                     | 4019.00  | 28      | root      |               | time:672.7ms, loops:2, RU:1159.679690      | Column#36:desc                                | 18.0 KB | 0 Bytes 
    └─Projection_7             | 4019.00  | 28      | root      |               | time:672.7ms, loops:6, Concurrency:5       | year(game.games.release_date)->Column#36, ... | 35.5 KB | N/A     
      └─HashAgg_15             | 4019.00  | 28      | root      |               | time:672.6ms, loops:6, partial_worker:...  | group by:Column#38, funcs:count(Column#39)... | 56.7 KB | N/A     
        └─TableReader_16       | 4019.00  | 28      | root      |               | time:672.4ms, loops:2, cop_task: {num:...  | data:HashAgg_9                                | 3.60 KB | N/A     
          └─HashAgg_9          | 4019.00  | 28      | cop[tikv] |               | tikv_task:{proc max:300ms, min:0s, avg...  | group by:year(game.games.release_date), ...   | N/A     | N/A     
            └─TableFullScan_14 | 68223.00 | 68223   | cop[tikv] | table:games   | tikv_task:{proc max:290ms, min:0s, avg...  | keep order:false                              | N/A     | N/A     
    (6 rows)
    ```

- To get the execution statistics of this query using TiFlash, execute the following statement:

    ```sql
    EXPLAIN ANALYZE SELECT
      YEAR(`release_date`) AS `release_year`,
      COUNT(*) AS `games_released`,
      AVG(`price`) AS `average_price`,
      AVG(`average_playtime_forever`) AS `average_playtime`
    FROM
      `games`
    GROUP BY
      `release_year`
    ORDER BY
      `release_year` DESC;
    ```

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                                   | estRows  | actRows | task         | access object | execution info                                        | operator info                              | memory  | disk    
    -------------------------------------+----------+---------+--------------+---------------+-------------------------------------------------------+--------------------------------------------+---------+---------
    Sort_5                               | 4019.00  | 28      | root         |               | time:222.2ms, loops:2, RU:25.609675                   | Column#36:desc                             | 3.77 KB | 0 Bytes 
    └─TableReader_39                     | 4019.00  | 28      | root         |               | time:222.1ms, loops:2, cop_task: {num: 2, max: 0s,... | MppVersion: 1, data:ExchangeSender_38      | 4.64 KB | N/A     
      └─ExchangeSender_38                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | ExchangeType: PassThrough                  | N/A     | N/A     
        └─Projection_8                   | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | year(game.games.release_date)->Column#3... | N/A     | N/A     
          └─Projection_34                | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | Column#33, div(Column#34, cast(case(eq(... | N/A     | N/A     
            └─HashAgg_35                 | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:1}       | group by:Column#63, funcs:sum(Column#64... | N/A     | N/A     
              └─ExchangeReceiver_37      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:214.8ms, loops:1, threads:8}       |                                            | N/A     | N/A     
                └─ExchangeSender_36      | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | ExchangeType: HashPartition, Compressio... | N/A     | N/A     
                  └─HashAgg_33           | 4019.00  | 28      | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:1, threads:1}       | group by:Column#75, funcs:count(1)->Col... | N/A     | N/A     
                    └─Projection_40      | 68223.00 | 68223   | mpp[tiflash] |               | tiflash_task:{time:210.6ms, loops:2, threads:8}       | game.games.price, game.games.price, gam... | N/A     | N/A     
                      └─TableFullScan_23 | 68223.00 | 68223   | mpp[tiflash] | table:games   | tiflash_task:{time:210.6ms, loops:2, threads:8}, ...  | keep order:false                           | N/A     | N/A     
    (11 rows)
    ```

> **Note:**
>
> Because the size of sample data is small and the query in this document is very simple, if you have already forced the optimizer to choose TiKV for this query and run the same query again, TiKV will reuse its cache, so the query might be much faster. If the data is updated frequently, the cache will be missed.

## Learn more

- [TiFlash Overview](/tiflash/tiflash-overview.md)
- [Create TiFlash Replicas](/tiflash/create-tiflash-replicas.md)
- [Read Data from TiFlash](/tiflash/use-tidb-to-read-tiflash.md)
- [Use MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [Supported Push-down Calculations](/tiflash/tiflash-supported-pushdown-calculations.md)
