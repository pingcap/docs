---
title: METRICS_SUMMARY
summary: TiDB 4.0 では、`information_schema.metrics_summary`と`information_schema.metrics_summary_by_label`テーブルが導入され、異常な監視メトリックを簡単に検出できます。これにより、TiDBクラスター内の監視データを効率的に確認できます。また、時間範囲を指定して特定の監視項目をクエリすることも可能です。監視集計テーブルを使用すると、ボトルネックを素早く特定できます。
---

# メトリクス_サマリー {#metrics-summary}

TiDB クラスターには多くの監視メトリックがあります。異常な監視メトリックを簡単に検出できるように、TiDB 4.0 では次の 2 つの監視概要テーブルが導入されています。

-   `information_schema.metrics_summary`
-   `information_schema.metrics_summary_by_label`

> **注記：**
>
> 前述の 2 つの監視概要テーブルは、TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

2 つの表には、各監視メトリックを効率的に確認できるように、すべての監視データがまとめられています。 `information_schema.metrics_summary`と比較して、 `information_schema.metrics_summary_by_label`テーブルには追加の`label`列があり、さまざまなラベルに従って差別化された統計を実行します。

```sql
USE information_schema;
DESC metrics_summary;
```

```sql
+--------------+--------------+------+------+---------+-------+
| Field        | Type         | Null | Key  | Default | Extra |
+--------------+--------------+------+------+---------+-------+
| METRICS_NAME | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE     | double       | YES  |      | NULL    |       |
| SUM_VALUE    | double(22,6) | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) | YES  |      | NULL    |       |
| COMMENT      | varchar(256) | YES  |      | NULL    |       |
+--------------+--------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

フィールドの説明:

-   `METRICS_NAME` : 監視テーブル名。
-   `QUANTILE` : パーセンタイル。 `QUANTILE` SQL文で指定できます。例えば：
    -   `select * from metrics_summary where quantile=0.99` 0.99 パーセンタイルのデータを表示することを指定します。
    -   `select * from metrics_summary where quantile in (0.80, 0.90, 0.99, 0.999)` 0.8、0.90、0.99、0.999 パーセンタイルのデータを同時に表示することを指定します。
-   `SUM_VALUE` `AVG_VALUE`それぞれ合計、平均値`MIN_VALUE`最小`MAX_VALUE` 、最大値を意味します。
-   `COMMENT` : 対応する監視テーブルのコメント。

例えば：

時間範囲`'2020-03-08 13:23:00', '2020-03-08 13: 33: 00'`内で TiDB クラスター内で平均消費時間が最も長い監視項目の 3 つのグループをクエリするには、 `information_schema.metrics_summary`テーブルを直接クエリし、 `/*+ time_range() */`ヒントを使用して時間範囲を指定します。 SQL ステートメントは次のとおりです。

```sql
SELECT /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
FROM information_schema.metrics_summary
WHERE metrics_name LIKE 'tidb%duration'
 AND avg_value > 0
 AND quantile = 0.99
ORDER BY avg_value DESC
LIMIT 3\G
```

```sql
***************************[ 1. row ]***************************
METRICS_NAME | tidb_get_token_duration
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
METRICS_NAME | tidb_query_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.269079
AVG_VALUE    | 0.007272
MIN_VALUE    | 0.000667
MAX_VALUE    | 0.01554
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
METRICS_NAME | tidb_kv_request_duration
QUANTILE     | 0.99
SUM_VALUE    | 0.170232
AVG_VALUE    | 0.004601
MIN_VALUE    | 0.000975
MAX_VALUE    | 0.013
COMMENT      | The quantile of kv requests durations by store
```

同様に、次の例では`metrics_summary_by_label`監視概要テーブルをクエリします。

```sql
SELECT /*+ time_range('2020-03-08 13:23:00','2020-03-08 13:33:00') */ *
FROM information_schema.metrics_summary_by_label
WHERE metrics_name LIKE 'tidb%duration'
 AND avg_value > 0
 AND quantile = 0.99
