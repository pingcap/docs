---
title: EXPLAIN Walkthrough
summary: Learn how to use EXPLAIN by walking through an example statement
---

# <code>EXPLAIN</code>ウォークスルー {#code-explain-code-walkthrough}

SQL は宣言型言語であるため、クエリが効率的に実行されたかどうかを自動的に判断することはできません。まず[`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用して、現在の実行計画を確認する必要があります。

<CustomContent platform="tidb">

[自転車シェアのサンプル データベース](/import-example-data.md)の次のステートメントは、2017 年 7 月 1 日に行われた旅行の数をカウントします。

</CustomContent>

<CustomContent platform="tidb-cloud">

[自転車シェアのサンプル データベース](/tidb-cloud/import-sample-data.md)の次のステートメントは、2017 年 7 月 1 日に行われた旅行の数をカウントします。

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

子演算子`└─TableFullScan_18`から遡ると、次のような実行プロセスがわかりますが、これは現時点では最適ではありません。

1.  コプロセッサ (TiKV) は、 `trips`テーブル全体を`TableFullScan`操作として読み取ります。次に、読み取った行を TiKV 内にある`Selection_19`オペレーターに渡します。
2.  次に、 `WHERE start_date BETWEEN ..`述語が`Selection_19`演算子でフィルタリングされます。約`250`行がこの選択を満たすと推定されます。この数値は統計とオペレーターのロジックに従って推定されることに注意してください。 `└─TableFullScan_18`演算子は`stats:pseudo`を示します。これは、テーブルに実際の統計情報がないことを意味します。 `ANALYZE TABLE trips`を実行して統計情報を収集すると、統計はより正確になることが期待されます。
3.  選択基準を満たす行には`count`関数が適用されます。これも、TiKV ( `cop[tikv]` ) 内にある`StreamAgg_9`オペレーター内で完了します。 TiKV コプロセッサは、多数の MySQL 組み込み関数を実行できます。そのうちの 1 つは`count`です。
4.  `StreamAgg_9`の結果は、TiDBサーバー内にある`TableReader_21`オペレーターに送信されます ( `root`のタスク)。この演算子の`estRows`列の値は`1`です。これは、演算子がアクセスされる各 TiKV リージョンから 1 行を受け取ることを意味します。これらのリクエストの詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を参照してください。
5.  次に、 `StreamAgg_20`演算子は`└─TableReader_21`演算子からの各行に`count`関数を適用します。これは[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)からわかるように、約 56 行になります。これはルート オペレーターであるため、結果をクライアントに返します。

> **注記：**
>
> テーブルに含まれるリージョンの概要を表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)を実行します。

## 現在のパフォーマンスを評価する {#assess-the-current-performance}

`EXPLAIN`クエリ実行プランを返すだけで、クエリは実行されません。実際の実行時間を取得するには、クエリを実行するか、 `EXPLAIN ANALYZE`使用します。

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

上記のクエリ例の実行には`1.03`秒かかりますが、これは理想的なパフォーマンスです。

上記`EXPLAIN ANALYZE`の結果から、 `actRows`推定値 ( `estRows` ) の一部が不正確であることを示します (10,000 行を期待していましたが、1,900 万行が見つかりました)。これは`└─TableFullScan_18`の`operator info` ( `stats:pseudo` ) ですでに示されています。最初に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行し、次に`EXPLAIN ANALYZE`再度実行すると、推定値がかなり近くなることがわかります。

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

`ANALYZE TABLE`が実行されると、 `└─TableFullScan_18`演算子の推定行が正確で、 `└─Selection_19`の推定もかなり近づいていることがわかります。上記の 2 つのケースでは、実行計画 (TiDB がこのクエリを実行するために使用する一連の演算子) は変更されていませんが、古い統計が原因で次善の計画が発生することがよくあります。

`ANALYZE TABLE`に加えて、TiDB はしきい値[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)に達した後、バックグラウンド操作として統計を自動的に再生成します。次の[`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを実行すると、TiDB がこのしきい値にどの程度近づいているか (TiDB が統計がどの程度健全であるとみなしているか) を確認できます。

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

-   作業のほとんどは TiKV コプロセッサ内で処理されます。処理のためにネットワーク経由で TiDB に送り返す必要があるのは 56 行だけです。これらの各行は短く、選択内容に一致するカウントのみが含まれます。

-   TiDB ( `StreamAgg_20` ) と TiKV ( `└─StreamAgg_9` ) の両方の行数の集計には、メモリ使用量が非常に効率的なストリーム集計が使用されます。

現在の実行計画の最大の問題は、述語`start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'`すぐに適用されないことです。最初に`TableFullScan`演算子を使用してすべての行が読み取られ、その後選択が適用されます。 `SHOW CREATE TABLE trips`の出力から原因を見つけることができます。

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

`start_date`にはインデックスがありませ**ん**。この述語をインデックス リーダー演算子にプッシュするにはインデックスが必要です。次のようにインデックスを追加します。

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **注記：**
>
> [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、DDL ジョブの進行状況を監視できます。 TiDB のデフォルトは、インデックスの追加が実本番ワークロードに大きな影響を与えないよう慎重に選択されています。テスト環境の場合は、 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)値を増やすことを検討してください。リファレンス システムでは、バッチ サイズ`10240`とワーカー数`32`により、デフォルトと比較して 10 倍のパフォーマンス向上を達成できます。

インデックスを追加した後、 `EXPLAIN`のクエリを繰り返すことができます。次の出力では、新しい実行プランが選択され、 `TableFullScan`と`Selection`演算子が削除されていることがわかります。

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

実際の実行時間を比較するには、再度[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用します。

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
> ここで適用されるもう 1 つの最適化は、コプロセッサ キャッシュです。インデックスを追加できない場合は、 [コプロセッサキャッシュ](/coprocessor-cache.md)を有効にすることを検討してください。これが有効な場合、オペレーターが最後に実行されてからリージョンが変更されていない限り、TiKV はキャッシュから値を返します。これは、高価な`TableFullScan`および`Selection`オペレータのコストの大幅な削減にも役立ちます。

## サブクエリの早期実行を無効にする {#disable-the-early-execution-of-subqueries}

クエリの最適化中に、TiDB は直接計算できるサブクエリを事前に実行します。例えば：

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

前の例では、 `a = (SELECT a FROM t1)`サブクエリが最適化中に計算され、 `t2.a=1`として書き換えられます。これにより、最適化中の定数伝播やフォールディングなど、より多くの最適化が可能になります。ただし、 `EXPLAIN`ステートメントの実行時間には影響します。サブクエリ自体の実行に時間がかかる場合、 `EXPLAIN`ステートメントが完了しない可能性があり、オンライン トラブルシューティングに影響を与える可能性があります。

v7.3.0 以降、TiDB は[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)システム変数を導入します。これは、 `EXPLAIN`でそのようなサブクエリの事前実行を無効にするかどうかを制御します。この変数のデフォルト値は`OFF`で、これはサブクエリが事前に計算されることを意味します。この変数を`ON`に設定すると、サブクエリの事前実行を無効にすることができます。

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

ご覧のとおり、スカラー サブクエリは実行中に展開されないため、SQL の具体的な実行プロセスを理解しやすくなります。

> **注記：**
>
> [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)ステートメント`EXPLAIN`の動作にのみ影響し、ステートメント`EXPLAIN ANALYZE`は引き続き事前にサブクエリを実行します。
