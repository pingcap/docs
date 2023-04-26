---
title: EXPLAIN Walkthrough
summary: Learn how to use EXPLAIN by walking through an example statement
---

# <code>EXPLAIN</code>ウォークスルー {#code-explain-code-walkthrough}

SQL は宣言型言語であるため、クエリが効率的に実行されているかどうかを自動的に判断することはできません。現在の実行計画を知るには、最初に[`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用する必要があります。

<CustomContent platform="tidb">

[バイクシェア サンプル データベース](/import-example-data.md)からの次のステートメントは、2017 年 7 月 1 日に行われた旅行の数をカウントします。

</CustomContent>

<CustomContent platform="tidb-cloud">

[バイクシェア サンプル データベース](/tidb-cloud/import-sample-data.md)からの次のステートメントは、2017 年 7 月 1 日に行われた旅行の数をカウントします。

</CustomContent>

{{< copyable "" >}}

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

子オペレーター`└─TableFullScan_18`から戻ると、次のような実行プロセスを見ることができますが、これは現在最適ではありません。

1.  コプロセッサー (TiKV) は、 `trips`テーブル全体を`TableFullScan`操作として読み取ります。次に、読み取った行をまだ TiKV 内にある`Selection_19`オペレーターに渡します。
2.  次に、述語`WHERE start_date BETWEEN ..`が`Selection_19`演算子でフィルター処理されます。この選択を満たすには、約`250`行が推定されます。この数は、統計とオペレーターのロジックに従って推定されることに注意してください。 `└─TableFullScan_18`演算子は`stats:pseudo`を示します。これは、テーブルに実際の統計情報がないことを意味します。 `ANALYZE TABLE trips`を実行して統計情報を収集すると、統計はより正確になることが期待されます。
3.  選択基準を満たす行には、 `count`関数が適用されます。これは、まだ TiKV ( `cop[tikv]` ) 内にある`StreamAgg_9`オペレーター内でも完了します。 TiKV コプロセッサは多数の MySQL 組み込み関数を実行できます。そのうちの`count`はその 1 つです。
4.  `StreamAgg_9`からの結果は、現在 TiDBサーバー内にある`TableReader_21`オペレーターに送信されます ( `root`のタスク)。このオペレーターの`estRows`列の値は`1`です。これは、オペレーターが、アクセスする各 TiKV リージョンから 1 行を受け取ることを意味します。これらのリクエストの詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を参照してください。
5.  `StreamAgg_20`演算子は、 `└─TableReader_21`演算子の各行に`count`関数を適用します。これは[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)からわかるように、約 56 行になります。これはルート オペレータであるため、クライアントに結果を返します。

> **ノート：**
>
> テーブルに含まれるリージョンの一般的なビューを表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)を実行します。

## 現在のパフォーマンスを評価する {#assess-the-current-performance}

`EXPLAIN`クエリ実行プランのみを返しますが、クエリは実行しません。実際の実行時間を取得するには、クエリを実行するか、 `EXPLAIN ANALYZE`使用できます。

{{< copyable "" >}}

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

上記のクエリの例では、実行に`1.03`秒かかります。これは理想的なパフォーマンスです。

上記の`EXPLAIN ANALYZE`の結果から、 `actRows`推定値 ( `estRows` ) の一部が不正確であることを示します (10,000 行を期待しているが、1,900 万行を検出)。これは、 `└─TableFullScan_18`の`operator info` ( `stats:pseudo` ) で既に示されています。最初に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)実行してからもう一度`EXPLAIN ANALYZE`を実行すると、推定値がはるかに近いことがわかります。

{{< copyable "" >}}

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

`ANALYZE TABLE`が実行された後、 `└─TableFullScan_18`演算子の推定行数が正確であり、 `└─Selection_19`の推定値もかなり近いことがわかります。上記の 2 つのケースでは、実行計画 (TiDB がこのクエリを実行するために使用する一連の演算子) は変更されていませんが、古い統計が原因で最適ではない計画が頻繁に発生します。

`ANALYZE TABLE`に加えて、TiDB は[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)のしきい値に達すると、バックグラウンド操作として統計を自動的に再生成します。 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを実行すると、TiDB がこのしきい値にどれだけ近づいているか (TiDB が統計をどの程度健全であると見なすか) を確認できます。

{{< copyable "" >}}

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

-   ほとんどの作業は、TiKV コプロセッサー内で処理されます。処理のためにネットワークを介して TiDB に送り返す必要があるのは 56 行だけです。これらの各行は短く、選択に一致するカウントのみが含まれます。

-   TiDB ( `StreamAgg_20` ) と TiKV ( `└─StreamAgg_9` ) の両方で行数を集計するには、メモリ使用量が非常に効率的なストリーム集計を使用します。

現在の実行計画の最大の問題は、述語`start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'`すぐに適用されないことです。最初にすべての行が`TableFullScan`演算子で読み取られ、その後で選択が適用されます。 `SHOW CREATE TABLE trips`の出力から原因を見つけることができます。

{{< copyable "" >}}

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

`start_date`には**索引が**ありません。この述語をインデックス リーダー オペレータにプッシュするには、インデックスが必要です。次のようにインデックスを追加します。

{{< copyable "" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **ノート：**
>
> [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、DDL ジョブの進行状況を監視できます。 TiDB のデフォルトは慎重に選択されているため、インデックスを追加しても本番環境のワークロードに大きな影響はありません。テスト環境では、 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)値を増やすことを検討してください。リファレンス システムでは、バッチ サイズが`10240`でワーカー数が`32`の場合、デフォルトの 10 倍のパフォーマンス向上を達成できます。

インデックスを追加したら、クエリを`EXPLAIN`で繰り返すことができます。次の出力では、新しい実行計画が選択され、 `TableFullScan`と`Selection`演算子が削除されていることがわかります。

{{< copyable "" >}}

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

実際の実行時間を比較するには、再び[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用できます。

{{< copyable "" >}}

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

> **ノート：**
>
> ここで適用されるもう 1 つの最適化は、コプロセッサ キャッシュです。インデックスを追加できない場合は、 [コプロセッサー・キャッシュ](/coprocessor-cache.md)を有効にすることを検討してください。有効にすると、オペレーターが最後に実行されてからリージョンが変更されていない限り、TiKV はキャッシュから値を返します。これは、高価な`TableFullScan`および`Selection`オペレーターのコストを大幅に削減するのにも役立ちます。
