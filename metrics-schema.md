---
title: Metrics Schema
summary: METRICS_SCHEMA` スキーマについて学習します。
---

# メトリクススキーマ {#metrics-schema}

`METRICS_SCHEMA`は、Prometheus に保存されている TiDB メトリックのビューのセットです。各テーブルの PromQL (Prometheus クエリ言語) のソースは[`INFORMATION_SCHEMA.METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)で入手できます。

```sql
USE metrics_schema;
SELECT * FROM uptime;
SELECT * FROM information_schema.metrics_tables WHERE table_name='uptime'\G
```

```sql
+----------------------------+-----------------+------------+--------------------+
| time                       | instance        | job        | value              |
+----------------------------+-----------------+------------+--------------------+
| 2020-07-06 15:26:26.203000 | 127.0.0.1:10080 | tidb       | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:10080 | tidb       | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:20180 | tikv       | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:20180 | tikv       | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:2379  | pd         | 123.60300016403198 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:2379  | pd         | 183.60300016403198 |
| 2020-07-06 15:26:26.203000 | 127.0.0.1:9090  | prometheus | 123.72300004959106 |
| 2020-07-06 15:27:26.203000 | 127.0.0.1:9090  | prometheus | 183.72300004959106 |
+----------------------------+-----------------+------------+--------------------+
8 rows in set (0.00 sec)

*************************** 1. row ***************************
TABLE_NAME: uptime
    PROMQL: (time() - process_start_time_seconds{$LABEL_CONDITIONS})
    LABELS: instance,job
  QUANTILE: 0
   COMMENT: TiDB uptime since last restart(second)
1 row in set (0.00 sec)
```

```sql
SHOW TABLES;
```

```sql
+---------------------------------------------------+
| Tables_in_metrics_schema                          |
+---------------------------------------------------+
| abnormal_stores                                   |
| etcd_disk_wal_fsync_rate                          |
| etcd_wal_fsync_duration                           |
| etcd_wal_fsync_total_count                        |
| etcd_wal_fsync_total_time                         |
| go_gc_count                                       |
| go_gc_cpu_usage                                   |
| go_gc_duration                                    |
| go_heap_mem_usage                                 |
| go_threads                                        |
| goroutines_count                                  |
| node_cpu_usage                                    |
| node_disk_available_size                          |
| node_disk_io_util                                 |
| node_disk_iops                                    |
| node_disk_read_latency                            |
| node_disk_size                                    |
..
| tikv_storage_async_request_total_time             |
| tikv_storage_async_requests                       |
| tikv_storage_async_requests_total_count           |
| tikv_storage_command_ops                          |
| tikv_store_size                                   |
| tikv_thread_cpu                                   |
| tikv_thread_nonvoluntary_context_switches         |
| tikv_thread_voluntary_context_switches            |
| tikv_threads_io                                   |
| tikv_threads_state                                |
| tikv_total_keys                                   |
| tikv_wal_sync_duration                            |
| tikv_wal_sync_max_duration                        |
| tikv_worker_handled_tasks                         |
| tikv_worker_handled_tasks_total_num               |
| tikv_worker_pending_tasks                         |
| tikv_worker_pending_tasks_total_num               |
| tikv_write_stall_avg_duration                     |
| tikv_write_stall_max_duration                     |
| tikv_write_stall_reason                           |
| up                                                |
| uptime                                            |
+---------------------------------------------------+
626 rows in set (0.00 sec)
```

