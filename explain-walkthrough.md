---
title: EXPLAIN Walkthrough
summary: 例文を順に見ながらEXPLAINの使い方を学びます
---

# <code>EXPLAIN</code>ウォークスルー {#code-explain-code-walkthrough}

SQL は宣言型言語であるため、クエリが効率的に実行されたかどうかを自動的に判断することはできません。まず[`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用して、現在の実行プランを確認する必要があります。

<CustomContent platform="tidb">

[バイクシェアのサンプルデータベース](/import-example-data.md)からの次の文は、2017 年 7 月 1 日に何回旅行が行われたかを数えています。

</CustomContent>

<CustomContent platform="tidb-cloud">

[バイクシェアのサンプルデータベース](/tidb-cloud/import-sample-data.md)からの次の文は、2017 年 7 月 1 日に何回旅行が行われたかを数えています。

</CustomContent>

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| id                           | estRows  | task      | access object | operator info                                                                                                          |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| StreamAgg_20                 | 1.00     | root      |               | funcs:count(Column#13)->Column#11                                                                                      |
| └─TableReader_21             | 1.00     | root      |               | data:StreamAgg_9                                                                                                       |
|   └─StreamAgg_9              | 1.00     | cop[tikv] |               | funcs:count(1)->Column#13                                                                                              |
|     └─Selection_19           | 250.00   | cop[tikv] |               | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) |
|       └─TableFullScan_18     | 10000.00 | cop[tikv] | table:trips   | keep order:false, stats:pseudo                                                                                         |
+------------------------------+----------+-----------+---------------+------------------------------------------------------------------------------------------------------------------------+
5 rows in set (0.00 sec)
```

子演算子`└─TableFullScan_18`から遡ると、その実行プロセスは次のようになりますが、これは現時点では最適ではありません。

1.  コプロセッサ (TiKV) は、 `trips`テーブル全体を`TableFullScan`操作として読み取ります。次に、読み取った行を、TiKV 内にある`Selection_19`演算子に渡します。
2.  次に、述語`WHERE start_date BETWEEN ..`は演算子`Selection_19`でフィルタリングされます。この選択を満たす行は約`250`行と推定されます。この数は統計と演算子のロジックに基づいて推定されることに注意してください。演算子`└─TableFullScan_18` `stats:pseudo`示します。これは、テーブルに実際の統計情報がないことを意味します。統計情報を収集するために`ANALYZE TABLE trips`実行すると、統計がより正確になると予想されます。
3.  選択基準を満たす行には、 `count`関数が適用されます。これも`StreamAgg_9`演算子内で完了しますが、これは TiKV ( `cop[tikv]` ) 内にあります。TiKV コプロセッサは、MySQL 組み込み関数の多くを実行できますが、 `count`もその 1 つです。
4.  `StreamAgg_9`の結果は、現在 TiDBサーバー内にある`TableReader_21`演算子に送信されます ( `root`のタスク)。この演算子の`estRows`列の値は`1`です。これは、演算子がアクセスする各 TiKV 領域から 1 行を受け取ることを意味します。これらの要求の詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)参照してください。
5.  次に、 `StreamAgg_20`演算子は`└─TableReader_21`演算子の各行に`count`関数を適用します。これは[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)からわかるように約 56 行になります。これはルート演算子であるため、クライアントに結果を返します。

> **注記：**
>
> テーブルに含まれるリージョンの一般的なビューを表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)実行します。

## 現在のパフォーマンスを評価する {#assess-the-current-performance}

