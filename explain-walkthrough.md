---
title: EXPLAIN Walkthrough
summary: Learn how to use EXPLAIN by walking through an example statement
---

# <code>EXPLAIN</code>ウォークスルー {#code-explain-code-walkthrough}

SQLは宣言型言語であるため、クエリが効率的に実行されているかどうかを自動的に判断することはできません。現在の実行プランを学習するには、最初に[`EXPLAIN`](/sql-statements/sql-statement-explain.md)ステートメントを使用する必要があります。

<CustomContent platform="tidb">

[バイクシェアのサンプルデータベース](/import-example-data.md)からの次のステートメントは、2017年7月1日に行われた旅行の数をカウントします。

</CustomContent>

<CustomContent platform="tidb-cloud">

[バイクシェアのサンプルデータベース](/tidb-cloud/import-sample-data.md)からの次のステートメントは、2017年7月1日に行われた旅行の数をカウントします。

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

子演算子`└─TableFullScan_18`から戻ると、その実行プロセスは次のようになりますが、現在は最適ではありません。

1.  コプロセッサー（TiKV）は、 `trips`のテーブル全体を`TableFullScan`の操作として読み取ります。次に、読み取った行を`Selection_19`オペレーターに渡します。5オペレーターはまだTiKV内にあります。
2.  次に、 `WHERE start_date BETWEEN ..`述語は`Selection_19`演算子でフィルタリングされます。この選択を満たすには、約`250`行が推定されます。この数は、統計とオペレーターのロジックに従って推定されていることに注意してください。 `└─TableFullScan_18`演算子は`stats:pseudo`を示します。これは、テーブルに実際の統計情報がないことを意味します。 `ANALYZE TABLE trips`を実行して統計情報を収集した後、統計はより正確になると予想されます。
3.  選択基準を満たす行には、 `count`の関数が適用されます。これは、まだTiKV（ `cop[tikv]` ）内にある`StreamAgg_9`演算子内でも完了します。 TiKVコプロセッサーは、いくつかのMySQL組み込み関数を実行でき、そのうちの`count`つがその1つです。
4.  `StreamAgg_9`の結果は、TiDBサーバー内にある`TableReader_21`オペレーターに送信されます（ `root`のタスク）。この演算子の`estRows`列の値は`1`です。これは、演算子がアクセスされる各TiKV領域から1行を受け取ることを意味します。これらのリクエストの詳細については、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を参照してください。
5.  次に、 `StreamAgg_20`演算子は、 `└─TableReader_21`演算子の各行に`count`関数を適用します。これは、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)から見ることができ、約56行になります。これはルート演算子であるため、結果をクライアントに返します。

> **ノート：**
>
> テーブルに含まれるリージョンの一般的なビューについては、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)を実行します。

## 現在のパフォーマンスを評価する {#assess-the-current-performance}

`EXPLAIN`はクエリ実行プランを返すだけで、クエリは実行しません。実際の実行時間を取得するには、クエリを実行するか、 `EXPLAIN ANALYZE`を使用します。

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

上記のクエリ例は、実行に`1.03`秒かかります。これは、理想的なパフォーマンスです。

上記の`EXPLAIN ANALYZE`の結果から、 `actRows`は、推定値（ `estRows` ）の一部が不正確であることを示します（1万行を期待しますが、1900万行を検出します）。これは、 `└─TableFullScan_18`の`operator info` （ `stats:pseudo` ）ですでに示されています。最初に[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を実行し、次に`EXPLAIN ANALYZE`を再度実行すると、見積もりがはるかに近いことがわかります。

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

`ANALYZE TABLE`が実行された後、 `└─TableFullScan_18`演算子の推定行が正確であり、 `└─Selection_19`の推定もはるかに近いことがわかります。上記の2つのケースでは、実行プラン（TiDBがこのクエリを実行するために使用する演算子のセット）は変更されていませんが、統計が古くなっているために最適ではないプランが発生することがよくあります。

`ANALYZE TABLE`に加えて、TiDBは、しきい値[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)に達した後、バックグラウンド操作として統計を自動的に再生成します。 [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを実行すると、TiDBがこのしきい値にどれだけ近いか（TiDBが統計をどの程度健全であると見なすか）を確認できます。

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

-   ほとんどの作業は、TiKVコプロセッサー内で処理されます。処理のためにネットワークを介してTiDBに送り返す必要があるのは56行だけです。これらの各行は短く、選択に一致するカウントのみが含まれています。

-   TiDB（ `StreamAgg_20` ）とTiKV（ `└─StreamAgg_9` ）の両方で行数を集計するには、ストリーム集計を使用します。これは、メモリ使用量が非常に効率的です。

現在の実行プランの最大の問題は、述語`start_date BETWEEN '2017-07-01 00:00:00' AND '2017-07-01 23:59:59'`がすぐには適用されないことです。すべての行は最初に`TableFullScan`演算子で読み取られ、その後選択が適用されます。 `SHOW CREATE TABLE trips`の出力から原因を見つけることができます：

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

`start_date`には**インデックス**がありません。この述語をインデックスリーダー演算子にプッシュするには、インデックスが必要になります。次のようにインデックスを追加します。

{{< copyable "" >}}

```sql
ALTER TABLE trips ADD INDEX (start_date);
```

```sql
Query OK, 0 rows affected (2 min 10.23 sec)
```

> **ノート：**
>
> [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin.md)コマンドを使用して、DDLジョブの進行状況を監視できます。 TiDBのデフォルトは、インデックスの追加が本番ワークロードにあまり影響を与えないように慎重に選択されています。テスト環境では、 [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)と[`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)の値を増やすことを検討してください。参照システムでは、バッチサイズが`10240`でワーカー数が`32`の場合、デフォルトの10倍のパフォーマンス向上を実現できます。

インデックスを追加した後、 `EXPLAIN`でクエリを繰り返すことができます。次の出力では、新しい実行プランが選択され、 `TableFullScan`つと`Selection`の演算子が削除されていることがわかります。

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

実際の実行時間を比較するために、もう一度[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用できます。

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

上記の結果から、クエリ時間は1.03秒から0.0秒に短縮されました。

> **ノート：**
>
> ここで適用されるもう1つの最適化は、コプロセッサーキャッシュです。インデックスを追加できない場合は、 [コプロセッサーキャッシュ](/coprocessor-cache.md)を有効にすることを検討してください。有効にすると、オペレーターが最後に実行されてからリージョンが変更されていない限り、TiKVはキャッシュから値を返します。これは、高価な`TableFullScan`および`Selection`オペレーターのコストの多くを削減するのにも役立ちます。
