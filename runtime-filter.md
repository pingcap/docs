---
title: Runtime Filter
summary: Learn the working principles of Runtime Filter and how to use it.
---

# ランタイムフィルター {#runtime-filter}

ランタイム フィルターは TiDB v7.3 で導入された新機能で、MPP シナリオでのハッシュ結合のパフォーマンスを向上させることを目的としています。 TiDB は、ハッシュ結合のデータを事前にフィルタリングするフィルターを動的に生成することで、実行時のデータ スキャン量とハッシュ結合の計算量を削減し、最終的にクエリのパフォーマンスを向上させることができます。

## コンセプト {#concepts}

-   ハッシュ結合: 結合リレーショナル代数を実装する方法。一方でハッシュ テーブルを構築し、もう一方でハッシュ テーブルを継続的に照合することで、結合の結果を取得します。
-   構築側: ハッシュ テーブルを構築するために使用されるハッシュ結合の一方の側。このドキュメントでは、デフォルトでハッシュ結合の右側のテーブルをビルド側と呼びます。
-   プローブ側: ハッシュ テーブルと継続的に照合するために使用されるハッシュ結合の一方の側。このドキュメントでは、デフォルトでハッシュ結合の左側のテーブルをプローブ側と呼びます。
-   フィルター: 述語とも呼ばれ、このドキュメントのフィルター条件を指します。

## ランタイムフィルターの動作原理 {#working-principles-of-runtime-filter}

ハッシュ結合は、右側のテーブルに基づいてハッシュ テーブルを構築し、左側のテーブルを使用してハッシュ テーブルを継続的に調査することによって結合操作を実行します。調査プロセス中に一部の結合キー値がハッシュ テーブルにヒットできない場合、データが正しいテーブルに存在せず、最終的な結合結果に表示されないことを意味します。したがって、TiDB がスキャン**中に結合キー データを事前にフィルタリング**できれば、スキャン時間とネットワーク オーバーヘッドが削減され、結合効率が大幅に向上します。

ランタイム フィルターは、クエリ計画フェーズ中に生成される**動的な述語**です。この述語には、TiDB 選択演算子の他の述語と同じ機能があります。これらの述語はすべてテーブル スキャン操作に適用され、述語に一致しない行をフィルターで除外します。唯一の違いは、ランタイム フィルターのパラメーター値がハッシュ結合ビルド プロセス中に生成された結果から取得されることです。

### 例 {#example}

`store_sales`テーブルと`date_dim`テーブルの間に結合クエリがあり、結合方法がハッシュ結合であるとします。 `store_sales`は、主に店舗の売上データを格納するファクトテーブルであり、行数は100万行である。 `date_dim`は、主に日付情報を格納する時間ディメンションテーブルである。 2001 年の売上データをクエリしたいと考えているため、 `date_dim`のテーブルの 365 行が結合操作に関係します。

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
    AND d_year = 2001;
