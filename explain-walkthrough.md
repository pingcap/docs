---
title: EXPLAIN Walkthrough
summary: 例文を順に見ながらEXPLAINの使い方を学びます
---

# <code>EXPLAIN</code>ウォークスルー {#code-explain-code-walkthrough}

SQLは宣言型言語であるため、クエリが効率的に実行されたかどうかを自動的に判断することはできません。まず[`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用して、現在の実行プランを確認する必要があります。

<CustomContent platform="tidb">

[自転車シェアリングのサンプルデータベース](/import-example-data.md)からの次の文は、2017 年 7 月 1 日に何回旅行が行われたかを数えています。

</CustomContent>

<CustomContent platform="tidb-cloud">

[自転車シェアリングのサンプルデータベース](/tidb-cloud/import-sample-data.md)からの次の文は、2017 年 7 月 1 日に何回旅行が行われたかを数えています。

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

子演算子`└─TableFullScan_18`から戻ると、その実行プロセスは次のようになります。これは現時点では最適ではありません。

1.  コプロセッサ（TiKV）は、 `trips`テーブル全体を`TableFullScan`演算として読み取ります。その後、読み取った行をTiKV内の`Selection_19`の演算子に渡します。
2.  述語`WHERE start_date BETWEEN ..`演算子`Selection_19`でフィルタリングされます。この選択に該当する行は約`250`行と推定されます。この数は統計情報と演算子のロジックに基づいて推定されることに注意してください。演算子`└─TableFullScan_18` `stats:pseudo`表示されますが、これはテーブルに実際の統計情報が存在しないことを意味します。11 `ANALYZE TABLE trips`実行して統計情報を収集すると、統計の精度が向上することが期待されます。
3.  選択基準を満たす行には、関数`count`が適用されます。これも演算子`StreamAgg_9`内で完了しますが、演算子 3 も TiKV 内にあります ( `cop[tikv]` )。TiKV コプロセッサは、MySQL の組み込み関数を多数実行できます。そのうちの 1 つが`count`です。
4.  `StreamAgg_9`の結果は、TiDBサーバー内にある`TableReader_21`演算子（ `root`のタスク）に送信されます。この演算子の`estRows`列目の値は`1`です。これは、演算子がアクセス対象のTiKVリージョンごとに1行ずつ受け取ることを意味します。これらのリクエストの詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)参照してください。
5.  次に、演算子`StreamAgg_20`は演算子`└─TableReader_21`の各行に関数`count`適用します。これは演算子[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)からもわかるように、約 56 行になります。これはルート演算子であるため、結果をクライアントに返します。

> **注記：**
>
> テーブルに含まれる地域の一般的なビューを表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)実行します。

## 現在のパフォーマンスを評価する {#assess-the-current-performance}

`EXPLAIN`クエリ実行プランを返すだけで、クエリは実行されません。実際の実行時間を取得するには、クエリを実行するか、 `EXPLAIN ANALYZE`使用してください。

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

上記のクエリの例は実行に`1.03`秒かかりますが、これは理想的なパフォーマンスではありません。

上記`EXPLAIN ANALYZE`の結果から、 `actRows`推定値の一部（ `estRows` ）が不正確であることを示しています（1万行と予想していたのに1900万行が検出された）。これは`└─TableFullScan_18`の`operator info` （ `stats:pseudo` ）で既に示されています。まず[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行し、次に`EXPLAIN ANALYZE`実行すると、推定値がはるかに近くなることがわかります。

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

`ANALYZE TABLE`実行すると、演算子`└─TableFullScan_18`推定行数が正確であり、演算子`└─Selection_19`の推定行数も大幅に近づいたことがわかります。上記の 2 つのケースでは、実行プラン（TiDB がこのクエリを実行するために使用する演算子セット）は変更されていませんが、統計情報が古くなっているために、最適ではないプランが頻繁に発生します。

`ANALYZE TABLE`に加えて、TiDB はしきい値[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)に達した後、バックグラウンド操作として統計情報を自動的に再生成します。5 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを実行すると、TiDB がこのしきい値にどれだけ近いか（TiDB が統計情報をどの程度健全であると見なしているか）を確認できます。

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

現在の実行プランは、次の点で効率的です。

-   作業の大部分はTiKVコプロセッサ内で処理されます。ネットワークを介してTiDBに送り返され、処理されるのは56行のみです。これらの行はそれぞれ短く、選択範囲に一致するカウントのみが格納されます。

-   TiDB ( `StreamAgg_20` )とTiKV ( `└─StreamAgg_9` )の両方で行数を集計するには、メモリ使用量の面で非常に効率的なストリーム集計を使用します。

現在の実行プランの最大の問題は、述語`start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'`すぐに適用されないことです。まず演算子`TableFullScan`ですべての行が読み込まれ、その後選択が適用されます。5 `SHOW CREATE TABLE trips`出力から原因がわかります。

```sql
SHOW CREATE TABLE trips\G
```

```sql
*************************** 1. row ***************************
       Table: trips
Create Table: CREATE TABLE `trips` (
  `trip_id` bigint NOT NULL AUTO_INCREMENT,
  `duration` int NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_station_number` int DEFAULT NULL,
  `start_station` varchar(255) DEFAULT NULL,
  `end_station_number` int DEFAULT NULL,
  `end_station` varchar(255) DEFAULT NULL,
  `bike_number` varchar(255) DEFAULT NULL,
  `member_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=20477318
1 row in set (0.00 sec)
```

`start_date`にはインデックスが**ありません**。この述語をインデックスリーダー演算子にプッシュするには、インデックスが必要です。次のようにインデックスを追加してください。

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **注記：**
>
> DDLジョブの進行状況は、 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して監視できます。TiDBのデフォルト設定は、インデックスの追加が本番環境の本番ロードに過度な影響を与えないよう、慎重に選択されています。テスト環境では、 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)値を増やすことを検討してください。リファレンスシステムでは、バッチサイズを`10240` 、ワーカー数を`32`にすることで、デフォルト設定の10倍のパフォーマンス向上を実現できます。

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
> Another optimization that applies here is the coprocessor cache. If you are unable to add indexes, consider enabling the [コプロセッサキャッシュ](/coprocessor-cache.md). When it is enabled, as long as the Region has not been modified since the operator is last executed, TiKV will return the value from the cache. This will also help reduce much of the cost of the expensive `TableFullScan` and `Selection` operators.

