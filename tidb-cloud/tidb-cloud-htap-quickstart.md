---
title: TiDB Cloud HTAP Quick Start
summary: Learn how to get started with HTAP in TiDB Cloud.
aliases: ['/tidbcloud/use-htap-cluster']
---

# TiDB Cloud HTAP Quick Start

[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) stands for Hybrid Transactional and Analytical Processing. The HTAP architecture in TiDB Cloud is composed of [TiKV](https://tikv.org), a row-based storage engine designed for transactional processing, and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), a columnar storage engine designed for analytical processing. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is a real-time replication from the row-based storage to the columnar storage.

This tutorial guides you through an easy way to experience the Hybrid Transactional and Analytical Processing (HTAP) feature of TiDB Cloud. The content includes how to replicate tables to TiFlash, how to run queries with TiFlash, and how to experience the performance boost.

## Before you begin

Before trying the HTAP feature, follow [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a {{{ .starter }}} instance, and then import your data (this document uses the **Steam Games Dataset 2021-2025** as an example) into the instance as follows:

1. Download the [Steam Games Dataset 2021-2025](https://www.kaggle.com/datasets/jypenpen54534/steam-games-dataset-2021-2025-65k) from Kaggle.
2. Open the **Import** page for your {{{ .starter }}} instance.

    1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .starter }}} instance to go to its overview page.
    2. On the overview page, click **Data** > **Import** in the left navigation pane.

3. Import the downloaded CSV file into your {{{ .starter }}} instance.

    1. On the **Import** page, click **Upload a local file**, and then select and upload the downloaded CSV file.
    2. In the **Destination** section, enter `steam` in the **Database** field and `games` in the **Table** field.
    3. Click **Define Table**, change the data type of the column `categories` to `TEXT`, and then change the data type of the column `developer` to `TEXT`.
    4. Click **Start Import**.

        You can view the import progress on the **Import Task Detail** page.

## Steps

### Step 1. Replicate the sample data to the columnar storage engine

After you create a {{{ .starter }}} instance, TiDB does not replicate data from TiKV to TiFlash by default. To replicate a target table to TiFlash, use a MySQL client to connect to your {{{ .starter }}} instance and execute a DDL statement. TiDB then creates the specified table replicas in TiFlash.

For example, to replicate the `games` table (from the **Steam Games Dataset 2021-2025**) to TiFlash, execute the following statements:

```sql
USE steam;
```

```sql
ALTER TABLE games SET TIFLASH REPLICA 2;
```

To check the replication progress, execute the following statement:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_ID, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'steam' AND TABLE_NAME = 'games';
```

```sql
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| steam        | games      |      227 |             2 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.24 sec)
```

In the result of the preceding statement:

- `AVAILABLE` indicates whether the TiFlash replica of a specific table is available or not. `1` means available and `0` means unavailable. Once a replica becomes available, this status does not change anymore.
- `PROGRESS` means the progress of the replication. The value is between `0` and `1`. `1` means at least one replica is replicated.

### Step 2. Query data using HTAP

After the replication completes, you can run queries.

For example, you can check the number of games released every year, as well as the average price and average number of recommendations:

```sql
SELECT
  `release_year`,
  COUNT(*) AS `games_released`,
  AVG(`price`) AS `average_price`,
  AVG(`recommendations`) AS `average_recommendations`
FROM
  `games`
WHERE
  `release_year` IS NOT NULL
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
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use either TiKV or TiFlash replicas based on the cost estimation. In the preceding `EXPLAIN ANALYZE` statement, the `/*+ READ_FROM_STORAGE(TIKV[games]) */` hint is used to force the optimizer to choose TiKV so you can check the execution statistics of TiKV.

    > **Note:**
    >
    > MySQL command-line clients earlier than 5.7.7 strip optimizer hints by default. If you are using the `Hint` syntax in these earlier versions, add the `--comments` option when starting the client. For example: `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                                | estRows  | actRows | task      | access object | execution info                              | operator info                              | memory   | disk
    ----------------------------------+----------+---------+-----------+---------------+---------------------------------------------+--------------------------------------------+----------+---------
    Projection_10                     | 20.00    | 20      | root      |               | time:234.4ms, loops:2, RU:241.66, ...       | steam.games.release_year, ...              | 6.03 KB  | N/A
    └─TopN_13                         | 20.00    | 20      | root      |               | time:234.4ms, loops:2                       | Column#13:desc, Column#12:desc, ...        | 12.6 KB  | 0 Bytes
      └─Selection_18                  | 36774.40 | 2458    | root      |               | time:233.9ms, loops:5                       | ge(Column#12, ?)                           | 187.0 KB | N/A
        └─HashAgg_22                  | 45968.00 | 59883   | root      |               | time:228.4ms, loops:62, partial_worker:...  | group by:Column#39, Column#40, ...         | 31.7 MB  | 0 Bytes
          └─Projection_38             | 65521.00 | 65521   | root      |               | time:142.9ms, loops:66, Concurrency:5       | cast(steam.games.recommendations, ...      | 1.16 MB  | N/A
            └─TableReader_32          | 65521.00 | 65521   | root      |               | time:49.5ms, loops:66, cop_task:{num:9...   | data:Selection_31                          | 3.26 MB  | N/A
              └─Selection_31          | 65521.00 | 65521   | cop[tikv] |               | tikv_task:{proc max:20ms, min:0s, ...       | not(isnull(steam.games.developer)), ...    | N/A      | N/A
                └─TableFullScan_30    | 65521.00 | 65521   | cop[tikv] | table:games   | tikv_task:{proc max:10ms, min:0s, ...       | keep order:false                           | N/A      | N/A
    (8 rows)
    ```