`METRICS_SCHEMA`は、（ [`metrics_summary`](/information-schema/information-schema-metrics-summary.md) 、 [`metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) 、 [`inspection_summary`](/information-schema/information-schema-inspection-summary.md)などの監視関連の要約表のデータソースとして使用されます。

## 追加の例 {#additional-examples}

このセクションでは、 `metrics_schema`の`tidb_query_duration`監視テーブルを例に、この監視テーブルの使用方法と動作について説明します。他の監視テーブルの動作原理は`tidb_query_duration`と同様です。

`information_schema.metrics_tables`の`tidb_query_duration`のテーブルに関連する情報を照会します。

```sql
SELECT * FROM information_schema.metrics_tables WHERE table_name='tidb_query_duration';
```

```sql
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| TABLE_NAME          | PROMQL                                                                                                                                                   | LABELS            | QUANTILE | COMMENT                                      |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
| tidb_query_duration | histogram_quantile($QUANTILE, sum(rate(tidb_server_handle_query_duration_seconds_bucket{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (le,sql_type,instance)) | instance,sql_type | 0.9      | The quantile of TiDB query durations(second) |
+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+----------+----------------------------------------------+
```

フィールドの説明:

-   `TABLE_NAME` : `metrics_schema`のテーブル名に対応します。この例では、テーブル名は`tidb_query_duration`です。
-   `PROMQL` : 監視テーブルの動作原理は、まずSQL文を`PromQL`にマッピングし、次にPrometheusからデータを要求し、Prometheusの結果をSQLクエリ結果に変換することです。このフィールドは`PromQL`の式テンプレートです。監視テーブルのデータをクエリすると、クエリ条件を使用してこのテンプレートの変数が書き換えられ、最終的なクエリ式が生成されます。
-   `LABELS` : 監視項目のラベル。2 `tidb_query_duration`は`instance`と`sql_type` 2 つのラベルがあります。
-   `QUANTILE` : パーセンタイル。ヒストグラムタイプの監視データの場合、デフォルトのパーセンタイルが指定されます。このフィールドの値が`0`の場合、監視テーブルに対応する監視項目はヒストグラムではないことを意味します。
-   `COMMENT` : 監視テーブルの説明。2 テーブル`tidb_query_duration` 、P999/P99/P90 のクエリ時間など、TiDB クエリ実行のパーセンタイル時間を照会するために使用されていることがわかります。単位は秒です。

`tidb_query_duration`テーブルのスキーマをクエリするには、次のステートメントを実行します。

```sql
SHOW CREATE TABLE metrics_schema.tidb_query_duration;
```

```sql
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| Table               | Create Table                                                                                                       |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
| tidb_query_duration | CREATE TABLE `tidb_query_duration` (                                                                               |
|                     |   `time` datetime unsigned DEFAULT CURRENT_TIMESTAMP,                                                              |
|                     |   `instance` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `sql_type` varchar(512) DEFAULT NULL,                                                                            |
|                     |   `quantile` double unsigned DEFAULT '0.9',                                                                        |
|                     |   `value` double unsigned DEFAULT NULL                                                                             |
|                     | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='The quantile of TiDB query durations(second)' |
+---------------------+--------------------------------------------------------------------------------------------------------------------+
```

-   `time` : 監視項目の時間。
-   `instance`と`sql_type` : `tidb_query_duration`監視項目のラベル。6 `instance`監視アドレスを意味します。8 `sql_type`実行された SQL 文の種類を意味します。
-   `quantile` : パーセンタイル。ヒストグラムタイプの監視項目にはこの列があり、クエリのパーセンタイル時間を示します。たとえば、 `quantile = 0.9` P90 の時間をクエリすることを意味します。
-   `value` : 監視項目の値。

次のステートメントは、[ `2020-03-25 23:40:00` , `2020-03-25 23:42:00` ]の範囲内のP99時間を照会します。

```sql
SELECT * FROM metrics_schema.tidb_query_duration WHERE value is not null AND time>='2020-03-25 23:40:00' AND time <= '2020-03-25 23:42:00' AND quantile=0.99;
```

```sql
+---------------------+-------------------+----------+----------+----------------+
| time                | instance          | sql_type | quantile | value          |
+---------------------+-------------------+----------+----------+----------------+
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.509929485256 |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.494690793986 |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.493460506934 |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.152058493415 |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.152193879678 |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.140498483232 |
| 2020-03-25 23:40:00 | 172.16.5.40:10089 | internal | 0.99     | 0.47104        |
| 2020-03-25 23:41:00 | 172.16.5.40:10089 | internal | 0.99     | 0.11776        |
| 2020-03-25 23:42:00 | 172.16.5.40:10089 | internal | 0.99     | 0.11776        |
+---------------------+-------------------+----------+----------+----------------+
```

上記のクエリ結果の最初の行は、2020-03-25 23:40:00 の時点で、TiDB インスタンス`172.16.5.40:10089`で、 `Insert`型ステートメントの P99 実行時間が`sql_type`秒であることを意味します。他の行の意味も同様です。5 列の他の値は次のように説明されます。

-   `Select` : `select`型ステートメントが実行されます。
-   `internal` : 統計情報を更新し、グローバル変数を取得するために使用される TiDB の内部 SQL ステートメント。

上記のステートメントの実行プランを表示するには、次のステートメントを実行します。

```sql
DESC SELECT * FROM metrics_schema.tidb_query_duration WHERE value is not null AND time>='2020-03-25 23:40:00' AND time <= '2020-03-25 23:42:00' AND quantile=0.99;
```

```sql
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id               | estRows  | task | access object             | operator info                                                                                                                                                                                          |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Selection_5      | 8000.00  | root |                           | not(isnull(Column#5))                                                                                                                                                                                  |
| └─MemTableScan_6 | 10000.00 | root | table:tidb_query_duration | PromQL:histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket{}[60s])) by (le,sql_type,instance)), start_time:2020-03-25 23:40:00, end_time:2020-03-25 23:42:00, step:1m0s |
+------------------+----------+------+---------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

上記の結果から、実行プランには`PromQL` 、 `start_time` 、 `end_time` 、 `step`が含まれていることがわかります。実行プロセス中に、TiDB は Prometheus の`query_range` HTTP API を呼び出して、監視データを照会します。

[ `2020-03-25 23:40:00` , `2020-03-25 23:42:00` ] の範囲では、各ラベルに時間値が 3 つしかないことがわかります。実行プランでは、値`step`は 1 分です。つまり、これらの値の間隔は 1 分です。7 `step`次の 2 つのセッション変数によって決定されます。

-   `tidb_metric_query_step` : クエリ解決ステップ幅。Prometheus から`query_range`データを取得するには、 `start_time` 、 `end_time` 、 `step`を指定する必要があります。 `step` 、この変数の値を使用します。
-   `tidb_metric_query_range_duration` : 監視データが照会されると、 `PROMQL`の`$ RANGE_DURATION`フィールドの値が、この変数の値に置き換えられます。デフォルト値は 60 秒です。

異なる粒度で監視項目の値を表示するには、監視テーブルをクエリする前に、上記の 2 つのセッション変数を変更します。例:

1.  2 つのセッション変数の値を変更し、時間の粒度を 30 秒に設定します。

    > **注記：**
    >
    > Prometheus でサポートされる最小粒度は 30 秒です。

    ```sql
    set @@tidb_metric_query_step=30;
    set @@tidb_metric_query_range_duration=30;
    ```

2.  `tidb_query_duration`監視項目を次のようにクエリします。結果から、3 分間の時間範囲内で、各ラベルに 6 つの時間値があり、各値の間隔が 30 秒であることがわかります。

    ```sql
    select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
    ```

    ```sql
    +---------------------+-------------------+----------+----------+-----------------+
    | time                | instance          | sql_type | quantile | value           |
    +---------------------+-------------------+----------+----------+-----------------+
    | 2020-03-25 23:40:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.483285651924  |
    | 2020-03-25 23:40:30 | 172.16.5.40:10089 | Insert   | 0.99     | 0.484151462113  |
    | 2020-03-25 23:41:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.504576        |
    | 2020-03-25 23:41:30 | 172.16.5.40:10089 | Insert   | 0.99     | 0.493577384561  |
    | 2020-03-25 23:42:00 | 172.16.5.40:10089 | Insert   | 0.99     | 0.49482474311   |
    | 2020-03-25 23:40:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.189253402185  |
    | 2020-03-25 23:40:30 | 172.16.5.40:10089 | Select   | 0.99     | 0.184224951851  |
    | 2020-03-25 23:41:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.151673410553  |
    | 2020-03-25 23:41:30 | 172.16.5.40:10089 | Select   | 0.99     | 0.127953838989  |
    | 2020-03-25 23:42:00 | 172.16.5.40:10089 | Select   | 0.99     | 0.127455434547  |
    | 2020-03-25 23:40:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0624          |
    | 2020-03-25 23:40:30 | 172.16.5.40:10089 | internal | 0.99     | 0.12416         |
    | 2020-03-25 23:41:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0304          |
    | 2020-03-25 23:41:30 | 172.16.5.40:10089 | internal | 0.99     | 0.06272         |
    | 2020-03-25 23:42:00 | 172.16.5.40:10089 | internal | 0.99     | 0.0629333333333 |
    +---------------------+-------------------+----------+----------+-----------------+
    ```

3.  実行プランをビュー。結果から、実行プランの`PromQL`と`step`の値が 30 秒に変更されたこともわかります。

    ```sql
    desc select * from metrics_schema.tidb_query_duration where value is not null and time>='2020-03-25 23:40:00' and time <= '2020-03-25 23:42:00' and quantile=0.99;
    ```

    ```sql
    +------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | id               | estRows  | task | access object             | operator info                                                                                                                                                                                         |
    +------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Selection_5      | 8000.00  | root |                           | not(isnull(Column#5))                                                                                                                                                                                 |
    | └─MemTableScan_6 | 10000.00 | root | table:tidb_query_duration | PromQL:histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket{}[30s])) by (le,sql_type,instance)), start_time:2020-03-25 23:40:00, end_time:2020-03-25 23:42:00, step:30s |
    +------------------+----------+------+---------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    ```