```

ハッシュ結合の実行計画は通常次のとおりです。

                     +-------------------+
                     | PhysicalHashJoin  |
            +------->|                   |<------+
            |        +-------------------+       |
            |                                    |
            |                                    |
      100w  |                                    | 365
            |                                    |
            |                                    |
    +-------+-------+                   +--------+-------+
    | TableFullScan |                   | TableFullScan  |
    |  store_sales  |                   |    date_dim    |
    +---------------+                   +----------------+

*(上図では交換ノードおよびその他のノードを省略しています。)*

ランタイムフィルターの実行プロセスは次のとおりです。

1.  `date_dim`テーブルのデータをスキャンします。
2.  `PhysicalHashJoin`ビルド側のデータに基づいてフィルター条件を計算します ( `date_dim in (2001/01/01~2001/12/31)`など)。
3.  スキャンを待機している`TableFullScan`オペレータにフィルタ条件を送信します`store_sales` 。
4.  `store_sales`にフィルタ条件を適用し、 `PhysicalHashJoin`にフィルタリングしたデータを渡すことで、プローブ側でスキャンするデータ量とハッシュテーブルのマッチングの計算量を削減します。

<!---->

                             2. Build RF values
                +-------->+-------------------+
                |         |PhysicalHashJoin   |<-----+
                |    +----+                   |      |
    4. After RF |    |    +-------------------+      | 1. Scan T2
        5000    |    |3. Send RF                     |      365
                |    | filter data                   |
                |    |                               |
          +-----+----v------+                +-------+--------+
          |  TableFullScan  |                | TabelFullScan  |
          |  store_sales    |                |    date_dim    |
          +-----------------+                +----------------+

*(RF はランタイムフィルターの略です)*

上の 2 つの図から、スキャンされるデータの量が`store_sales`によって 100 万から 5000 に減少することがわかります。スキャンされるデータの量を`TableFullScan`に減らすことで、ランタイム フィルターはハッシュ テーブルと一致する回数を減らし、ハッシュ テーブルとの照合回数を減らすことができます。不要な I/O とネットワーク送信が削減され、結合操作の効率が大幅に向上します。

## ランタイムフィルターを使用する {#use-runtime-filter}

ランタイム フィルターを使用するには、 TiFlashレプリカを含むテーブルを作成し、 [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) ～ `LOCAL`を設定する必要があります。

TPC-DS データセットを例として、このセクションでは結合操作に`catalog_sales`テーブルと`date_dim`テーブルを使用して、ランタイム フィルターがクエリ効率をどのように向上させるかを説明します。

### ステップ 1. 結合するテーブルのTiFlashレプリカを作成する {#step-1-create-tiflash-replicas-for-tables-to-be-joined}

TiFlashレプリカを`catalog_sales`テーブルと`date_dim`テーブルのそれぞれに追加します。

```sql
ALTER TABLE catalog_sales SET tiflash REPLICA 1;
ALTER TABLE date_dim SET tiflash REPLICA 1;
```

2 つのテーブルのTiFlashレプリカの準備ができるまで、つまり、レプリカの`AVAILABLE`と`PROGRESS`フィールドが両方とも`1`なるまで待ちます。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+

SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### ステップ 2. ランタイムフィルターを有効にする {#step-2-enable-runtime-filter}

ランタイム フィルターを有効にするには、システム変数の値を[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)から`LOCAL`に設定します。

```sql
SET tidb_runtime_filter_mode="LOCAL";
```

変更が成功したかどうかを確認します。

```sql
SHOW VARIABLES LIKE "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

システム変数の値が`LOCAL`の場合、ランタイム フィルターが有効になります。

### ステップ 3. クエリを実行する {#step-3-execute-the-query}

クエリを実行する前に、 [`EXPLAIN`ステートメント](/sql-statements/sql-statement-explain.md)使用して実行計画を表示し、ランタイム フィルターが有効になっているかどうかを確認します。

```sql
EXPLAIN SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

ランタイム フィルターが有効になると、対応するランタイム フィルターが`HashJoin`ノードと`TableScan`ノードにマウントされ、ランタイム フィルターが正常に適用されたことが示されます。

    TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk
    HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |

完全なクエリ実行プランは次のとおりです。

    +----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
    | id                                     | estRows     | task         | access object       | operator info                                                                                                                                 |
    +----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
    | TableReader_53                         | 37343.19    | root         |                     | MppVersion: 1, data:ExchangeSender_52                                                                                                         |
    | └─ExchangeSender_52                    | 37343.19    | mpp[tiflash] |                     | ExchangeType: PassThrough                                                                                                                     |
    |   └─Projection_51                      | 37343.19    | mpp[tiflash] |                     | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         |
    |     └─HashJoin_48                      | 37343.19    | mpp[tiflash] |                     | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
    |       ├─ExchangeReceiver_29(Build)     | 1.00        | mpp[tiflash] |                     |                                                                                                                                               |
    |       │ └─ExchangeSender_28            | 1.00        | mpp[tiflash] |                     | ExchangeType: Broadcast, Compression: FAST                                                                                                    |
    |       │   └─TableFullScan_26           | 1.00        | mpp[tiflash] | table:date_dim      | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  |
    |       └─Selection_31(Probe)            | 71638034.00 | mpp[tiflash] |                     | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            |
    |         └─TableFullScan_30             | 71997669.00 | mpp[tiflash] | table:catalog_sales | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     |
    +----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
    9 rows in set (0.01 sec)

ここで SQL クエリを実行すると、ランタイム フィルターが適用されます。

```sql
SELECT cs_ship_date_sk FROM catalog_sales, date_dim
WHERE d_date = '2002-2-01' AND
     cs_ship_date_sk = d_date_sk;
