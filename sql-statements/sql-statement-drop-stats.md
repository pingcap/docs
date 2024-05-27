---
title: DROP STATS
summary: TiDB データベースの DROP STATS の使用法の概要。
---

# ドロップ統計 {#drop-stats}

`DROP STATS`ステートメントは、選択したデータベースから選択したテーブルの統計を削除するために使用されます。

## 概要 {#synopsis}

```ebnf+diagram
DropStatsStmt ::=
    'DROP' 'STATS' TableName  ("PARTITION" partition | "GLOBAL")? ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 使用法 {#usage}

次の文は、 `TableName`のすべての統計情報を削除します。パーティションテーブルが指定されている場合、この文は、このテーブル内のすべてのパーティションの統計情報と[動的プルーニングモードで生成されたGlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)統計情報を削除します。

```sql
DROP STATS TableName
```

    Query OK, 0 rows affected (0.00 sec)

次のステートメントは、 `PartitionNameList`内の指定されたパーティションの統計のみを削除します。

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

    Query OK, 0 rows affected (0.00 sec)

次のステートメントは、指定されたテーブルの動的プルーニング モードで生成された GlobalStats のみを削除します。

```sql
DROP STATS TableName GLOBAL;
```

    Query OK, 0 rows affected (0.00 sec)

## 例 {#examples}

```sql
CREATE TABLE t(a INT);
```

    Query OK, 0 rows affected (0.01 sec)

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

    +---------+------------+----------------+---------------------+--------------+-----------+
    | Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
    +---------+------------+----------------+---------------------+--------------+-----------+
    | test    | t          |                | 2020-05-25 20:34:33 |            0 |         0 |
    +---------+------------+----------------+---------------------+--------------+-----------+
    1 row in set (0.00 sec)

```sql
DROP STATS t;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SHOW STATS_META WHERE db_name='test' and table_name='t';
```

    Empty set (0.00 sec)

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [統計入門](/statistics.md)
