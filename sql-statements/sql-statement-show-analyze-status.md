---
title: SHOW ANALYZE STATUS
summary: An overview of the usage of SHOW ANALYZE STATUS for the TiDB database.
---

# 分析ステータスの表示 {#show-analyze-status}

`SHOW ANALYZE STATUS`ステートメントは、TiDB によって実行されている統計収集タスクと、限られた数の履歴タスク レコードを示します。

TiDB v6.1.0 以降、 `SHOW ANALYZE STATUS`ステートメントはクラスターレベルのタスクの表示をサポートします。 TiDB の再起動後でも、このステートメントを使用して再起動前のタスク レコードを表示できます。 TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンス レベルのタスクのみを表示でき、タスク レコードは TiDB の再起動後にクリアされます。

TiDB v6.1.0 以降、システム テーブル`mysql.analyze_jobs`を通じて過去 7 日間の履歴タスクを表示できるようになりました。

TiDB v7.3.0 以降、システム テーブル`mysql.analyze_jobs`または`SHOW ANALYZE STATUS`を通じて現在の`ANALYZE`タスクの進行状況を表示できます。

## あらすじ {#synopsis}

```ebnf+diagram
ShowAnalyzeStatusStmt ::= 'SHOW' 'ANALYZE' 'STATUS' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## 例 {#examples}

```sql
mysql> create table t(x int, index idx(x)) partition by hash(x) partitions 2;
Query OK, 0 rows affected (0.69 sec)

mysql> set @@tidb_analyze_version = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected (0.20 sec)

mysql> show analyze status;
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds| Progress | Estimated_total_rows|
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| test         | t          | p1             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p1             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t1         | p0             | analyze columns   |       28523259 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | running  | NULL        | 127.0.0.1:4000 | 690208308  | 0s               | 0.9843   | 28978290            |
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
4 rows in set (0.01 sec)

mysql> set @@tidb_analyze_version = 2;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 2 warnings (0.03 sec)

mysql> show analyze status;
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| Table_schema | Table_name | Partition_name | Job_info                                                           | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds  | Progress | Estimated_total_rows |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p1             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze index idx                                                  |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p1             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze columns                                                    |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
6 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [ANALYZE_STATUS テーブル](/information-schema/information-schema-analyze-status.md)