```

### ステップ 4. パフォーマンスの比較 {#step-4-performance-comparison}

この例では、50 GB の TPC-DS データを使用します。ランタイム フィルターを有効にすると、クエリ時間が 0.38 秒から 0.17 秒に短縮され、効率が 50% 向上しました。 `ANALYZE`ステートメントを使用すると、ランタイム フィルターが有効になった後の各オペレーターの実行時間を表示できます。

ランタイム フィルターが有効になっていない場合のクエリの実行情報は次のとおりです。

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim WHERE d_date = '2002-2-01' AND cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows  | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                    | operator info                                                                                | memory  | disk |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574    | root         |                     | time:379.7ms, loops:83, RU:0.000000, cop_task: {num: 48, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                          | MppVersion: 1, data:ExchangeSender_52                                                        | 12.0 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | ExchangeType: PassThrough                                                                    | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | tpcds50.catalog_sales.cs_ship_date_sk                                                        | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)]    | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2        | mpp[tiflash] |                     | tiflash_task:{proc max:291.3ms, min:290ms, avg: 290.6ms, p80:291.3ms, p95:291.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  |                                                                                              | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1        | mpp[tiflash] |                     | tiflash_task:{proc max:290.9ms, min:0s, avg: 145.4ms, p80:290.9ms, p95:290.9ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                      | ExchangeType: Broadcast, Compression: FAST                                                   | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1        | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.88ms, min:0s, avg: 1.94ms, p80:3.88ms, p95:3.88ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                  | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 71638034 | mpp[tiflash] |                     | tiflash_task:{proc max:47ms, min:34.3ms, avg: 40.6ms, p80:47ms, p95:47ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                        | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                           | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 71997669 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:34ms, min:17.3ms, avg: 25.6ms, p80:34ms, p95:34ms, iters:1160, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:8893, total_skipped_packs:4007, total_scanned_rows:72056474, total_skipped_rows:32476901, total_rs_index_load_time: 8ms, total_read_time: 579ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false                                                   | N/A     | N/A  |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.38 sec)
```

ランタイム フィルターが有効になっている場合のクエリの実行情報は次のとおりです。

```sql
EXPLAIN ANALYZE SELECT cs_ship_date_sk FROM catalog_sales, date_dim
    -> WHERE d_date = '2002-2-01' AND
    ->      cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                 | memory  | disk |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574   | root         |                     | time:162.1ms, loops:82, RU:0.000000, cop_task: {num: 47, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                             | MppVersion: 1, data:ExchangeSender_52                                                                                                         | 12.7 KB | N/A  |
| └─ExchangeSender_52                    | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | ExchangeType: PassThrough                                                                                                                     | N/A     | N/A  |
|   └─Projection_51                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         | N/A     | N/A  |
|     └─HashJoin_48                      | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | 2       | mpp[tiflash] |                     | tiflash_task:{proc max:132.3ms, min:130.8ms, avg: 131.6ms, p80:132.3ms, p95:132.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   |                                                                                                                                               | N/A     | N/A  |
|       │ └─ExchangeSender_28            | 1.00        | 1       | mpp[tiflash] |                     | tiflash_task:{proc max:131ms, min:0s, avg: 65.5ms, p80:131ms, p95:131ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                                | ExchangeType: Broadcast, Compression: FAST                                                                                                    | N/A     | N/A  |
|       │   └─TableFullScan_26           | 1.00        | 1       | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.01ms, min:0s, avg: 1.51ms, p80:3.01ms, p95:3.01ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                     | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  | N/A     | N/A  |
|       └─Selection_31(Probe)            | 71638034.00 | 5308995 | mpp[tiflash] |                     | tiflash_task:{proc max:39.8ms, min:24.3ms, avg: 32.1ms, p80:39.8ms, p95:39.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                       | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            | N/A     | N/A  |
|         └─TableFullScan_30             | 71997669.00 | 5335549 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:36.8ms, min:23.3ms, avg: 30.1ms, p80:36.8ms, p95:36.8ms, iters:86, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:660, total_skipped_packs:12451, total_scanned_rows:5335549, total_skipped_rows:100905778, total_rs_index_load_time: 2ms, total_read_time: 47ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     | N/A     | N/A  |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.17 sec)
```

