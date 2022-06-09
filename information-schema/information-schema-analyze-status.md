---
title: ANALYZE_STATUS
summary: Learn the `ANALYZE_STATUS` information_schema table.
---

# ANALYZE_STATUS {#analyze-status}

`ANALYZE_STATUS`の表は、統計を収集する実行中のタスクと限られた数の履歴タスクに関する情報を提供します。

{{< copyable "" >}}

```sql
USE information_schema;
DESC analyze_status;
```

```
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TABLE_SCHEMA   | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64)         | YES  |      | NULL    |       |
| PARTITION_NAME | varchar(64)         | YES  |      | NULL    |       |
| JOB_INFO       | varchar(64)         | YES  |      | NULL    |       |
| PROCESSED_ROWS | bigint(20) unsigned | YES  |      | NULL    |       |
| START_TIME     | datetime            | YES  |      | NULL    |       |
| STATE          | varchar(64)         | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
7 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM `ANALYZE_STATUS`;
```

```
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO          | PROCESSED_ROWS | START_TIME          | STATE    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          |                | analyze index idx | 2              | 2019-06-21 19:51:14 | finished |
| test         | t          |                | analyze columns   | 2              | 2019-06-21 19:51:14 | finished |
| test         | t1         | p0             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p3             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p1             | analyze columns   | 0              | 2019-06-21 19:51:15 | finished |
| test         | t1         | p2             | analyze columns   | 1              | 2019-06-21 19:51:15 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
6 rows in set
```

`ANALYZE_STATUS`表のフィールドは次のように説明されています。

-   `TABLE_SCHEMA` ：テーブルが属するデータベースの名前。
-   `TABLE_NAME` ：テーブルの名前。
-   `PARTITION_NAME` ：パーティションテーブルの名前。
-   `JOB_INFO` ： `ANALYZE`のタスクの情報。
-   `PROCESSED_ROWS` ：処理された行の数。
-   `START_TIME` ： `ANALYZE`のタスクの開始時刻。
-   `STATE` ： `ANALYZE`タスクの実行状態。その値は、 `pending` 、または`running`にすることが`failed` `finished` 。