ORDER BY avg_value DESC
LIMIT 10\G
```

```sql
***************************[ 1. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_get_token_duration
LABEL        |
QUANTILE     | 0.99
SUM_VALUE    | 8.972509
AVG_VALUE    | 0.996945
MIN_VALUE    | 0.996515
MAX_VALUE    | 0.997458
COMMENT      |  The quantile of Duration (us) for getting token, it should be small until concurrency limit is reached(second)
***************************[ 2. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Select
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
***************************[ 3. row ]***************************
INSTANCE     | 172.16.5.40:10089
METRICS_NAME | tidb_query_duration
LABEL        | Rollback
QUANTILE     | 0.99
SUM_VALUE    | 0.072083
AVG_VALUE    | 0.008009
MIN_VALUE    | 0.007905
MAX_VALUE    | 0.008241
COMMENT      | The quantile of TiDB query durations(second)
```

上記のクエリ結果の 2 行目と 3 行目は、 `tidb_query_duration`の`Select`と`Rollback`ステートメントの平均実行時間が長いことを示しています。

上記の例に加えて、監視集計テーブルを使用すると、2 つの時間帯の全リンク監視項目を比較することにより、監視データから最も変化が大きいモジュールを素早く見つけ、ボトルネックを迅速に特定できます。次の例では、2 つの期間 (t1 がベースライン) のすべての監視項目を比較し、最大の差に従ってこれらの項目を並べ替えます。

-   期間 t1: `("2020-03-03 17:08:00", "2020-03-03 17:11:00")`
-   期間 t2: `("2020-03-03 17:18:00", "2020-03-03 17:21:00")`

2 つの時間帯の監視項目を`METRICS_NAME`に従って結合し、差分値に従ってソートします。 `TIME_RANGE`はクエリ時間を指定するヒントです。

```sql
SELECT GREATEST(t1.avg_value,t2.avg_value)/LEAST(t1.avg_value,
         t2.avg_value) AS ratio,
         t1.metrics_name,
         t1.avg_value as t1_avg_value,
         t2.avg_value as t2_avg_value,
         t2.comment
FROM
    (SELECT /*+ time_range("2020-03-03 17:08:00", "2020-03-03 17:11:00")*/ *
    FROM information_schema.metrics_summary ) t1
JOIN
    (SELECT /*+ time_range("2020-03-03 17:18:00", "2020-03-03 17:21:00")*/ *
    FROM information_schema.metrics_summary ) t2
    ON t1.metrics_name = t2.metrics_name
ORDER BY ratio DESC LIMIT 10;
```

```sql
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| ratio          | metrics_name                             | t1_avg_value   | t2_avg_value     | comment                                                                                     |
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
| 5865.59537065  | tidb_slow_query_cop_process_total_time   |       0.016333 |        95.804724 | The total time of TiDB slow query statistics with slow query total cop process time(second) |
| 3648.74109023  | tidb_distsql_partial_scan_key_total_num  |   10865.666667 |  39646004.4394   | The total num of distsql partial scan key numbers                                           |
|  267.002351165 | tidb_slow_query_cop_wait_total_time      |       0.003333 |         0.890008 | The total time of TiDB slow query statistics with slow query total cop wait time(second)    |
|  192.43267836  | tikv_cop_total_response_total_size       | 2515333.66667  | 484032394.445    |                                                                                             |
|  192.43267836  | tikv_cop_total_response_size_per_seconds |   41922.227778 |   8067206.57408  |                                                                                             |
|  152.780296296 | tidb_distsql_scan_key_total_num          |    5304.333333 |    810397.618317 | The total num of distsql scan numbers                                                       |
|  126.042290167 | tidb_distsql_execution_total_time        |       0.421622 |        53.142143 | The total time of distsql execution(second)                                                 |
|  105.164020657 | tikv_cop_scan_details                    |     134.450733 |     14139.379665 |                                                                                             |
|  105.164020657 | tikv_cop_scan_details_total              |    8067.043981 |    848362.77991  |                                                                                             |
|  101.635495394 | tikv_cop_scan_keys_num                   |    1070.875    |    108838.91113  |                                                                                             |
+----------------+------------------------------------------+----------------+------------------+---------------------------------------------------------------------------------------------+
```

上記のクエリ結果から、次の情報を取得できます。

-   期間 t2 の`tib_slow_query_cop_process_total_time` (TiDB スロー クエリの消費時間`cop process` ) は、期間 t1 の 5,865 倍です。
-   期間 t2 の`tidb_distsql_partial_scan_key_total_num` (TiDB `distsql`によって要求されたスキャンするキーの数) は、期間 t1 の 3,648 倍です。期間`tidb_slow_query_cop_wait_total_time` (TiDB スロー クエリでキューアップを要求するコプロセッサーの待ち時間) は、期間 t1 の 267 倍になります。
-   期間 t2 の`tikv_cop_total_response_size` (TiKVコプロセッサー要求結果のサイズ) は、期間 t1 の 192 倍です。
-   期間 t2 (TiKVコプロセッサーによって要求されたスキャン) の`tikv_cop_scan_details` 、期間 t1 の 0 の 105 倍です。

上記の結果から、期間 t2 のコプロセッサーリクエストが期間 t1 のリクエストよりもはるかに多いことがわかります。これにより、TiKVコプロセッサーが過負荷になり、 `cop task`待機する必要があります。期間 t2 に、より多くの負荷をもたらす大規模なクエリがいくつか出現する可能性があります。

実際、t1 から t2 までの全期間中、 `go-ycsb`圧力テストが実行されています。次に、期間 t2 中に 20 `tpch`クエリが実行されます。したがって、多くのコプロセッサーリクエストを引き起こすのは`tpch`クエリです。
