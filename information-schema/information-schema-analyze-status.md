---
title: ANALYZE_STATUS
summary: Learn the `ANALYZE_STATUS` information_schema table.
---

# ANALYZE_STATUS {#analyze-status}

`ANALYZE_STATUS`の表は、統計を収集する実行中のタスクと限られた数の履歴タスクに関する情報を提供します。

TiDB v6.1.0以降、 `ANALYZE_STATUS`テーブルはクラスターレベルのタスクの表示をサポートします。 TiDBを再起動した後でも、このテーブルを使用して、再起動前のタスクレコードを表示できます。 TiDB v6.1.0より前は、 `ANALYZE_STATUS`のテーブルはインスタンスレベルのタスクのみを表示でき、タスクレコードはTiDBの再起動後にクリアされます。

TiDB v6.1.0以降、システムテーブル`mysql.analyze_jobs`を介して過去7日間の履歴タスクを表示できます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC analyze_status;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TABLE_SCHEMA   | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME     | varchar(64)         | YES  |      | NULL    |       |
| PARTITION_NAME | varchar(64)         | YES  |      | NULL    |       |
| JOB_INFO       | longtext            | YES  |      | NULL    |       |
| PROCESSED_ROWS | bigint(64) unsigned | YES  |      | NULL    |       |
| START_TIME     | datetime            | YES  |      | NULL    |       |
| END_TIME       | datetime            | YES  |      | NULL    |       |
| STATE          | varchar(64)         | YES  |      | NULL    |       |
| FAIL_REASON    | longtext            | YES  |      | NULL    |       |
| INSTANCE       | varchar(512)        | YES  |      | NULL    |       |
| PROCESS_ID     | bigint(64) unsigned | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
11 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.analyze_status;
```

```sql
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO                                                           | PROCESSED_ROWS | START_TIME          | END_TIME            | STATE    | FAIL_REASON | INSTANCE       | PROCESS_ID |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 |       NULL |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 |       NULL |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+
6 rows in set (0.00 sec)
```

`ANALYZE_STATUS`表のフィールドは次のように説明されています。

-   `TABLE_SCHEMA` ：テーブルが属するデータベースの名前。
-   `TABLE_NAME` ：テーブルの名前。
-   `PARTITION_NAME` ：パーティションテーブルの名前。
-   `JOB_INFO` ： `ANALYZE`タスクの情報。インデックスが分析される場合、この情報にはインデックス名が含まれます。 `tidb_analyze_version =2`の場合、この情報にはサンプルレートなどの構成項目が含まれます。
-   `PROCESSED_ROWS` ：処理された行の数。
-   `START_TIME` ： `ANALYZE`タスクの開始時刻。
-   `END_TIME` ： `ANALYZE`タスクの終了時間。
-   `STATE` ： `ANALYZE`タスクの実行状態。その値は、 `pending` 、または`running`にすることが`failed` `finished` 。
-   `FAIL_REASON` ：タスクが失敗する理由。実行が成功した場合、値は`NULL`です。
-   `INSTANCE` ：タスクを実行するTiDBインスタンス。
-   `PROCESS_ID` ：タスクを実行するプロセスID。
