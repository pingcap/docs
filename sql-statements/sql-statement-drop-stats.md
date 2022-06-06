---
title: DROP STATS
summary: An overview of the usage of DROP STATS for the TiDB database.
---

# ドロップ統計 {#drop-stats}

`DROP STATS`ステートメントは、選択したデータベースから選択したテーブルの統計を削除するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName

TableName ::=
    Identifier ('.' Identifier)?
```

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE TABLE t(a INT);
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
DROP STATS t;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

```sql
Empty set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [統計入門](/statistics.md)