## サブクエリの早期実行を無効にする {#disable-the-early-execution-of-subqueries}

クエリの最適化中、TiDB は直接計算できるサブクエリを事前に実行します。例:

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

上記の例では、 `a = (SELECT a FROM t1)`サブクエリは最適化中に計算され、 `t2.a=1`に書き換えられます。これにより、最適化中に定数伝播やフォールディングなどの最適化が可能になります。ただし、 `EXPLAIN`のステートメントの実行時間に影響します。サブクエリ自体の実行に時間がかかる場合、 `EXPLAIN`ステートメントが完了しない可能性があり、オンライントラブルシューティングに影響する可能性があります。

TiDB v7.3.0以降、システム変数[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)が導入されました。この変数は、 `EXPLAIN`におけるこのようなサブクエリの事前実行を無効にするかどうかを制御します。この変数のデフォルト値は`OFF`で、これはサブクエリが事前計算されることを意味します。この変数を`ON`に設定すると、サブクエリの事前実行が無効になります。

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

ご覧のとおり、スカラーサブクエリは実行中に展開されないため、このような SQL の具体的な実行プロセスを理解しやすくなります。

> **注記：**
>
> [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) `EXPLAIN`ステートメントの動作にのみ影響し、 `EXPLAIN ANALYZE`ステートメントは引き続きサブクエリを事前に実行します。
