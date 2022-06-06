---
title: SHOW ANALYZE STATUS
summary: An overview of the usage of SHOW ANALYZE STATUS for the TiDB database.
---

# ステータスの分析を表示 {#show-analyze-status}

`SHOW ANALYZE STATUS`ステートメントは、TiDBによって実行されている統計収集タスクと、限られた数の履歴タスクレコードを示しています。

## あらすじ {#synopsis}

**ShowStmt：**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable：**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## 例 {#examples}

{{< copyable "" >}}

```sql
create table t(x int, index idx(x)) partition by hash(x) partition 4;
analyze table t;
show analyze status;
```

```sql
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | State    |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
| test         | t          | p1             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p0             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p1             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze index idx |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p3             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
| test         | t          | p2             | analyze columns   |              0 | 2020-05-25 17:23:55 | finished |
+--------------+------------+----------------+-------------------+----------------+---------------------+----------+
8 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [ANALYZE_STATUSテーブル](/information-schema/information-schema-analyze-status.md)
