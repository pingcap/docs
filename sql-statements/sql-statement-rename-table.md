---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの RENAME TABLE の使用法の概要。
---

# テーブル名の変更 {#rename-table}

このステートメントは、既存のテーブルとビューの名前を変更するために使用され、複数のテーブルの名前を一度に変更したり、データベース間で名前を変更したりすることをサポートします。

## 概要 {#synopsis}

```ebnf+diagram
RenameTableStmt ::=
    'RENAME' 'TABLE' TableToTable ( ',' TableToTable )*

TableToTable ::=
    TableName 'TO' TableName
```

## 例 {#examples}

```sql
CREATE TABLE t1 (a int);
```

    Query OK, 0 rows affected (0.12 sec)

```sql
SHOW TABLES;
```

    +----------------+
    | Tables_in_test |
    +----------------+
    | t1             |
    +----------------+
    1 row in set (0.00 sec)

```sql
RENAME TABLE t1 TO t2;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
SHOW TABLES;
```

    +----------------+
    | Tables_in_test |
    +----------------+
    | t2             |
    +----------------+
    1 row in set (0.00 sec)

次の例は、 `db3` `db1` `db2`既に存在し、テーブル`db1.t1`と`db4` `db3.t3`既に存在していることを前提として、データベース間で複数のテーブルの名前を変更する方法を示しています。

```sql
RENAME TABLE db1.t1 To db2.t2, db3.t3 To db4.t4;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
USE db1; SHOW TABLES;
```

    Database changed
    Empty set (0.00 sec)

```sql
USE db2; SHOW TABLES;
```

    Database changed
    +---------------+
    | Tables_in_db2 |
    +---------------+
    | t2            |
    +---------------+
    1 row in set (0.00 sec)

```sql
USE db3; SHOW TABLES;
```

    Database changed
    Empty set (0.00 sec)

```sql
USE db4; SHOW TABLES;
```

    Database changed
    +---------------+
    | Tables_in_db4 |
    +---------------+
    | t4            |
    +---------------+
    1 row in set (0.00 sec)

アトミック名前変更を使用すると、テーブルが存在しない瞬間を発生させずにテーブルをスワップアウトできます。

```sql
CREATE TABLE t1(id int PRIMARY KEY);
```

    Query OK, 0 rows affected (0.04 sec)

```sql
CREATE TABLE t1_new(id int PRIMARY KEY, n CHAR(0));
```

    Query OK, 0 rows affected (0.04 sec)

```sql
RENAME TABLE t1 TO t1_old, t1_new TO t1;
```

    Query OK, 0 rows affected (0.07 sec)

```sql
SHOW CREATE TABLE t1\G
```

    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `id` int NOT NULL,
      `n` char(0) DEFAULT NULL,
      PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    1 row in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

TiDBの`RENAME TABLE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [テーブルの変更](/sql-statements/sql-statement-alter-table.md)
