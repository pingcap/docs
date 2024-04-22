---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: テーブルの名前を変更するステートメントは、既存のテーブルの名前を新しい名前に変更します。このステートメントは、MySQLと完全な互換性があります。例えば、テーブルt1をt2に変更することができます。他にもテーブルの作成や表示、他の机に関するステートメントもあります。
---

# テーブルの名前を変更 {#rename-table}

このステートメントは、既存のテーブルの名前を新しい名前に変更します。

## あらすじ {#synopsis}

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

## MySQLの互換性 {#mysql-compatibility}

TiDB の`RENAME TABLE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [他の机](/sql-statements/sql-statement-alter-table.md)