`EXPLAIN`クエリ実行プランを返すだけで、クエリは実行しません。実際の実行時間を取得するには、クエリを実行するか、 `EXPLAIN ANALYZE`使用します。

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows  | actRows  | task      | access object | execution info                                                                                                                                                                                                                                    | operator info                                                                                                          | memory    | disk |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00     | 1        | root      |               | time:1.031417203s, loops:2                                                                                                                                                                                                                        | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00     | 56       | root      |               | time:1.031408123s, loops:2, cop_task: {num: 56, max: 782.147269ms, min: 5.759953ms, avg: 252.005927ms, p95: 609.294603ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 11.524s, tot_wait: 580ms, rpc_num: 56, rpc_time: 14.111932641s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00     | 56       | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                              | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 250.00   | 11409    | cop[tikv] |               | proc max:640ms, min:8ms, p80:276ms, p95:476ms, iters:18695, tasks:56                                                                                                                                                                              | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 10000.00 | 19117643 | cop[tikv] | table:trips   | proc max:612ms, min:8ms, p80:248ms, p95:460ms, iters:18695, tasks:56                                                                                                                                                                              | keep order:false, stats:pseudo                                                                                         | N/A       | N/A  |
+------------------------------+----------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (1.03 sec)
```

上記の例のクエリの実行には`1.03`秒かかりますが、これは理想的なパフォーマンスです。

上記`EXPLAIN ANALYZE`の結果から、 `actRows`推定値の一部 ( `estRows` ) が不正確であることを示しています (1 万行を予想していたが 1,900 万行が検出された)。これは`└─TableFullScan_18`の`operator info` ( `stats:pseudo` ) ですでに示されています。 最初に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行し、次に`EXPLAIN ANALYZE`もう一度実行すると、推定値がはるかに近くなることがわかります。

```sql
ANALYZE TABLE trips;
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
Query OK, 0 rows affected (10.22 sec)

+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| id                           | estRows     | actRows  | task      | access object | execution info                                                                                                                                                                                                                                   | operator info                                                                                                          | memory    | disk |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
| StreamAgg_20                 | 1.00        | 1        | root      |               | time:926.393612ms, loops:2                                                                                                                                                                                                                       | funcs:count(Column#13)->Column#11                                                                                      | 632 Bytes | N/A  |
| └─TableReader_21             | 1.00        | 56       | root      |               | time:926.384792ms, loops:2, cop_task: {num: 56, max: 850.94424ms, min: 6.042079ms, avg: 234.987725ms, p95: 495.474806ms, max_proc_keys: 910371, p95_proc_keys: 704775, tot_proc: 10.656s, tot_wait: 904ms, rpc_num: 56, rpc_time: 13.158911952s} | data:StreamAgg_9                                                                                                       | 328 Bytes | N/A  |
|   └─StreamAgg_9              | 1.00        | 56       | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | funcs:count(1)->Column#13                                                                                              | N/A       | N/A  |
|     └─Selection_19           | 432.89      | 11409    | cop[tikv] |               | proc max:592ms, min:4ms, p80:244ms, p95:480ms, iters:18695, tasks:56                                                                                                                                                                             | ge(bikeshare.trips.start_date, 2017-07-01 00:00:00.000000), le(bikeshare.trips.start_date, 2017-07-01 23:59:59.000000) | N/A       | N/A  |
|       └─TableFullScan_18     | 19117643.00 | 19117643 | cop[tikv] | table:trips   | proc max:564ms, min:4ms, p80:228ms, p95:456ms, iters:18695, tasks:56                                                                                                                                                                             | keep order:false                                                                                                       | N/A       | N/A  |
+------------------------------+-------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------+-----------+------+
5 rows in set (0.93 sec)
```

`ANALYZE TABLE`が実行されると、 `└─TableFullScan_18`演算子の推定行数が正確であり、 `└─Selection_19`の推定値も大幅に近くなっていることがわかります。上記の 2 つのケースでは、実行プラン (TiDB がこのクエリを実行するために使用する演算子のセット) は変更されていませんが、統計が古くなっているために、最適ではないプランが頻繁に発生します。

`ANALYZE TABLE`に加えて、しきい値[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)に達した後、TiDB はバックグラウンド操作として統計を自動的に再生成します[`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを実行すると、TiDB がこのしきい値にどれだけ近いか (TiDB が統計をどれだけ健全であると見なしているか) を確認できます。

```sql
SHOW STATS_HEALTHY;
```

```sql
+-----------+------------+----------------+---------+
| Db_name   | Table_name | Partition_name | Healthy |
+-----------+------------+----------------+---------+
| bikeshare | trips      |                |     100 |
+-----------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## 最適化を特定する {#identify-optimizations}

現在の実行計画は、次の点で効率的です。

-   作業のほとんどは TiKV コプロセッサ内で処理されます。処理のためにネットワーク経由で TiDB に送り返す必要があるのは 56 行だけです。これらの各行は短く、選択に一致するカウントのみが含まれています。

-   TiDB（ `StreamAgg_20` ）とTiKV（ `└─StreamAgg_9` ）の両方で行数を集計するには、メモリ使用量が非常に効率的なストリーム集計を使用します。

現在の実行プランの最大の問題は、述語`start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'`すぐに適用されないことです。すべての行は最初に`TableFullScan`演算子で読み取られ、その後選択が適用されます。原因は`SHOW CREATE TABLE trips`の出力からわかります。

```sql
SHOW CREATE TABLE trips\G
```

```sql
*************************** 1. row ***************************
       Table: trips
Create Table: CREATE TABLE `trips` (
  `trip_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `duration` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int(11) DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int(11) DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=20477318
1 row in set (0.00 sec)
```

`start_date`にはインデックスが**ありません**。この述語をインデックス リーダー演算子にプッシュするには、インデックスが必要です。次のようにインデックスを追加します。

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **注記：**
>
> [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、DDL ジョブの進行状況を監視できます。TiDB のデフォルトは、インデックスを追加しても本番ワークロードにあまり影響が及ばないように慎重に選択されています。テスト環境では、 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)値を増やすことを検討してください。リファレンス システムでは、バッチ サイズを`10240` 、ワーカー数を`32`にすると、デフォルトよりも 10 倍のパフォーマンス向上が実現できます。

インデックスを追加したら、 `EXPLAIN`のクエリを繰り返すことができます。次の出力では、新しい実行プランが選択され、 `TableFullScan`と`Selection`演算子が削除されていることがわかります。

```sql
EXPLAIN SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| id                          | estRows | task      | access object                             | operator info                                                     |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
| StreamAgg_17                | 1.00    | root      |                                           | funcs:count(Column#13)->Column#11                                 |
| └─IndexReader_18            | 1.00    | root      |                                           | index:StreamAgg_9                                                 |
|   └─StreamAgg_9             | 1.00    | cop[tikv] |                                           | funcs:count(1)->Column#13                                         |
|     └─IndexRangeScan_16     | 8471.88 | cop[tikv] | table:trips, index:start_date(start_date) | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false |
+-----------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

実際の実行時間を比較するには、再度[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)使用します。

```sql
EXPLAIN ANALYZE SELECT count(*) FROM trips WHERE start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59';
```

```sql
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| id                          | estRows | actRows | task      | access object                             | execution info                                                                                                   | operator info                                                     | memory    | disk |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
| StreamAgg_17                | 1.00    | 1       | root      |                                           | time:4.516728ms, loops:2                                                                                         | funcs:count(Column#13)->Column#11                                 | 372 Bytes | N/A  |
| └─IndexReader_18            | 1.00    | 1       | root      |                                           | time:4.514278ms, loops:2, cop_task: {num: 1, max:4.462288ms, proc_keys: 11409, rpc_num: 1, rpc_time: 4.457148ms} | index:StreamAgg_9                                                 | 238 Bytes | N/A  |
|   └─StreamAgg_9             | 1.00    | 1       | cop[tikv] |                                           | time:4ms, loops:12                                                                                               | funcs:count(1)->Column#13                                         | N/A       | N/A  |
|     └─IndexRangeScan_16     | 8471.88 | 11409   | cop[tikv] | table:trips, index:start_date(start_date) | time:4ms, loops:12                                                                                               | range:[2017-07-01 00:00:00,2017-07-01 23:59:59], keep order:false | N/A       | N/A  |
+-----------------------------+---------+---------+-----------+-------------------------------------------+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------+-----------+------+
4 rows in set (0.00 sec)
```

上記の結果から、クエリ時間は 1.03 秒から 0.0 秒に短縮されました。

> **注記：**
>
> ここで適用されるもう 1 つの最適化は、コプロセッサ キャッシュです。インデックスを追加できない場合は、 [コプロセッサキャッシュ](/coprocessor-cache.md)を有効にすることを検討してください。有効にすると、演算子が最後に実行されてからリージョンが変更されていない限り、TiKV はキャッシュから値を返します。これにより、高価な`TableFullScan`および`Selection`演算子のコストを大幅に削減することもできます。

## サブクエリの早期実行を無効にする {#disable-the-early-execution-of-subqueries}

クエリの最適化中に、TiDB は直接計算できるサブクエリを事前に実行します。例:

```sql
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES(1);
CREATE TABLE t2(a int);
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+--------------------------+----------+-----------+---------------+--------------------------------+
| id                       | estRows  | task      | access object | operator info                  |
+--------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_14           | 10.00    | root      |               | data:Selection_13              |
| └─Selection_13           | 10.00    | cop[tikv] |               | eq(test.t2.a, 1)               |
|   └─TableFullScan_12     | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo |
+--------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

前の例では、 `a = (SELECT a FROM t1)`サブクエリは最適化中に計算され、 `t2.a=1`に書き換えられます。これにより、最適化中に定数の伝播や折りたたみなどの最適化をさらに行うことができます。ただし、 `EXPLAIN`ステートメントの実行時間に影響します。サブクエリ自体の実行に時間がかかる場合、 `EXPLAIN`ステートメントが完了しない可能性があり、オンライン トラブルシューティングに影響する可能性があります。

v7.3.0 以降、TiDB は[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)システム変数を導入し、 `EXPLAIN`でこのようなサブクエリの事前実行を無効にするかどうかを制御します。この変数のデフォルト値は`OFF`で、サブクエリが事前に計算されることを意味します。この変数を`ON`に設定すると、サブクエリの事前実行を無効にすることができます。

```sql
SET @@tidb_opt_enable_non_eval_scalar_subquery = ON;
EXPLAIN SELECT * FROM t2 WHERE a = (SELECT a FROM t1);
```

```sql
+---------------------------+----------+-----------+---------------+---------------------------------+
| id                        | estRows  | task      | access object | operator info                   |
+---------------------------+----------+-----------+---------------+---------------------------------+
| Selection_13              | 8000.00  | root      |               | eq(test.t2.a, ScalarQueryCol#5) |
| └─TableReader_15          | 10000.00 | root      |               | data:TableFullScan_14           |
|   └─TableFullScan_14      | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo  |
| ScalarSubQuery_10         | N/A      | root      |               | Output: ScalarQueryCol#5        |
| └─MaxOneRow_6             | 1.00     | root      |               |                                 |
|   └─TableReader_9         | 1.00     | root      |               | data:TableFullScan_8            |
|     └─TableFullScan_8     | 1.00     | cop[tikv] | table:t1      | keep order:false, stats:pseudo  |
+---------------------------+----------+-----------+---------------+---------------------------------+
7 rows in set (0.00 sec)
```

ご覧のとおり、スカラー サブクエリは実行中に展開されないため、このような SQL の具体的な実行プロセスを理解しやすくなります。

> **注記：**
>
> [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) `EXPLAIN`ステートメントの動作にのみ影響し、 `EXPLAIN ANALYZE`ステートメントは引き続きサブクエリを事前に実行します。
