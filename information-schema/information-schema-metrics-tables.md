---
title: METRICS_TABLES
summary: Learn the `METRICS_TABLES` system table.
---

# METRICS_TABLES {#metrics-tables}

`METRICS_TABLES`の表は、 [メトリックススキーマ](/metrics-schema.md)のデータベースの各ビューのPromQL（Prometheusクエリ言語）定義を提供します。

{{< copyable "" >}}

```sql
USE information_schema;
DESC metrics_tables;
```

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

フィールドの説明：

-   `TABLE_NAME` ： `metrics_schema`のテーブル名に対応します。
-   `PROMQL` ：監視テーブルの動作原理は、SQLステートメントを`PromQL`にマップし、Prometheusの結果をSQLクエリの結果に変換することです。このフィールドは`PromQL`の式テンプレートです。監視テーブルのデータをクエリする場合、クエリ条件を使用してこのテンプレートの変数を書き換え、最終的なクエリ式を生成します。
-   `LABELS` ：監視項目のラベル。各ラベルは、監視テーブルの列に対応しています。 SQLステートメントに対応する列のフィルターが含まれている場合、対応する`PromQL`はそれに応じて変更されます。
-   `QUANTILE` ：パーセンタイル。ヒストグラムタイプのデータを監視するために、デフォルトのパーセンタイルが指定されています。このフィールドの値が`0`の場合、監視テーブルに対応する監視項目がヒストグラムではないことを意味します。
-   `COMMENT` ：監視テーブルに関するコメント。

{{< copyable "" >}}

```sql
SELECT * FROM metrics_tables LIMIT 5\G
```

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
