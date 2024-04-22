---
title: METRICS_TABLES
summary: METRICS_TABLESテーブルは、METRICS_SCHEMAデータベース内の各ビューのPromQL定義を提供します。このテーブルはTiDBセルフホスト型にのみ適用され、TiDB Cloudでは使用できません。テーブル名、PromQL、ラベル、パーセンタイル、コメントのフィールドが含まれます。これにより、監視テーブルの動作原理が説明されます。監視テーブルのデータをクエリすると、クエリ条件を使用してクエリ式が生成されます。5つのテーブルが示され、それぞれのテーブルにはTABLE_NAME、PROMQL、LABELS、QUANTILE、COMMENTの情報が含まれます。
---

# METRICS_TABLES {#metrics-tables}

`METRICS_TABLES`テーブルは、 [`METRICS_SCHEMA`](/metrics-schema.md)データベース内の各ビューの PromQL (Prometheus Query Language) 定義を提供します。

> **注記：**
>
> このテーブルは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

```sql
USE INFORMATION_SCHEMA;
DESC METRICS_TABLES;
```

出力は次のとおりです。

```sql
+------------+--------------+------+------+---------+-------+
| Field      | Type         | Null | Key  | Default | Extra |
+------------+--------------+------+------+---------+-------+
| TABLE_NAME | varchar(64)  | YES  |      | NULL    |       |
| PROMQL     | varchar(64)  | YES  |      | NULL    |       |
| LABELS     | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE   | double       | YES  |      | NULL    |       |
| COMMENT    | varchar(256) | YES  |      | NULL    |       |
+------------+--------------+------+------+---------+-------+
```

フィールドの説明:

-   `TABLE_NAME` ： `METRICS_SCHEMA`のテーブル名に対応します。
-   `PROMQL` : 監視テーブルの動作原理は、SQL ステートメントを`PromQL`にマップし、Prometheus の結果を SQL クエリの結果に変換することです。このフィールドは`PromQL`の式テンプレートです。監視テーブルのデータをクエリすると、クエリ条件を使用してこのテンプレート内の変数が書き換えられ、最終的なクエリ式が生成されます。
-   `LABELS` : 監視項目のラベル。各ラベルは監視テーブルの列に対応します。 SQL ステートメントに対応する列のフィルターが含まれている場合、対応する`PromQL`それに応じて変更されます。
-   `QUANTILE` : パーセンタイル。ヒストグラム タイプの監視データの場合、デフォルトのパーセンタイルが指定されます。このフィールドの値が`0`の場合、監視テーブルに対応する監視項目がヒストグラムではないことを意味します。
-   `COMMENT` : 監視テーブルに関するコメント。

```sql
SELECT * FROM metrics_tables LIMIT 5\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
TABLE_NAME: abnormal_stores
    PROMQL: sum(pd_cluster_status{ type=~"store_disconnected_count|store_unhealth_count|store_low_space_count|store_down_count|store_offline_count|store_tombstone_count"})
    LABELS: instance,type
  QUANTILE: 0
   COMMENT:
*************************** 2. row ***************************
TABLE_NAME: etcd_disk_wal_fsync_rate
    PROMQL: delta(etcd_disk_wal_fsync_duration_seconds_count{$LABEL_CONDITIONS}[$RANGE_DURATION])
    LABELS: instance
  QUANTILE: 0
   COMMENT: The rate of writing WAL into the persistent storage
*************************** 3. row ***************************
TABLE_NAME: etcd_wal_fsync_duration
    PROMQL: histogram_quantile($QUANTILE, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (le,instance))
    LABELS: instance
  QUANTILE: 0.99
   COMMENT: The quantile time consumed of writing WAL into the persistent storage
*************************** 4. row ***************************
TABLE_NAME: etcd_wal_fsync_total_count
    PROMQL: sum(increase(etcd_disk_wal_fsync_duration_seconds_count{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (instance)
    LABELS: instance
  QUANTILE: 0
   COMMENT: The total count of writing WAL into the persistent storage
*************************** 5. row ***************************
TABLE_NAME: etcd_wal_fsync_total_time
    PROMQL: sum(increase(etcd_disk_wal_fsync_duration_seconds_sum{$LABEL_CONDITIONS}[$RANGE_DURATION])) by (instance)
    LABELS: instance
  QUANTILE: 0
   COMMENT: The total time of writing WAL into the persistent storage
5 rows in set (0.00 sec)
```
