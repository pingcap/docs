---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの RENAME TABLE の使用法の概要。
---

# テーブル名の変更 {#rename-table}

このステートメントは、既存のテーブルの名前を新しい名前に変更します。

## 概要 {#synopsis}

```ebnf+diagram
RenameTableStmt ::=
    'RENAME' 'TABLE' TableToTable ( ',' TableToTable )*

TableToTable ::=
    TableName 'TO' TableName
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)

mysql> RENAME TABLE t1 TO t2;
Query OK, 0 rows affected (0.08 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t2             |
+----------------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`RENAME TABLE`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [テーブルの変更](/sql-statements/sql-statement-alter-table.md)
