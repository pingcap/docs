---
title: SHOW CREATE TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW CREATE TABLE の使用法の概要。
---

# SHOW CREATE TABLE {#show-create-table}

このステートメントは、SQL を使用して既存のテーブルを再作成するための正確なステートメントを表示します。

## 概要 {#synopsis}

```ebnf+diagram
ShowCreateTableStmt ::=
    "SHOW" "CREATE" "TABLE" (SchemaName ".")? TableName
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW CREATE TABLE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)を参照してください。

## 参照 {#see-also}

-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
-   [SHOW [FULL] TABLES](/sql-statements/sql-statement-show-tables.md)
-   [SHOW [FULL] COLUMNS FROM](/sql-statements/sql-statement-show-columns-from.md)