- To get the execution statistics of this query using TiFlash, execute the same statement without the `/*+ READ_FROM_STORAGE(TIKV[games]) */` hint:

    ```sql
    EXPLAIN ANALYZE SELECT
      `release_year`,
      `genres`,
      `developer`,
      COUNT(*) AS `games_released`,
      SUM(`recommendations`) AS `total_recommendations`,
      AVG(`recommendations`) AS `average_recommendations`,
      AVG(`price`) AS `average_price`,
      MAX(`recommendations`) AS `max_recommendations`
    FROM
      `games`
    WHERE
      `release_year` IS NOT NULL
      AND `genres` IS NOT NULL
      AND `developer` IS NOT NULL
    GROUP BY
      `release_year`,
      `genres`,
      `developer`
    HAVING
      COUNT(*) >= 2
    ORDER BY
      `total_recommendations` DESC,
      `games_released` DESC
    LIMIT 20;
    ```

    In the output, you can get the execution time from the `execution info` column.

    ```sql
    id                                      | estRows  | actRows | task         | access object | execution info                              | operator info                              | memory  | disk
    ----------------------------------------+----------+---------+--------------+---------------+---------------------------------------------+--------------------------------------------+---------+---------
    Projection_10                           | 20.00    | 20      | root         |               | time:92.5ms, loops:2, RU:120.42, ...        | steam.games.release_year, ...              | 6.03 KB | N/A
    └─TopN_14                               | 20.00    | 20      | root         |               | time:92.4ms, loops:2                        | Column#13:desc, Column#12:desc, ...        | 4.32 KB | 0 Bytes
      └─TableReader_68                      | 20.00    | 20      | root         |               | time:92.4ms, loops:2, cop_task:{num:2...    | MppVersion: 2, data:ExchangeSender_67      | 7.99 KB | N/A
        └─ExchangeSender_67                 | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ExchangeType: PassThrough                  | N/A     | N/A
          └─TopN_66                         | 20.00    | 20      | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#13:desc, Column#12:desc, ...        | N/A     | N/A
            └─Selection_65                  | 36774.40 | 2458    | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | ge(Column#12, ?)                           | N/A     | N/A
              └─Projection_58               | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:91ms, loops:1, ...       | Column#12, Column#13, div(Column#14, ...   | N/A     | N/A
                └─HashAgg_56                | 45968.00 | 59883   | mpp[tiflash] |               | tiflash_task:{time:71ms, loops:1, ...       | group by:Column#79, Column#80, ...         | N/A     | N/A
                  └─Projection_71           | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       | cast(steam.games.recommendations, ...      | N/A     | N/A
                    └─ExchangeReceiver_41   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31ms, loops:7, ...       |                                            | N/A     | N/A
                      └─ExchangeSender_40   | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:31.2ms, loops:7, ...     | ExchangeType: HashPartition, ...           | N/A     | N/A
                        └─Selection_39      | 65521.00 | 65521   | mpp[tiflash] |               | tiflash_task:{time:21.2ms, loops:7, ...     | not(isnull(steam.games.developer)), ...    | N/A     | N/A
                          └─TableFullScan_38| 65521.00 | 65521   | mpp[tiflash] | table:games   | tiflash_task:{time:21.2ms, loops:7, ...     | pushed down filter:empty, keep order:false | N/A     | N/A
    (13 rows)
    ```

> **Note:**
>
> Because the sample dataset is small and the query in this document is relatively simple, if you force the optimizer to choose TiKV for this query and then run the same query again, TiKV reuses its cache, which makes the query much faster. If the data is updated frequently, the cache is invalidated.

## Learn more

- [TiFlash Overview](/tiflash/tiflash-overview.md)
- [Create TiFlash Replicas](/tiflash/create-tiflash-replicas.md)
- [Read Data from TiFlash](/tiflash/use-tidb-to-read-tiflash.md)
- [Use MPP Mode](/tiflash/use-tiflash-mpp-mode.md)
- [Supported Push-down Calculations](/tiflash/tiflash-supported-pushdown-calculations.md)
