---
title: ANALYZE_STATUS
summary: Learn the `ANALYZE_STATUS` information_schema table.
---

# 分析ステータス {#analyze-status}

`ANALYZE_STATUS`表には、統計を収集する実行中のタスクと限られた数の履歴タスクに関する情報が表示されます。

TiDB v6.1.0 以降、 `ANALYZE_STATUS`テーブルはクラスターレベルのタスクの表示をサポートします。 TiDB の再起動後でも、このテーブルを使用して再起動前のタスク レコードを表示できます。 TiDB v6.1.0 より前では、 `ANALYZE_STATUS`テーブルにはインスタンス レベルのタスクのみが表示され、タスク レコードは TiDB の再起動後にクリアされます。

TiDB v6.1.0 以降、システム テーブル`mysql.analyze_jobs`を通じて過去 7 日間の履歴タスクを表示できるようになりました。

```sql
USE information_schema;
DESC analyze_status;
```

```sql
+----------------------+---------------------+------+------+---------+-------+
| Field                | Type                | Null | Key  | Default | Extra |
+----------------------+---------------------+------+------+---------+-------+
| TABLE_SCHEMA         | varchar(64)         | YES  |      | NULL    |       |
| TABLE_NAME           | varchar(64)         | YES  |      | NULL    |       |
| PARTITION_NAME       | varchar(64)         | YES  |      | NULL    |       |
| JOB_INFO             | longtext            | YES  |      | NULL    |       |
| PROCESSED_ROWS       | bigint(64) unsigned | YES  |      | NULL    |       |
| START_TIME           | datetime            | YES  |      | NULL    |       |
| END_TIME             | datetime            | YES  |      | NULL    |       |
| STATE                | varchar(64)         | YES  |      | NULL    |       |
| FAIL_REASON          | longtext            | YES  |      | NULL    |       |
| INSTANCE             | varchar(512)        | YES  |      | NULL    |       |
| PROCESS_ID           | bigint(64) unsigned | YES  |      | NULL    |       |
| REMAINING_SECONDS    | bigint(64) unsigned | YES  |      | NULL    |       |
| PROGRESS             | varchar(20)         | YES  |      | NULL    |       |
| ESTIMATED_TOTAL_ROWS | bigint(64) unsigned | YES  |      | NULL    |       |
+----------------------+---------------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

```sql
SELECT * FROM information_schema.analyze_status;
```

```sql
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
| TABLE_SCHEMA | TABLE_NAME | PARTITION_NAME | JOB_INFO                                                           | PROCESSED_ROWS | START_TIME          | END_TIME            | STATE    | FAIL_REASON | INSTANCE       | PROCESS_ID | REMAINING_SECONDS    | PROGRESS | ESTIMATED_TOTAL_ROWS  |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished |        NULL | 127.0.0.1:4000 | NULL       | NULL                 | NULL     |                  NULL |
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |        1000000 | 2022-05-27 11:30:12 | 2022-05-27 11:40:12 | running  |        NULL | 127.0.0.1:4000 | 690208308  | 600s                 | 0.25     | 4000000               |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+----------------------+----------+-----------------------+
6 rows in set (0.00 sec)
```

`ANALYZE_STATUS`テーブルのフィールドは次のように説明されています。

-   `TABLE_SCHEMA` : テーブルが属するデータベースの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `PARTITION_NAME` :パーティションテーブルの名前。
-   `JOB_INFO` : `ANALYZE`のタスクの情報。インデックスが分析される場合、この情報にはインデックス名が含まれます。 `tidb_analyze_version = 2`の場合、この情報にはサンプル レートなどの設定項目が含まれます。
-   `PROCESSED_ROWS` : 処理された行数。
-   `START_TIME` : `ANALYZE`タスクの開始時刻。
-   `END_TIME` : `ANALYZE`タスクの終了時刻。
-   `STATE` : `ANALYZE`タスクの実行ステータス。その値は`pending` 、 `running` 、 `finished`または`failed`です。
-   `FAIL_REASON` : タスクが失敗した理由。実行が成功した場合、値は`NULL`になります。
-   `INSTANCE` : タスクを実行する TiDB インスタンス。
-   `PROCESS_ID` : タスクを実行するプロセスID。
-   `REMAINING_SECONDS` : タスクが完了するまでの推定残り時間 (秒単位)。
-   `PROGRESS` : タスクの進行状況。
-   `ESTIMATED_TOTAL_ROWS` : タスクによって分析する必要がある行の合計。
