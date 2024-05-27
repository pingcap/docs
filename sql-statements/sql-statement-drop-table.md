---
title: DROP TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの DROP TABLE の使用法の概要。
---

# テーブルを削除 {#drop-table}

このステートメントは、現在選択されているデータベースからテーブルを削除し`IF EXISTS` 。1 修飾子が使用されていない限り、テーブルが存在しない場合はエラーが返されます。

## 概要 {#synopsis}

```ebnf+diagram
DropTableStmt ::=
    'DROP' OptTemporary TableOrTables IfExists TableNameList RestrictOrCascadeOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameList ::=
    TableName ( ',' TableName )*
```

## 一時テーブルを削除する {#drop-temporary-tables}

通常のテーブルと一時テーブルを削除するには、次の構文を使用できます。

-   ローカル一時テーブルを削除するには`DROP TEMPORARY TABLE`使用します。
-   グローバル一時テーブルを削除するには`DROP GLOBAL TEMPORARY TABLE`使用します。
-   通常のテーブルまたは一時テーブルを削除するには`DROP TABLE`使用します。

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> DROP TABLE t1;
Query OK, 0 rows affected (0.22 sec)

mysql> DROP TABLE table_not_exists;
ERROR 1051 (42S02): Unknown table 'test.table_not_exists'

mysql> DROP TABLE IF EXISTS table_not_exists;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+---------------------------------------+
| Level | Code | Message                               |
+-------+------+---------------------------------------+
| Note  | 1051 | Unknown table 'test.table_not_exists' |
+-------+------+---------------------------------------+
1 row in set (0.01 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> DROP TABLE v1;
Query OK, 0 rows affected (0.23 sec)
```

## MySQL 互換性 {#mysql-compatibility}

現在、 `RESTRICT`と`CASCADE`構文的にのみサポートされています。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
