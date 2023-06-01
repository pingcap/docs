---
title: RENAME TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of RENAME TABLE for the TiDB database.
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

このステートメントは、MySQL と完全な互換性があると理解されています。 GitHub では互換性の違いは[<a href="https://github.com/pingcap/tidb/issues/new/choose">問題を通じて報告されました</a>](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-create-table.md">テーブルの作成</a>](/sql-statements/sql-statement-create-table.md)
-   [<a href="/sql-statements/sql-statement-show-tables.md">テーブルを表示</a>](/sql-statements/sql-statement-show-tables.md)
-   [<a href="/sql-statements/sql-statement-alter-table.md">他の机</a>](/sql-statements/sql-statement-alter-table.md)