2 つのクエリの実行情報を比較すると、次の改善点がわかります。

-   IO の削減: TableFullScan オペレーターの`total_scanned_rows`比較すると、ランタイム フィルターが有効になった後、スキャン ボリューム`TableFullScan`が 2/3 削減されることがわかります。
-   ハッシュ結合のパフォーマンスの向上: `HashJoin`オペレーターの実行時間が 376.1 ミリ秒から 157.6 ミリ秒に短縮されました。

### ベストプラクティス {#best-practices}

ランタイム フィルターは、ファクト テーブルとディメンション テーブルの結合クエリなど、大きなテーブルと小さなテーブルが結合されるシナリオに適用できます。ディメンション テーブルに含まれるヒット データの量が少ないということは、フィルターに含まれる値が少ないことを意味するため、ファクト テーブルは条件を満たさないデータをより効果的にフィルターで除外できます。ファクト テーブル全体がスキャンされるデフォルトのシナリオと比較して、クエリのパフォーマンスが大幅に向上します。

TPC-DS における`Sales`テーブルと`date_dim`テーブルの結合操作はその代表的な例です。

## ランタイムフィルターの構成 {#configure-runtime-filter}

ランタイム フィルターを使用する場合、ランタイム フィルターのモードと述語の種類を構成できます。

### ランタイムフィルターモード {#runtime-filter-mode}

ランタイム フィルターのモードは、**フィルター送信者オペレーター**と**フィルター受信者オペレーター**の間の関係です。 `OFF` 、 `LOCAL` 、および`GLOBAL`の 3 つのモードがあります。 v7.3.0 では、 `OFF`および`LOCAL`モードのみがサポートされます。ランタイム フィルター モードは、システム変数[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)によって制御されます。

-   `OFF` : ランタイムフィルターは無効です。無効にした後のクエリの動作は、以前のバージョンと同じになります。
-   `LOCAL` : ランタイムフィルターはローカルモードで有効になります。ローカル モードでは、**フィルター送信者オペレーター**と**フィルター受信者オペレーターは**同じ MPP タスク内にあります。つまり、ランタイム フィルターは、HashJoin オペレーターと TableScan オペレーターが同じタスク内にあるシナリオに適用できます。現在、ランタイム フィルターはローカル モードのみをサポートしています。このモードを有効にするには、 `LOCAL`に設定します。
-   `GLOBAL` : 現在、グローバル モードはサポートされていません。ランタイム フィルターをこのモードに設定することはできません。

### ランタイムフィルターの種類 {#runtime-filter-type}

実行時フィルターのタイプは、生成されたフィルター演算子によって使用される述語のタイプです。現在、サポートされているタイプは`IN`のみです。これは、生成された述語が`k1 in (xxx)`に似ていることを意味します。ランタイム フィルターのタイプは、システム変数[`tidb_runtime_filter_type`](/system-variables.md#tidb_runtime_filter_type-new-in-v720)によって制御されます。

-   `IN` : デフォルトのタイプ。これは、生成されたランタイム フィルターが`IN`種類の述語を使用することを意味します。

## 制限事項 {#limitations}

-   ランタイム フィルターは MPPアーキテクチャの最適化であり、 TiFlashにプッシュダウンされたクエリにのみ適用できます。
-   結合タイプ: 左外部結合、完全外部結合、およびアンチ結合 (左のテーブルがプローブ側の場合) は、ランタイム フィルターをサポートしません。ランタイム フィルターは結合に含まれるデータを事前にフィルター処理するため、前述の種類の結合では一致しないデータが破棄されないため、ランタイム フィルターは使用できません。
-   等価結合式: 等価結合式のプローブ列が複雑な式である場合、またはプローブ列のタイプが JSON、Blob、Array、またはその他の複雑なデータ型である場合、ランタイム フィルターは生成されません。主な理由は、前述のタイプの列が結合列として使用されることがほとんどないためです。フィルタが生成されたとしても、フィルタリング率は通常低いです。

前述の制限事項について、ランタイム フィルターが正しく生成されているかどうかを確認する必要がある場合は、 [`EXPLAIN`ステートメント](/sql-statements/sql-statement-explain.md)を使用して実行計画を確認できます。
